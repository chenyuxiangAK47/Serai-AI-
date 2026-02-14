from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "serai-backend"
    version: str = "0.1.0"

    generator_mode: str = "mock"  # mock | llm
    llm_api_key: str | None = None  # 不要硬编码，走 env

    class Config:
        env_file = ".env"  # 本地开发用
        extra = "ignore"


settings = Settings()
