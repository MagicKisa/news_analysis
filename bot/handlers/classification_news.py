import asyncio
import os
import tempfile
import aiofiles
from aiogram import F, Router, types
from aiogram.types import Message
import logging

router = Router()

url = 'http://fastapi_service:8000/uploadnews/'


@router.callback_query(F.data == "Классифицировать новость")
async def callback_check(callback: types.CallbackQuery):
    await callback.message.answer(
        text="Пришлите текст новости:)"
    )

@router.message(F.text)
async def text_classification(message: Message):
    text = message.text

    logging.info(f"Received news text: {text[:100]}...")

    try:
        # Создаем уникальный временный файл во временной папке
        temp_dir = tempfile.mkdtemp()
        temp_file_path = os.path.join(temp_dir, 'temp_file.txt')

        # Записываем текст в временный файл
        async with aiofiles.open(temp_file_path, 'w', encoding='utf-8') as temp_file:
            await temp_file.write(text)

        # Выполняем HTTP запрос с использованием curl
        proc = await asyncio.create_subprocess_exec(
            "curl", "-X", "POST", url, "-F", f"news=@{temp_file_path}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await proc.communicate()

        if proc.returncode != 0:
            raise subprocess.CalledProcessError(proc.returncode, proc.args, output=stdout, stderr=stderr)

        content_class = stdout.strip().decode()
    except subprocess.CalledProcessError as e:
        logging.error(f"Curl command error: {e.stderr.decode()}")
        content_class = 'Ошибка при классификации'
    except Exception as err:
        logging.error(f"Other error occurred: {err}")
        content_class = 'Ошибка при классификации'

    await message.answer(f"Тема этой новости: {content_class}")