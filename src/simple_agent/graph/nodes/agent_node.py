from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langgraph.runtime import Runtime

from simple_agent.graph.prompts.agent_prompt import AGENT_SYS_PROMPT, build_agent_prompt
from simple_agent.graph.deps import GraphDeps
from simple_agent.graph.state import State
from simple_agent.graph.tools import TOOLS



async def agent_node(state: State, runtime: Runtime[GraphDeps]) -> State:
    llm = runtime.context.llm.bind_tools(TOOLS)
    messages = [SystemMessage(content=AGENT_SYS_PROMPT), *state["messages"]]
    response = await llm.ainvoke(messages)
    return {'messages': [response]}
