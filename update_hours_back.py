import re

file_path = r'd:\Data Science\GitHub\PET - v1\Estudios\Presupuestos\generador_presupuesto.py'
with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Change hours back to 60 for fixed cost
content = content.replace('horas_med3 = 0  # 100% Variable (Solo si se abre FDS)', 'horas_med3 = 60')
content = content.replace('horas_tec = 0  # 100% Variable (Solo si hay hospitalizados)', 'horas_tec = 60')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
