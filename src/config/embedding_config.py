from dotenv import load_dotenv
from pydantic import SecretStr
from pydantic_settings import SettingsConfigDict

from src.config.base import ConfigBase

load_dotenv()


class EmbedConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="EMB_")

    api_key: SecretStr
    model: str
    base_url: str | None = None

    dimensions: int | None = None       # None -> не отправляем параметр
    timeout_seconds: float = 60.0

    batch_size: int = 128
    max_retries: int = 5        # -> ретраи openai SDK внутри LangChain



def get_embed_config() -> EmbedConfig:
    return EmbedConfig()



if __name__ == "__main__":
    embed_model_config = get_embed_config()
    print(embed_model_config)
