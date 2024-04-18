import logging
import asyncio
from aiogram import Router, F
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command, StateFilter
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config_reader import config
from handlers import about_work, common, classification_news


# Устанавливаем уровень логгирования
logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()


async def main():
    dp.include_routers(common.router, about_work.router, classification_news.router)
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    asyncio.run(main())


