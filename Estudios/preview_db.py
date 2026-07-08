import sqlite3
import pandas as pd
import sys

db = 'd:/Data Science/GitHub/PET - v1/Estudios/Dashboard/clinica_historico.db'
conn = sqlite3.connect(db)
tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)['name'].tolist()
out = ['# Vista Previa de la Base de Datos: `clinica_historico.db`\n']

for t in tables:
    out.append(f'## Tabla: `{t}`')
    df = pd.read_sql_query(f'SELECT * FROM {t} LIMIT 5', conn)
    out.append(df.to_csv(index=False))
    out.append(f'\n*Total de columnas: {len(df.columns)}*\n')
    
with open('d:/Data Science/GitHub/PET - v1/Estudios/db_preview.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))
    
conn.close()
print('Listo.')
