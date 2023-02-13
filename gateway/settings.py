from functools import lru_cache
from typing import Any, Optional

from pydantic import BaseSettings, Field, validator


class Settings(BaseSettings):
    class Config:
        env_prefix = ""
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"

    # Run
    server_host: str = Field(default="localhost", env="SERVER_HOST")
    server_port: int = Field(default=7000, env="SERVER_PORT")

    # RabbitMq
    rabbitmq_default_user: str = Field(default="guest", env="RABBITMQ_DEFAULT_USER")
    rabbitmq_default_pass: str = Field(default="guest", env="RABBITMQ_DEFAULT_PASS")
    rabbitmq_host: str = Field(default="127.0.0.1", env="RABBITMQ_HOST")
    rabbitmq_port: int = Field(default=5671, env="RABBITMQ_PORT")
    rabbitmq_vhost: str = Field(default="", env="RABBITMQ_VHOST")
    amqp_url: Optional[str]

    @validator("amqp_url")
    def amqp_url_path(cls, v: Any, values: Any) -> str:
        return "amqp://{user}:{password}@{host}:{port}/{vhost}".format(
            user=values.get("rabbitmq_default_user"),
            password=values.get("rabbitmq_default_pass"),
            host=values.get("rabbitmq_host"),
            port=values.get("rabbitmq_port"),
            vhost=values.get("rabbitmq_vhost"),
        )


@lru_cache()
def get_settings() -> Settings:
    return Settings()


setting = get_settings()
