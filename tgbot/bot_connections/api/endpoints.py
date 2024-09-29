from enum import Enum


class ChatApiHandlersV1(Enum):
    """Ручки для API чата v1"""

    # Создать сообщение
    POST_CREATE_MESSAGE = "/messages.json"

    # Получить сообщения
    GET_MESSAGES = "/messages.json"

    def handler_url(self, host: str) -> str:
        """Получение полного пути к хендлеру"""
        return f"{host}{self.value}"

    def __str__(self) -> str:
        return self.value
