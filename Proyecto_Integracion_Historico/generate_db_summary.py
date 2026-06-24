import sqlite3
import pandas as pd
import os

db_path = r'd:\Data Science\GitHub\PET\Proyecto_Integracion_Historico\pet_historico.db'
conn = sqlite3.connect(db_path)

tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)

artifact_dir = r"C:\Users\Sasha\.gemini\antigravity-ide\brain\0d176447-68f4-46ff-9e1b-b4cd4b854cbb"
out_path = os.path.join(artifact_dir, 'database_summary.md')

with open(out_path, 'w', encoding='utf-8') as f:
    f.write("# Resumen Completo de la Base de Datos `pet_historico.db`\n\n")
    f.write("A continuación se muestra el esquema y una muestra de datos de todas las tablas integradas en la base.\n\n")
    
    for table in tables['name']:
        count_df = pd.read_sql(f"SELECT COUNT(*) as count FROM {table}", conn)
        count = count_df['count'][0]
        
        f.write(f"## Tabla: `{table}`\n")
        f.write(f"**Total de Registros:** {count:,}\n\n")
        
        if count > 0:
            schema = pd.read_sql(f"PRAGMA table_info({table});", conn)
            columnas = ", ".join(schema['name'].tolist())
            f.write(f"**Columnas disponibles:** {columnas}\n\n")

            sample_df = pd.read_sql(f"SELECT * FROM {table} LIMIT 3", conn)
            f.write("**Muestra de Datos (Primeros 3 registros):**\n")
            f.write("```text\n")
            f.write(sample_df.to_string(index=False))
            f.write("\n```\n\n")
        
        f.write("---\n")

conn.close()
print("Summary generated successfully in brain directory.")
