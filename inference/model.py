import joblib
from catboost import CatBoostClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from natasha import Doc, Segmenter, MorphVocab, NewsEmbedding, NewsMorphTagger
from nltk.corpus import stopwords
vectorizer = joblib.load('tfidf_vectorizer20000.pkl')
model = CatBoostClassifier()
model.load_model('model20000.cbm')
classes_names = ['Культура', 'Россия', 'Мир', 'Наука и технологии', 'Спорт', 'Экономика', 'Путешествия']


stop_words = stopwords.words('russian')
stop_words.extend(['что', 'это', 'так',
                    'вот', 'быть', 'как',
                    'в', '—', 'к', 'за', 'из', 'из-за',
                    'на', 'ок', 'кстати',
                    'который', 'мочь', 'весь',
                    'еще', 'также', 'свой',
                    'ещё', 'самый', 'ул', 'комментарий',
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
    news_text = text_prep(news_text).split()
    return vectorizer.transform(news_text)

def predict_by_filename(filename):
    with open(filename, 'r') as f:
        news_text = f.read()

    embedding = news_embedding(news_text)
    
    number_of_class = model.predict(embedding)[0][0]

    # return number_of_class
    return classes_names[number_of_class]
