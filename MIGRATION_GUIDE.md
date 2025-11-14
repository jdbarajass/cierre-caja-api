# Guía de Migración a v2.0

## 📊 Resumen de Cambios

### ✅ Lo que se mantiene igual:

- **Lógica de negocio**: El algoritmo knapsack y cálculos son idénticos
- **API endpoint**: `/sum_payments` funciona exactamente igual
- **Request/Response**: El formato JSON es 100% compatible
- **Integración Alegra**: Funcionalidad sin cambios
- **Variables de entorno**: `.env` funciona igual (solo agregar nuevas opcionales)

### 🆕 Lo que es nuevo:

- ✨ Arquitectura modular (app/, services/, models/, utils/)
- ✨ Validación automática con Pydantic
- ✨ Logging profesional
- ✨ Tests unitarios
- ✨ Documentación Swagger en `/api/docs`
- ✨ Health check en `/health`
- ✨ Rate limiting
- ✨ Mejor manejo de errores

---

## 🚀 Pasos de Migración

### Paso 1: Backup de tu configuración

```bash
# Copia tu .env actual
cp .env .env.backup
```

### Paso 2: Instalar nuevas dependencias

```bash
# Actualizar dependencias
pip install -r requirements.txt
```

### Paso 3: Verificar variables de entorno

Tu `.env` actual debería funcionar. Opcionalmente puedes agregar nuevas:

```bash
# Agregar a tu .env (opcional)
SECRET_KEY=tu-secret-key-aqui
DEBUG=False
FLASK_ENV=production
```

### Paso 4: Probar localmente

```bash
# Ejecutar en desarrollo
python run.py
```

Visita:
- API: http://localhost:5000/sum_payments
- Docs: http://localhost:5000/api/docs
- Health: http://localhost:5000/health

### Paso 5: Ejecutar tests (opcional)

```bash
pytest
```

### Paso 6: Desplegar en Render

**IMPORTANTE**: Render usará el nuevo `Procfile` automáticamente.

1. Haz commit de los cambios:
   ```bash
   git add .
   git commit -m "Migración a v2.0 - Arquitectura modular"
   git push
   ```

2. Render detectará los cambios y re-desplegará automáticamente

3. Verifica el health check: `https://tu-app.onrender.com/health`

---

## 🔍 Verificación Post-Migración

### Checklist:

- [ ] El endpoint `/sum_payments` responde correctamente
- [ ] El endpoint `/health` retorna status "healthy"
- [ ] Los logs aparecen en el dashboard de Render
- [ ] El frontend puede hacer requests sin problemas
- [ ] Swagger docs accesible en `/api/docs`

### Prueba rápida con curl:

```bash
curl -X POST https://tu-app.onrender.com/sum_payments \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2025-11-06",
    "coins": {"50": 0, "100": 6, "200": 40, "500": 1, "1000": 0},
    "bills": {"2000": 16, "5000": 7, "10000": 7, "20000": 12, "50000": 12, "100000": 9},
    "excedente": 13500,
    "gastos_operativos": 0,
    "prestamos": 0
  }'
```

---

## 🐛 Troubleshooting

### Problema: "ModuleNotFoundError: No module named 'app'"

**Solución:**
```bash
# Asegúrate de estar en el directorio correcto
cd cierre-caja-api

# Reinstala dependencias
pip install -r requirements.txt
```

### Problema: "ALEGRA_PASS no está configurado"

**Solución:**
```bash
# Verifica que .env tiene las credenciales
cat .env | grep ALEGRA_PASS

# Si no, agrégalo:
echo "ALEGRA_PASS=tu_token_aqui" >> .env
```

### Problema: "Error en Swagger docs"

**Solución:**
- Swagger puede tardar en cargar la primera vez
- Verifica que `flasgger` esté instalado: `pip install flasgger`

### Problema: Los tests fallan

**Solución:**
```bash
# Instala dependencias de desarrollo
pip install -r requirements-dev.txt

# Ejecuta tests con verbose
pytest -v
```

---

## 🔄 Rollback (Si es necesario)

Si necesitas volver a la versión anterior:

```bash
# 1. Restaurar archivo original
mv UnionCierreKoajExtraccionAlegraApi_v1_backup.py UnionCierreKoajExtraccionAlegraApi.py

# 2. Actualizar Procfile
echo "web: gunicorn UnionCierreKoajExtraccionAlegraApi:app --bind 0.0.0.0:\$PORT" > Procfile

# 3. Commit y push
git add .
git commit -m "Rollback a v1.0"
git push
```

---

## 📊 Comparación de Performance

### v1.0 (Monolítico):
- 1 archivo Python de ~430 líneas
- Sin tests
- Sin validación
- Logging básico

### v2.0 (Modular):
- Múltiples módulos bien organizados
- 12+ tests unitarios
- Validación automática con Pydantic
- Logging profesional con niveles
- Documentación Swagger
- Health checks
- Rate limiting

**Performance**: Igual o mejor (validación tiene overhead mínimo)

---

## 🎯 Mejoras Futuras Posibles

1. **Base de datos**: Guardar historial de cierres
2. **Autenticación**: JWT para proteger endpoints
3. **Webhooks**: Notificaciones automáticas
4. **Dashboards**: Visualización de métricas
5. **Cache**: Redis para mejorar performance
6. **CI/CD**: Tests automáticos en cada commit

---

## 📧 Soporte

Si tienes problemas con la migración:

1. Revisa los logs: `logs/cierre_caja.log` (local) o Render dashboard
2. Verifica el health endpoint: `/health`
3. Consulta la documentación: `/api/docs`
4. Contacta: koaj.puertocarreno@gmail.com

---

**¡Migración exitosa! 🎉**
