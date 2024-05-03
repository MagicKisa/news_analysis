from fastapi import FastAPI, UploadFile
from model import predict_by_filename
from pydantic import BaseModel


app = FastAPI()

@app.post('/uploadnews/')
async def classificate_news(news: UploadFile):
    with open(news.filename, 'wb') as f:
        content = await news.read()
        f.write(content)
    
    content_class = str(predict_by_filename(news.filename))

    return {'answer': content_class}
