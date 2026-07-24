import re

file_path = r'd:\Data Science\GitHub\PET - v1\Estudios\Presupuestos\generador_presupuesto.py'
with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Change hours for Med 3 and Tec to 0
content = content.replace('horas_med3 = 60', 'horas_med3 = 0  # 100% Variable (Solo si se abre FDS)')
content = content.replace('horas_tec = 60', 'horas_tec = 0  # 100% Variable (Solo si hay hospitalizados)')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
