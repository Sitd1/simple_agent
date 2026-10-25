from dotenv import load_dotenv
from pydantic import AliasChoices, SecretStr, field_validator, Field
from pydantic_settings import SettingsConfigDict, BaseSettings

from src.config.base import ConfigBase, strip_wrapping_quotes


load_dotenv()


# LLM Agent (OpenRouter, OpenAI-совместимый API — см. scripts/indicator_manifest_search_llm_tag.py)
class BaseLLMConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="LLM_")

    # alias'ы на OPENROUTER_* — тот же ключ/модель, что читает
    # scripts/indicator_manifest_search_llm_tag.py напрямую из os.environ, чтобы
    # секрет не дублировался в .env под двумя разными именами.
    api_key: SecretStr | None = Field(
        default=None,
        validation_alias=AliasChoices("LLM_API_KEY", "OPENROUTER_API_KEY"),
    )
    model: str = Field(
        default="anthropic/claude-haiku-4.5",
        validation_alias=AliasChoices("LLM_MODEL", "OPENROUTER_MODEL"),
    )
    base_url: str = "https://openrouter.ai/api/v1"
    max_retries: int = 2
    temperature: float = 0.1
    timeout_seconds: float = 300.0

    retry_max_attempts: int = 5
    retry_min_wait_seconds: float = 1.0
    retry_max_wait_seconds: float = 60.0
    retry_jitter_seconds: float = 1.0

    batch_delay_seconds: float = 1.0

    @field_validator("base_url", "model", "api_key", mode="before")
    @classmethod
    def _strip_quotes(cls, value: object) -> object:
        return strip_wrapping_quotes(value)


# class ModelSettings(BaseSettings):
#     model: str = Field(
#         default="Qwen/Qwen2.5-32B-Instruct-GPTQ-Int4",
#         validation_alias="model_name",
#     )
#     api_key: str = Field(default="EMPTY")
#     base_url: str = Field(default="http://vllm:8000/v1")
#     temperature: float = Field(default=0)
#     extra_body: dict = Field(
#         default_factory=lambda: {"chat_template_kwargs": {"enable_thinking": False}},
#     )
#     model_config = SettingsConfigDict(
#         env_prefix="MODEL_",
#         env_file_encoding="utf-8",
#     )


llm_config = BaseLLMConfig()

if __name__ == "__main__":
    print(llm_config)
