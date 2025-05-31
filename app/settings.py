from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Authentication
    api_key: str = "default_api_key"

    # Database Settings
    database_url: str = "sqlite:///./fastqueue.db"  # Default SQLite database URL

    # Queue Settings
    visibility_timeout_seconds: int = 15  # Default message visibility timeout
    max_queue_length: int = 10000  # Optional limit for queue size
    restore_interval_ms: int = 500  # Interval for restoring messages in milliseconds

    # Logging / Debug
    debug: bool = False

    # Secret Key
    JWT_SECRET_KEY: str = "default_secret_key"
    JWT_REFRESH_SECRET_KEY: str = "default_refresh_secret_key"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 15  # 15 minutes
    JWT_REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # User
    default_username: str = "admin"
    default_password: str = "password"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
