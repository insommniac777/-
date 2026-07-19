import asyncio
import logging
from typing import Final

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)

BOT_TOKEN: Final[str] = "ВАШ_ТОКЕН_БОТА"
ADMIN_ID: Final[int] = 0

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

forward_map: dict[int, int] = {}
user_ids: dict[int, int] = {}


@dp.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer("Привет! 👋\n\nНапишите сюда ваш вопрос или предложение, и я передам его разработчику.")


@dp.message(F.chat.id == ADMIN_ID, F.reply_to_message.as_("replied"))
async def admin_reply(message: Message, replied: Message) -> None:
    user_id = forward_map.get(replied.message_id) or user_ids.get(replied.message_id)
    if user_id is None:
        await message.reply("Не удалось определить получателя. Возможно, сообщение устарело.")
        return

    try:
        if message.photo:
            await bot.send_photo(user_id, message.photo[-1].file_id, caption=message.caption or "")
        elif message.document:
            await bot.send_document(user_id, message.document.file_id, caption=message.caption or "")
        elif message.audio:
            await bot.send_audio(user_id, message.audio.file_id, caption=message.caption or "")
        elif message.voice:
            await bot.send_voice(user_id, message.voice.file_id)
        elif message.text:
            await bot.send_message(user_id, message.text)
        else:
            await message.reply("Этот тип сообщений пока не поддерживается для ответа.")
            return

        await message.reply("✅ Ответ доставлен пользователю.")
    except Exception:
        log.warning("Ошибка доставки ответа user_id=%s", user_id)
        await message.reply("❌ Не удалось доставить сообщение. Возможно, пользователь заблокировал бота.")


@dp.message(F.chat.id == ADMIN_ID)
async def admin_unknown(message: Message) -> None:
    await message.reply("Используйте «Ответить» на пересланное сообщение пользователя.")


@dp.message()
async def user_message(message: Message) -> None:
    user_id = message.from_user.id
    if user_id == ADMIN_ID:
        return

    try:
        msg = await message.forward(chat_id=ADMIN_ID)
    except Exception:
        log.warning("Не удалось переслать сообщение от user_id=%s", user_id)
        return

    forward_map[msg.message_id] = user_id
    user_ids[msg.message_id] = user_id
    await message.reply("✅ Ваше сообщение передано разработчику. Ожидайте ответ.")


async def main() -> None:
    if BOT_TOKEN == "ВАШ_ТОКЕН_БОТА" or ADMIN_ID == 0:
        log.error("Укажите BOT_TOKEN и ADMIN_ID в коде перед запуском!")
        return
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
