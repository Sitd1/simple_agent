import asyncio

from langchain_core.messages import AnyMessage, HumanMessage
from langgraph.errors import GraphRecursionError

from simple_agent.bootstrap.graph_deps import build_deps
from simple_agent.graph.graph import build_graph


EXIT_COMMANDS = {"exit", "quit", "выход"}

# Максимум шагов графа за один ответ: защищает от бесконечного цикла agent → tools → agent.
RECURSION_LIMIT = 10


async def chat() -> None:
    deps = build_deps()
    messages: list[AnyMessage] = []
    graph = build_graph()
    print("Агент готов. Для выхода введите exit или нажмите Ctrl+D.")

    while True:
        try:
            user_input = input("\nвы> ")
        except (EOFError, KeyboardInterrupt) as e:
            print(e)
            break
        if not user_input:
            continue
        if user_input.lower() in EXIT_COMMANDS:
            break

        try:
            result = await graph.ainvoke(
                {"messages": [*messages, HumanMessage(user_input)]},
                context=deps,
                cconfig={"recursion_limit": RECURSION_LIMIT},
            )
        except GraphRecursionError as e:
            print(e)
            print("агент> Не уложился в лимит шагов, попробуйте переформулировать вопрос.")
            continue

        messages = result["messages"]
        print(f"агент> {messages[-1].content}")


def main() -> None:
    asyncio.run(chat())


if __name__ == "__main__":
    main()
