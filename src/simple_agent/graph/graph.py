from langgraph.graph import START, END, StateGraph
from langgraph.prebuilt import ToolNode

from simple_agent.graph.deps import Deps
from simple_agent.graph.state import State

from simple_agent.graph.nodes.agent_node import agent_node


def build_graph() -> StateGraph:
    builder = StateGraph(State, context_schema=Deps)

    builder.add_node("agent", agent_node())
    builder.add_node("tools", ToolNode(TOOLS))

    builder.add_edge(START, "agent")
    builder.add_edge("agent", END)
    return builder.compile()

