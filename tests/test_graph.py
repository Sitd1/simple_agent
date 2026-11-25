from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

from simple_agent.graph.graph import build_graph

graph = build_graph()


async def test_answers_without_tools(make_deps):
    deps = make_deps("Привет!")

    result = await graph.ainvoke({"messages": [HumanMessage("Привет")]}, context=deps)

    assert result["messages"][-1].content == "Привет!"


async def test_calls_calculator_and_answers(make_deps):
    deps = make_deps(
        AIMessage(
            content="",
            tool_calls=[{"name": "calculate", "args": {"expression": "2 + 2 * 2"}, "id": "call_1"}],
        ),
        "Получается 6.",
    )

    result = await graph.ainvoke(
        {"messages": [HumanMessage("Сколько будет 2 + 2 * 2?")]}, context=deps
    )

    tool_messages = [m for m in result["messages"] if isinstance(m, ToolMessage)]
    assert [m.content for m in tool_messages] == ["6"]
    assert result["messages"][-1].content == "Получается 6."
