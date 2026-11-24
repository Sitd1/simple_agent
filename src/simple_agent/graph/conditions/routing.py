from typing import Literal

from langchain_core.messages import AIMessage

from simple_agent.graph.state import State


def route_after_agent(state: State) -> Literal["tools", "__end__"]:
    """Если модель запросила инструменты, идём в tools, иначе завершаем."""
    last_message = state["messages"][-1]
    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        return "tools"
    return "__end__"
