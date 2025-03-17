import pandas as pd
from db_connect import create_connection, close_connection

def get_cars_dataframe():
    """
    Retrieve all car data from the database and return as a pandas DataFrame
    """
    connection = create_connection()
    if not connection:
        print("Failed to establish database connection")
        return None
    
    try:
        # Create cursor and execute query
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM cars"
        cursor.execute(query)
        
        # Fetch all results and convert to DataFrame
        results = cursor.fetchall()
        df = pd.DataFrame(results)
        
        # Close cursor
        cursor.close()
        
        print(f"Successfully imported {len(df)} records from cars table")
        return df
        
    except Exception as e:
        print(f"Error retrieving data: {e}")
        return None
    
    finally:
        close_connection(connection)

# Example usage
if __name__ == "__main__":
    cars_df = get_cars_dataframe()
    
    if cars_df is not None:
        # Display basic information about the data
        print("\nData Preview:")
        print(cars_df.head())
        
        print("\nData Summary:")
        print(cars_df.info())
        
        print("\nStatistical Summary:")
        print(cars_df.describe())
        
        # Example analysis
        if 'price' in cars_df.columns:
            print(f"\nAverage car price: {cars_df['price'].mean():.2f}")
        
        if 'year' in cars_df.columns:
            print("\nCars per year:")
            print(cars_df['year'].value_counts().sort_index())