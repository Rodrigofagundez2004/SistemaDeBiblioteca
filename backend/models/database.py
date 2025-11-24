# backend/models/database.py
import mysql.connector

class Database:
    def get_connection(self):
        try:
            connection = mysql.connector.connect(
                host='sistemabiblioteca.mysql.database.azure.com',
                user='adminmysql',
                password='Bruno123',
                database='sistemadebiblioteca',
                port=3306
            )
            return connection
        except Exception as e:
            print(f"❌ Error conectando a la nube: {e}")
            return None