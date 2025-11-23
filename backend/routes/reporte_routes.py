# backend/routes/reportes_routes.py
from flask import Blueprint, render_template
from backend.models.reporte_model import ReporteModel

reportes_bp = Blueprint('reportes', __name__)

@reportes_bp.route('/')
def index_reportes():
    """Página principal de reportes"""
    return render_template('reportes/index.html')

@reportes_bp.route('/salas-mas-reservadas')
def salas_mas_reservadas():  
    """Salas más reservadas"""
    model = ReporteModel()
    datos = model.salas_mas_reservadas()  
    return render_template('reportes/salas_mas_reservadas.html', datos=datos)

@reportes_bp.route('/turnos-mas-demandados')
def turnos_mas_demandados():
    """Los turnos más demandados"""
    model = ReporteModel()
    datos = model.turnos_mas_demandados()  
    return render_template('reportes/turnos_mas_demandados.html', datos=datos)

@reportes_bp.route('/promedio-participantes')
def promedio_participantes():
    """Promedio de participantes por sala"""
    model = ReporteModel()
    datos = model.promedio_participantes_por_sala()  
    return render_template('reportes/promedio_participantes.html', datos=datos)

@reportes_bp.route('/reservas-por-carrera')
def reservas_por_carrera():
    """Reservas por carrera"""
    model = ReporteModel()
    datos = model.reservas_por_carrera_facultad()  
    return render_template('reportes/reservas_por_carrera.html', datos=datos)

@reportes_bp.route('/ocupacion-edificios')
def ocupacion_edificios():
    """Porcentaje de ocupación de edificios"""
    model = ReporteModel()
    datos = model.porcentaje_ocupacion_edificio()  
    return render_template('reportes/ocupacion_edificios.html', datos=datos)

@reportes_bp.route('/uso-por-tipo-usuario')
def uso_por_tipo_usuario():
    """Reservas y asistencias por tipo usuario"""
    model = ReporteModel()
    datos = model.reservas_asistencias_por_tipo_usuario()  
    return render_template('reportes/uso_por_tipo_usuario.html', datos=datos)

@reportes_bp.route('/sanciones-por-tipo')
def sanciones_por_tipo():  
    """Sanciones por tipo de usuario"""
    model = ReporteModel()
    datos = model.sanciones_por_tipo_usuario()  
    return render_template('reportes/sanciones_por_tipo.html', datos=datos)

@reportes_bp.route('/porcentaje-uso')
def porcentaje_uso():  
    """Porcentaje de uso de reservas"""
    model = ReporteModel()
    datos = model.porcentaje_uso_reservas() 
    return render_template('reportes/porcentaje_uso.html', datos=datos)

