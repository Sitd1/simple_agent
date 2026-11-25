from pathlib import Path

from charset_normalizer.md import lru_cache
from pydantic_settings import SettingsConfigDict

from simple_agent.config.base import ConfigBase


# LLM Agent (OpenRouter, OpenAI-совместимый API — см. scripts/indicator_manifest_search_llm_tag.py)
class StorageConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="STORAGE_")

    sqlite_path: str = "data/checkpoints.db"

    def ensure_dir(self) -> None:
        Path(self.sqlite_path).parent.mkdir(parents=True, exist_ok=True)




@lru_cache
def build_storage_config() -> StorageConfig:
    return StorageConfig()

if __name__ == "__main__":
    print(build_storage_config())
