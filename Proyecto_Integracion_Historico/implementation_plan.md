# Integración de Registros a Base de Datos

Este documento propone un plan para integrar de forma limpia todos los registros históricos (`.csv`, `.xls` y `.zip`) que se encuentran en el directorio `d:\Data Science\GitHub\PET\historico` hacia una única base de datos estructurada.

## ⚠️ User Review Required

> [!IMPORTANT]
> Necesitamos definir en qué tipo de base de datos deseas almacenar esta información. 
> - ¿Te gustaría usar **SQLite** (una base de datos ligera contenida en un solo archivo `.db`, ideal para análisis local con Python/Pandas o BI)?
> - ¿O prefieres un motor más robusto como **PostgreSQL** o **MySQL**?
> 
> Mi recomendación es usar **SQLite** para empezar, ya que es rápida de configurar, no requiere instalación de un servidor externo y se puede integrar fácilmente en un proyecto de Data Science.

## Open Questions

> [!WARNING]
> 1. Hay archivos repetidos en formato `.csv` y `.xls`. Para la integración, sugiero priorizar los `.csv` para facilitar la lectura automatizada, a menos que prefieras que extraigamos de los `.xls`. ¿Estás de acuerdo?
> 2. Hay algunos archivos comprimidos `.zip` (como `Pet Exotic Veterinaria-*.zip` y `Facturas-*.zip`). ¿Deberíamos descomprimir e integrar también la información de su interior?
> 3. ¿Deseas que el script de integración limpie automáticamente errores comunes (espacios en blanco adicionales, formatos de fecha estandarizados como `YYYY-MM-DD`, etc.)?

## Proposed Changes

La propuesta se dividirá en 3 etapas principales mediante un script de Python (`etl_historico.py` o en un Jupyter Notebook).

### 1. Extracción y Exploración (Extract)
- Leer los archivos `.csv` relevantes:
  - `Contactos_Clinica.csv`
  - `Informe Prestaciones Vencidas o por Vencer.csv`
  - `Informe de Productos y Servicios Vendidos por Cliente.csv`
  - `Informe_Ventas_*.csv`
  - `Informe_detallede ventas.csv`
- Revisar y extraer el contenido de los archivos `.zip` si se aprueba.

### 2. Transformación y Limpieza (Transform)
- **Limpieza de strings:** Remover espacios sobrantes de los nombres de las columnas y los valores (ej. de `"PETEXOTIC      "` a `"PETEXOTIC"`).
- **Fechas:** Estandarizar todas las columnas de fechas (`FECHA INICIO`, `FECHA TERMINO`, etc.) a formato estándar `YYYY-MM-DD`.
- **Estructuración:** Crear modelos relacionales lógicos:
  - `Clientes / Pacientes`
  - `Ventas / Facturas`
  - `Prestaciones / Citas`

### 3. Carga en Base de Datos (Load)
- Crear la base de datos de destino (ej. `pet_historico.db`).
- Crear las tablas correspondientes e insertar los datos limpios.

#### [NEW] [etl_historico.py](file:///d:/Data%20Science/GitHub/PET/etl_historico.py)
Script en Python responsable de ejecutar el proceso ETL (Extraer, Transformar, Cargar).

## Verification Plan

### Automated Tests
- Validar mediante el script que ninguna tabla quede vacía luego del proceso de carga.
- Imprimir un reporte resumen (cantidad de registros cargados por tabla vs. líneas en los CSV originales).

### Manual Verification
- Te proporcionaré consultas SQL de prueba (ej. `SELECT COUNT(*) FROM Ventas;`) para que puedas verificar que los datos se visualizan correctamente en tu entorno.
