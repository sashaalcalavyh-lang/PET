import pandas as pd
import numpy as np

# 1. OPEX
opex_data = {
    'Ítem (OPEX)': ['Arriendo Local', 'Servicios Básicos (Luz/Agua)', 'REAS (Retiro Cortopunzantes/Biológicos)', 'Software e Internet', 'Marketing Mantención (Ads)', 'Insumos Aseo y Limpieza Clínica', 'Honorarios Contador Mensual'],
    'Costo Mensual (CLP)': [1000000, 250000, 80000, 150000, 500000, 80000, 100000],
    'Observaciones': ['Acuerdo progresivo en mente.', 'Autoclave consume alto amperaje', 'Empresa certificada viene mensual (Obligatorio)', 'Caja y agenda', 'Mantención competitiva', 'Ajustado a consumo realista', 'Declaración F29 mensual y libros']
}
df_opex = pd.DataFrame(opex_data)

# 2. RRHH (Fase 1 con Carga Legal y Provisiones)
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
horas_med3 = 0  # 100% Variable (Solo si se abre FDS)
costo_empresa_med3 = valor_hora_med3 * horas_med3
liquido_med3 = costo_empresa_med3 * (1 - 0.1375)

# 5. Técnicos (Llamados según necesidad) - Boleta Honorarios
# Asumimos 60 horas al mes a \.000 (Monto Bruto pagado por clínica)
valor_hora_tec = 3000
horas_tec = 0  # 100% Variable (Solo si hay hospitalizados)
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
    'Costo Empresa Fijo Mensual': [costo_empresa_dani, costo_empresa_sasha, costo_empresa_med2, costo_empresa_med3, costo_empresa_tec, costo_empresa_recep2]
}
df_rrhh = pd.DataFrame(rrhh_data)

# 3. CAPEX DETALLADO (Sincronizado)
capex_detalle_data = [
    ['Recepción', 'Mesón', 1, 149990, 0, 149990],
    ['Recepción', 'Computador', 1, 300000, 0, 300000],
    ['Recepción', 'POINT mercado pago', 1, 50000, 9500, 59500],
    ['Recepción', 'Teléfono', 1, 90000, 0, 90000],
    ['Recepción', 'Impresora', 1, 100000, 0, 100000],
    ['Recepción', 'Silla computador', 1, 32990, 0, 32990],
    ['Recepción', 'Sillas espera x4', 1, 99990, 0, 99990],
    ['Consulta', 'Mesa procedimiento', 1, 89700, 0, 89700],
    ['Consulta', 'Refrigerador', 1, 39990, 0, 39990],
    ['Consulta', 'Pesa grande', 1, 210000, 0, 210000],
    ['Consulta', 'Pesa pequeña', 1, 15000, 0, 15000],
    ['Consulta', 'Pesa gramera', 1, 15000, 0, 15000],
    ['Consulta', 'Mueble', 1, 100000, 0, 100000],
    ['Consulta', 'Escritorio', 1, 38990, 0, 38990],
    ['Consulta', 'Silla', 1, 32990, 0, 32990],
    ['Pabellón', 'Máquina anestesia', 1, 3570000, 678300, 4248300],
    ['Pabellón', 'Mesa quirúrgica', 1, 1420000, 269800, 1689800],
    ['Pabellón', 'Concentrador oxígeno', 1, 752952, 143061, 896013],
    ['Pabellón', 'Mesa mayo', 1, 68500, 0, 68500],
    ['Pabellón', 'Mueble', 1, 100000, 0, 100000],
    ['Pabellón', 'Lámpara cirugía', 2, 98980, 0, 98980],
    ['Pabellón', 'Autoclave', 1, 110960, 0, 110960],
    ['Hospital', 'Canil estación UCI/6 mod', 1, 3990000, 758100, 4748100],
    ['Hospital', 'Mesa procedimiento', 1, 89700, 0, 89700],
    ['Hospital', 'Mueble almacenamiento', 1, 100000, 0, 100000],
    ['Hospital', 'Porta suero', 1, 81990, 15578, 97568],
    ['Costos Iniciales', 'Arriendo Fraccionado (Mes 1)', 1, 1000000, 0, 1000000],
    ['Costos Iniciales', 'Constitucion de soc y patente', 1, 200000, 0, 200000],
    ['Costos Iniciales', 'Honorarios Contador (Config inicial)', 1, 100000, 0, 100000],
    ['Costos Iniciales', 'Sueldo Sasha (Mes 1 Sincronizado)', 1, costo_empresa_sasha, 0, costo_empresa_sasha],
    ['Costos Iniciales', 'Sueldo Dani (Mes 1 Sincronizado)', 1, costo_empresa_dani, 0, costo_empresa_dani],
    ['Costos Iniciales', 'Sueldo Médico 2 (Mes 1 Sincronizado)', 1, costo_empresa_med2, 0, costo_empresa_med2],
    ['Costos Iniciales', 'Sueldo Médico 3 (Mes 1 Sincronizado)', 1, costo_empresa_med3, 0, costo_empresa_med3],
    ['Costos Iniciales', 'Sueldo Técnicos (Mes 1 Sincronizado)', 1, costo_empresa_tec, 0, costo_empresa_tec],
    ['Costos Iniciales', 'Sueldo Recepcionista 2 (Mes 1 Sincronizado)', 1, costo_empresa_recep2, 0, costo_empresa_recep2],
    ['Costos Iniciales', 'Internet', 1, 27000, 0, 27000],
    ['Costos Iniciales', 'Insumos Hospital y Consulta', 1, 1200000, 228000, 1428000],
    ['Costos Iniciales', 'Camara de seguridad x4', 1, 200000, 38000, 238000],
    ['Costos Iniciales', 'Software + stack', 1, 300000, 57000, 357000],
    ['Costos Iniciales', 'SEO Inicial', 1, 1000000, 0, 1000000]
]
df_capex_detallado = pd.DataFrame(capex_detalle_data, columns=['Área', 'Ítem', 'Cantidad', 'Monto Neto (CLP)', 'IVA (CLP)', 'Monto Total (CLP)'])
total_capex_fisico = df_capex_detallado['Monto Total (CLP)'].sum()

