# app.py
import sys
import os
from flask import Flask, render_template

# Agregar la carpeta backend al path (CON MINÚSCULA)
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

app = Flask(__name__,
    template_folder='frontend/pages',
    static_folder='frontend'
)

@app.route('/')
def index():
    return render_template('index.html')

# 👇 IMPORT CORREGIDO - usa el nombre EXACTO del archivo
try:
    from backend.routes.participantes_routes import participantes_bp
    app.register_blueprint(participantes_bp, url_prefix='/participantes')
    print("✅ Rutas de participantes cargadas correctamente")
except ImportError as e:
    print(f"❌ Error cargando rutas: {e}")

if __name__ == '__main__':
    print("🚀 Iniciando servidor en http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)