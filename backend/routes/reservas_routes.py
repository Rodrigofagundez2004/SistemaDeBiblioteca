from flask import Blueprint, render_template, request, redirect, url_for
from backend.models.reserva_model import ReservaModel
from backend.models.sala_model import SalaModel
from backend.models.participante_model import ParticipanteModel
from backend.models.database import Database

reservas_bp = Blueprint('reservas', __name__)

def obtener_turnos():
    db = Database()
    conn = db.get_connection()
    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                id_turno,
                CONCAT(DATE_FORMAT(hora_inicio, '%H:%i'), ' - ', DATE_FORMAT(hora_fin, '%H:%i')) AS descripcion
            FROM turno
            ORDER BY id_turno
        """)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al obtener turnos: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



@reservas_bp.route('/')
def listar_reservas():
    model = ReservaModel()
    reservas = model.listar_reservas()
    return render_template('reservas/listar.html', reservas=reservas)


@reservas_bp.route('/crear', methods=['GET', 'POST'])
def crear_reserva():
    if request.method == 'POST':
        nombre_sala = request.form['nombre_sala']
        fecha = request.form['fecha']          # formato YYYY-MM-DD
        id_turno = int(request.form['id_turno'])
        ci_principal = request.form['ci_principal']
        participantes = request.form.getlist('participantes')  # lista de CI

        # Aseguramos que el participante principal esté incluido
        if ci_principal not in participantes:
            participantes.append(ci_principal)

        model = ReservaModel()
        success, message = model.crear_reserva(
            nombre_sala=nombre_sala,
            fecha=fecha,
            id_turno=id_turno,
            ci_participante=ci_principal,
            participantes=participantes
        )

        if success:
            return redirect(url_for('reservas.listar_reservas'))
        else:
            return f"Error: {message}", 400

    # GET: mostrar formulario
    salas = SalaModel().get_all()
    participantes = ParticipanteModel().get_all()
    turnos = obtener_turnos()
    return render_template(
        'reservas/crear.html',
        salas=salas,
        participantes=participantes,
        turnos=turnos
    )


@reservas_bp.route('/cancelar/<int:id_reserva>', methods=['POST'])
def cancelar_reserva(id_reserva):
    model = ReservaModel()
    model.cancelar_reserva(id_reserva)
    return redirect(url_for('reservas.listar_reservas'))
