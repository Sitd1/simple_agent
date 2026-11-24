from simple_agent.infrastructure.llm_client import get_llm_client
from simple_agent.graph.deps import Deps

async def build_deps():
    return Deps(llm=get_llm_client())
