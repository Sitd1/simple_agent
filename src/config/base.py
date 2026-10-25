from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# Загружаем переменные окружения из .env файла
load_dotenv()


def strip_wrapping_quotes(value: object) -> object:
    """Убирает кавычки, попавшие в значение из Makefile export или docker-compose."""
    if value is None:
        return value
    s = str(value).strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in ('"', "'"):
        return s[1:-1].strip()
    return s


class ConfigBase(BaseSettings):
    """Только общий model_config, никаких доменных полей."""
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )
