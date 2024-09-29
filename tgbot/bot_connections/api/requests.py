import logging
import uuid

import aiohttp
import pydantic_core

from bot_connections.api.endpoints import ChatApiHandlersV1 as Handlers
from bot_connections.api.schemas import MessageBody, MessageResponse
from config import config

# TODO: сделать нормальное хранилище

# Словарь для хранения связи между user_id и id комнаты на платформе
user_ids_to_room_ids = {}

# Словарь для хранения связи между ID юзера в Telegram и ID юзера на платформе
tg_user_ids_to_user_ids = {}

# Стандартный заголовок для хэндлера
default_headers = {"Content-Type": "application/json"}

# Telegram ID юзеров
user_mode_ids = []


async def create_message(
    user_id: str | None,
    room_id: int | None,
    message_text: str | None,
    tg_user_id: int | None,
    user_mode: bool | None,
) -> MessageResponse | str:
    """
    Отправка сообщения в систему.

    Args:
        user_id (str | None): ID пользователя в системе
        room_id (int | None): ID комнаты в системе
        message_text (str | None): Текст сообщения для отправки на сервер
        tg_user_id (int | None): ID пользователя в Telegram
        user_mode (bool | None): флаг режима пользователя

    Returns:
        dict: Словарь с ответом сервера или информацией об ошибке
    """
    api_url = f"{config.api_url}{Handlers.POST_CREATE_MESSAGE.value}"

    if not user_id:
        user_id = f"tg_user_{uuid.uuid4()}"
    if not room_id:
        room_id = None
    if not message_text:
        message_text = "У меня есть вопрос"

    params = {"username": user_id}

    message_body = MessageBody(text=message_text, room_id=room_id)

    if not user_mode:
        message_body.llm = "enabled"

    # Сессия содержит внутри пул подключений
    # Плохая идея создавать сессию под каждый запрос, но мы на хакатоне)))
    # TODO: Переделать на оправку единичного запроса
    async with aiohttp.ClientSession(
        headers=default_headers,
    ) as session:
        try:
            # Отправка POST запроса для создания первого сообщения и инициализации комнаты
            async with session.post(
                api_url,
                params=params,
                data=message_body.model_dump_json().encode(),
                ssl=False,
            ) as response:
                logging.debug(f"Отправка сообщения. URL: {response.url}")
                if response.status == 200:
                    response_json = await response.json()
                    try:
                        # Валидация полученных данных
                        result = MessageResponse.model_validate(response_json)
                        user_ids_to_room_ids[user_id] = result.room_id
                        # Создание связи между tg id и user id
                        if tg_user_id:
                            tg_user_ids_to_user_ids[tg_user_id] = user_id
                        return result
                    except pydantic_core._pydantic_core.ValidationError:
                        logging.error(response_json)
                        return "❌ Ошибка валидации данных с сервера"
                else:
                    err_str = f"❌ Ошибка сервера: {response.status}"
                    logging.error(response.json)
                    logging.error(err_str)
                    return err_str
        except aiohttp.ClientError as e:
            err_str = f"❌ Ошибка при отправке запроса: {str(e)}"
            logging.error(err_str)
            return err_str
