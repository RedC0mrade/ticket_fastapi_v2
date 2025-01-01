from pathlib import Path

from pydantic import BaseModel
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "JuliaBars.sqlite3"


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class ApiPrefix(BaseModel):
    prefix: str = "/api"


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    poll_size: int = 50
    max_overflow: int = 10


class Settings(BaseSettings):
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

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
