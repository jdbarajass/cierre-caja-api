# Guía de Implementación: Carga de Archivo de Inventario

## 📋 Objetivo

Implementar funcionalidad en la sección de inventario del frontend para cargar y analizar archivos de inventario (CSV o Excel) desde Alegra.

---

## 🎯 Requerimientos

### 1. Dos Botones en la Sección de Inventario

#### Botón 1: "Ver Inventario Actual"
- **Endpoint**: `GET /api/inventory/analysis`
- **Descripción**: Consulta el inventario actual desde la API de Alegra en tiempo real

#### Botón 2: "Cargar Archivo de Inventario"
- **Endpoint**: `POST /api/inventory/upload-file`
- **Formatos**: `.csv`, `.xlsx`, `.xls`
- **Descripción**: Carga un archivo exportado de Alegra para análisis offline

---

## 🔌 API Endpoint

### POST /api/inventory/upload-file

**Autenticación**: Requiere token JWT en header `Authorization: Bearer {token}`

**Request**:
```http
POST /api/inventory/upload-file
Content-Type: multipart/form-data
Authorization: Bearer {your-jwt-token}

FormData:
  file: [archivo.csv o archivo.xlsx]
```

**Response** (200 OK):
```json
{
  "success": true,
  "resumen_general": {
    "total_items": 2213,
    "valor_total_costo": 94077075.00,
    "valor_total_precio": 125242500.00,
    "margen_total": 31165425.00,
    "margen_porcentaje": 24.88,
    "total_categorias": 73
  },
  "por_departamento": {
    "hombre": {
      "cantidad": 385,
      "valor_costo": 31949250.00,
      "valor_precio": 42561600.00,
      "margen_total": 10612350.00,
      "margen_porcentaje": 25.00,
      "precio_promedio": 110549.09,
      "costo_promedio": 82985.07,
      "porcentaje_inventario": 17.40,
      "items": [...]
    },
    "mujer": {...},
    "nino": {...},
    "nina": {...},
    "accesorios": {...},
    "otros": {...}
  },
  "top_categorias": [
    {"categoria": "JEAN MUJER", "cantidad": 117},
    {"categoria": "ZAPATO HOMBRE", "cantidad": 98},
    ...
  ],
  "departamentos_ordenados": [
    {"nombre": "mujer", "cantidad": 575, "valor": 56775400.00},
    ...
  ]
}
```

**Errores**:
- `400`: Archivo no válido o formato no soportado
- `401`: Token inválido o expirado
- `500`: Error interno del servidor

---

## 💻 Implementación JavaScript/TypeScript

### Función de Upload

```javascript
const handleFileUpload = async (event) => {
  const file = event.target.files[0];

  if (!file) {
    alert('Por favor selecciona un archivo');
    return;
  }

  // Validar extensión
  const validExtensions = ['.csv', '.xlsx', '.xls'];
  const fileExt = '.' + file.name.split('.').pop().toLowerCase();

  if (!validExtensions.includes(fileExt)) {
    alert('Formato no soportado. Use CSV o Excel');
    return;
  }

  // Crear FormData
  const formData = new FormData();
  formData.append('file', file);

  // Obtener token
  const token = localStorage.getItem('token');

  try {
    setLoading(true);

    const response = await fetch('http://localhost:5000/api/inventory/upload-file', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      body: formData
    });

    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }

    const result = await response.json();

    if (result.success) {
      displayInventoryAnalysis(result);
    }
  } catch (error) {
    console.error('Error:', error);
    alert('Error al cargar el archivo');
  } finally {
    setLoading(false);
  }
};
```

---

## ⚛️ Ejemplo con React

