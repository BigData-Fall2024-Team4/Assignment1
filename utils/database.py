import os
import mysql.connector
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_data_from_db():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            passwd=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE"),
            auth_plugin='mysql_native_password'
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT question, final_answer, steps, file_name FROM validation_cases")
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return results
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return []