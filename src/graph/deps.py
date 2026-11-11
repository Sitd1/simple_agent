from dataclasses import dataclass
from langchain_core.language_models import BaseChatModel


@dataclass
class Deps:
    llm: BaseChatModel
