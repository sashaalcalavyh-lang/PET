import re

file_path = r'd:\Data Science\GitHub\PET - v1\Estudios\Presupuestos\generador_presupuesto.py'
with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

new_rrhh_content = '''# 2. RRHH (Fase 1 con Carga Legal y Provisiones)
sueldo_minimo = 500000

# 1. Daniela (Socia Directora Médica) - 25 hrs
sueldo_base_dani = 395395
gratificacion_dani = sueldo_base_dani * 0.25
imponible_dani = sueldo_base_dani + gratificacion_dani
aportes_empleador_dani = imponible_dani * 0.0487 # SIS + AFC + Mutual
provisiones_dani = imponible_dani * 0.1249 # Vacaciones + IAS
retiro_dani = 1700000 - imponible_dani * 0.80 # Aprox liquido sin retiro = 80% del imponible
costo_empresa_dani = imponible_dani + aportes_empleador_dani + provisiones_dani + retiro_dani

# 2. Sasha (Socia Recepción) - 30 hrs
sueldo_base_sasha = 395395
gratificacion_sasha = sueldo_base_sasha * 0.25
imponible_sasha = sueldo_base_sasha + gratificacion_sasha
aportes_empleador_sasha = imponible_sasha * 0.0487
provisiones_sasha = imponible_sasha * 0.1249
retiro_sasha = 800000 - imponible_sasha * 0.80
costo_empresa_sasha = imponible_sasha + aportes_empleador_sasha + provisiones_sasha + retiro_sasha

# 3. Médico 2 (Tarde/Sábado) - 30 hrs Part-Time
sueldo_base_med2 = 395395
gratificacion_med2 = sueldo_base_med2 * 0.25
imponible_med2 = sueldo_base_med2 + gratificacion_med2
aportes_empleador_med2 = imponible_med2 * 0.0487
provisiones_med2 = imponible_med2 * 0.1249
comision_estimada_med2 = 300000 # Estimado para presupuesto
costo_empresa_med2 = imponible_med2 + aportes_empleador_med2 + provisiones_med2 + comision_estimada_med2
liquido_med2 = (imponible_med2 * 0.80) + comision_estimada_med2

# 4. Médico 3 (Fines de semana) - Boleta Honorarios
# Asumimos 60 horas al mes a \.000 (Monto Bruto pagado por clínica)
valor_hora_med3 = 5000
horas_med3 = 60
costo_empresa_med3 = valor_hora_med3 * horas_med3
liquido_med3 = costo_empresa_med3 * (1 - 0.1375)

# 5. Técnicos (Llamados según necesidad) - Boleta Honorarios
# Asumimos 60 horas al mes a \.000 (Monto Bruto pagado por clínica)
valor_hora_tec = 3000
horas_tec = 60
costo_empresa_tec = valor_hora_tec * horas_tec
liquido_tec = costo_empresa_tec * (1 - 0.1375)

# 6. Recepcionista 2 - 40 hrs
sueldo_base_recep2 = 553553
gratificacion_recep2 = sueldo_base_recep2 * 0.25
imponible_recep2 = sueldo_base_recep2 + gratificacion_recep2
aportes_empleador_recep2 = imponible_recep2 * 0.0487
provisiones_recep2 = imponible_recep2 * 0.1249
costo_empresa_recep2 = imponible_recep2 + aportes_empleador_recep2 + provisiones_recep2
liquido_recep2 = imponible_recep2 * 0.80

rrhh_data = {
    'Cargo': [
        'Daniela (Socia Directora Médica)', 
        'Sasha (Socia Recepción)', 
        'Médico 2 (Tarde/Sábado)', 
        'Médico 3 (Fines de semana)', 
        'Técnicos (Diurno/Nocturno)', 
        'Recepcionista 2'
    ],
    'Estructura Contractual': [
        'Contrato Trabajo + Retiro', 
        'Contrato Trabajo + Retiro', 
        'Contrato Trabajo (Part-Time)', 
        'Boleta Honorarios', 
        'Boleta Honorarios', 
        'Contrato Trabajo (Full-Time)'
    ],
    'Sueldo Base (Base Cálculo)': [sueldo_base_dani, sueldo_base_sasha, sueldo_base_med2, 0, 0, sueldo_base_recep2],
    'Retiro de Socia (Libre Imp.)': [retiro_dani, retiro_sasha, 0, 0, 0, 0],
    'Ingreso Líquido (Bolsillo)': [1700000, 800000, liquido_med2, liquido_med3, liquido_tec, liquido_recep2],
    'Costo Empresa Mensual': [costo_empresa_dani, costo_empresa_sasha, costo_empresa_med2, costo_empresa_med3, costo_empresa_tec, costo_empresa_recep2]
}
df_rrhh = pd.DataFrame(rrhh_data)

'''

content = re.sub(r'# 2\. RRHH \(Fase 1 con Carga Legal y Provisiones\).*?(?=# 3\. CAPEX DETALLADO)', new_rrhh_content, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
