from os import getenv
from typing import Optional
from urllib.parse import quote


class Config:
    RUNNING_ENV: str = getenv("RUNNING_ENV", "local")
    DEBUG: bool = True
    APP_NAME: str = getenv("APP_NAME")
    APP_HOST: str = getenv("APP_HOST", "0.0.0.0")
    APP_PORT: int = int(getenv("APP_PORT", "8000"))
    APP_TIMEZONE: str = getenv("APP_TIMEZONE", "Asia/Seoul")
    DOCS_URL: Optional[str] = "/docs"
    REDOC_URL: Optional[str] = "/redoc"
    DB_URL: str = f"mysql+aiomysql://{quote(getenv('DB_USERNAME'))}:{quote(getenv('DB_PASSWORD'))}@" \
                  f"{quote(getenv('DB_HOST'))}:{getenv('DB_PORT')}/{quote(getenv('DB_NAME'))}"
    JWT_SECRET_KEY: str = getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM: str = getenv("JWT_ALGORITHM", "HS256")
    JWT_ACCESS_TOKEN_EXPIRES: int = int(getenv("JWT_ACCESS_TOKEN_EXPIRES", "3600"))  # 1 hour
    JWT_REFRESH_TOKEN_EXPIRES: int = int(getenv("JWT_REFRESH_TOKEN_EXPIRES", "2592000"))  # 30 days
    ADMIN_USERNAME: str = getenv("ADMIN_USERNAME")
    ADMIN_PASSWORD: str = getenv("ADMIN_PASSWORD")


class LocalConfig(Config):
    pass


class ProductionConfig(Config):
    DEBUG: str = False
    DOCS_URL: None
    REDOC_URL: None


def get_config():
    running_env = getenv("RUNNING_ENV", "local")
    config_type = {
        "local": LocalConfig(),
        "production": ProductionConfig(),
    }
    return config_type[running_env]


config: Config = get_config()
