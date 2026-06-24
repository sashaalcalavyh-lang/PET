import sqlite3
import pandas as pd

# Conectar a la base de datos (con la nueva ruta)
conn = sqlite3.connect(r"d:\Data Science\GitHub\PET\Proyecto_Integracion_Historico\pet_historico.db")

# Consultar datos
df_ventas = pd.read_sql("SELECT * FROM TBL_INFORME_VENTAS_PORCLIENTES LIMIT 10;", conn)
print(df_ventas)

conn.close()
