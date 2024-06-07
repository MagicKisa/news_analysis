from fastapi import FastAPI, UploadFile, HTTPException
from roberta_model import predict_by_filename
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO)

@app.post('/uploadnews/')
async def classificate_news(news: UploadFile):
    try:
        with open(news.filename, 'wb') as f:
            content = await news.read()
            f.write(content)
        
        logging.info(f"Received file: {news.filename}")
        
        content_class = str(predict_by_filename(news.filename))
        logging.info(f"Classified news as: {content_class}")

        return content_class
    except Exception as e:
        logging.error(f"Error processing news: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при классификации")
