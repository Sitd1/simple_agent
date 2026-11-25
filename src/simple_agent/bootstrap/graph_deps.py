from simple_agent.config import get_llm_config
from simple_agent.infrastructure.llm_client import build_llm_client
from simple_agent.graph.deps import GraphDeps

def build_deps():
    return GraphDeps(llm=build_llm_client(config=get_llm_config()))
