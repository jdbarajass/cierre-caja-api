# Guía de Inicio Rápido - Cierre de Caja API

Esta guía te permite levantar el servidor en menos de 5 minutos.

---

## Método 1: Script Automático (Recomendado) ⚡

### Windows:
```bash
# 1. Ejecutar script de instalación
install_dependencies.bat

# 2. Levantar servidor
python run.py
```

### Linux/Mac:
```bash
# 1. Dar permisos y ejecutar script de instalación
chmod +x install_dependencies.sh
./install_dependencies.sh

# 2. Levantar servidor
python run.py
```

### Verificar que funciona:
Abre tu navegador en: http://10.28.168.57:5000/health

Si ves `"status": "healthy"` → **¡Listo!** ✅

---

## Método 2: Manual (si el script falla)

```bash
# 1. Instalar dependencias paso a paso
pip install Flask==2.2.5 flask-cors==4.0.0 Flask-Limiter==3.5.0 flasgger==0.9.7.1 python-dotenv==1.0.0 tzdata==2023.3 pytz==2023.3 python-dateutil==2.8.2 PyJWT==2.8.0 bcrypt==4.1.2 Flask-SQLAlchemy==3.1.1 reportlab==4.0.7 requests==2.31.0 gunicorn==20.1.0

# 2. Instalar Werkzeug compatible
pip install Werkzeug==3.0.0

# 3. Instalar pydantic
pip install pydantic --upgrade

# 4. Levantar servidor
python run.py
```

---

## Problemas Comunes

### ❌ Error: "ModuleNotFoundError: No module named 'flask_limiter'"
**Solución:** Ejecuta `install_dependencies.bat` (Windows) o `install_dependencies.sh` (Linux/Mac)

### ❌ Error: "AttributeError: module 'ast' has no attribute 'Str'"
**Solución:**
```bash
pip install Werkzeug==3.0.0
```
Este error ocurre en Python 3.14+. Werkzeug 3.0.0 lo soluciona.

### ❌ Error: "Cargo, the Rust package manager, is not installed"
**Solución:**
```bash
pip install pydantic --upgrade
```
Esto instala una versión de pydantic con binarios precompilados.

### ❌ Warning: 'FLASK_ENV' is deprecated
**Solución:** Este es solo un warning, puedes ignorarlo. El servidor funcionará correctamente.

---

## URLs Importantes

Una vez el servidor esté corriendo:

- **Health Check:** http://10.28.168.57:5000/health
- **Documentación API (Swagger):** http://10.28.168.57:5000/api/docs
- **Endpoint Principal:** http://10.28.168.57:5000/api/sum_payments

---

## ¿Más Problemas?

Lee la documentación completa de troubleshooting:

📖 **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Soluciones detalladas a todos los problemas

---

## Verificación Completa

Para asegurarte de que todo está funcionando:

```bash
# 1. Health check
curl http://10.28.168.57:5000/health

# Deberías ver:
# {
#   "status": "healthy",
#   "service": "cierre-caja-api",
#   "version": "2.0.0",
#   "alegra": "connected"
# }
```

Si ves `"status": "healthy"` → **¡El servidor está funcionando correctamente!** 🎉

---

**Última actualización:** 2025-11-28
