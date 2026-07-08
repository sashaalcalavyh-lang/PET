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
sueldo_minimo = 553553

# Para Socias (Sueldo Patronal)
costo_patronal = sueldo_minimo * 1.20 
costo_empresa_sasha = costo_patronal + (800000 - sueldo_minimo)
costo_empresa_dani = costo_patronal + (1200000 - sueldo_minimo)

# Para Técnico Fijo:
gratificacion_legal = sueldo_minimo * 0.25
imponible_tecnico = sueldo_minimo + gratificacion_legal
aportes_empleador = imponible_tecnico * 0.0487 # SIS + AFC + Mutual
provisiones_tecnico = imponible_tecnico * 0.1249 # Vacaciones (4.16%) + IAS (8.33%)
costo_empresa_tecnico = imponible_tecnico + aportes_empleador + provisiones_tecnico

# Para Boleta
retencion_boleta = 1.1375
costo_empresa_boleta = 300000 * retencion_boleta

rrhh_data = {
    'Cargo': ['Sasha (Socia Administradora)', 'Daniela (Socia Jefe Médico)', 'Técnico Veterinario (Fijo)', 'Técnico (Boleta/Part-Time)'],
    'Estructura Contractual': ['Sueldo Patronal + Retiro', 'Sueldo Patronal + Retiro', 'Contrato Fijo (Con Aportes + Provisiones Ahorro)', 'Prestación de Servicios'],
    'Sueldo Base (Base Cálculo)': [sueldo_minimo, sueldo_minimo, sueldo_minimo, 0],
    'Retiro Mensual (Libre Imp.)': [800000 - sueldo_minimo, 1200000 - sueldo_minimo, 0, 0],
    'Ingreso Líquido Aprox (Bolsillo)': [800000, 1200000, imponible_tecnico * 0.80, 300000],
    'Costo Empresa Fijo Mensual': [costo_empresa_sasha, costo_empresa_dani, costo_empresa_tecnico, costo_empresa_boleta]
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
    ['Costos Iniciales', 'Sueldo Técnico Fijo (Mes 1 Sincronizado)', 1, costo_empresa_tecnico, 0, costo_empresa_tecnico],
    ['Costos Iniciales', 'Sueldo Técnico Boleta (Mes 1 Sincronizado)', 1, costo_empresa_boleta, 0, costo_empresa_boleta],
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

excel_path = 'd:/Data Science/GitHub/PET - v1/presupuesto_clinica_mejorado_13.xlsx'
with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
    df_resumen.to_excel(writer, sheet_name='RESUMEN EJECUTIVO', index=False)
    df_capex_completo.to_excel(writer, sheet_name='INVERSIÓN DETALLADA', index=False)
    df_opex.to_excel(writer, sheet_name='OPEX (Costos Fijos)', index=False)
    df_rrhh.to_excel(writer, sheet_name='NÓMINA INICIAL (Fase 1)', index=False)
    df_escalamiento.to_excel(writer, sheet_name='ESCALAMIENTO Y IMPUESTOS', index=False)

print('Excel V13 generado con exito (Sincronizacion CAPEX y Provisiones)')
