"""
WSGI Configuration for PythonAnywhere

Este archivo debe configurarse en la pestaña "Web" de PythonAnywhere.

IMPORTANTE: En PythonAnywhere necesitas:
1. Configurar el path del código fuente (Source code)
2. Configurar el path del virtualenv
3. Configurar las variables de entorno necesarias
4. Configurar el WSGI configuration file apuntando a este archivo
"""
import sys
import os
from dotenv import load_dotenv

# ============================================================
# CONFIGURACIÓN DE PATHS - ACTUALIZAR SEGÚN TU USUARIO
# ============================================================
# Ejemplo: si tu usuario es "jdbarajass"
# El código estará en: /home/jdbarajass/cierre-caja-api
# El frontend estará en: /home/jdbarajass/cierre-caja-frontend/dist

# Path del proyecto (actualizar con tu usuario de PythonAnywhere)
project_home = os.path.dirname(os.path.abspath(__file__))

# Agregar el path del proyecto al PYTHONPATH
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# ============================================================
# CARGAR VARIABLES DE ENTORNO
# ============================================================
# Cargar el archivo .env si existe
dotenv_path = os.path.join(project_home, '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# ============================================================
# CONFIGURAR VARIABLES DE ENTORNO CRÍTICAS
# ============================================================
# Si no están en .env, configurarlas aquí:

# Frontend path - CRÍTICO para que las rutas funcionen
# Actualizar con la ruta real en PythonAnywhere
if not os.getenv('FRONTEND_DIST_PATH'):
    # Ejemplo: /home/jdbarajass/cierre-caja-frontend/dist
    # ACTUALIZAR ESTO CON TU USUARIO:
    username = os.path.basename(os.path.dirname(project_home))
    frontend_path = f'/home/{username}/cierre-caja-frontend/dist'
    os.environ['FRONTEND_DIST_PATH'] = frontend_path

# Ambiente de producción
os.environ['FLASK_ENV'] = os.getenv('FLASK_ENV', 'production')

# Debug en False para producción
if 'DEBUG' not in os.environ:
    os.environ['DEBUG'] = 'False'

# CORS - Agregar el dominio de PythonAnywhere
if 'ALLOWED_ORIGINS' not in os.environ:
    # Obtener el usuario para construir la URL automáticamente
    username = os.path.basename(os.path.dirname(project_home))
    os.environ['ALLOWED_ORIGINS'] = f'https://{username}.pythonanywhere.com'

# ============================================================
# IMPORTAR Y CONFIGURAR LA APLICACIÓN FLASK
# ============================================================
from app import create_app
from app.config import get_config

# Crear la aplicación
config = get_config('production')
application = create_app(config)

# Log de inicio
application.logger.info("=" * 70)
application.logger.info("WSGI Application Started for PythonAnywhere")
application.logger.info(f"Project home: {project_home}")
application.logger.info(f"Frontend path: {os.getenv('FRONTEND_DIST_PATH')}")
application.logger.info(f"Python path: {sys.path[:3]}")
application.logger.info(f"Environment: {os.getenv('FLASK_ENV')}")
application.logger.info("=" * 70)

# Verificar que el frontend existe
frontend_dist = os.getenv('FRONTEND_DIST_PATH')
if frontend_dist and os.path.isdir(frontend_dist):
    application.logger.info(f"✓ Frontend encontrado en: {frontend_dist}")
    index_html = os.path.join(frontend_dist, 'index.html')
    if os.path.isfile(index_html):
        application.logger.info("✓ index.html encontrado")
    else:
        application.logger.error("✗ index.html NO encontrado")
else:
    application.logger.error(f"✗ Frontend NO encontrado en: {frontend_dist}")
    application.logger.error("Las rutas del frontend NO funcionarán correctamente")
    application.logger.error("Configura FRONTEND_DIST_PATH correctamente")
