from langchain_openai import ChatOpenAI
from simple_agent.config.llm_config import BaseLLMConfig


def build_llm_client(config: BaseLLMConfig, **overrides) -> ChatOpenAI:
    return ChatOpenAI(
        model=config.model,
        api_key=config.api_key,
        base_url=config.base_url,          # https://openrouter.ai/api/v1
        temperature=config.temperature,
        timeout=config.timeout_seconds,
        **overrides,
    )


async def _main(q: str, llm_config: BaseLLMConfig) -> None:
    llm = build_llm_client(config=llm_config)
    resp = await llm.ainvoke(q)
    print(resp.content)


if __name__ == "__main__":
    from simple_agent.config import get_llm_config
    import asyncio
    asyncio.run(_main(q="А Ты кто, Воин?", llm_config=get_llm_config()))
