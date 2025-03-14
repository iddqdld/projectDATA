import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Замените на ваше имя пользователя
            password="",  # Замените на ваш пароль
            database="cars_db"  # Название вашей БД
        )
        
        if connection.is_connected():
            print("Con success")
            return connection
            
    except Error as e:
        print(f"fail to con: {e}")
        return None

def close_connection(connection):
    if connection.is_connected():
        connection.close()
        print("con closed")