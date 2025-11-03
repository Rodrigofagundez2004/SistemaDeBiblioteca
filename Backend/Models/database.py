import mysql.connector

class Database:
    def get_connection(self):
    
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',                    
                password='Agusrodpro1',          
                database='SistemaDeBiblioteca'   
            )
            return connection
        except Exception as e:
            print(f"Error: {e}")
            return None
        