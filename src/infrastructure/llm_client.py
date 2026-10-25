from langchain_openai import ChatOpenAI
from src.config.llm_config import llm_config


def get_llm_client(**overrides) -> ChatOpenAI:
    if llm_config.api_key is None:
        raise RuntimeError("LLM_API_KEY (или OPENROUTER_API_KEY) не задан")
    return ChatOpenAI(
        model=llm_config.model,
        api_key=llm_config.api_key.get_secret_value(),
        base_url=llm_config.base_url,          # https://openrouter.ai/api/v1
        temperature=llm_config.temperature,
        timeout=llm_config.timeout_seconds,
        **overrides,
    )


async def _main(q: str) -> None:
    llm = get_llm_client()
    resp = await llm.ainvoke(q)
    print(resp.content)


if __name__ == "__main__":
    import asyncio
    asyncio.run(_main(q="А Ты кто, Воин?"))
