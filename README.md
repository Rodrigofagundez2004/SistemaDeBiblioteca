# SistemaDeBiblioteca — Instrucciones para ejecutar

## Requisitos
- Python 3.7+ instalado
- Acceso a la terminal (PowerShell / CMD / Bash)

## 1) Crear y activar un entorno virtual (recomendado)
Windows (PowerShell):
```
python -m venv .venv
.venv\Scripts\Activate.ps1
```
Windows (CMD):
```
python -m venv .venv
.venv\Scripts\activate
```
Linux / macOS:
```
python3 -m venv .venv
source .venv/bin/activate
```

## 2) Instalar dependencias
```
pip install --upgrade pip
pip install -r requirements.txt
```

## 3) Ejecutar la aplicación
Desde la raíz del proyecto:
```
python app.py
```