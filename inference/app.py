from fastapi import FastAPI, UploadFile, HTTPException
import tempfile
import aiofiles
import os
import logging
from roberta_model import predict_by_filename 

app = FastAPI()

logging.basicConfig(level=logging.INFO)

@app.post('/uploadnews/')
async def classificate_news(news: UploadFile):
    try:
        # Создаем уникальный временный файл во временной папке
        temp_dir = tempfile.mkdtemp()
        temp_file_path = os.path.join(temp_dir, 'temp_file.txt')

        # Записываем данные из файла в временный файл
        async with aiofiles.open(temp_file_path, 'wb') as f:
            content = await news.read()
            await f.write(content)

        logging.info(f"Received file: {news.filename}")

        # Выполняем классификацию новости и возвращаем результат
        content_class = str(predict_by_filename(temp_file_path))
        logging.info(f"Classified news as: {content_class}")

        return content_class
    except Exception as e:
        logging.error(f"Error processing news: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при классификации")