```jsx
import React, { useState } from 'react';

const InventoryFileUpload = () => {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);

  const handleFileSelect = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    const token = localStorage.getItem('token');

    try {
      setLoading(true);

      const response = await fetch('http://localhost:5000/api/inventory/upload-file', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` },
        body: formData
      });

      const result = await response.json();

      if (result.success) {
        setData(result);
      }
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="inventory-section">
      {/* Botones */}
      <div className="button-group">
        <button onClick={() => fetchCurrentInventory()}>
          Ver Inventario Actual
        </button>

        <label className="upload-btn">
          <input
            type="file"
            accept=".csv,.xlsx,.xls"
            onChange={handleFileSelect}
            style={{ display: 'none' }}
          />
          Cargar Archivo de Inventario
        </label>
      </div>

      {/* Loading */}
      {loading && <div className="loading">Procesando archivo...</div>}

      {/* Resultados */}
      {data && (
        <div className="results">
          {/* Resumen General */}
          <div className="summary-cards">
            <div className="card">
              <h3>Total Items</h3>
              <p>{data.resumen_general.total_items}</p>
            </div>
            <div className="card">
              <h3>Valor Inventario</h3>
              <p>${data.resumen_general.valor_total_precio.toLocaleString()}</p>
            </div>
            <div className="card">
              <h3>Margen</h3>
              <p>{data.resumen_general.margen_porcentaje.toFixed(2)}%</p>
            </div>
          </div>

          {/* Tabla de Departamentos */}
          <table className="departments-table">
            <thead>
              <tr>
                <th>Departamento</th>
                <th>Cantidad</th>
                <th>Valor</th>
                <th>Margen %</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(data.por_departamento).map(([dept, info]) => (
                <tr key={dept}>
                  <td>{dept.toUpperCase()}</td>
                  <td>{info.cantidad}</td>
                  <td>${info.valor_precio.toLocaleString()}</td>
                  <td>{info.margen_porcentaje.toFixed(2)}%</td>
                </tr>
              ))}
            </tbody>
          </table>

          {/* Top Categorías */}
          <div className="top-categories">
            <h3>Top 10 Categorías</h3>
            <ul>
              {data.top_categorias.slice(0, 10).map((cat, i) => (
                <li key={i}>{cat.categoria}: {cat.cantidad} items</li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
};

export default InventoryFileUpload;
```

---

## 🎨 Estilos CSS

```css
.inventory-section {
  padding: 20px;
}

.button-group {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
}

.upload-btn {
  padding: 12px 24px;
  background-color: #007bff;
  color: white;
  border-radius: 4px;
  cursor: pointer;
  display: inline-block;
}

.upload-btn:hover {
  background-color: #0056b3;
}

.summary-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.card h3 {
  margin: 0 0 8px 0;
  font-size: 14px;
  color: #666;
}

.card p {
  margin: 0;
  font-size: 24px;
  font-weight: bold;
}

.departments-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 24px;
}

.departments-table th,
.departments-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.departments-table th {
  background-color: #f8f9fa;
  font-weight: 600;
}

.loading {
  text-align: center;
  padding: 40px;
  font-size: 18px;
  color: #666;
}
```

---

## 📊 Componentes de UI Sugeridos

### 1. Tarjetas de Resumen
- Total de Items
- Valor Total de Inventario
- Margen Total ($)
- Margen Porcentaje (%)
- Total de Categorías

### 2. Gráfico de Departamentos
- Pie Chart o Bar Chart
- Usar `departamentos_ordenados`
- Mostrar distribución por valor

### 3. Tabla de Departamentos
Columnas:
- Departamento
- Cantidad de Items
- Valor Costo
- Valor Precio
- Margen ($)
- Margen (%)
- % del Inventario

### 4. Top Categorías
- Lista o gráfico de barras
- Top 10-20 categorías

---

## ⚠️ Manejo de Errores

```javascript
try {
  const response = await fetch(endpoint, options);

  if (!response.ok) {
    switch (response.status) {
      case 400:
        alert('Formato de archivo no válido');
        break;
      case 401:
        alert('Sesión expirada. Inicia sesión nuevamente');
        // Redirigir al login
        break;
      case 500:
        alert('Error del servidor. Intenta nuevamente');
        break;
      default:
        alert('Error desconocido');
    }
    return;
  }

  const result = await response.json();
  // Procesar resultado...

} catch (error) {
  console.error('Error:', error);
  alert('Error de conexión');
}
```

---

## 🚀 Mejoras Opcionales

1. **Drag & Drop**: Arrastrar y soltar archivos
2. **Barra de Progreso**: Mostrar progreso durante la carga
3. **Preview**: Vista previa de los primeros items
4. **Exportar**: Descargar el análisis en PDF o Excel
5. **Histórico**: Guardar análisis anteriores para comparar
6. **Filtros**: Filtrar por departamento o categoría
7. **Gráficos Avanzados**: Usar Chart.js o Recharts

---

## 🧪 Testing

Probar con:
- ✅ Archivo CSV de Alegra (formato estándar)
- ✅ Archivo Excel (.xlsx)
- ✅ CSV con separador de coma (`,`)
- ✅ CSV con separador de punto y coma (`;`)
- ✅ Archivos con caracteres especiales (ñ, tildes)
- ✅ Archivos grandes (>1000 productos)

---

## 🔗 URLs de Producción

```javascript
const API_URL = process.env.REACT_APP_API_URL || 'https://cierre-caja-api.onrender.com';
const endpoint = `${API_URL}/api/inventory/upload-file`;
```

---

## 📝 Notas Importantes

- El endpoint requiere autenticación JWT
- Los archivos CSV pueden usar `,` o `;` como separador (se detecta automáticamente)
- El backend clasifica automáticamente por departamentos basándose en palabras clave
- El procesamiento puede tomar unos segundos para archivos grandes
- El límite de tamaño de archivo es manejado por el servidor

---

## 🆘 Soporte

Para problemas o dudas, consultar:
- Documentación del backend: `README.md`
- Troubleshooting: `TROUBLESHOOTING.md`
- Analytics API: `ANALYTICS_API_DOCUMENTATION.md`
