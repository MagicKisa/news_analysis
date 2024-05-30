import os
import torch
from transformers import RobertaTokenizer, RobertaForSequenceClassification
from natasha import Doc, Segmenter, MorphVocab, NewsEmbedding, NewsMorphTagger
from nltk.corpus import stopwords
import logging


model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../model'))
logging.info(f"Model path: {model_path}")
logging.info(f"Contents of model directory: {os.listdir(model_path)}")


try:
    tokenizer = RobertaTokenizer.from_pretrained(model_path)
    model = RobertaForSequenceClassification.from_pretrained(model_path)
except Exception as e:
    logging.error(f"Error loading model: {e}")
    raise


class_names = ['Культура', 'Россия', 'Мир', 'Наука и технологии', 'Спорт', 'Экономика', 'Путешествия']

stop_words = stopwords.words('russian')
stop_words.extend(['что', 'это', 'так', 'вот', 'быть', 'как', 'в', '—', 'к', 'за', 'из', 'из-за', 'на', 'ок', 'кстати',
                   'который', 'мочь', 'весь', 'еще', 'также', 'свой', 'ещё', 'самый', 'ул', 'комментарий',
                   'английский', 'язык'])

segmenter = Segmenter()
morph_vocab = MorphVocab()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)

def text_prep(text) -> str:
    doc = Doc(text)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    
    for token in doc.tokens:
        token.lemmatize(morph_vocab)
    
    lemmas = [_.lemma for _ in doc.tokens]
    words = [lemma for lemma in lemmas if lemma.isalpha() and len(lemma) > 2]
    filtered_words = [word for word in words if word not in stop_words]
    return " ".join(filtered_words)

def news_embedding(news_text):
    return tokenizer(news_text, padding=True, truncation=True, return_tensors="pt")

def predict_by_filename(filename):
    try:
        with open(filename, 'r') as f:
            news_text = f.read()
        
        logging.info(f"Processing text: {news_text[:100]}...")  # Логируем первые 100 символов текста

        processed_text = text_prep(news_text)
        inputs = news_embedding(processed_text)
        outputs = model(**inputs)
        predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
        predicted_class = torch.argmax(predictions, dim=1).item()
        
        return class_names[predicted_class]
    except Exception as e:
        logging.error(f"Error in prediction: {e}")
        raise
