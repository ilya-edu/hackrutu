import pydantic_core
from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bot_token: SecretStr = Field(description="Токен бота")

    level: str = Field(description="Уровень логирования")

    web_url: str = Field(description="URL адрес системы")

    api_url: str = Field(description="API URL адрес")
    api_port: str = Field(description="API Порт")

    ws_url: str = Field(description="WebSocket адрес")
    ws_port: str = Field(description="WebSocket порт")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


try:
    config = Settings()
except pydantic_core._pydantic_core.ValidationError as err:
    print(err)
    print("Невозможно загрузить настройки бота из файла `.env`")
    exit(-1)
