# Mineria de Datos Moderna con Python — Segmentacion de Clientes (RFM + K-Means)

Proyecto de Inteligencia de Negocios para el **Taller Donald**. Extrae el
comportamiento de los clientes desde SQL Server, construye el modelo **RFM**
(Proximidad, Frecuencia, ValorMonetario) y aplica el algoritmo **K-Means** para descubrir
grupos de clientes que la Licenciada Claudia puede usar en campanas de marketing
directo en Guatemala.

## Modelo RFM

| Dimension | Significado | Origen de los datos |
|-----------|-------------|---------------------|
| **Proximidad** (Recencia) | Dias transcurridos desde la **ultima visita** del cliente | `Cita.FechaCita` |
| **Frecuencia** | Numero de **visitas distintas** al taller | `Cita.NumeroCita` |
| **ValorMonetario** | **Total facturado** al cliente | `DocumentoFiscal.ValorTotal` via `OrdeDeTrabajo` + `DetalleManoDeObra` |

La fecha de referencia para la proximidad es la **cita mas reciente** registrada en
la base de datos (estandar reproducible para analisis RFM). Se puede cambiar en
[`sql/query_rfm.sql`](sql/query_rfm.sql) modificando `@FechaReferencia`.

## Estructura del proyecto

```
proyecto_rfm/
├── .env                      # Credenciales de SQL Server (no se versiona)
├── requirements.txt
├── sql/
│   └── query_rfm.sql         # Consulta que consolida Proximidad, Frecuencia y ValorMonetario
├── src/
│   ├── conexion.py           # Conexion a BD, ejecucion de queries y guardado de CSV
│   ├── preparacion.py        # Limpieza, validacion, scores RFM y estandarizacion
│   └── segmentacion.py       # K-Means, metricas y etiquetado de segmentos de negocio
├── notebooks/
│   ├── 01_exploracion_db.ipynb       # Extraccion desde SQL Server
│   ├── 02_rfm_preparacion.ipynb      # Preparacion y scores RFM
│   ├── 03_kmeans_segmentacion.ipynb  # Elbow, Silhouette y entrenamiento K-Means
│   └── 04_resultados_y_perfiles.ipynb# Perfiles de negocio y graficos
├── data/                     # CSV intermedios y resultados (generados)
└── outputs/graficos/         # Graficos exportados (generados)
```

## Como ejecutar

1. **Configurar credenciales** en `.env`:

   ```
   SERVER=TU_SERVIDOR
   DATABASE=DonaldV2
   USER=sa
   PASSWORD=tu_password
   ```

2. **Instalar dependencias** (en el entorno virtual `.venv`):

   ```powershell
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

3. **Ejecutar los notebooks en orden** (`01` → `02` → `03` → `04`). Cada uno deja
   un CSV que el siguiente consume:

   | Notebook | Entrada | Salida |
   |----------|---------|--------|
   | 01 | SQL Server | `data/clientes_rfm.csv` |
   | 02 | `clientes_rfm.csv` | `clientes_rfm_preparado.csv`, `X_rfm_scaled.npy` |
   | 03 | `clientes_rfm_preparado.csv` | `clientes_clusterizados.csv` |
   | 04 | `clientes_clusterizados.csv` | `clientes_rfm_segmentados.csv`, `resumen_clusters.csv` |

## Patrones de cliente (entregable de BI)

A partir del perfil RFM promedio de cada cluster, se etiquetan los siguientes
patrones de negocio con su estrategia de marketing sugerida:

| Segmento | Perfil RFM | Estrategia |
|----------|------------|------------|
| **Clientes VIP** | Recientes, frecuentes y de alto gasto | Fidelizacion, atencion preferencial, upselling premium |
| **Clientes en Riesgo de Abandono** | Antes valiosos pero sin volver hace mucho | Reactivacion: descuentos y recordatorios de mantenimiento |
| **Clientes Esporadicos de Bajo Ticket** | Pocas visitas y bajo gasto | Promociones de bajo costo y paquetes para subir frecuencia |
| **Clientes Regulares** | Comportamiento intermedio | Comunicacion constante y ofertas estacionales |

## Tecnologias

Python · pandas · NumPy · scikit-learn (K-Means) · matplotlib · seaborn ·
pyodbc · SQL Server.
