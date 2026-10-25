from functools import lru_cache
from langchain_openai import OpenAIEmbeddings


from src.config.embedding_config import EmbedConfig, get_embed_config


@lru_cache(maxsize=1)
def get_embedding_service(cfg: EmbedConfig | None = None) -> OpenAIEmbeddings:
    """Клиент эмбеддингов.

    embed_query(text)            -> вектор одной строки
    embed_documents([t1, t2])    -> батч; режется по chunk_size
    aembed_documents([...])      -> асинхронный вариант
    """
    cfg = cfg or get_embed_config()
    return OpenAIEmbeddings(
        model=cfg.model,
        api_key=cfg.api_key,
        base_url=cfg.base_url,
        dimensions=cfg.dimensions,        # None -> параметр не уйдёт в запрос
        chunk_size=cfg.batch_size,
        max_retries=cfg.max_retries,
        request_timeout=cfg.timeout_seconds,
        # для не-OpenAI эндпоинта отключаем токенизацию через tiktoken
        check_embedding_ctx_length=cfg.base_url is None,
    )


if __name__ == "__main__":
    embed_model = get_embedding_service()

    # Пример создания эмбеддинга для одной строки
    text = "Что ты, Воин?"
    # vector = embed_model.embed_query(text)
    # print(f"Длина вектора: {len(vector)}")
    # print(f"Первые 5 значений: {vector[:5]}")
    vectors = embed_model.embed_documents([text, text])
    print(len(vectors))
    print(len(vectors[0]))
    print(vectors[0][:5])
