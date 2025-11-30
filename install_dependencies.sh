#!/bin/bash
# ================================================================
# Script de Instalación de Dependencias - Cierre de Caja API
# Compatible con Python 3.11, 3.12, 3.13, 3.14+
# ================================================================

echo ""
echo "================================================================"
echo "Instalando dependencias del servidor Cierre de Caja API"
echo "================================================================"
echo ""

# Verificar versión de Python
echo "[1/5] Verificando versión de Python..."
python3 --version
if [ $? -ne 0 ]; then
    echo "ERROR: Python no está instalado o no está en PATH"
    exit 1
fi
echo ""

# Paso 1: Instalar dependencias base
echo "[2/5] Instalando dependencias base..."
pip install Flask==2.2.5 flask-cors==4.0.0 Flask-Limiter==3.5.0 flasgger==0.9.7.1 python-dotenv==1.0.0 tzdata==2023.3 pytz==2023.3 python-dateutil==2.8.2 PyJWT==2.8.0 bcrypt==4.1.2 Flask-SQLAlchemy==3.1.1 reportlab==4.0.7 requests==2.31.0 gunicorn==20.1.0
if [ $? -ne 0 ]; then
    echo "ERROR: Falló la instalación de dependencias base"
    exit 1
fi
echo ""

# Paso 2: Instalar Werkzeug compatible con Python 3.14+
echo "[3/5] Instalando Werkzeug 3.0.0 (compatible con Python 3.14+)..."
pip install Werkzeug==3.0.0
if [ $? -ne 0 ]; then
    echo "ERROR: Falló la instalación de Werkzeug"
    exit 1
fi
echo ""

# Paso 3: Instalar pydantic con binarios precompilados
echo "[4/5] Instalando pydantic (versión con binarios precompilados)..."
pip install pydantic --upgrade
if [ $? -ne 0 ]; then
    echo "ERROR: Falló la instalación de pydantic"
    exit 1
fi
echo ""

# Verificar instalación
echo "[5/5] Verificando instalación..."
python3 -c "import flask; import pydantic; import werkzeug; print('Flask:', flask.__version__); print('Pydantic:', pydantic.__version__); print('Werkzeug:', werkzeug.__version__)"
if [ $? -ne 0 ]; then
    echo "ERROR: La verificación de módulos falló"
    exit 1
fi
echo ""

echo "================================================================"
echo "Instalación completada exitosamente!"
echo "================================================================"
echo ""
echo "Próximos pasos:"
echo "1. Verifica que el archivo .env está configurado correctamente"
echo "2. Ejecuta: python3 run.py"
echo "3. Accede a: http://10.28.168.57:5000/health"
echo ""
echo "Para más información, lee: TROUBLESHOOTING.md"
echo "================================================================"
echo ""
