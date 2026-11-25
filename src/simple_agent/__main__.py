import asyncio

from langchain_core.messages import HumanMessage
from langgraph.errors import GraphRecursionError

from simple_agent.bootstrap.graph_deps import build_graph_deps
from simple_agent.graph.graph import build_graph
from simple_agent.infrastructure.checkpointer import manage_sqlite_checkpointer

EXIT_COMMANDS = {"exit", "quit", "выход"}

# Максимум шагов графа за один ответ: защищает от бесконечного цикла agent → tools → agent.
RECURSION_LIMIT = 10


async def chat() -> None:
    deps = build_graph_deps()
    config = {
        "configurable": {"thread_id": "cli_1"},
        "recursion_limit": RECURSION_LIMIT,
    }

    async with manage_sqlite_checkpointer() as checkpointer:
        graph = build_graph(checkpointer=checkpointer)
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
                    {"messages": [HumanMessage(user_input)]},
                    config=config,
                    context=deps
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
