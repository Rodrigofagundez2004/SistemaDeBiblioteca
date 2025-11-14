# backend/routes/auth_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        from backend.models.login_model import LoginModel
        model = LoginModel()
        success, resultado = model.verificar_login(email, password)  # 👈 'resultado' no 'result'
        
        if success:
            session['usuario'] = resultado  # 👈 Aquí usas 'resultado'
            flash(f"¡Bienvenido {resultado['nombre']}!", 'success')  # 👈 Y aquí también
            return redirect(url_for('index'))
        else:
            flash(resultado, 'error')  # 👈 Y aquí también
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    """Cerrar sesión"""
    session.pop('usuario', None)
    flash("Sesión cerrada", 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    """Registro de nuevo usuario"""
    if request.method == 'POST':
        ci = request.form['ci']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        password = request.form['password']
        
        from backend.models.participante_model import ParticipanteModel
        from backend.models.login_model import LoginModel
        
        # 1. Crear participante
        participante_model = ParticipanteModel()
        success_part, mensaje_part = participante_model.create(ci, nombre, apellido, email)
        
        if not success_part:
            flash(mensaje_part, 'error')
            return render_template('auth/registro.html')
        
        # 2. Crear login
        login_model = LoginModel()
        success_login, mensaje_login = login_model.crear_usuario(ci, email, password)
        
        if success_login:
            flash("Usuario registrado. Ahora puedes iniciar sesión.", 'success')
            return redirect(url_for('auth.login'))
        else:
            flash(mensaje_login, 'error')
    
    return render_template('auth/registro.html')