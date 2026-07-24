import re

file_path = r'd:\Data Science\GitHub\PET - v1\Estudios\Presupuestos\generador_presupuesto.py'
with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Replace the CAPEX section salaries
new_capex_salaries = '''    ['Costos Iniciales', 'Sueldo Sasha (Mes 1 Sincronizado)', 1, costo_empresa_sasha, 0, costo_empresa_sasha],
    ['Costos Iniciales', 'Sueldo Dani (Mes 1 Sincronizado)', 1, costo_empresa_dani, 0, costo_empresa_dani],
    ['Costos Iniciales', 'Sueldo Médico 2 (Mes 1 Sincronizado)', 1, costo_empresa_med2, 0, costo_empresa_med2],
    ['Costos Iniciales', 'Sueldo Médico 3 (Mes 1 Sincronizado)', 1, costo_empresa_med3, 0, costo_empresa_med3],
    ['Costos Iniciales', 'Sueldo Técnicos (Mes 1 Sincronizado)', 1, costo_empresa_tec, 0, costo_empresa_tec],
    ['Costos Iniciales', 'Sueldo Recepcionista 2 (Mes 1 Sincronizado)', 1, costo_empresa_recep2, 0, costo_empresa_recep2],'''

content = re.sub(
    r"\s+\['Costos Iniciales', 'Sueldo Sasha.*?Sueldo T.*?Boleta.*?\],",
    f"\n{new_capex_salaries}",
    content,
    flags=re.DOTALL
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
