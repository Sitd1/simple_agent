from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.runtime import Runtime

from simple_agent.graph.prompts.example_prompt import EXAMPLE_SYS_PROMPT, build_example_prompt
from simple_agent.graph.schemas.example_schema import ExampleSchema
from simple_agent.graph.deps import Deps
from simple_agent.graph.state import State


async def example_node(state: State, runtime: Runtime[Deps]) -> State:
    structured = runtime.context.llm.with_structured_output(ExampleSchema)

    messages = [
        SystemMessage(content=EXAMPLE_SYS_PROMPT),
        HumanMessage(content=build_example_prompt(message=state["messages"][-1])),
    ]

    answer = await structured.ainvoke(messages)
    return {'messages': answer}
