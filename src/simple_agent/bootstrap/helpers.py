from langchain_core.runnables import RunnableConfig


def make_run_config(
    user_id: str = "default_user",
    thread_id: str = "default",
    recursion_limit: int = 10,
) -> RunnableConfig:
    return {
        "configurable": {
            "thread_id": f"{user_id}:{thread_id}",  # Изоляция памяти в SQLite по пользователю
            "user_id": user_id,                     # Сырой user_id для нод/инструментов
        },
        "recursion_limit": recursion_limit,
    }
