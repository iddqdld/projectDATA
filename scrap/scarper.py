import requests
from bs4 import BeautifulSoup
import time
import mysql.connector
from mysql.connector import Error
import random
import re

# Настройки базы данных
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'cars_db'
}

BASE_URL = "https://www.autotrader.com/cars-for-sale/all"
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0'
]

def create_connection():
    """Создание подключения к MySQL"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            print("Успешное подключение к базе данных")
            return conn
    except Error as e:
        print(f"Ошибка подключения: {e}")
        return None

def create_table(conn):
    """Создание таблицы"""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS cars (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        price DECIMAL(10,2),
        mileage INT,
        year YEAR,
        link TEXT,
        scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_query)
        conn.commit()
    except Error as e:
        print(f"Ошибка создания таблицы: {e}")

def clean_price(price_str):
    """Очистка цены"""
    try:
        return float(re.sub(r'[^\d.]', '', price_str))
    except:
        return None

def clean_mileage(mileage_str):
    """Очистка пробега"""
    try:
        return int(re.sub(r'\D', '', mileage_str))
    except:
        return None

def safe_get_text(element, selector, default=None):
    """Безопасное извлечение текста"""
    result = element.select_one(selector)
    return result.text.strip() if result else default

def insert_car(conn, data):
    """Вставка данных"""
    insert_query = """
    INSERT INTO cars (title, price, mileage, year, link)
    VALUES (%s, %s, %s, %s, %s)
    """
    try:
        cursor = conn.cursor()
        cursor.execute(insert_query, data)
        conn.commit()
        print(f"Добавлен автомобиль: {data[0]}")
    except Error as e:
        print(f"Ошибка вставки: {e}")

def scrape_autotrader():
    conn = create_connection()
    if not conn:
        return

    create_table(conn)
    
    try:
        for page in range(1, 6):
            headers = {'User-Agent': random.choice(USER_AGENTS)}
            params = {
                'searchRadius': 0,
                'sortBy': 'relevance',
                'numRecords': 25,
                'firstRecord': (page-1)*25
            }

            try:
                response = requests.get(
                    BASE_URL,
                    params=params,
                    headers=headers,
                    timeout=20
                )
                response.raise_for_status()
            except Exception as e:
                print(f"Ошибка страницы {page}: {e}")
                continue

            soup = BeautifulSoup(response.text, 'html.parser')
            
            for card in soup.find_all('div', class_='inventory-listing'):
                try:
                    # Извлечение данных с новыми селекторами
                    title = safe_get_text(card, 'h2[data-cmp="subheading"]')
                    price = safe_get_text(card, 'div[data-cmp="firstPrice"]') 
                    mileage = safe_get_text(card, 'div[data-cmp="mileageSpecification"]')
                    year = safe_get_text(card, 'span.year')
                    link = card.find('a', {'data-cmp': 'link'})['href'] if card.find('a', {'data-cmp': 'link'}) else None
                    
                    # Очистка данных
                    cleaned_price = clean_price(price) if price else None
                    cleaned_mileage = clean_mileage(mileage) if mileage else None
                    cleaned_year = int(year) if year and year.isdigit() else None
                    full_link = f"https://www.autotrader.com{link}" if link else None

                    # Проверка обязательных полей
                    if not title or not cleaned_price:
                        continue
                    
                    # Вставка в БД
                    insert_car(conn, (
                        title,
                        cleaned_price,
                        cleaned_mileage,
                        cleaned_year,
                        full_link
                    ))
                    
                except Exception as e:
                    print(f"Ошибка обработки: {str(e)[:80]}")
                    continue

            print(f"Страница {page} обработана")
            time.sleep(random.uniform(2, 5))
            
    finally:
        if conn and conn.is_connected():
            conn.close()
            print("Соединение закрыто")

if __name__ == "__main__":
    scrape_autotrader()