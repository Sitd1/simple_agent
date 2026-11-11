from langgraph.graph import START, END, StateGraph

from src.graph.deps import Deps
from src.graph.state import State

from src.graph.nodes.example_node import example_node


def build_graph() -> StateGraph:
    graph = StateGraph(State, context_schema=Deps)

    graph.add_node("example", example_node)
    graph.add_edge(START, "example")
    graph.add_edge("example", END)
    return graph.compile()