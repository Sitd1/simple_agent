from langgraph.graph import START, END, StateGraph

from simple_agent.graph.deps import Deps
from simple_agent.graph.state import State

from simple_agent.graph.nodes.agent_node import example_node


def build_graph() -> StateGraph:
    graph = StateGraph(State, context_schema=Deps)

    graph.add_node("example", example_node)
    graph.add_edge(START, "example")
    graph.add_edge("example", END)
    return graph.compile()

