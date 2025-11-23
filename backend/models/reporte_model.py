from .database import Database

class ReporteModel:
    def salas_mas_reservadas(self):
        """Salas más reservadas"""
        db = Database()
        conn = db.get_connection()
        cursor = None
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    r.nombre_sala,
                    s.edificio,
                    s.tipo_sala,
                    s.capacidad,
                    COUNT(*) as total_reservas
                FROM reserva r
                JOIN sala s ON r.nombre_sala = s.nombre_sala
                WHERE r.estado = 'activa'
                GROUP BY r.nombre_sala, s.edificio, s.tipo_sala, s.capacidad
                ORDER BY total_reservas DESC
            """)
            return cursor.fetchall()
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def turnos_mas_demandados(self):
        """Turnos más demandados"""
        db = Database()
        conn = db.get_connection()
        cursor = None
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    t.id_turno,
                    t.hora_inicio,
                    t.hora_fin,
                    COUNT(*) as total_reservas
                FROM reserva r
                JOIN turno t ON r.id_turno = t.id_turno
                WHERE r.estado = 'activa'
                GROUP BY t.id_turno, t.hora_inicio, t.hora_fin
                ORDER BY total_reservas DESC
            """)
            return cursor.fetchall()
        finally:
            if cursor: cursor.close()
            if conn: conn.close()
    def promedio_participantes_por_salas(self):
        db = Database()
        db = db.get_connection()
        cursor = None
        try:
            cursor = db.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    r.nombre_sala,
                    s.edificio,
                    COUNT(DISTINCT r.id_reserva) as total_reservas,
                    COUNT(rp.ci_participante) as total_participantes,
                    ROUND(COUNT(rp.ci_participante) / COUNT(DISTINCT r.id_reserva), 2) as promedio_participantes
                FROM reserva r
                JOIN sala s ON r.nombre_sala = s.nombre_sala
                JOIN reserva_participante rp ON r.id_reserva = rp.id_reserva
                WHERE r.estado = 'activa'
                GROUP BY r.nombre_sala, s.edificio
                ORDER BY promedio_participantes DESC
            """) 
            return cursor.fetchall()
        finally:
            if cursor: cursor.close()
            if db: db.close()
    def reservas_por_carrera_facultad(self):
        db = Database()
        conn = db.get_connection()
        cursor = None 
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    f.nombre as facultad,
                    pa.nombre_programa,
                    pa.tipo as tipo_programa,
                    COUNT(DISTINCT r.id_reserva) as total_reservas
                FROM reserva r
                JOIN reserva_participante rp ON r.id_reserva = rp.id_reserva
                JOIN participante_programa_academico ppa ON rp.ci_participante = ppa.ci_participante
                JOIN programa_academico pa ON ppa.nombre_programa = pa.nombre_programa
                JOIN facultad f ON pa.id_facultad = f.id_facultad
                WHERE r.estado = 'activa'
                GROUP BY f.nombre, pa.nombre_programa, pa.tipo
                ORDER BY total_reservas DESC
            """)
            return cursor.fetchall()
        finally:
            if cursor: cursor.close()
            if conn: conn.close()
    def porcentaje_ocupacion_edificio(self):
        db = Database()
        conn = db.get_connection()
        cursor = None

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    e.nombre_edificio,
                    e.departamento,
                    COUNT(DISTINCT s.nombre_sala) as total_salas,
                    COUNT(DISTINCT r.id_reserva) as reservas_activas,
                    ROUND((COUNT(DISTINCT r.id_reserva) * 100.0 / 
                          (SELECT COUNT(*) FROM reserva WHERE estado = 'activa')), 2) as porcentaje_ocupacion
                FROM edificio e
                LEFT JOIN sala s ON e.nombre_edificio = s.edificio
                LEFT JOIN reserva r ON s.nombre_sala = r.nombre_sala AND r.estado = 'activa'
                GROUP BY e.nombre_edificio, e.departamento
                ORDER BY porcentaje_ocupacion DESC
            """)
            return cursor.fetchall()
        finally:
            if cursor: cursor.close()
            if conn: conn.close()
    def reservas_asistencias_por_tipo_usuario(self):
        db = Database()
        conn = db.get_connection()
        cursor = None

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    ppa.rol,
                    pa.tipo as tipo_programa,
                    COUNT(DISTINCT r.id_reserva) as total_reservas,
                    COUNT(CASE WHEN rp.asistencia = TRUE THEN 1 END) as asistencias,
                    COUNT(CASE WHEN rp.asistencia = FALSE THEN 1 END) as inasistencias,
                    COUNT(CASE WHEN rp.asistencia IS NULL THEN 1 END) as sin_registro
                FROM reserva r
                JOIN reserva_participante rp ON r.id_reserva = rp.id_reserva
                JOIN participante_programa_academico ppa ON rp.ci_participante = ppa.ci_participante
                JOIN programa_academico pa ON ppa.nombre_programa = pa.nombre_programa
                WHERE r.estado = 'activa'
                GROUP BY ppa.rol, pa.tipo
                ORDER BY total_reservas DESC
            """)
            return cursor.fetchall()
        finally:
            if cursor: cursor.close()
            if conn: conn.close()
    def sanciones_por_tipo_usuario(self):
        db = Database()
        conn = db.get_connection()
        cursor = None

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    ppa.rol,
                    pa.tipo as tipo_programa,
                    COUNT(*) as total_sanciones
                FROM sancion_participante sp
                JOIN participante_programa_academico ppa ON sp.ci_participante = ppa.ci_participante
                JOIN programa_academico pa ON ppa.nombre_programa = pa.nombre_programa
                WHERE sp.fecha_fin >= CURDATE()
                GROUP BY ppa.rol, pa.tipo
                ORDER BY total_sanciones DESC
            """)
            return cursor.fetchall()
        finally:
            if cursor:cursor.close()
            if conn: conn.close()
    def porcentaje_uso_reservas(self):
        db = Database()
        conn = db.get_connection()
        cursor = None

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    estado,
                    COUNT(*) as cantidad,
                    ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM reserva)), 2) as porcentaje
                FROM reserva
                GROUP BY estado
                ORDER BY cantidad DESC
            """)
            return cursor.fetchall()
        finally:
            if cursor: cursor.close()
            if conn: conn.close()