total_opex = df_opex['Costo Mensual (CLP)'].sum()
total_rrhh_fijo = df_rrhh['Costo Empresa Fijo Mensual'].sum()
costo_fijo_mensual = total_opex + total_rrhh_fijo
ingreso_peor_mes = 4500000
margen_bruto = ingreso_peor_mes * 0.50 
deficit_invierno = costo_fijo_mensual - margen_bruto
fondo_emergencia = costo_fijo_mensual * 6

df_fondo = pd.DataFrame([['Caja Seguridad', 'FONDO DE EMERGENCIA (6 Meses Costos Fijos)', 1, fondo_emergencia, 0, fondo_emergencia]], columns=['Área', 'Ítem', 'Cantidad', 'Monto Neto (CLP)', 'IVA (CLP)', 'Monto Total (CLP)'])
df_capex_completo = pd.concat([df_capex_detallado, df_fondo], ignore_index=True)

# 4. ESCALAMIENTO Y PROVISIONES (Fase 2) - Limpio porque provisiones pasaron a Fase 1
escalamiento_data = {
    'Categoría': [
        'Sueldo Mercado (Sasha - Gerencia/Admin)', 
        'Sueldo Mercado (Daniela - Director Médico/Cirujano)',
        'Sueldo Mercado (Veterinario Clínico Turno)',
        'Comp & Ben: Comisiones Variables',
        'C.A.C. y Retención (Framework Hormozi)',
        'Reserva Licencias Médicas (Reemplazos)',
        'Impuestos Mensuales (IVA y PPM - F29)',
        'Impuesto a la Renta Anual (F22)'
    ],
    'Monto Estimado': [
        '$1.800.000 a $2.500.000',
        '$2.500.000 a $3.500.000',
        '$1.200.000 (Base + Variable)',
        '20% a 30% sobre procedimientos / ventas',
        'Costo Adquisición > LTV',
        'Fondo rotativo: $1.000.000',
        'Flujo de caja neutral (retiene de clientes)',
        '10% al 27% sobre utilidades anuales'
    ],
    'Ley Laboral / Justificación': [
        'Sueldo base de mercado para una clínica consolidada.',
        'Cirujanos especialistas con rol de jefatura en Valparaíso.',
        'Sueldo escalable: Base bajo + comisiones para proteger la caja.',
        'Hormozi / Comp & Ben: Alinear los incentivos del veterinario.',
        'Hormozi: Dejar de gastar ciego en Ads, medir costo de adquisición.',
        'FONASA paga el sueldo del enfermo, tú pagas el reemplazo.',
        'El IVA lo paga el cliente final (19%).',
        'Se paga en abril sobre utilidades.'
    ]
}
df_escalamiento = pd.DataFrame(escalamiento_data)

# 5. Resumen
resumen_data = {
    'Métrica Financiera': [
        'Gastos Operativos (OPEX Mensual Inicial)',
        'Nómina y Retiros Societarios (Inc. Provisiones)',
        'Egresos Fijos Totales (Punto de Quiebre)', 
        'Margen Bruto Límite Histórico (Peor Mes 50% COGS)', 
        'Déficit Real Estimado en Invierno',
        'Inversión Inicial Tangible (CAPEX Físico Sincerado)',
        'Fondo de Emergencia (Salvavidas 6 meses)',
        'Inversión Total Requerida'
    ],
    'Valor (CLP)': [
        total_opex,
        total_rrhh_fijo,
        costo_fijo_mensual, 
        margen_bruto, 
        deficit_invierno, 
        total_capex_fisico,
        fondo_emergencia,
        total_capex_fisico + fondo_emergencia
    ]
}
df_resumen = pd.DataFrame(resumen_data)

excel_path = 'd:/Data Science/GitHub/PET - v1/Estudios/Presupuestos/presupuesto_clinica_mejorado_13.xlsx'
with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
    df_resumen.to_excel(writer, sheet_name='RESUMEN EJECUTIVO', index=False)
    df_capex_completo.to_excel(writer, sheet_name='INVERSIÓN DETALLADA', index=False)
    df_opex.to_excel(writer, sheet_name='OPEX (Costos Fijos)', index=False)
    df_rrhh.to_excel(writer, sheet_name='NÓMINA INICIAL (Fase 1)', index=False)
    df_escalamiento.to_excel(writer, sheet_name='ESCALAMIENTO Y IMPUESTOS', index=False)

print('Excel V13 generado con exito (Sincronizacion CAPEX y Provisiones)')
