import requests
from bs4 import BeautifulSoup
import time
import random
import re
from database.db_connect import create_connection, close_connection  # import db conn

BASE_URL = "https://www.autotrader.com/cars-for-sale/all"
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0'
]


def create_table(conn):
    """creation de table"""
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
    except Exception as e:
        print(f"error de creat table: {e}")


def clean_price(price_str):
    # price format
    try:
        return float(re.sub(r'[^\d.]', '', price_str))
    except:
        return None

# mileage format
def clean_mileage(mileage_str):
    try:
        return int(re.sub(r'\D', '', mileage_str))
    except:
        return None


def get_text(element, selector, default=None):
    result = element.select_one(selector)
    return result.text.strip() if result else default

#insertion dans le table
def insert_car(conn, data):
    insert_query = """
    INSERT INTO cars (title, price, mileage, year, link)
    VALUES (%s, %s, %s, %s, %s)
    """
    try:
        cursor = conn.cursor()
        cursor.execute(insert_query, data)
        conn.commit()
        print(f"car aded: {data[0]}")
    except Exception as e:
        print(f"error d insertion {e}")


def scrape_autotrader():
    conn = create_connection()  # conn
    if not conn:
        return

    create_table(conn)  # table if not exist

    try:
        for page in range(1, 6):
            headers = {'User-Agent': random.choice(USER_AGENTS)}
            params = {
                'searchRadius': 0,
                'sortBy': 'relevance',
                'numRecords': 25,
                'firstRecord': (page - 1) * 25
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
                print(f"404 {page}: {e}")
                continue

            soup = BeautifulSoup(response.text, 'html.parser')

            for card in soup.find_all('div', class_='inventory-listing'):
                try:
                    title = get_text(card, 'h2[data-cmp="subheading"]')
                    price = get_text(card, 'div[data-cmp="firstPrice"]')
                    mileage = get_text(card, 'div[data-cmp="mileageSpecification"]')
                    year = get_text(card, 'span.year')
                    link = card.find('a', {'data-cmp': 'link'})['href'] if card.find('a',
                                                                                     {'data-cmp': 'link'}) else None

                    cleaned_price = clean_price(price) if price else None
                    cleaned_mileage = clean_mileage(mileage) if mileage else None
                    cleaned_year = int(year) if year and year.isdigit() else None
                    full_link = f"https://www.autotrader.com{link}" if link else None

                    if not title or not cleaned_price:
                        continue

                    insert_car(conn, (
                        title,
                        cleaned_price,
                        cleaned_mileage,
                        cleaned_year,
                        full_link
                    ))

                except Exception as e:
                    print(f"failed to insert: {str(e)[:80]}")
                    continue

            print(f"page {page} scraped")
            time.sleep(random.uniform(2, 5))

    finally:
        if conn and conn.is_connected():
            close_connection(conn)  # conn close
            print("conn closed")


if __name__ == "__main__":
    scrape_autotrader()