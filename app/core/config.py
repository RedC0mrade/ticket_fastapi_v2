from pathlib import Path

from pydantic import BaseModel
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class ApiPrefix(BaseModel):
    prefix: str = "/api"


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="FASTAPI__",
        env_file=(".env", ".env_template")
    )
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig

    private_key: Path = (
        BASE_DIR / "app" / "authentication" / "certs" / "jwt-private.pem"
    )
    public_key: Path = (
        BASE_DIR / "app" / "authentication" / "certs" / "jwt-public.pem"
    )

    algorithm: str = "RS256"
    access_token_expire_minute: int = 24 * 60
    access_token_refresh_days: int = 30


settings = Settings()
