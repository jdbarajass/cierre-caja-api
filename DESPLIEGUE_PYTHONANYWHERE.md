# Guía de Despliegue en PythonAnywhere

Esta guía explica cómo configurar correctamente la aplicación en PythonAnywhere para que las rutas del frontend funcionen correctamente.

## Problema Identificado

Cuando accedes directamente a URLs como `https://jdbarajass.pythonanywhere.com/dashboard` o `https://jdbarajass.pythonanywhere.com/estadisticas-estandar/productos`, obtienes un error "Page not found". Esto ocurre porque el servidor necesita estar configurado para redirigir todas las rutas al `index.html` del frontend, permitiendo que React Router maneje la navegación.

## Solución

### 1. Estructura de Archivos en PythonAnywhere

Asegúrate de tener esta estructura en tu cuenta de PythonAnywhere:

```
/home/jdbarajass/
├── cierre-caja-api/
│   ├── app/
│   ├── wsgi.py          ← NUEVO ARCHIVO
│   ├── run.py
│   ├── .env
│   └── requirements.txt
└── cierre-caja-frontend/
    └── dist/            ← Build del frontend
        ├── index.html
        ├── assets/
        └── ...
```

### 2. Configurar Variables de Entorno en PythonAnywhere

Ve a la pestaña **Web** en PythonAnywhere y configura las siguientes variables de entorno:

```bash
# CRÍTICO: Ruta al build del frontend
FRONTEND_DIST_PATH=/home/jdbarajass/cierre-caja-frontend/dist

# Credenciales de Alegra
ALEGRA_USER=tu_usuario_alegra
ALEGRA_PASS=tu_contraseña_alegra

# JWT y seguridad
JWT_SECRET_KEY=tu_clave_secreta_jwt_minimo_32_caracteres
SECRET_KEY=tu_clave_secreta_flask

# Ambiente
FLASK_ENV=production
DEBUG=False

# CORS - tu dominio de PythonAnywhere
ALLOWED_ORIGINS=https://jdbarajass.pythonanywhere.com

# Zona horaria
TIMEZONE=America/Bogota

# Base objetivo
BASE_OBJETIVO=450000
UMBRAL_MENUDO=10000
```

### 3. Configurar el archivo WSGI en PythonAnywhere

1. Ve a la pestaña **Web** en tu dashboard de PythonAnywhere
2. Haz clic en el enlace "WSGI configuration file" (algo como `/var/www/jdbarajass_pythonanywhere_com_wsgi.py`)
3. **REEMPLAZA TODO EL CONTENIDO** del archivo con:

```python
# +++++++++++ FLASK +++++++++++
import sys
import os

# Agregar el directorio del proyecto al path
project_home = '/home/jdbarajass/cierre-caja-api'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Cargar variables de entorno desde .env
from dotenv import load_dotenv
dotenv_path = os.path.join(project_home, '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# Configurar variable de entorno crítica si no está en .env
if not os.getenv('FRONTEND_DIST_PATH'):
    os.environ['FRONTEND_DIST_PATH'] = '/home/jdbarajass/cierre-caja-frontend/dist'

# Configurar ambiente
os.environ['FLASK_ENV'] = 'production'
os.environ['DEBUG'] = 'False'

# Importar la aplicación
from app import create_app
from app.config import get_config

# Crear la aplicación
config = get_config('production')
application = create_app(config)
```

**IMPORTANTE**: Cambia `jdbarajass` por tu nombre de usuario real de PythonAnywhere en las rutas.

### 4. Verificar la Configuración del Virtualenv

1. En la pestaña **Web**, asegúrate de que "Virtualenv" esté configurado correctamente
2. Ejemplo: `/home/jdbarajass/.virtualenvs/cierre-caja-env`
3. Si no tienes un virtualenv, créalo:

```bash
# En la consola de PythonAnywhere
cd ~
python3.10 -m venv .virtualenvs/cierre-caja-env
source .virtualenvs/cierre-caja-env/bin/activate
cd cierre-caja-api
pip install -r requirements.txt
```

### 5. Verificar el Build del Frontend

Asegúrate de que el frontend esté construido correctamente:

```bash
# En tu máquina local
cd cierre-caja-frontend
npm run build

# Luego sube la carpeta dist/ a PythonAnywhere
# Puedes usar el botón "Upload a file" en el tab "Files"
# O usar git para sincronizar
```

### 6. Configuración en la pestaña Web

En la pestaña **Web** de PythonAnywhere:

1. **Source code**: `/home/jdbarajass/cierre-caja-api`
2. **Working directory**: `/home/jdbarajass/cierre-caja-api`
3. **WSGI configuration file**: El archivo que editaste en el paso 3
4. **Virtualenv**: `/home/jdbarajass/.virtualenvs/cierre-caja-env`

