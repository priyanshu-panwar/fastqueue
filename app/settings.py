from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Authentication
    api_key: str = "default_api_key"

    # Database Settings
    database_url: str = "sqlite:///./fastqueue.db"  # Default SQLite database URL

    # Queue Settings
    visibility_timeout_seconds: int = 15  # Default message visibility timeout
    max_queue_length: int = 10000  # Optional limit for queue size

    # Logging / Debug
    debug: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
