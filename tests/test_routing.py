from langchain_core.messages import AIMessage, HumanMessage

from simple_agent.graph.conditions import route_after_agent


def test_routes_to_tools_when_model_requests_them():
    message = AIMessage(content="", tool_calls=[{"name": "calculate", "args": {}, "id": "1"}])
    assert route_after_agent({"messages": [HumanMessage("x"), message]}) == "tools"


def test_ends_when_model_answers():
    assert route_after_agent({"messages": [AIMessage("Готово")]}) == "__end__"
