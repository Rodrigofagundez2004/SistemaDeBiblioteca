# app.py
import sys
import os
from flask import Flask, render_template, session, redirect, url_for, request

# Agregar la carpeta backend al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

app = Flask(
    __name__,
    template_folder='frontend/pages',
    static_folder='frontend'
)

# SECRET KEY PARA SESIONES
app.secret_key = 'sistema_biblioteca_ucu_2025_clave_segura_agus'

# filtro global para exigir login
@app.before_request
def requerir_login():
    # Endpoints que NO requieren estar logueado
    endpoints_publicos = {
        'auth.login',
        'auth.registro',
        'auth.logout',
        'static'
    }

    if request.endpoint is None:
        return

    # Si el endpoint es público, dejamos pasar
    if request.endpoint in endpoints_publicos:
        return

    # Si no hay usuario en sesión, redirigimos al login
    if 'usuario' not in session:
        return redirect(url_for('auth.login'))


@app.route('/')
def index():
    return render_template('index.html')

# REGISTRAR TODAS LAS RUTAS (DESPUÉS de crear 'app')
try:
    from backend.routes.participantes_routes import participantes_bp
    app.register_blueprint(participantes_bp, url_prefix='/participantes')
    print("✅ Rutas de participantes cargadas")
    
    from backend.routes.reservas_routes import reservas_bp
    app.register_blueprint(reservas_bp, url_prefix='/reservas') 
    print("✅ Rutas de reservas cargadas")
    
    from backend.routes.salas_routes import salas_bp
    app.register_blueprint(salas_bp, url_prefix='/salas')
    print("✅ Rutas de salas cargadas")
    
    # 👇 Rutas de autenticación
    from backend.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    print("✅ Rutas de autenticación cargadas")

    from backend.routes.reporte_routes import reportes_bp
    app.register_blueprint(reportes_bp, url_prefix='/reportes')
    print("✅ Rutas de reportes cargadas")
    
except ImportError as e:
    print(f"❌ Error cargando rutas: {e}")

if __name__ == '__main__':
    print("🚀 Iniciando servidor en http://localhost:5000")
    print("🔐 Sistema de login activado")
    app.run(debug=True, host='0.0.0.0', port=5000)
