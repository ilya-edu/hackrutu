from pydantic import BaseModel, Field


# DEPRECATED
class WebSocketMessageDataObjectReference(BaseModel):
    """Модель ссылок в данных сообщения"""

    name: str = Field(description="Название источника")
    url: str = Field(description="URL источника")


class WebSocketMessageDataObjectUser(BaseModel):
    """Модель пользователя в данных сообщения"""

    id: int = Field(description="Внутренний ID пользователя")
    name: str = Field(description="Имя пользователя, оно же внешний ID")


class WebSocketMessageDataObject(BaseModel):
    """Модель объекта в данных сообщения"""

    id: int = Field(description="ID")
    room_id: int = Field(description="ID комнаты")
    assistant_room_id: int | None = Field(description="ID комнаты ассистента")
    last_message: bool | None = Field(
        description="Флаг, последнее ли это сообщение в стриме"
    )
    user_id: int = Field(description="Внутренний ID пользователя")
    text: str = Field(description="Текст сообщения")
    tg_text: str = Field(description="Текст сообщения для Telegram")
    # DEPRECATED
    # references: list[WebSocketMessageDataObjectReference]
    references: list[str] | None = Field(description="Ссылки на источники")
    created_at: str = Field(description="Дата создания сообщения")
    updated_at: str = Field(description="Дата изменения сообщения")
    user: WebSocketMessageDataObjectUser = Field(description="Данные об отправителе")


class WebSocketMessageData(BaseModel):
    """Модель данных в сообщении"""

    kind: str = Field(description="Тип сообщения")
    obj: WebSocketMessageDataObject = Field(
        alias="object", description="Данные сообщения"
    )


class WebSocketMessage(BaseModel):
    """Модель сообщения в WebSocket"""

    identifier: str = Field(description="Идентификатор типа канала")
    message: WebSocketMessageData = Field(description="Сообщение")
