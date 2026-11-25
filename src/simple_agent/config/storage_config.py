from pathlib import Path

from charset_normalizer.md import lru_cache
from pydantic import field_validator
from pydantic_settings import SettingsConfigDict

from simple_agent.config.base import ConfigBase
from simple_agent.config.constants import PROJECT_ROOT


# LLM Agent (OpenRouter, OpenAI-совместимый API — см. scripts/indicator_manifest_search_llm_tag.py)
class StorageConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="STORAGE_")

    sqlite_path: Path = PROJECT_ROOT / "data" / "checkpoints.db"

    @field_validator("sqlite_path", mode="before")
    @classmethod
    def resolve_path(cls, value: str | Path) -> Path:
        path = Path(value)
        if not path.is_absolute():
            return PROJECT_ROOT / path
        return path

    def ensure_dir(self) -> None:
        self.sqlite_path.parent.mkdir(parents=True, exist_ok=True)




@lru_cache
def build_storage_config() -> StorageConfig:
    return StorageConfig()

if __name__ == "__main__":
    print(build_storage_config())
