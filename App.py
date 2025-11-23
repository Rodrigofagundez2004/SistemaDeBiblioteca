# app.py
import sys
import os
from flask import Flask, render_template


sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

app = Flask(__name__,
    template_folder='frontend/pages',
    static_folder='frontend'
)


app.secret_key = 'sistema_biblioteca_ucu_2025_clave_segura_agus'

@app.route('/')
def index():
    return render_template('index.html')


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