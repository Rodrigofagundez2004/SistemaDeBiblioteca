import mysql.connector
def connection_db():
    mydb = mysql.connector.connect(
        host="localhost",
        user= "root",
        password="Agusrodpro1",
        database="SistemaDeBiblioteca",
        port=3306
    )
    if mydb.is_connected():
        print("Conexion Sin errores")
        return mydb
    else:
        print("Error en la conexion")   