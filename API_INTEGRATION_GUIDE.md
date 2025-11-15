# Guía de Integración API - Frontend

Documentación para integrar el frontend con la API de Cierre de Caja v2.0

---

## 📋 Cambios en la API

La API ahora procesa toda la lógica de negocio en el backend. El frontend solo debe recolectar y enviar datos.

### ¿Qué cambió?

- ✅ Procesamiento de excedentes movido al backend
- ✅ Cálculo de totales de métodos de pago movido al backend
- ✅ Validación del cierre movida al backend
- ✅ Todos los cálculos y categorización se hacen en el servidor

---

## 📤 Formato del Request

### Endpoint: `POST /sum_payments`

**Payload simplificado:**

```json
{
  "date": "2025-11-14",
  "coins": {
    "50": 0,
    "100": 0,
    "200": 2,
    "500": 0,
    "1000": 0
  },
  "bills": {
    "2000": 0,
    "5000": 4,
    "10000": 7,
    "20000": 7,
    "50000": 13,
    "100000": 1
  },
  "excedentes": [
    {
      "tipo": "efectivo",
      "subtipo": null,
      "valor": 10000
    }
  ],
  "gastos_operativos": 0,
  "gastos_operativos_nota": "",
  "prestamos": 0,
  "prestamos_nota": "",
  "metodos_pago": {
    "addi_datafono": 0,
    "nequi_luz_helena": 0,
    "daviplata_jose": 0,
    "qr_julieth": 0,
    "tarjeta_debito": 464000,
    "tarjeta_credito": 0
  }
}
```

### Tipos de Excedentes

```javascript
// Efectivo
{ "tipo": "efectivo", "subtipo": null, "valor": 10000 }

// Datafono
{ "tipo": "datafono", "subtipo": null, "valor": 5000 }

// Transferencias QR
{ "tipo": "qr_transferencias", "subtipo": "nequi", "valor": 3000 }
{ "tipo": "qr_transferencias", "subtipo": "daviplata", "valor": 2000 }
{ "tipo": "qr_transferencias", "subtipo": "qr", "valor": 1000 }
```

---

## 📥 Formato de la Respuesta

### Response Exitoso (200)

```json
{
  "request_datetime": "2025-11-14T21:51:36.035958-05:00",
  "request_date": "2025-11-14",
  "request_time": "21:51:36",
  "request_tz": "America/Bogota",
  "date_requested": "2025-11-14",
  "username_used": "koaj.puertocarreno@gmail.com",

  "alegra": {
    "date_requested": "2025-11-14",
    "results": {
      "cash": { "formatted": "$520.300", "label": "Efectivo", "total": 520300 },
      "debit-card": { "formatted": "$464.000", "label": "Tarjeta débito", "total": 464000 },
      "credit-card": { "formatted": "$0", "label": "Tarjeta crédito", "total": 0 },
      "transfer": { "formatted": "$852.500", "label": "Transferencia", "total": 852500 }
    },
    "total_sale": {
      "formatted": "$1.836.800",
      "label": "TOTAL VENTA DEL DÍA",
      "total": 1836800
    }
  },

  "cash_count": {
    "totals": {
      "total_general": 980400,
      "total_general_formatted": "$980.400"
    },
    "base": {
      "total_base": 450000,
      "total_base_formatted": "$450.000",
      "base_status": "sobrante",
      "mensaje_base": "Sobra $530.400 por encima de la base de $450.000"
    },
    "consignar": {
      "efectivo_para_consignar_final": 530400,
      "efectivo_para_consignar_final_formatted": "$530.400"
    },
    "adjustments": {
      "excedente": 10000,
      "excedente_formatted": "$10.000",
      "excedente_efectivo": 10000,
      "excedente_datafono": 0,
      "excedente_nequi": 0,
      "excedente_daviplata": 0,
      "excedente_qr": 0
    }
  },

  "excedentes_detalle": [
    { "tipo": "Efectivo", "valor": 10000 }
  ],

  "gastos_operativos_nota": "",
  "prestamos_nota": "",

  "metodos_pago_registrados": {
    "addi_datafono": 0,
    "nequi_luz_helena": 0,
    "daviplata_jose": 0,
    "qr_julieth": 0,
    "tarjeta_debito": 464000,
    "tarjeta_credito": 0,
    "total_transferencias_registradas": 0,
    "total_datafono_registrado": 464000
  },

  "validation": {
    "cierre_validado": false,
    "validation_status": "warning",
    "mensaje_validacion": "Diferencia en transferencias: $852.500",
    "diferencias": {
      "transferencias": {
        "alegra": 852500,
        "registrado": 0,
        "diferencia": 852500,
        "diferencia_formatted": "$852.500",
        "es_significativa": true
      },
      "datafono": {
        "alegra": 464000,
        "registrado": 464000,
        "diferencia": 0,
        "diferencia_formatted": "$0",
        "es_significativa": false
      }
    }
  }
}
```

