import sys

sys.stdin.reconfigure(encoding="utf-8", errors="replace")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")


import argparse
import asyncio

from langchain_core.messages import HumanMessage
from langgraph.errors import GraphRecursionError

from simple_agent.bootstrap.graph_deps import build_graph_deps
from simple_agent.bootstrap.helpers import make_run_config
from simple_agent.graph.graph import build_graph
from simple_agent.infrastructure.checkpointer import manage_sqlite_checkpointer

EXIT_COMMANDS = {"exit", "quit", "выход"}

# Максимум шагов графа за один ответ: защищает от бесконечного цикла agent → tools → agent.
RECURSION_LIMIT = 10


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Simple Agent CLI")
    parser.add_argument("--user", default="local_user", help="ID пользователя")
    parser.add_argument("--thread", default="cli", help="ID диалога (треда)")
    return parser.parse_args()


async def chat(user_id: str, thread_id: str) -> None:
    deps = build_graph_deps()
    config = make_run_config(
        user_id=user_id,
        thread_id=thread_id,
        recursion_limit=RECURSION_LIMIT
    )

    async with manage_sqlite_checkpointer() as checkpointer:
        graph = build_graph(checkpointer=checkpointer)
        print(f"Агент готов [user={user_id}, thread={thread_id}]. Для выхода введите exit.")

        while True:
            try:
                user_input = input("\nвы> ")
                user_input.encode("utf-8", errors="ignore").decode("utf-8")
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
    args = parse_args()
    asyncio.run(chat(user_id=args.user, thread_id=args.thread))


if __name__ == "__main__":
    main()
