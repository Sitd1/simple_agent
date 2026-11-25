from simple_agent.config.llm_config import BaseLLMConfig, build_llm_config

from simple_agent.graph.deps import GraphDeps
from simple_agent.infrastructure.llm_client import build_llm_client


def build_graph_deps(llm_config: BaseLLMConfig | None = None) -> GraphDeps:
    config = llm_config or build_llm_config()
    llm = build_llm_client(config)
    return GraphDeps(llm=llm)
