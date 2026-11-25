from dataclasses import dataclass
from langchain_core.language_models import BaseChatModel


@dataclass
class GraphDeps:
    llm: BaseChatModel
