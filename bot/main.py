import logging
import asyncio
from aiogram import Router, F
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command, StateFilter
from aiogram.utils.keyboard import InlineKeyboardBuilder

from handlers import about_work, common, classification_news

# Устанавливаем уровень логгирования
logging.basicConfig(level=logging.INFO)

# Замените 'YOUR_BOT_TOKEN' на токен вашего бота
TOKEN = '6525731519:AAHfDAZHDQiJCb3Fl0CMB3v2YYtG5jaFtxc'
bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    dp.include_routers(common.router, about_work.router, classification_news.router)
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    asyncio.run(main())


