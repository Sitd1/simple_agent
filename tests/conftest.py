from collections.abc import Callable, Sequence
from typing import Any

import pytest
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import AIMessage

from simple_agent.graph.deps import GraphDeps


class FakeToolCallingModel(GenericFakeChatModel):
    """GenericFakeChatModel не умеет bind_tools; в тестах инструменты просто игнорируются."""

    def bind_tools(self, tools: Sequence[Any], **kwargs: Any) -> "FakeToolCallingModel":  # type: ignore[override]
        return self


@pytest.fixture
def make_deps() -> Callable[..., GraphDeps]:
    """Фабрика зависимостей: модель по очереди вернёт переданные ответы."""

    def _make(*responses: AIMessage | str) -> GraphDeps:
        return GraphDeps(llm=FakeToolCallingModel(messages=iter(responses)))

    return _make
