# API configuration and credential management for API operation



from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):

    # app
    APP_NAME: str = "Northwind Enterprise API"
    APP_VERSION: str = "1.0.0"
    APP_DEBUG: bool = False

    # databes config (postgresql)
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    # redis
    REDIS_PORT: int
    REDIS_HOST: str


    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )



settings = Settings()


