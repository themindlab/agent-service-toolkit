
from pydantic import BaseModel, Field

class AgentInfo(BaseModel):
    """Info about an available agent."""

    key: str = Field(
        description="Agent key.",
        examples=["research-assistant"],
    )
    description: str = Field(
        description="Description of the agent.",
        examples=["A research assistant for generating research papers."],
    )


class ExecuteWorkflowInput(BaseModel):
    """ workflow input """
    initial_state: dict = Field(
        title="Data",
        description="Data to be consumed by agent"
        # TODO: add examplewhen data schema figured out
    )
    workflow_id: str = Field(
        title="Workflow",
        description="Workflow to be executed",
        examples=['proportion_agent']
    )
    thread_id: str | None = Field(
        description="Thread ID to be used to fetch workflow state.",
        default=None,
        examples=["847c6285-8fc9-4560-a83f-4e6285809254"],
    )

class GetThreadStateInput(BaseModel):
    """thread id input """
    thread_id: str | None = Field(
        description="Thread ID to persist and continue a multi-turn conversation.",
        default=None,
        examples=["847c6285-8fc9-4560-a83f-4e6285809254"],
    )
    workflow_id: str = Field(
        title="Workflow",
        description="Workflow to be executed",
        examples=['proportion_agent']
    )
