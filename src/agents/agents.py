from dataclasses import dataclass

from langgraph.graph.state import CompiledStateGraph

from .bg_task_agent.bg_task_agent import bg_task_agent
from .data_insights.proportion_insight import proportion_insight_agent
from .chatbot import chatbot
from .command_agent import command_agent
from .research_assistant import research_assistant
from .test_graph import test_graph
from schema import AgentInfo

# There are the submodule workflows
from workflows import workflows

DEFAULT_AGENT = "research-assistant"


@dataclass
class Agent:
    description: str
    graph: CompiledStateGraph


agents: dict[str, Agent] = {
    "chatbot": Agent(description="A simple chatbot.", graph=chatbot),
    "research-assistant": Agent(
        description="A research assistant with web search and calculator.", graph=research_assistant
    ),
    "command-agent": Agent(description="A command agent.", graph=command_agent),
    "bg-task-agent": Agent(description="A background task agent.", graph=bg_task_agent),
    "test_graph": Agent(description="a test graph", graph=test_graph),
    "proportion_agent": Agent(description="A data insights agent for proportion.", graph=proportion_insight_agent),
}

print("workflows")

for workflow in workflows:
    agents[workflow['workflow_id']] = Agent(description=workflow['description'], graph=workflow['agent'])


def get_agent(agent_id: str) -> CompiledStateGraph:
    return agents[agent_id].graph


def get_all_agent_info() -> list[AgentInfo]:
    return [
        AgentInfo(key=agent_id, description=agent.description) for agent_id, agent in agents.items()
    ]
