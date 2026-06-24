import sqlite3
import pandas as pd

conn = sqlite3.connect(r'd:\Data Science\GitHub\PET\Proyecto_Integracion_Historico\pet_historico.db')
tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
print("Tables:")
print(tables)

for table in tables['name']:
    print(f"\nSchema for {table}:")
    schema = pd.read_sql(f"PRAGMA table_info({table});", conn)
    print(schema[['name', 'type']])

conn.close()
