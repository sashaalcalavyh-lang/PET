import plotly.graph_objects as go
import plotly.express as px
import sqlite3
import pandas as pd
import os

# Configuracion
out_dir = r"d:\Data Science\GitHub\PET\Analisis_Administracion_Anterior_vs_Nueva"

# 1. Grafico de Punto de Equilibrio (Breakeven)
# Comparando Admin Anterior (Costos 7.5M, Ticket 53k) vs Admin Nueva (Costos 3.98M, Ticket 42k)
fig1 = go.Figure()
fig1.add_trace(go.Bar(
    x=['Admin Anterior (Costos $7.5M)', 'Nueva Admin (Costos $3.98M)'],
    y=[140, 95], # 7500000 / 53754 ~= 140 pacientes vs 3980000 / 42000 ~= 95 pacientes
    marker_color=['#ef4444', '#10b981'],
    text=[140, 95],
    textposition='auto',
))
fig1.update_layout(
    title='Punto de Equilibrio: Pacientes Necesarios para no quebrar (Mes)',
    yaxis_title='Cantidad de Pacientes',
    template='plotly_white'
)
fig1.write_html(os.path.join(out_dir, "1_punto_equilibrio.html"))

# 2. Estructura del Ticket Histórico (Consulta vs Upsell)
# Lead Magnet $15k + Upsell 27k = 42k Total
fig2 = go.Figure(data=[
    go.Pie(labels=['Consulta Base / Lead Magnet', 'Upsell Real (Farmacia/Exámenes)'],
           values=[15000, 26988],
           hole=.4,
           marker_colors=['#3b82f6', '#f59e0b'])
])
fig2.update_layout(
    title='Estructura de Ticket Promedio Esperado ($41.988 CLP)',
    annotations=[dict(text='Ticket', x=0.5, y=0.5, font_size=20, showarrow=False)]
)
fig2.write_html(os.path.join(out_dir, "2_estructura_ticket_upsell.html"))

# 3. Rentabilidad (Ingresos vs Costos Fijos)
# Admin anterior: 158 pacientes * 53k = 8.5M Ingresos. Costos 7.5M. Utilidad Bruta 1M.
# Admin Nueva (Conservadora 110 pacientes): 110 * 42k = 4.62M Ingresos. Costos 3.98M. Utilidad Bruta 640k.
fig3 = go.Figure(data=[
    go.Bar(name='Ingresos', x=['Admin Anterior', 'Nueva Admin (Conservador)'], y=[8500000, 4620000], marker_color='#3b82f6'),
    go.Bar(name='Costos Fijos', x=['Admin Anterior', 'Nueva Admin (Conservador)'], y=[7500000, 3980000], marker_color='#ef4444'),
    go.Bar(name='Utilidad Neta (Aprox)', x=['Admin Anterior', 'Nueva Admin (Conservador)'], y=[1000000, 640000], marker_color='#10b981')
])
# Change the bar mode
fig3.update_layout(barmode='group', title='Comparativo de Rentabilidad (CLP)', template='plotly_white')
fig3.write_html(os.path.join(out_dir, "3_rentabilidad_esperada.html"))

print("Gráficos interactivos HTML generados con éxito.")
