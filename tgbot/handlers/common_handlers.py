import asyncio
from datetime import datetime
import logging

from aiogram import F, Router, html
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender
from aiogram.utils.formatting import Text, as_list, as_marked_section

from bot_connections.api.requests import (
    create_message,
    user_ids_to_room_ids,
    tg_user_ids_to_user_ids,
    user_mode_ids,
)
from bot_connections.sockets.sockets import websocket_listener, ws_connections
from keyboards import common_keyboards as kbs

from config import config

router = Router()


@router.message(
    CommandStart(deep_link=True),
)
async def command_start_chat_from_web(
    message: Message, command: CommandObject, chat_info: dict
) -> None:
    """
    Хэндлер для обработки перехода с сайта.

    Args:
        message (Message): сообщение пользователя
        command (CommandObject): уникальный ID пользователя в системе
        chat_info (dict): словарь для хранения ID пользователя в системе и Telegram
    """
    chat_info["web_id"][message.from_user.id] = command.args
    answer = f"Здравствуйте, {html.bold(message.from_user.full_name)}!\n"
    answer += f"Ваш ID: {html.code(command.args)}\n"
    answer += "Вы можете продолжить общение в чате, история ваших сообщений сохранена."
    async with ChatActionSender.typing(bot=message.bot, chat_id=message.chat.id):
        await message.answer(answer)
        # TODO: получать ID комнаты в command.args
        api_message = await create_message(
            user_id=command.args,
            room_id=None
            if command.args not in user_ids_to_room_ids
            else user_ids_to_room_ids[command.args],
            message_text=None,
            tg_user_id=message.from_user.id,
            user_mode=True,
        )
        if isinstance(api_message, str):
            await message.answer(api_message)
        else:
            if config.level == "DEBUG":
                a = (
                    f"{html.bold("Вы находитесь в режиме оператора-админа")} (для теста).\n"
                    + "Ваш запрос будет обработан ИИ без участия оператора поддержки."
                    + "Если хотите переключиться на режим обычного пользователя, "
                    + "воспользуйтесь меню бота и выберете «Пользователь».\n"
                )
                room_str = f"Room ID: {api_message.room_id}"
                await message.answer(a + room_str)
        if message.chat.id not in ws_connections:
            # Запуск нового WebSocket listener для этого chat_id
            asyncio.create_task(
                websocket_listener(
                    message.bot,
                    message.chat.id,
                    api_message.user.name,
                    api_message.room_id,
                )
            )


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Хэндлер для обработки стандартной команды /start.

    Args:
        message (Message): сообщение пользователя с командой
    """
    answer = f"Здравствуйте, {html.bold(message.from_user.full_name)}!\n"
    answer += "Напишите в чат свой вопрос, мы постараемся на него ответить."
    # Состояние бота, что он печатает в чат
    async with ChatActionSender.typing(bot=message.bot, chat_id=message.chat.id):
        await message.answer(
            answer,
            reply_markup=kbs.start_keyboard_markup(),
        )
        # Выбор ID комнаты
        room_id = (
            None
            if message.chat.id not in user_ids_to_room_ids
            else user_ids_to_room_ids[message.chat.id]
        )
        # Если комнаты не существует, то создаём
        if not room_id:
            # Отправка сообщения для создания комнаты
            api_message = await create_message(
                user_id=message.chat.id,
                room_id=room_id,
                message_text=None,
                tg_user_id=message.from_user.id,
                user_mode=True,
            )
            # Если пришло сообщение об ошибке
            if isinstance(api_message, str):
                await message.answer(api_message)
            # Иначе пишем в чат ID комнаты при дебаг режиме
            else:
                if config.level == "DEBUG":
                    a = (
                        f"{html.bold("Вы находитесь в режиме оператора-админа")} (для теста).\n"
                        + "Ваш запрос будет обработан ИИ без участия оператора поддержки."
                        + "Если хотите переключиться на режим обычного пользователя, "
                        + "воспользуйтесь меню бота и выберете «Пользователь».\n"
                    )
                    room_str = f"Room ID: {api_message.room_id}"
                    await message.answer(a + room_str)
            room_id = api_message.room_id
            internal_id = api_message.user.name
        # Если комната существует, просто подключемся к ней
        else:
            room_id = user_ids_to_room_ids[message.chat.id]
            internal_id = tg_user_ids_to_user_ids[message.chat.id]
            if config.level == "DEBUG":
                await message.answer(f"Room ID: {room_id}")

        await asyncio.sleep(1)
        # Поднимаем WebSocket для общения с беком
        if message.chat.id not in ws_connections:
            # Запуск нового WebSocket для этого chat_id
            asyncio.create_task(
                websocket_listener(
                    message.bot,
                    message.chat.id,
                    internal_id,
                    room_id,
                )
            )


@router.message(F.text == "🌍 Перейти на сайт")
async def go_to_web_btn_handler(message: Message) -> None:
    """
    Хэндлер для отправки ссылки на web чат.

    Args:
        message (Message): сообщения пользователя
    """
    await message.reply(
        "Хорошо! Нажмите на кнопку ниже👇\nЧат автоматически перенесётся",
        reply_markup=kbs.go_to_web_keyboard_markup(),
    )


@router.message(F.text == "🤖 О боте")
async def about_bot_btn_handler(message: Message) -> None:
    """
    Хэндлер для вывода справки о боте.

    Args:
        message (Message): сообщения пользователя
    """
    await message.reply("Я бот Rutube!")


@router.message(F.text == "👨‍💻 Режим пользователя")
async def enable_user_mode_btn_handler(message: Message) -> None:
    """
    Хэндлер для включения режима пользователя.

    Args:
        message (Message): сообщения пользователя
    """
    if message.from_user.id not in user_mode_ids:
        user_mode_ids.append(message.from_user.id)
        await message.reply("Теперь вы обычный пользователь!")
    else:
        user_mode_ids.remove(message.from_user.id)
        await message.reply("Теперь вы снова админ!")


@router.callback_query(F.data == "voted_up")
async def thumb_up_btn_handler(message: Message) -> None:
    """
    Callback для обработки нажатия лайка.

    Args:
        message (Message): сообщения пользователя
    """
    # TODO: отправка на бек
    await message.answer("Спасибо за оценку!")


@router.callback_query(F.data == "voted_down")
async def thumb_down_btn_handler(message: Message) -> None:
    """
    Callback для обработки нажатия дизлайка.

    Args:
        message (Message): сообщения пользователя
    """
    # TODO: отправка на бек
    await message.answer("Спасибо за оценку! Будем улучшать качество ответов!")


@router.message(Command("info", prefix="!"))
async def info_handler(message: Message, system_info: dict, chat_info: str) -> None:
    """
    Системный хэндлер для вывода технической информации о боте.

    Args:
        message (Message): сообщение с командой
        system_info (dict): информация о боте
        chat_info (str): информация о чате (DEPRECATED)
    """
    content = as_list(
        as_marked_section(
            Text(html.bold("Общая информация")),
            f"🚀 Запуск: {system_info["started_at"]}",
            f"🧑‍💻 Web ID: {html.code(chat_info["web_id"][message.from_user.id]) \
                if len(chat_info["web_id"][message.from_user.id]) else "Отсутствует"}",
            marker=" ",
        ),
        Text(f"Информация на {datetime.now().strftime("%d.%m.%Y %H:%M:%S")}"),
        sep="\n\n",
    )
    await message.answer(**content.as_kwargs(parse_mode_key="html"))


@router.message(
    F.content_type.in_(
        {
            "photo",
            "sticker",
            "animation",
            "document",
            "story",
            "audio",
            "video",
            "voice",
        }
    )
)
async def message_with_another_type_content_handler(message: Message) -> None:
    """
    Хэндлер для обработки присланных изображений.

    Args:
        message (Message): сообщения пользователя
    """
    """
    Хэндлер для обработки присланных изображений.

    Args:
        message (Message): сообщения пользователя
    """
    answer = f"{html.bold('K P A C U B O !')}✨\n"
    answer += "Но мы обрабатываем только текстовые вопросы 👉👈😬"
    await message.answer(answer)


@router.message(F.text)
async def message_handler(message: Message) -> None:
    """
    Хэндлер для обработки присланных текстовых сообщений.

    Args:
        message (Message): сообщения пользователя
    """
    async with ChatActionSender.typing(bot=message.bot, chat_id=message.chat.id):
        if message.chat.id in ws_connections:
            # Отправка сообщения через WebSocket
            await ws_connections[message.chat.id].send_str(message.text)
            user_id = tg_user_ids_to_user_ids[message.from_user.id]
            room_id = user_ids_to_room_ids[user_id]
            user_mode = True if message.from_user.id in user_mode_ids else False
            logging.error(f"{user_mode=}")
            logging.error(f"{user_mode_ids=}")
            await create_message(
                user_id=user_id,
                room_id=room_id,
                message_text=message.text,
                tg_user_id=None,
                user_mode=user_mode,
            )
        else:
            await message.answer(
                f"{html.bold("❌ Соединение с платформой не установлено.")}\n"
                + "Отправьте /start для подключения."
            )
