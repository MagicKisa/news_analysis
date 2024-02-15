import os
import requests
import csv
import pandas as pd
from bs4 import BeautifulSoup
import re
import json
import datetime


def all_dates(to_date):
    # Задайте начальную и конечную даты
    start_date = to_date
    end_date = '2024-01-10'

    # Преобразуйте строки в объекты datetime
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Получите все даты между начальной и конечной датами (включая их)
    date_range = pd.date_range(start=start_date, end=end_date)
    
    return date_range.to_list()

def news_to_csv(data, filename):
    # Получаем текущую директорию, где находится скрипт
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Собираем путь к файлу file.csv с использованием относительного пути
    file_path = os.path.join(current_dir, f'../data/{filename}.csv')

    # Запись данных в CSV-файл
    with open(file_path, 'a', newline='', encoding='utf-8') as file:
        # Предполагаем, что data - это список словарей
        fieldnames = data[0].keys() if data else []
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Если файл пустой, записываем заголовки
        if os.stat(file_path).st_size == 0:
            writer.writeheader()

        # Записываем данные
        writer.writerows(data)
    return

def all_news(to_date):
    data = []
    last_save_date = datetime.datetime.strptime('2023-12-01', '%Y-%m-%d')
    for date in all_dates(to_date):
        data.extend(news_by_date(date))
        delta = date - last_save_date
        if delta.days >= 30:
            news_to_csv(data, 'lenta_news')
            data = []
            last_save_date = date

    # Сохраняем оставшиеся данные
    news_to_csv(data, 'lenta_news')

def news_by_date(date):
    print(date)
    data = []
    page = 1
    news = news_by_page(date, page)
    while news:
        data.extend(news)
        page += 1
        news = news_by_page(date, page)
    return data

def news_by_page(date, page):
    split_date = str(date).split()[0].split('-')
    year = split_date[0]
    month = split_date[1]
    day = split_date[2]

    url = f'https://lenta.ru/news/{year}/{month}/{day}/page/{page}'
    response = requests.get(url)
    html = response.text
    urls = extract_urls_from_html(html)
    news = [extract_news_by_url(url) for url in urls]
    return news

def extract_urls_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    # Найти все элементы с классом "archive-page__item"
    news_items = soup.find_all('li', class_='archive-page__item')
    if not news_items:
        return False
    
    urls = []
    # Пройти по каждой новости и извлечь нужные данные
    for news_item in news_items:
        # URL-адрес новости
        url_element = news_item.find('a', class_='card-full-news')
        if url_element:
            url = url_element.get('href')  
            url = f"https://lenta.ru{url}"
            if url not in urls:
                urls.append(url)       
    return urls

def extract_news_by_url(url):
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    
    # Извлекаем headline и description из мета-тегов
    headline_tag = soup.find('meta', property='og:title')
    description_tag = soup.find('meta', property='og:description')

    headline = headline_tag['content'] if headline_tag else None
    description = description_tag['content'] if description_tag else None

    # Извлекаем articleBody из встроенного JSON-LD
    json_ld_script = soup.find('script', type='application/ld+json')

    if json_ld_script:
        json_ld_data = json.loads(json_ld_script.string)
        article_body = json_ld_data.get('articleBody', None)
        author_link = json_ld_data.get('author', {}).get('url', None)
        date_published = json_ld_data.get('datePublished', None)
    else:
        json_ld_data = None
        article_body = None
        author_link = None
        date_published = None

    # Если дата публикации отсутствует в JSON-LD, попробуем извлечь её из мета-тега
    if not date_published:
        date_published_tag = soup.find('meta', property='article:published_time')
        date_published = date_published_tag['content'] if date_published_tag else None

    # Извлекаем заголовок из тега <title>
    title_tag = soup.find('title')
    if title_tag:
        # Извлекаем рубрики из заголовка
        categories = title_tag.text.split(':')
        categories = [category.strip() for category in categories[1:-1]]
    else:
        categories = None

    news = {
        'content': article_body,
        'description': description,
        'title': headline,
        'publishedAt': date_published,
        'categories': categories,
        'authorLink': author_link,
        'url' : url
    }
    return news


all_news('2023-12-01')

