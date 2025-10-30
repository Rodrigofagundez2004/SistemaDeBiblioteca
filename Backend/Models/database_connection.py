import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv() #carga las variables de entorno desde el archivo .env
class DatabaseConnection:
    @staticmethod
    def get_connection():
        try:
            connection = mysql.connector.connect(
                host.getenv("DB_HOST"
                , database=os.getenv("DB_NAME")
                , user=os.getenv("DB_USER")
                , password=os.getenv("DB_PASSWORD")
                , port=os.getenv("DB_PORT")
                
            )
            print("Connection to database established")
            return connection
            except Error as e:
            print(F"Error while connecting to database: {e}")
            return None
            
    @staticmethod
    def execute_query(query, params=None):
        connection = None
        cursor = None
        try:
            connection = DatabaseConnection.get_connection()
            if connection is None:
                return None
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params or ())

       
