import os
import glob

base_dir = os.path.dirname(__file__)
historico_dir = os.path.abspath(os.path.join(base_dir, '..', '..', 'historico'))

# Buscar TODOS los archivos Excel, sin importar su nombre, y capturar .xls y .xlsx
todos_los_excel = glob.glob(os.path.join(historico_dir, '**', '*.xls*'), recursive=True)

print(f"[EXPLORADOR] Total de archivos Excel encontrados: {len(todos_los_excel)}\n")
print("Aquí tienes una muestra de los nombres reales de tus archivos:")
print("-" * 50)

# Mostrar solo los nombres de los primeros 30 archivos encontrados
for f in todos_los_excel[:30]:
    print(os.path.basename(f))
