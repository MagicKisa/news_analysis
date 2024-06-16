from aiogram import F, Router, types
from aiogram.types import Message
import subprocess
import logging
import os

router = Router()

url = 'http://fastapi:8000/uploadnews/'


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
temp_file_path = os.path.join(BASE_DIR, 'temp_file.txt')

@router.callback_query(F.data == "Классифицировать новость")
async def callback_check(callback: types.CallbackQuery):
    await callback.message.answer(
        text="Пришлите текст новости:)"
    )

@router.message(F.text)
async def text_classification(message: Message):
    text = message.text

    # Логируем текст новости
    logging.info(f"Received news text: {text[:100]}...")  # Логируем первые 100 символов текста


    with open(temp_file_path, 'w', encoding='utf-8') as temp_file:
        temp_file.write(text)

    try:
       
        result = subprocess.run(
            ["curl", "-X", "POST", url, "-F", f"news=@{temp_file_path}"],
            capture_output=True,
            text=True
        )

        
        if result.returncode != 0:
            raise subprocess.CalledProcessError(result.returncode, result.args, output=result.stdout, stderr=result.stderr)


        logging.info(f"Server response: {result.stdout}")

    
        content_class = result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logging.error(f"Curl command error: {e.stderr}")
        content_class = 'Ошибка при классификации'
    except Exception as err:
        logging.error(f"Other error occurred: {err}")
        content_class = 'Ошибка при классификации'

    await message.answer(f"Тема этой новости: {content_class}")



