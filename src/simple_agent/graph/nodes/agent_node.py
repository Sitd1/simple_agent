from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.runtime import Runtime

from simple_agent.graph.prompts.agent_prompt import AGENT_SYS_PROMPT, build_agent_prompt
from simple_agent.graph.schemas import AgentSchema
from simple_agent.graph.deps import Deps
from simple_agent.graph.state import State


TOOLS = None

async def agent_node(state: State, runtime: Runtime[Deps]) -> State:
    llm = runtime.context.llm.bind_tools(TOOLS)
    structured = llm.with_structured_output(AgentSchema)

    messages = [
        SystemMessage(content=AGENT_SYS_PROMPT),
        HumanMessage(content=build_agent_prompt(message=state["messages"][-1])),
    ]

    response = await structured.ainvoke(messages)
    return {'messages': response}
