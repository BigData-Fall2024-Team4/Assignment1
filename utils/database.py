import os
import pymssql
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_data_from_db():
    try:
        # Establish connection to Azure MSSQL
        connection = pymssql.connect(
            server=os.getenv("MSSQL_SERVER"),
            user=os.getenv("MSSQL_USER"),
            password=os.getenv("MSSQL_PASSWORD"),
            database=os.getenv("MSSQL_DATABASE")
        )
        
        cursor = connection.cursor(as_dict=True)

        # Execute SQL query to fetch data from validation_cases table
        cursor.execute("SELECT question, final_answer, steps, file_name FROM validation_cases")
        
        # Fetch all results
        results = cursor.fetchall()
        
        # Close cursor and connection
        cursor.close()
        connection.close()
        
        return results

    except pymssql.Error as err:
        print(f"Error connecting to Azure MSSQL: {err}")
        return []

def update_attempt(question, result, attempt_number):
    conn = pymssql.connect(
            server=os.getenv("MSSQL_SERVER"),
            user=os.getenv("MSSQL_USER"),
            password=os.getenv("MSSQL_PASSWORD"),
            database=os.getenv("MSSQL_DATABASE")
        )
        
    cursor = conn.cursor()

    # Use f-string to insert the column name dynamically
    column_name = f"attempt_{attempt_number}_answer"
    
    # Use %s for parameterized queries with pymssql
    sql_query = f"UPDATE attempts SET {column_name} = %s WHERE CAST(question AS NVARCHAR(MAX)) = %s"
    cursor.execute(sql_query, (result, question))

    
    conn.commit()
    conn.close()

def get_attempts_data():
    conn = pymssql.connect(
            server=os.getenv("MSSQL_SERVER"),
            user=os.getenv("MSSQL_USER"),
            password=os.getenv("MSSQL_PASSWORD"),
            database=os.getenv("MSSQL_DATABASE")
        )
        
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM attempts")
    data = cursor.fetchall()
    
    columns = [description[0] for description in cursor.description]
    
    conn.close()
    
    return [dict(zip(columns, row)) for row in data]

if __name__ == "__main__":
    # Fetch data and print results
    data = get_data_from_db()
    for row in data:
        print(row)
