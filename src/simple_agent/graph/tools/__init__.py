from simple_agent.graph.tools.calculator import calculate
from simple_agent.graph.tools.datetime_tool import get_current_datetime

# Единый список: его используют и bind_tools в узле агента, и ToolNode в графе
TOOLS = [calculate, get_current_datetime]

__all__ = ["TOOLS", "calculate", "get_current_datetime"]
