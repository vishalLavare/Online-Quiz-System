import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'quiz_db')
}

def get_db_connection():
    """Establish and return a MySQL database connection."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def init_db():
    """Initialize the database with the schema."""
    connection = None
    try:
        # Connect without database first to create it if it doesn't exist
        temp_config = DB_CONFIG.copy()
        db_name = temp_config.pop('database')
        connection = mysql.connector.connect(**temp_config)
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        connection.commit()
        cursor.close()
        connection.close()

        # Connect to the specific database
        connection = get_db_connection()
        cursor = connection.cursor()

        # Read and execute schema.sql
        with open('schema.sql', 'r') as f:
            schema_sql = f.read()
            # Split by semicolon to execute multiple statements
            commands = schema_sql.split(';')
            for command in commands:
                if command.strip():
                    try:
                        cursor.execute(command)
                    except Error as e:
                        # Ignore "Duplicate entry" or "Column already exists" errors during init
                        if e.errno == 1061 or e.errno == 1062:
                            continue
                        else:
                            print(f"Warning during SQL execution: {e}")
        
        connection.commit()
        print("Database structure verified.")
    except Error as e:
        print(f"Error initializing database: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    init_db()
