import re

file_path = r'd:\Data Science\GitHub\PET - v1\Estudios\Presupuestos\generador_presupuesto.py'
with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

content = content.replace("excel_path = 'd:/Data Science/GitHub/PET - v1/presupuesto_clinica_mejorado_13.xlsx'", "excel_path = 'd:/Data Science/GitHub/PET - v1/Estudios/Presupuestos/presupuesto_clinica_mejorado_13.xlsx'")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
