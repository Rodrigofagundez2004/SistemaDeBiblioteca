from flask import Blueprint, render_template, request, redirect, url_for
from backend.models.participante_model import ParticipanteModel

participantes_bp = Blueprint('participantes', __name__)

@participantes_bp.route('/')
def listar_participantes():
    model = ParticipanteModel()
    participantes = model.get_all()
    return render_template('participantes/listar.html', participantes=participantes)

@participantes_bp.route('/crear', methods=['GET', 'POST'])
def crear_participante():
    if request.method == 'POST':
        ci = request.form['ci']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        
        model = ParticipanteModel()
        success, message = model.create(ci, nombre, apellido, email)
        
        if success:
            return redirect(url_for('participantes.listar_participantes'))
        else:
            return f"Error: {message}"
    
    return render_template('participantes/crear.html')