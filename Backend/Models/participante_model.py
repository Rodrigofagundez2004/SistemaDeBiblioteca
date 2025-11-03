from .database import Database
import mysql.connector

class ParticipanteModel:
    def get_all(self):
        db = Database()
        conn = db.get_connection()
        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM participante")  # 👈 ESPACIO AGREGADO
            return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener participantes: {e}")
            return []
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def get_by_ci(self, ci):
        db = Database()
        conn = db.get_connection()
        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM participante WHERE ci = %s", (ci,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error al obtener participante por CI: {e}")
            return None
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def create(self, ci, nombre, apellido, email):
        """CORREGIDO: quitado telefono que no existe en tu tabla"""
        db = Database()
        conn = db.get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO participante (ci, nombre, apellido, email) VALUES (%s, %s, %s, %s)", 
                (ci, nombre, apellido, email)
            )
            conn.commit()
            return True, "Participante creado de forma exitosa."
        except mysql.connector.IntegrityError as e:
            return False, "Error: Ya existe un participante con esa cédula o email"
        except Exception as e:
            return False, f"Error al crear participante: {e}"
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def update(self, ci, nombre, apellido, email):
        db = Database()
        conn = db.get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE participante SET nombre = %s, apellido = %s, email = %s WHERE ci = %s", 
                (nombre, apellido, email, ci)
            )
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error al actualizar participante: {e}")
            return False
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def delete(self, ci):
        db = Database()
        conn = db.get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM participante WHERE ci = %s", (ci,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error al eliminar participante: {e}")
            return False
        finally:
            if cursor: cursor.close()
            if conn: conn.close()