from datetime import datetime

from langchain_core.tools import tool


@tool
def get_current_datetime() -> str:
    """Возвращает текущие дату и время с часовым поясом в формате ISO 8601."""
    return datetime.now().astimezone().isoformat(timespec="seconds")
