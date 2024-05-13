import aiohttp
import asyncio
from bs4 import BeautifulSoup
import sqlite3
import datetime


# Скраппинг пользовательских блогов и комментариев с форума StopGame.ru

SITE_URL = 'https://stopgame.ru/blogs/all'
BASE_TOPIC_URL = 'https://stopgame.ru' # Начало URL Статьи
PAGE_URL = lambda page_number: f'{SITE_URL}/p{page_number}'

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'
}

# Функция для создания таблицы в базе данных SQLite
def create_table(conn):
    try:
        cursor_article = conn.cursor() # Статьи
        cursor_article.execute('''CREATE TABLE IF NOT EXISTS articles
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          title TEXT,
                          date DATE,
                          body TEXT,
                          type TEXT,
                          rating INT)''')
        CURSOS = conn.cursor() # Комментарии
        CURSOS.execute('''CREATE TABLE IF NOT EXISTS commentaries
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          article_id INT,
                          body TEXT,
                          FOREIGN KEY(article_id) REFERENCES articles(id))''')
        conn.commit()
    except sqlite3.Error as e:
        print("Ошибка при создании таблицы:", e)

# Функция для добавления статьи в базу данных SQLite
def insert_article(conn, title, text_date, text_type, rating, body):
    try:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO articles (title, date, type, rating, body) VALUES (?, ?, ?, ?, ?)''', (title, text_date, text_type, rating, body))
        conn.commit()
    except sqlite3.Error as e:
        print("Ошибка при добавлении записи:", e)

# Функция для добавления комментариев в базу данных SQLite
def insert_commentaries(conn, commentary, title):
    try:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO commentaries (article_id, body) VALUES ((SELECT id FROM articles WHERE title=?), ?)''', (title, commentary))
        conn.commit()
    except sqlite3.Error as e:
        print("Ошибка при добавлении записи:", e)
        
# Основная функция для сохранения данных в базу данных SQLite
def save_to_database(title, text_date, text_type, rating, body, commentaries):
    conn = sqlite3.connect('articles.db')
    create_table(conn)
    insert_article(conn, title, text_date, text_type, rating, body)
    if commentaries:
        for commentary in commentaries:
            insert_commentaries(conn, commentary, title)
    conn.close()

async def fetch_content(url, session):
    async with session.get(url, headers=headers) as response:
        return await response.text()

async def get_page_urls(session):
    async with session.get(SITE_URL, headers=headers) as response:
        if response.status == 200:
            content = await response.text()
            soup = BeautifulSoup(content, 'html.parser')
            pagination = soup.find(class_='_container_1jx37_2 _container--no-padding_1jx37_1') # На сайте нестандартная пагинация
            cleaned_text = pagination.text.strip()
            pages = cleaned_text.replace('\xa0', '').split('\n')
            pages = [int(page) for page in pages[0:8] if page != '...'] # Отрезаются лишние кнопки, оставляя последние страницы
            min_page = min(pages)
            max_page = max(pages)
            return [PAGE_URL(page_number) for page_number in range(min_page, max_page + 1)]
        else:
            print('Ошибка при запросе:', response.status)
            return []

async def get_article_urls(url, session):
    async with session.get(url, headers=headers) as response:
        if response.status == 200:
            content = await response.text()
            soup = BeautifulSoup(content, 'html.parser')
            content = soup.find_all(class_='_card__content_1r5g3_478') # Класс статьи
            return [item.find('a').get('href') for item in content]
        else:
            print('Ошибка при запросе:', response.status)
            return []

async def get_article_content(url, session):
    async with session.get(BASE_TOPIC_URL + url, headers=headers) as response:
        if response.status == 200:
            content = await response.text()
            soup = BeautifulSoup(content, 'html.parser')
            
            # Название статьи
            title = soup.find('h1').text
            # Текст статьи
            body = [p.text for p in soup.find("div", {"class": "_content_12po9_13"}).find_all('p')]
            body = "\n".join(body)
            body = body.replace("\n", '')
            body = body.replace("\xa0", ' ')

            # Тип статьи
            types = ["Блог StopGame", "Общеигровое", "Кино и сериалы", "Обзоры и рассуждения", "Gamedev", "Видео"]
            text_type = soup.find("div", {"id": "sg-breadcrumbs"}).find_all('a')[-1].text
            
            if text_type not in types:
                text_type = "Персональный блог"
                
            # Возня с преобразованием дат
            rus_months = ["января", "февраля", "марта", 
                          "апреля", "мая", "июня", 
                          "июля", "августа", "сентября", 
                          "октября", "ноября", "декабря"]
            
            text_date = soup.find("span", {"class": "_date_12po9_591 _date--full_12po9_1"}).text.replace('\n', '')
            if text_date:
                if text_date == "Вчера ":
                    text_date = datetime.datetime.strptime(str(datetime.date.today() - datetime.timedelta(1)), '%Y-%m-%d')
                    text_date = str(text_date)[0:10]
                elif text_date == "Сегодня ":
                    text_date = datetime.datetime.strptime(str(datetime.date.today()), '%Y-%m-%d')
                    text_date = str(text_date)[0:10]
                else:
                    day = str(text_date.split(' ')[0]) if int(text_date.split(' ')[0]) > 9 else '0' + str(text_date.split(' ')[0])
                    year = str(text_date.split(' ')[2]) if str(text_date.split(' ')[2]) else '2024'
                    month = str(int(rus_months.index(text_date.split(' ')[1])) + 1) if rus_months.index(text_date.split(' ')[1]) + 1 > 9 else '0' +  str(rus_months.index(text_date.split(' ')[1]) + 1)
                    text_date = year + "-" + month + "-"+ day
            
            #  Рейтинг статьи
            rating = int(soup.find("div", {"class": "_rating-spinner_1ljrf_4"}).find("span").text)
            
            # Комментарии
            commentary_block = soup.find("section", {"class": "_page-section_c584a_472 _section_12po9_6 _comments-container_12po9_1688"})
            # У пары статей блока комментариев нет, нужна проверка
            all_commentaries = commentary_block.find_all("div", {"class": '_comment__body_jkkxx_1'}) if commentary_block is not None else [] 
            # Все комментарии, доступные для скрапинга без интерактивных элементов (Если много комментариев в одной ветке)
            commentaries = []
            # Перевод из блоков HTML-кода в текст
            if all_commentaries:
                for commentary in all_commentaries:
                    commentaries.append((' '.join([p.text for p in commentary.find_all('p')])).replace('\xa0', ' '))
            
            return title, text_date, text_type, rating, body, commentaries
        else:
            print('Ошибка при запросе:', response.status)
            return None, None, None, None, None, None

async def main():
    conn = sqlite3.connect('articles.db')
    count = 0
    async with aiohttp.ClientSession() as session:
        page_urls = await get_page_urls(session)
        for page_url in page_urls:
            article_urls = await get_article_urls(page_url, session)
            for article_url in article_urls:
                title, text_date, text_type, rating, body, commentaries = await get_article_content(article_url, session)
                if title and body:
                    count += 1
                    print(count)
                    save_to_database(title, text_date, text_type, rating, body, commentaries)
    conn.close()

if __name__ == "__main__":
    asyncio.run(main())
    