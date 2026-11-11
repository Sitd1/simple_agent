from src.infrastructure.llm_client import get_llm_client
from src.graph.deps import Deps

async def build_deps():
    return Deps(llm=get_llm_client())
