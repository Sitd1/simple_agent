from langgraph.graph import START, StateGraph
from langgraph.prebuilt import ToolNode

from simple_agent.graph.deps import GraphDeps
from simple_agent.graph.state import State

from simple_agent.graph.nodes.agent_node import agent_node
from simple_agent.graph.tools import TOOLS
from simple_agent.graph.conditions import route_after_agent


def build_graph() -> StateGraph:
    builder = StateGraph(State, context_schema=GraphDeps)

    builder.add_node("agent", agent_node)
    builder.add_node("tools", ToolNode(TOOLS))

    builder.add_edge(START, "agent")
    builder.add_conditional_edges("agent", route_after_agent)
    builder.add_edge("tools", "agent")

    return builder.compile()
