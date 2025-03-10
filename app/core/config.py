from pathlib import Path

from pydantic import BaseModel
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent.parent.parent


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    users: str = "/users"
    tickets: str = "/tickets"
    tags: str = "/tags"
    ticket_tag_associations: str = "/ticket_tag_associations"
    relationship: str = "/relationship"
    messages: str = "/messages"
    blacklist: str = "/blacklist"
    bearer_token_url: str = "/auth/jwt/loggin"
    test: str = "/test"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    ticket_prefix: str = "/ticket"
    v1: ApiV1Prefix = ApiV1Prefix()


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="FASTAPI__",
        env_file=(".env", ".env_template"),
    )

    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig

    # private_key: Path = (
    #     BASE_DIR / "app" / "authentication" / "certs" / "jwt-private.pem"
    # )
    # public_key: Path = (
    #     BASE_DIR / "app" / "authentication" / "certs" / "jwt-public.pem"
    # )

    # algorithm: str = "RS256"
    # access_token_expire_minute: int = 24 * 60
    # access_token_refresh_days: int = 30


settings = Settings()
