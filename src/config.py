from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    postgres_db: str = Field()
    postgres_user: str = Field()
    postgres_password: str = Field()
    postgres_port: int = Field()
    postgres_host: str = Field()

    secret_key: str = Field()
    algorithm: str = Field()

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
