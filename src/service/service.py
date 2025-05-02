import logging
import warnings
import asyncio
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Annotated
from uuid import uuid4
from psycopg_pool import AsyncConnectionPool

from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from langchain_core._api import LangChainBetaWarning
from langchain_core.runnables import RunnableConfig

from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver


from .agents import get_agent, get_all_agent_info
from core import settings
from schema import (
    ExecuteWorkflowInput,
    GetThreadStateInput
)

from lg_utils_package.lg_utils import Status

warnings.filterwarnings("ignore", category=LangChainBetaWarning)
logger = logging.getLogger(__name__)


def verify_bearer(
    http_auth: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(HTTPBearer(description="Please provide AUTH_SECRET api key.", auto_error=False)),
    ],
) -> None:
    if not settings.AUTH_SECRET:
        return
    auth_secret = settings.AUTH_SECRET.get_secret_value()
    if not http_auth or http_auth.credentials != auth_secret:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Construct agent with Postgres checkpointer
    # TODO: It's probably dangerous to share the same checkpointer on multiple agents
    
    async with AsyncConnectionPool(conninfo=settings.DB_URI, max_size=20, kwargs={"autocommit": True}) as pool:
        checkpointer = AsyncPostgresSaver(pool)
        await checkpointer.setup()

        agents = get_all_agent_info()
        for a in agents:
            agent = get_agent(a.key)
            agent.checkpointer = checkpointer
        yield


app = FastAPI(lifespan=lifespan)
router = APIRouter(dependencies=[Depends(verify_bearer)])


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


##### New Routes #####

@router.post("/list_workflows")
def get_workflows():
    return get_all_agent_info()

@router.post("/execute_workflow")
async def execute_workflow(input: ExecuteWorkflowInput):

    kwargs = {
        'input': {
            **input.initial_state,
            'workflow': input.workflow_id
        },
        'config': {
            'configurable':{
                'thread_id': input.thread_id if input.thread_id else str(uuid4()),
            }
        }
    }

    async def run_workflow():
        try:
            agent = get_agent(input.workflow_id)
            async for event in agent.astream(**kwargs):
                print(event)
        except Exception as e:
            await agent.aupdate_state(kwargs['config'], {
                "status": Status.FAILED,
                "error": str(e)
            })
            print(e)


    agent = get_agent(input.workflow_id)
    loop = asyncio.get_event_loop()
    try:
        loop.create_task(run_workflow())
        return kwargs
    except Exception as e:
        logger.error(f"An exception occurred: {e}")
        raise HTTPException(status_code=500, detail="Unexpected error")




@router.post("/get_thread_state")
def get_thread_state(input: GetThreadStateInput):
    agent = get_agent(input.workflow_id)
    try:
        state_snapshot = agent.get_state(
            config=RunnableConfig(
                configurable={
                    "thread_id": input.thread_id,
                }
            )
        )
        return state_snapshot.values
    except Exception as e:
        logger.error(f"An exception occurred: {e}")
        raise HTTPException(status_code=500, detail="Unexpected error")


app.include_router(router)
