from .database import Database
import mysql.connector
from datetime import datetime, timedelta

class ReservaModel:
    def crear_reserva(self, nombre_sala, fecha, id_turno, ci_participante, participantes):
        db = Database()
        conn = db.get_connection()
        cursor = None

        try:
            if not participantes:
                return False, "Debe haber al menos un participante"

            cursor = conn.cursor(dictionary=True)

            # 1. Validar que la sala existe
            cursor.execute(
                "SELECT capacidad, tipo_sala, edificio FROM sala WHERE nombre_sala = %s",
                (nombre_sala,)
            )
            sala_data = cursor.fetchone()
            if not sala_data:
                return False, "La sala no existe"

            capacidad = sala_data['capacidad']
            tipo_sala = sala_data['tipo_sala']
            edificio = sala_data['edificio']

            # 2. Validar capacidad
            if len(participantes) > capacidad:
                return False, f"Excede la capacidad de la sala ({capacidad})"

            # 3. Validar que los participantes existen
            placeholders = ",".join(["%s"] * len(participantes))
            cursor.execute(
                f"SELECT ci FROM participante WHERE ci IN ({placeholders})",
                participantes
            )
            participantes_existentes = {row['ci'] for row in cursor.fetchall()}
            if len(participantes_existentes) != len(participantes):
                return False, "Algunos participantes no existen en el sistema"

            # 4. Validar tipo de usuario vs tipo de sala
            error_tipo = self.validar_tipo_sala(ci_participante, tipo_sala)
            if error_tipo:
                return False, error_tipo

            # 5. Validar sanciones activas
            if self._tiene_sancion_activa(ci_participante, fecha):
                return False, "El participante tiene una sanción activa y no puede reservar"

            # 6. Validar disponibilidad de la sala
            if not self._validar_disponibilidad(nombre_sala, fecha, id_turno):
                return False, "La sala no está disponible en la fecha y turno seleccionados"

            # 7. Validar límites (solo para salas libres, como pide la letra)
            if tipo_sala == "libre":
                error_limite = self._validar_limites_participante(ci_participante, fecha)
                if error_limite:
                    return False, error_limite

            # 8. Crear la reserva
            cursor.execute(
                """
                INSERT INTO reserva (nombre_sala, edificio, fecha, id_turno, estado)
                VALUES (%s, %s, %s, %s, 'activa')
                """,
                (nombre_sala, edificio, fecha, id_turno)
            )
            id_reserva = cursor.lastrowid

            # 9. Registrar participantes
            for ci in participantes:
                cursor.execute(
                    """
                    INSERT INTO reserva_participante
                        (ci_participante, id_reserva, fecha_solicitud_reserva, asistencia)
                    VALUES (%s, %s, NOW(), 0)
                    """,
                    (ci, id_reserva)
                )

            conn.commit()
            return True, "Reserva creada correctamente"

        except mysql.connector.IntegrityError:
            if conn:
                conn.rollback()
            return False, "Error de integridad en la base de datos"

        except mysql.connector.Error as e:
            if conn:
                conn.rollback()
            return False, f"Error en la base de datos: {e}"

        except Exception as e:
            if conn:
                conn.rollback()
            return False, f"Error al crear reserva: {e}"

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # ----------------------------
    # Validaciones de negocio
    # ----------------------------

    def _validar_disponibilidad(self, nombre_sala, fecha, id_turno):
        """La sala no puede tener otra reserva activa en esa fecha y turno."""
        db = Database()
        conn = db.get_connection()
        cursor = None

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT COUNT(*) AS total
                FROM reserva
                WHERE nombre_sala = %s
                  AND fecha = %s
                  AND id_turno = %s
                  AND estado = 'activa'
                """,
                (nombre_sala, fecha, id_turno)
            )
            row = cursor.fetchone()
            return row['total'] == 0
        except Exception as e:
            print(f"Error al validar disponibilidad: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def _tiene_sancion_activa(self, ci_participante, fecha):
        """Verifica si el participante tiene una sanción activa en esa fecha."""
        db = Database()
        conn = db.get_connection()
        cursor = None

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT COUNT(*) AS total
                FROM sancion_participante
                WHERE ci_participante = %s
                  AND %s BETWEEN fecha_inicio AND fecha_fin
                """,
                (ci_participante, fecha)
            )
            row = cursor.fetchone()
            return row['total'] > 0
        except Exception as e:
            print(f"Error al validar sanción activa: {e}")
            return True  # por seguridad, si falla, consideramos que no puede reservar
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def _validar_limites_participante(self, ci_participante, fecha):
        """
        Reglas para salas de uso libre:
        - No más de 2 horas diarias (asumimos 1 turno = 1 hora).
        - No más de 3 reservas activas en la semana de esa fecha.
        """
        db = Database()
        conn = db.get_connection()
        cursor = None

        try:
            cursor = conn.cursor(dictionary=True)

            # 1) Máximo 2 reservas activas en el mismo día
            cursor.execute(
                """
                SELECT COUNT(*) AS total
                FROM reserva r
                JOIN reserva_participante rp ON r.id_reserva = rp.id_reserva
                WHERE rp.ci_participante = %s
                  AND r.fecha = %s
                  AND r.estado = 'activa'
                """,
                (ci_participante, fecha)
            )
            row = cursor.fetchone()
            if row['total'] >= 2:
                return "El participante ya tiene 2 horas reservadas en ese día"

            # 2) Máximo 3 reservas activas en la misma semana
            cursor.execute(
                """
                SELECT COUNT(*) AS total
                FROM reserva r
                JOIN reserva_participante rp ON r.id_reserva = rp.id_reserva
                WHERE rp.ci_participante = %s
                  AND YEARWEEK(r.fecha, 1) = YEARWEEK(%s, 1)
                  AND r.estado = 'activa'
                """,
                (ci_participante, fecha)
            )
            row = cursor.fetchone()
            if row['total'] >= 3:
                return "El participante ya tiene 3 reservas activas en esa semana"

            return None

        except Exception as e:
            print(f"Error al validar límites de participante: {e}")
            return "Error al validar límites del participante"
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # ----------------------------
    # Tipo de sala vs tipo de usuario
    # ----------------------------

    def validar_tipo_sala(self, ci_participante, tipo_sala):
        db = Database()
        conn = db.get_connection()
        cursor = None

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT pp.rol, pa.tipo
                FROM participante_programa_academico pp
                JOIN programa_academico pa
                    ON pp.nombre_programa = pa.nombre_programa
                WHERE pp.ci_participante = %s
                """,
                (ci_participante,)
            )
            usuario_data = cursor.fetchone()
            if not usuario_data:
                return "Usuario no encontrado en ningún programa académico"

            rol = usuario_data['rol']          # 'alumno' | 'docente'
            tipo_programa = usuario_data['tipo']  # 'grado' | 'posgrado'

            if tipo_sala == 'docente' and rol != 'docente':
                return "Esta sala es exclusiva para docentes"

            if tipo_sala == 'posgrado' and rol == 'alumno' and tipo_programa != 'posgrado':
                return "Esta sala es exclusiva para programas de posgrado"

            return None

        except mysql.connector.Error as e:
            return f"Error en la BD al validar tipo de sala: {e}"
        except Exception as e:
            return f"Error al validar tipo de sala: {e}"
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # ----------------------------
    # Asistencia y sanciones
    # ----------------------------

    def registrar_asistencia(self, id_reserva, asistentes_ci):
        """
        asistentes_ci: lista de cédulas que SÍ asistieron.
        Marca asistencia y aplica sanción si nadie asistió.
        """
        db = Database()
        conn = db.get_connection()
        cursor = None

        try:
            cursor = conn.cursor(dictionary=True)

            # Obtener todos los participantes de la reserva
            cursor.execute(
                "SELECT ci_participante FROM reserva_participante WHERE id_reserva = %s",
                (id_reserva,)
            )
            todos = [row['ci_participante'] for row in cursor.fetchall()]

            if not todos:
                return False, "La reserva no tiene participantes"

            # Actualizar asistencia por cada participante
            for ci in todos:
                asistio = 1 if ci in asistentes_ci else 0
                cursor.execute(
                    """
                    UPDATE reserva_participante
                    SET asistencia = %s
                    WHERE id_reserva = %s AND ci_participante = %s
                    """,
                    (asistio, id_reserva, ci)
                )

            # Verificar si alguien asistió
            cursor.execute(
                """
                SELECT SUM(asistencia) AS total_asistencias
                FROM reserva_participante
                WHERE id_reserva = %s
                """,
                (id_reserva,)
            )
            row = cursor.fetchone()
            total_asistencias = row['total_asistencias'] or 0

            if total_asistencias == 0:
                # Nadie asistió: cambiar estado y sancionar
                cursor.execute(
                    "UPDATE reserva SET estado = 'sin asistencia' WHERE id_reserva = %s",
                    (id_reserva,)
                )
                # Crear sanción de 2 meses para cada participante
                cursor.execute("SELECT fecha FROM reserva WHERE id_reserva = %s", (id_reserva,))
                reserva_row = cursor.fetchone()
                fecha_reserva = reserva_row['fecha']

                for ci in todos:
                    cursor.execute(
                        """
                        INSERT INTO sancion_participante (ci_participante, fecha_inicio, fecha_fin)
                        VALUES (%s, %s, DATE_ADD(%s, INTERVAL 2 MONTH))
                        """,
                        (ci, fecha_reserva, fecha_reserva)
                    )
            else:
                # Hubo asistencia → la reserva se puede marcar como finalizada
                cursor.execute(
                    "UPDATE reserva SET estado = 'finalizada' WHERE id_reserva = %s",
                    (id_reserva,)
                )

            conn.commit()
            return True, "Asistencia registrada correctamente"

        except Exception as e:
            if conn:
                conn.rollback()
            return False, f"Error al registrar asistencia: {e}"
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def cancelar_reserva(self, id_reserva):
        """Cambia el estado de la reserva a 'cancelada'."""
        db = Database()
        conn = db.get_connection()
        cursor = None

        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE reserva SET estado = 'cancelada' WHERE id_reserva = %s AND estado = 'activa'",
                (id_reserva,)
            )
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error al cancelar reserva: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # ----------------------------
    # Listar reservas.
    # ----------------------------

    def listar_reservas(self):
        """Devuelve todas las reservas con info básica + nombres de participantes."""
        db = Database()
        conn = db.get_connection()
        cursor = None
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT 
                    r.id_reserva,
                    r.fecha,
                    r.id_turno,
                    r.estado,
                    r.nombre_sala,
                    r.edificio,
                    GROUP_CONCAT(CONCAT(p.nombre, ' ', p.apellido) SEPARATOR ', ') AS participantes
                FROM reserva r
                JOIN reserva_participante rp ON r.id_reserva = rp.id_reserva
                JOIN participante p ON p.ci = rp.ci_participante
                GROUP BY 
                    r.id_reserva, r.fecha, r.id_turno, r.estado, 
                    r.nombre_sala, r.edificio
                ORDER BY r.fecha DESC, r.id_turno ASC
                """
            )
            return cursor.fetchall()
        except Exception as e:
            print(f"Error al listar reservas: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()