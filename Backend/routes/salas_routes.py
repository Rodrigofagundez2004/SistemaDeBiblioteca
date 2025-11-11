from flask import Blueprint, render_template, request, redirect, url_for
from backend.models.sala_model import SalaModel
from backend.models.database import Database

salas_bp = Blueprint('salas', __name__)

def obtener_edificios():
    db = Database()
    conn = db.get_connection()
    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT nombre_edificio FROM edificio ORDER BY nombre_edificio")
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al obtener edificios: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@salas_bp.route('/')
def listar_salas():
    model = SalaModel()
    salas = model.get_all()
    return render_template('salas/listar.html', salas=salas)


@salas_bp.route('/crear', methods=['GET', 'POST'])
def crear_sala():
    if request.method == 'POST':
        nombre_sala = request.form['nombre_sala'].strip()
        edificio = request.form['edificio'].strip()
        capacidad = request.form['capacidad'].strip()
        tipo_sala = request.form['tipo_sala'].strip()

        # Validaciones básicas
        if not capacidad.isdigit() or int(capacidad) <= 0:
            return "Error: la capacidad debe ser un número positivo.", 400

        if tipo_sala not in ('libre', 'posgrado', 'docente'):
            return "Error: tipo de sala inválido.", 400

        model = SalaModel()
        success, message = model.create(
            nombre_sala=nombre_sala,
            edificio=edificio,
            capacidad=int(capacidad),
            tipo_sala=tipo_sala
        )

        if success:
            return redirect(url_for('salas.listar_salas'))
        else:
            return f"Error: {message}", 400

    # GET → mostrar formulario con edificios válidos
    edificios = obtener_edificios()
    return render_template('salas/crear.html', edificios=edificios)


@salas_bp.route('/eliminar/<nombre_sala>', methods=['POST'])
def eliminar_sala(nombre_sala):
    model = SalaModel()
    ok = model.delete(nombre_sala)
    return redirect(url_for('salas.listar_salas'))
