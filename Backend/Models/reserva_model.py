from .database import Database 
import mysql.connector 
from datetime import datetime, timedelta

class ReservaMode:
    def crear_reserva(self, nombre_sala, fecha, id_turno, ci_participante, participantes):

        db = Database()
        conn = db.get_connection()
        cursor = None
        
        try:
            cursor = conn.cursor(dictionary = True)
            #1 validacion que la sala existe y obtengo los datos
            cursor.execute("SELECT capacidad, tipo_sala, edificio FROM sala WHERE nombre_sala = %s", (nombre_sala,))
            sala_data = cursor.fetchone()
            if not sala_data:
                return False, "La sala no existe"
            capacidad, tipo_sala, edificio = sala_data['capacidad'], sala_data['tipo_sala'], sala_data['edificio']
            #2 Validar capacidad 
            if len(participantes) > capacidad:
                return False, f"Excede la capacidad de la sala ({capacidad})"
            #3 validar que todos los pariticpantes existen 
            placeholders = ','.join(['%s'] * len(participantes))
            cursor.execute(f"SELECT ci FROM participante WHERE ci IN ({placeholders})", participanteS)
            participantes_existentes = {row['ci'] for row in cursor.fetchall()}

            if len(participantes_existentes) != len(participantes):
                return False, "Algunos participantes no existen en el sistema"
            #4 validar tipo usuario vs tio sala
            error_tipo = self.validar_tipo_sala(ci_participante, tipo_sala)
            if error_tipo:
                return False, error_tipo
            #5 validar disponibilidad
            if not self._validar_disponibilidad(nombre_sala, fecha, id_turno):
                return False, "La sala no esta disponible en la fecha y turno que seleccionaste"
            #6 Validar limites del participante principao
            if tipo_sala == "libre":
                error_limite = self._validar_limites_participante(ci_participante, fecha)
                if error_limite:
                    return False, error_limite
            #7 crear la reserva
            cursor.execute("""
                INSERT INTO reserva (nombre_sala, edificio, fecha, id_turno, estado) 
                VALUES (%s, %s, %s, %s, 'activa')
            """, (nombre_sala, edificio, fecha, id_turno))
            id_reserva = cursor.lastrowid
            
            # 8. Registrar participantes
            for ci in participantes:
                cursor.execute("""
                    INSERT INTO reserva_participante (ci_participante, id_reserva, fecha_solicitud_reserva) 
                    VALUES (%s, %s, NOW())
                """, (ci, id_reserva))
                conn.commit()
                return True, f"Reserva #{id_reserva} creada exitosamente"
        except mysql.connector.integrityError as e:
            conn.rollback()
            return False, "Error en la BD"
        except Exception as e:
            conn.rollback()
            return False, f"Error al crear reserva: {e}"
        finally:

        
