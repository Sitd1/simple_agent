from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.runtime import Runtime

from src.graph.prompts.example_prompt import EXAMPLE_SYS_PROMPT, build_example_prompt
from src.graph.schemas.example_schema import ExampleSchema
from src.graph.deps import Deps
from src.graph.state import State


async def example_node(state: State, runtime: Runtime[Deps]) -> State:
    structured = runtime.context.llm.with_structured_output(ExampleSchema)

    messages = [
        SystemMessage(content=EXAMPLE_SYS_PROMPT),
        HumanMessage(content=build_example_prompt(message=state["messages"][-1])),
    ]

    answer = await structured.ainvoke(messages)
    return {'messages': answer}
