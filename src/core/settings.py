from typing import Annotated, Any

from dotenv import find_dotenv
from pydantic import BeforeValidator, HttpUrl, SecretStr, TypeAdapter, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


def check_str_is_http(x: str) -> str:
    http_url_adapter = TypeAdapter(HttpUrl)
    return str(http_url_adapter.validate_python(x))


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=find_dotenv(),
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
        validate_default=False,
    )
    MODE: str | None = None

    HOST: str = "0.0.0.0"
    PORT: int = 80

    AUTH_SECRET: SecretStr | None = None

    OPENAI_API_KEY: SecretStr | None = None
    USE_FAKE_MODEL: bool = False

    ##DEEPSEEK_API_KEY: SecretStr | None = None
    ##ANTHROPIC_API_KEY: SecretStr | None = None
    ##GOOGLE_API_KEY: SecretStr | None = None
    ##GROQ_API_KEY: SecretStr | None = None
    ##USE_AWS_BEDROCK: bool = False
    ##OLLAMA_MODEL: str | None = None
    ##OLLAMA_BASE_URL: str | None = None

    HTTP_DATA_SERVER: str = "data-server"
    HTTP_QUERY_SERVER: str = "query-server"

    DATABASE_USER: str = None
    DATABASE_PASSWORD: str = None
    DATABASE_HOST: str = None
    DATABASE_NAME: str = None
    DATABASE_PORT: str = "5432"

    @computed_field
    @property
    def BASE_URL(self) -> str:
        return f"http://{self.HOST}:{self.PORT}"
    
    @computed_field
    @property
    def DB_URI(self) -> str:
        return f"postgresql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"

    def is_dev(self) -> bool:
        return self.MODE == "dev"


settings = Settings()
