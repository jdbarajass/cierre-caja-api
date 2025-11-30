@echo off
REM ================================================================
REM Script de Instalacion de Dependencias - Cierre de Caja API
REM Compatible con Python 3.11, 3.12, 3.13, 3.14+
REM ================================================================

echo.
echo ================================================================
echo Instalando dependencias del servidor Cierre de Caja API
echo ================================================================
echo.

REM Verificar version de Python
echo [1/5] Verificando version de Python...
python --version
if errorlevel 1 (
    echo ERROR: Python no esta instalado o no esta en PATH
    pause
    exit /b 1
)
echo.

REM Paso 1: Instalar dependencias base
echo [2/5] Instalando dependencias base...
pip install Flask==2.2.5 flask-cors==4.0.0 Flask-Limiter==3.5.0 flasgger==0.9.7.1 python-dotenv==1.0.0 tzdata==2023.3 pytz==2023.3 python-dateutil==2.8.2 PyJWT==2.8.0 bcrypt==4.1.2 Flask-SQLAlchemy==3.1.1 reportlab==4.0.7 requests==2.31.0 gunicorn==20.1.0
if errorlevel 1 (
    echo ERROR: Fallo la instalacion de dependencias base
    pause
    exit /b 1
)
echo.

REM Paso 2: Instalar Werkzeug compatible con Python 3.14+
echo [3/5] Instalando Werkzeug 3.0.0 (compatible con Python 3.14+)...
pip install Werkzeug==3.0.0
if errorlevel 1 (
    echo ERROR: Fallo la instalacion de Werkzeug
    pause
    exit /b 1
)
echo.

REM Paso 3: Instalar pydantic con binarios precompilados
echo [4/5] Instalando pydantic (version con binarios precompilados)...
pip install pydantic --upgrade
if errorlevel 1 (
    echo ERROR: Fallo la instalacion de pydantic
    pause
    exit /b 1
)
echo.

REM Verificar instalacion
echo [5/5] Verificando instalacion...
python -c "import flask; import pydantic; import werkzeug; print('Flask:', flask.__version__); print('Pydantic:', pydantic.__version__); print('Werkzeug:', werkzeug.__version__)"
if errorlevel 1 (
    echo ERROR: La verificacion de modulos fallo
    pause
    exit /b 1
)
echo.

echo ================================================================
echo Instalacion completada exitosamente!
echo ================================================================
echo.
echo Proximos pasos:
echo 1. Verifica que el archivo .env esta configurado correctamente
echo 2. Ejecuta: python run.py
echo 3. Accede a: http://10.28.168.57:5000/health
echo.
echo Para mas informacion, lee: TROUBLESHOOTING.md
echo ================================================================
echo.
pause
