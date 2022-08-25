from os import getenv, path
from typing import Optional, List
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
    JWT_ACCESS_TOKEN_EXPIRES: int = int(getenv("JWT_ACCESS_TOKEN_EXPIRES", "600"))  # 10 Minutes
    JWT_REFRESH_TOKEN_EXPIRES: int = int(getenv("JWT_REFRESH_TOKEN_EXPIRES", "2592000"))  # 30 Days
    ADMIN_USERNAME: str = getenv("ADMIN_USERNAME")
    ADMIN_PASSWORD: str = getenv("ADMIN_PASSWORD")
    MAX_LOGIN_ATTEMPT: int = 5
    LOGIN_FORBIDDEN_TIME: int = 5  # 5 Minutes
    ALLOWED_IMAGE_TYPES: List[str] = ["PNG", "JPEG"]
    MAX_IMAGE_SIZE: int = 1024 * 1024 * 10  # 10MB
    BASE_DIR: str = path.dirname(path.dirname(path.abspath(__file__)))
    MEDIA_DIR: str = path.join(BASE_DIR, "media")
    USER_PROFILE_IMAGE_DIR: str = path.join(MEDIA_DIR, "user_profile_images")
    USER_PROFILE_REVEAL_IMAGE_DIR: str = USER_PROFILE_IMAGE_DIR[USER_PROFILE_IMAGE_DIR.find("/media"):]
    PRODUCT_IMAGE_DIR: str = path.join(MEDIA_DIR, "product_images")
    PRODUCT_REVEAL_IMAGE_DIR: str = PRODUCT_IMAGE_DIR[PRODUCT_IMAGE_DIR.find("/media"):]
    REVIEW_IMAGE_DIR: str = path.join(MEDIA_DIR, "review_images")
    REVIEW_REVEAL_IMAGE_DIR: str = REVIEW_IMAGE_DIR[REVIEW_IMAGE_DIR.find("/media"):]
    BEAUTY_IMAGE_DIR: str = path.join(MEDIA_DIR, "beauty_images")


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