---

## 🎯 Campos Clave para el Frontend

### Validación del Cierre

```javascript
// Verificar si el cierre fue exitoso
if (response.validation.cierre_validado) {
  showSuccessModal();
} else {
  showWarning(response.validation.mensaje_validacion);
}

// Mostrar diferencias
const { diferencias } = response.validation;
if (diferencias.transferencias.es_significativa) {
  console.warn('Diferencia en transferencias:',
    diferencias.transferencias.diferencia_formatted);
}
```

### Excedentes Categorizados

```javascript
// Ya vienen procesados del backend
response.excedentes_detalle.forEach(exc => {
  console.log(`${exc.tipo}: ${exc.valor}`);
});
```

### Totales de Métodos de Pago

```javascript
// Totales calculados automáticamente
const { metodos_pago_registrados } = response;
console.log('Transferencias:', metodos_pago_registrados.total_transferencias_registradas);
console.log('Datafono:', metodos_pago_registrados.total_datafono_registrado);
```

---

## 🚨 Manejo de Errores

### Error 400 - Validación

```json
{
  "error": "Errores de validación: date: field required",
  "status_code": 400,
  "type": "ValidationError"
}
```

### Error 502 - Fallo de Alegra

```json
{
  "request_datetime": "2025-11-14T21:51:36.035958-05:00",
  "date_requested": "2025-11-14",
  "cash_count": { /* datos de caja */ },
  "alegra": {
    "error": "Error al conectar con Alegra",
    "details": { /* detalles del error */ }
  }
}
```

---

## 💡 Ejemplos de Uso

### Ejemplo React/JavaScript

```javascript
const handleSubmit = async () => {
  const payload = {
    date: selectedDate,
    coins: coinValues,
    bills: billValues,
    excedentes: excedentesList,
    gastos_operativos: gastosValue,
    gastos_operativos_nota: gastosNota,
    prestamos: prestamosValue,
    prestamos_nota: prestamosNota,
    metodos_pago: metodosPagoValues
  };

  try {
    const response = await fetch('http://10.28.168.57:5000/sum_payments', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const data = await response.json();

    if (response.ok) {
      // Usar validación del backend
      if (data.validation.cierre_validado) {
        showSuccessModal();
      } else {
        showWarningModal(data.validation.mensaje_validacion);
      }

      // Mostrar datos
      setCierreData(data);
    } else {
      showError(data.error);
    }
  } catch (error) {
    console.error('Error:', error);
    showError('Error de conexión con el servidor');
  }
};
```

---

## 🔗 URLs de la API

### Desarrollo Local
- API: `http://10.28.168.57:5000`
- Health Check: `http://10.28.168.57:5000/health`
- Docs: `http://10.28.168.57:5000/api/docs`

### Producción
- API: `https://cierre-caja-api.onrender.com`
- Health Check: `https://cierre-caja-api.onrender.com/health`

---

## 📝 Notas Importantes

1. **No calcular totales en el frontend** - El backend los calcula automáticamente
2. **Usar `validation.cierre_validado`** - Para mostrar modal de éxito
3. **Confiar en los datos del backend** - Son la única fuente de verdad
4. **Manejar errores 502** - Cuando Alegra falla, se recibe respuesta parcial

---

**Versión API:** 2.0.0
**Última actualización:** 2025-11-15
