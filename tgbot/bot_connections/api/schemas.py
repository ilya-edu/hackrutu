from pydantic import BaseModel, Field


class MessageBody(BaseModel):
    """Модель тела запроса на создание сообщения"""

    text: str = Field(description="Текст сообщения")
    room_id: int | None = Field(description="ID комнаты чата")
    llm: str = Field(default="disabled")


class MessageResponseUser(BaseModel):
    """Модель пользователя в ответе на запрос"""

    id: int = Field(description="Внутренний ID пользователя")
    name: str = Field(description="Имя пользователя, оно же внешний ID")


class MessageResponse(BaseModel):
    """Модель ответа на запрос создания сообщения"""

    id: int = Field(description="ID сообщения")
    room_id: int = Field(description="ID комнаты")
    user_id: int = Field(description="Внутренний ID пользоватля")
    text: str = Field(description="Текст сообщения")
    references: list[str] | None = Field(description="Ссылки на источники")
    created_at: str = Field(description="Дата создания сообщения")
    updated_at: str = Field(description="Дата изменения сообщения")
    user: MessageResponseUser