### 7. Recargar la Aplicación

Después de hacer los cambios:

1. Haz clic en el botón verde **"Reload jdbarajass.pythonanywhere.com"**
2. Espera unos segundos
3. Verifica los logs de error en la pestaña **"Log files"** → **"Error log"**

### 8. Verificación

Después de recargar, prueba estas URLs directamente en el navegador:

- ✅ `https://jdbarajass.pythonanywhere.com/`
- ✅ `https://jdbarajass.pythonanywhere.com/dashboard`
- ✅ `https://jdbarajass.pythonanywhere.com/monthly-sales`
- ✅ `https://jdbarajass.pythonanywhere.com/estadisticas-estandar/productos`

Todas deberían cargar correctamente (aunque requieran login).

## Troubleshooting

### Error: "Page not found" en rutas del frontend

**Causa**: `FRONTEND_DIST_PATH` no está configurado o la ruta es incorrecta.

**Solución**:
1. Verifica que la variable de entorno `FRONTEND_DIST_PATH` esté configurada
2. Verifica que la ruta apunte al directorio correcto
3. Verifica que el archivo `index.html` exista en esa ubicación
4. Revisa los logs de error

### Error: "Frontend no encontrado"

**Causa**: El directorio `dist/` no existe o está vacío.

**Solución**:
1. Construye el frontend: `npm run build`
2. Sube la carpeta `dist/` completa a PythonAnywhere
3. Verifica la ruta en `FRONTEND_DIST_PATH`

### Las rutas API funcionan pero el frontend no

**Causa**: El archivo WSGI no está configurado correctamente.

**Solución**:
1. Verifica que el archivo WSGI tenga el código del paso 3
2. Verifica que `FRONTEND_DIST_PATH` apunte a la carpeta correcta
3. Recarga la aplicación web

### Error 500 al cargar cualquier ruta

**Causa**: Error en la aplicación Flask o configuración incorrecta.

**Solución**:
1. Revisa los logs de error en la pestaña "Log files"
2. Verifica que todas las variables de entorno estén configuradas
3. Verifica que el virtualenv tenga todas las dependencias instaladas

### CORS errors en el navegador

**Causa**: `ALLOWED_ORIGINS` no incluye tu dominio de PythonAnywhere.

**Solución**:
1. Agrega tu dominio a `ALLOWED_ORIGINS`: `https://jdbarajass.pythonanywhere.com`
2. Recarga la aplicación

## Logs Útiles

Para revisar problemas, consulta estos logs en la pestaña "Log files":

1. **Error log**: Errores de la aplicación Flask
2. **Server log**: Logs del servidor web
3. **Access log**: Peticiones HTTP recibidas

## Comandos Útiles en la Consola

```bash
# Activar virtualenv
source ~/.virtualenvs/cierre-caja-env/bin/activate

# Verificar instalación de dependencias
pip list

# Ver estructura de archivos
tree -L 2 ~/cierre-caja-frontend/dist/

# Verificar que index.html existe
ls -la ~/cierre-caja-frontend/dist/index.html

# Ver variables de entorno (en Python console)
import os
print(os.getenv('FRONTEND_DIST_PATH'))
```

## Flujo de Actualización

Cuando hagas cambios en el código:

### Backend (API)
```bash
# Subir cambios a PythonAnywhere
# Luego en la consola de PythonAnywhere:
cd ~/cierre-caja-api
git pull  # Si usas git

# Recargar la aplicación web en la pestaña Web
```

### Frontend
```bash
# En tu máquina local:
cd cierre-caja-frontend
npm run build

# Subir la carpeta dist/ a PythonAnywhere
# O usar git para sincronizar

# Recargar la aplicación web en la pestaña Web
```

## Notas Importantes

1. **Siempre usa rutas absolutas** en PythonAnywhere (`/home/usuario/...`)
2. **El archivo WSGI es crítico** - cualquier error ahí rompe toda la aplicación
3. **Las variables de entorno son sensibles** - no las incluyas en el código, usa `.env`
4. **El directorio `dist/` debe estar actualizado** - reconstruye el frontend después de cada cambio
5. **CORS es importante** - asegúrate de que tu dominio esté en `ALLOWED_ORIGINS`

## ¿Necesitas Ayuda?

Si sigues teniendo problemas:

1. Revisa los logs de error
2. Verifica que todas las rutas sean absolutas y correctas
3. Asegúrate de que el virtualenv tenga todas las dependencias
4. Verifica que el frontend esté construido y en la ubicación correcta
5. Consulta la documentación de PythonAnywhere: https://help.pythonanywhere.com/

---

**Última actualización**: 2025-12-16
