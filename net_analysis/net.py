import pandas as pd
import mysql.connector
from sqlalchemy import create_engine

# Option 1: Using mysql-connector-python
def get_cars_data_connector():
    # Replace these with your actual database connection details
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="cars_db"
    )
    
    query = "SELECT * FROM cars"
    df = pd.read_sql(query, conn)
    conn.close()
    
    return df

print(df);