from enum import Enum


class ChatWebSocketHandlersV1(Enum):
    """Ручки для WebSocket v1"""

    CABLE = "/cable"

    GET_MESSAGES = "/messages.json"

    def handler_url(self, host: str) -> str:
        """Получение полного пути к хендлеру"""
        return f"{host}{self.value}"

    def __str__(self) -> str:
        return self.value
