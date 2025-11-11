from .database import Database
class SalaModel:
    def get_all(self):
        db = Database()
        conn = db.get_connection()
        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT *FROM sala")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener salas: {e}"
                  return []
                  )
        finally:
            if cursor: cursor.close()
            if conn: conn.close()
    def create(self, nombre_sala, edificio, capacidad, tipo_sala):
        db = Database()
        conn = db.get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO sala (nombre_sala, edificio, capacidad, tipo_sala) VALUES (%s, %s, %s, %s)", (nombre_sala, edificio, capacidad, tipo_sala))
            conn.commit()
            return True, "Sala creada exitosamente"
        except Exception as e:
            return False, f"Error al crear sala: {e}"
        finally:
            if cursor: cursor.close()
            if conn: conn.close()
    def delete(self, nombre_sala):
        db = Database()
        conn = db.get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM sala WHERE nombre_sala = %s", (nombre_sala,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error al eliminar sala: {e}")
            return False
        finally:
            if cursor: cursor.close()
            if conn: conn.close()