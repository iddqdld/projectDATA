import pandas as pd
from database.db_connect import create_connection, close_connection  # import des functions de conn db



def get_cars_dataframe():
    connection = create_connection()
    if not connection:
        print("error conn db")
        return None

    try:
        # sql query
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT 
                id,
                title,
                NULLIF(price, 'NULL') AS price,
                NULLIF(mileage, 'NULL') AS mileage,
                NULLIF(year, 'NULL') AS year,
                link,
                scraped_at
            FROM cars
        """
        cursor.execute(query)
        results = cursor.fetchall()

        # creation de df
        df = pd.DataFrame(results)

        # types import
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        df['mileage'] = pd.to_numeric(df['mileage'], errors='coerce').astype('Int32')
        df['year'] = pd.to_numeric(df['year'], errors='coerce').astype('Int16')
        df['scraped_at'] = pd.to_datetime(df['scraped_at'])

        # net
        text_columns = ['title', 'link']
        df[text_columns] = df[text_columns].replace(['NULL', 'N/A', ''], None)

        # test
        print(f"\nsucces import {len(df)} lines")
        print(df.dtypes)


        return df

    except Error as e:
        print(f"error db: {e}")
        return None

    except Exception as e:
        print(f"error gen: {e}")
        return None

    finally:
        if connection.is_connected():
            cursor.close()
            close_connection(connection)


# test
if __name__ == "__main__":
    cars_df = get_cars_dataframe()

    if cars_df is not None:
        print("\nresultat:")
        print(cars_df.head())
        cars_df.to_csv("cars.csv", sep = ",", index = False)
    else:
        print("error d import")