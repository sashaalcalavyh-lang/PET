# Integración Exitosa de Base de Datos Histórica

¡El proceso de integración ha concluido de forma exitosa! A continuación te explico los detalles de lo que se realizó y cómo acceder a tu nueva base de datos.

## ¿Qué se hizo?

1. **Extracción y limpieza:** Se leyeron y extrajeron de forma recursiva los archivos `.csv` en la carpeta `historico` y al interior de los `.zip`. Los espacios adicionales fueron removidos y los nombres de las columnas se estandarizaron para evitar problemas a futuro.
2. **Transformación:** Las columnas que indicaban fechas se estandarizaron al formato estándar de Pandas/SQL, facilitando su análisis a futuro.
3. **Carga en SQLite:** Toda la información fue volcada en un solo archivo de base de datos llamado `pet_historico.db`.

> [!TIP]
> Se ignoraron archivos corruptos o bloqueados por permisos de Windows (como `Calendario_Historico.zip`) y rutas demasiado largas dentro de algunos `.zip`, pero se cargó con éxito el cuerpo principal de las bases de datos de **Ventas**, **Contactos** y **Prestaciones**.

## Tablas Generadas

Dentro de la base de datos `pet_historico.db` encontrarás las siguientes tablas con sus respectivos registros consolidados:

- `TBL_CONTACTOS_CLINICACSV` (421 registros)
- `TBL_INFORME_DE_PRODUCTOS_Y_SERVICIOS_VENDIDOS_POR_CLIENTE` (12,261 registros)
- `TBL_INFORME_E_INDICADORES_PARA_MEDICIN_CALIDAD_DE_ATENCIN` (18 registros)
- `TBL_INFORME_PRESTACIONES_VENCIDAS_O_POR_VENCER` (429 registros)
- `TBL_INFORME_DETALLEDE_VENTAS` (11,490 registros)
- `TBL_INFORME_VENTAS_PORCLIENTES` (11,515 registros)
- `TBL_INFORME_VENTAS_PORPRODUCTO` (11,515 registros)
- `TBL_INFORME_VENTAS_PORVENDEDOR` (11,515 registros)

## ¿Cómo acceder a los datos?

El archivo final está ubicado en:
[pet_historico.db](file:///d:/Data%20Science/GitHub/PET/pet_historico.db)

También creamos el script que realizó esta tarea por si quieres ejecutarlo de nuevo a futuro con archivos nuevos:
[etl_historico.py](file:///d:/Data%20Science/GitHub/PET/etl_historico.py)

Para comenzar a analizar, puedes conectar **Python (Pandas)** directamente al archivo así:

```python
import sqlite3
import pandas as pd

# Conectar a la base de datos
conn = sqlite3.connect(r"d:\Data Science\GitHub\PET\pet_historico.db")

# Consultar datos
df_ventas = pd.read_sql("SELECT * FROM TBL_INFORME_VENTAS_PORCLIENTES LIMIT 10;", conn)
print(df_ventas)

conn.close()
```
