from dataclasses import dataclass

from langgraph.graph.state import CompiledStateGraph

from schema import AgentInfo

# These are the submodule workflows
# TODO: rename 'workflows' to submodule name/something more clear
from workflows import workflows

DEFAULT_AGENT = "research-assistant"


@dataclass
class Agent:
    description: str
    graph: CompiledStateGraph


agents: dict[str, Agent] = {}

for workflow in workflows:
    agents[workflow['workflow_id']] = Agent(description=workflow['description'], graph=workflow['agent'])


def get_agent(agent_id: str) -> CompiledStateGraph:
    try:
        return agents[agent_id].graph
    except KeyError:
        raise ValueError(f"Agent {agent_id} not found.")


def get_all_agent_info() -> list[AgentInfo]:
    return [
        AgentInfo(key=agent_id, description=agent.description) for agent_id, agent in agents.items()
    ]
