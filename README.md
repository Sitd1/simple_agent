# simple_agent

Шаблон агента на [LangGraph](https://langchain-ai.github.io/langgraph/). Граф, узлы, промпты и инфраструктура разложены по отдельным слоям, а клиенты LLM передаются в граф при вызове через `context_schema`. Поэтому граф компилируется один раз, не зависит от конкретных клиентов и тестируется без сети.

## Быстрый старт

Нужны [uv](https://docs.astral.sh/uv/) и Python версии, указанной в `pyproject.toml`.

```bash
uv sync                          # окружение + пакет в editable-режиме
cp .env.example .env             # заполните ключи
uv run python -m simple_agent    # запуск агента
uv run pytest                    # тесты
```

## Структура

```
src/simple_agent/
├── __main__.py           # точка входа
├── bootstrap/
│   └── graph_deps.py     # build_deps(): создаёт реальные клиенты из настроек
├── config/               # Settings (pydantic-settings), по файлу на секцию
├── graph/
│   ├── deps.py           # GraphDeps: что нужно узлам
│   ├── state.py          # состояние графа
│   ├── graph.py          # сборка и compile(), build_graph() -> StateGraph
│   ├── nodes/            # узлы: async (state, runtime) -> dict
│   ├── conditions/       # функции ветвления для add_conditional_edges
│   ├── prompts/          # тексты промптов, шаблоны промптов
│   ├── tools/            # встроенные инструменты
│   └── schemas/          # Pydantic-схемы для structured output
└── infrastructure/       # фабрики клиентов LLM и эмбеддингов
tests/                    # conftest.py с фейковыми зависимостями
notebooks/                # эксперименты (в .gitignore)
```

## Как устроены зависимости

```
.env → Settings → build_deps() → GraphDeps → graph.ainvoke(..., context=deps) → runtime.context в узлах
```

Шаблон держится на трёх правилах:

- Узлы не импортируют `infrastructure` и не читают настройки. Всё, что им нужно, они получают из `runtime.context`.
- Реальные клиенты создаются только в `bootstrap/graph_deps.py`.
- Граф компилируется без зависимостей, они передаются при каждом вызове. В тестах вместо реальных клиентов передаются фейковые.

## Конфигурация

Настройки читаются из переменных окружения и файла `.env`. Вложенные секции разделяются через префикс:
Префиксы задаются при создании config в `src/simple_agent/config/`

```dotenv
LLM_MODEL=...
LLM_API_KEY=...
LLM_BASE_URL=...        # опционально

# Эмбеддинги опциональны: если секция не задана, embedder в GraphDeps будет None
EMBEDDING_MODEL=...
```

Полный список переменных лежит в `.env.example`.

## Как добавить узел

1. **Промпт.** Создайте `graph/prompts/<name>_prompt.py` с константой промпта.

2. **Схема**, если нужен structured output. Опишите Pydantic-модель в `graph/schemas/`.

3. **Узел.** Создайте `graph/nodes/<name>_node.py`. Узел получает состояние и `runtime`, а возвращает только изменившиеся поля состояния:

   ```python
   from langgraph.runtime import Runtime

   from simple_agent.graph.deps import GraphDeps
   from simple_agent.graph.prompts.summarize_prompt import SUMMARIZE_PROMPT
   from simple_agent.graph.state import State


   async def summarize_node(state: State, runtime: Runtime[GraphDeps]) -> dict:
       messages = [("system", SUMMARIZE_PROMPT), *state["messages"]]
       answer = await runtime.context.llm.ainvoke(messages)
       return {"messages": [answer]}
   ```

4. **Регистрация.** Добавьте узел и рёбра в `graph/graph.py`. Если после узла нужно ветвление, функцию выбора положите в `graph/conditions/`. Тип `Literal` в её аннотации позволяет LangGraph правильно отрисовать граф:

   ```python
   # graph/conditions/example_condition.py
   from typing import Literal

   from simple_agent.graph.state import State


   def route_after_example(state: State) -> Literal["summarize", "__end__"]:
       return "summarize" if len(state["messages"]) > 10 else "__end__"
   ```

   ```python
   # graph/graph.py
   builder.add_node("summarize", summarize_node)
   builder.add_conditional_edges("example", route_after_example)
   builder.add_edge("summarize", END)
   ```

5. **Тест.** Добавьте проверку в `tests/`, используя фикстуру `fake_deps`.

## Как добавить зависимость

Например, клиент базы данных или поиска:

1. Фабрика клиента в `infrastructure/`.
2. Секция настроек в `config/` и переменные в `.env.example`.
3. Поле в `GraphDeps` (`graph/deps.py`).
4. Создание клиента в `build_deps()` (`bootstrap/graph_deps.py`).
5. Фейковая реализация в `tests/conftest.py`.

## Тесты

Тесты не ходят в сеть: вместо настоящей модели в граф передаётся `GenericFakeChatModel`, которая возвращает заранее заданные ответы.

```python
# tests/conftest.py
import pytest
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel

from simple_agent.graph.deps import GraphDeps


@pytest.fixture
def fake_deps() -> GraphDeps:
    return GraphDeps(llm=GenericFakeChatModel(messages=iter(["Привет!"])))
```

```python
# tests/test_graph_smoke.py
from simple_agent.graph.graph import build_graph


async def test_graph_answers(fake_deps):
    graph = build_graph()
    result = await graph.ainvoke({"messages": [("user", "hello")]}, context=fake_deps)
    assert result["messages"][-1].content == "Привет!"
```

```bash
uv run pytest
```

## Ноутбуки

Ноутбуки в `notebooks/` работают в окружении проекта, поэтому в качестве ядра выберите `.venv`. Пакет установлен в editable-режиме, а чтобы изменения в `src/` подхватывались без перезапуска ядра, включите autoreload:

```python
%load_ext
autoreload
%autoreload
2

from simple_agent.bootstrap.graph_deps import build_graph_deps
from simple_agent.graph.graph import graph

result = await graph.ainvoke({"messages": [("user", "Привет")]}, context=build_graph_deps())
```

## Разработка

```bash
uv run ruff check .      # линтер
uv run ruff format .     # форматирование
uv run mypy src          # проверка типов
```
