from aiogram import F, Router, types
from aiogram.types import Message
import requests

router = Router()

url = 'http://127.0.0.1:8000/uploadnews/'

@router.callback_query(F.data == "Классифицировать новость")
async def callback_check(callback: types.CallbackQuery):
    await callback.message.answer(
        text="Пришлите текст новости:)"
    )

@router.message(F.text)
async def text_classification(message: Message):
    text = message.text
    with open('news_file.txt', 'w') as f:
        f.write(text)

    files = {'news': open('news_file.txt', 'rb')}
    response = requests.post(url=url, files=files)
    content_class = response.content

    # answer = f"Тема этой новости:{content_class}"
    await message.answer(content_class)
