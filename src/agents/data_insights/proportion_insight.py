import asyncio
from core import get_model
from typing import TypedDict

from langchain_core.messages import AIMessage
from langchain_core.prompts import PromptTemplate
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph

class State(TypedDict):

    data: dict
    result: AIMessage


model = get_model("gpt-4o-mini")

prompt = f"""
A group of people were asked their age in a survey. Below is a list of key-value pairs.
The keys represent an age group and the values represent the proportion of people in the survey that selected
that age group. What can you tell me about the age distribution of the survey participants?

{{data}}
"""

prompt = PromptTemplate.from_template(prompt)

async def pre_process(state, config):
    print("Some work is being done...")
    await asyncio.sleep(5)
    print("work is done")
    #await asyncio.sleep(0)
    return {}

async def invoke(state, config):
    print("STATE")
    print(state)
    data = state['data']
    data_str = "\n".join([f"{k}: {v}" for k, v in data.items()])
    prompt_str = prompt.format(data=data_str)
    result = await model.ainvoke([prompt_str])
    print("RESULT")
    print(result)
    return {'result': result}

agent = StateGraph(State)
agent.add_node("pre_process", pre_process)
agent.add_node("invoke", invoke)
agent.add_edge("pre_process", "invoke")
agent.set_entry_point("pre_process")
agent.add_edge("invoke", END)

proportion_insight_agent = agent.compile(
    checkpointer=MemorySaver()
)