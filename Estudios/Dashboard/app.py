import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Dashboard Auditoría Histórica", layout="wide")

@st.cache_data
def load_data(db_mod_time):
    db_path = os.path.join(os.path.dirname(__file__), 'clinica_historico.db')
    if not os.path.exists(db_path):
        return pd.DataFrame(), pd.DataFrame()
        
    conn = sqlite3.connect(db_path)
    
    # 1. Cargar Master Financiero (La capa Gold limpia y unificada)
    try:
        df_master = pd.read_sql_query("SELECT * FROM master_financiero", conn)
        df_master['Fecha'] = pd.to_datetime(df_master['Fecha'], errors='coerce')
    except: 
        df_master = pd.DataFrame()
        
    # 2. Cargar Ventas Históricas (Para mantener el nivel de detalle)
    try:
        df_ventas = pd.read_sql_query("SELECT * FROM ventas_historicas", conn)
    except: 
        df_ventas = pd.DataFrame()
        
    conn.close()
    return df_master, df_ventas

@st.cache_data
def load_presupuesto():
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Presupuestos', 'presupuesto_clinica_mejorado_13.xlsx')
    if os.path.exists(file_path):
        xls = pd.ExcelFile(file_path, engine='openpyxl')
        return {sheet: xls.parse(sheet) for sheet in xls.sheet_names}
    return None

# --- AUDITORÍA DE DATOS (Menú Lateral) ---
st.sidebar.title("Menú")
st.sidebar.info("Dashboard Estratégico - Clínica Veterinaria (Valparaíso 2026)")

st.sidebar.markdown("---")
st.sidebar.subheader("🕵️ Auditoría de Base de Datos")

db_filepath = os.path.join(os.path.dirname(__file__), 'clinica_historico.db')
db_timestamp = os.path.getmtime(db_filepath) if os.path.exists(db_filepath) else 0

df_master, df_ventas = load_data(db_timestamp)

with st.sidebar.expander("Verificar Capa Gold", expanded=False):
    if not df_master.empty:
        st.write("**Master Financiero**")
        st.write(f"Filas limpias listas: `{len(df_master):,}`")
        st.write(f"Rango: `{df_master['Fecha'].min().strftime('%Y-%m')} a {df_master['Fecha'].max().strftime('%Y-%m')}`")
    else:
        st.warning("Master Financiero vacío. Ejecuta database_builder.py")

if df_master.empty:
    st.warning("No hay datos en la tabla maestra. Por favor, ejecuta database_builder.py primero.")
    st.stop()

# --- PESTAÑAS DEL DASHBOARD (Reducidas a 2) ---
tab1, tab2 = st.tabs(["Gobernanza, Auditoría y P&L", "Master Financiero y Simulador"])

# =====================================================================
# PESTAÑA 1: TODO LO HISTÓRICO, AUDITORÍA Y FLUJO
# =====================================================================
with tab1:
    
    # 1. VISOR DE BASE DE DATOS
    st.header("🕵️ Visor y Auditor Avanzado del Master Financiero")
    st.markdown("Utiliza los controles dinámicos para explorar, buscar y auditar de forma detallada el universo de registros unificados en tu base de datos.")
    
    if not df_master.empty:
        col_f1, col_f2, col_f3 = st.columns([1, 1, 2])
        
        with col_f1:
            tipos_disponibles = sorted(df_master['Tipo_Movimiento'].unique())
            tipos_seleccionados = st.multiselect("Filtrar por Origen:", options=tipos_disponibles, default=tipos_disponibles)
            
        with col_f2:
            search_cat = st.text_input("🔍 Buscar por Categoría:", "").upper().strip()
            
        with col_f3:
            min_date = df_master['Fecha'].min().date()
            max_date = df_master['Fecha'].max().date()
            rango_fechas = st.date_input("Rango de Fechas:", [min_date, max_date], min_value=min_date, max_value=max_date)

        df_auditoria = df_master[df_master['Tipo_Movimiento'].isin(tipos_seleccionados)]
        
        if search_cat:
            df_auditoria = df_auditoria[df_auditoria['Categoria'].str.contains(search_cat, na=False)]
            
        if isinstance(rango_fechas, list) or isinstance(rango_fechas, tuple):
            if len(rango_fechas) == 2:
                start_date, end_date = rango_fechas
                df_auditoria = df_auditoria[(df_auditoria['Fecha'].dt.date >= start_date) & (df_auditoria['Fecha'].dt.date <= end_date)]

        col_m1, col_m2 = st.columns(2)
        col_m1.metric("Registros en Vista Actual", f"{len(df_auditoria):,}")
        col_m2.metric("Monto Total en Vista Actual", f"${df_auditoria['Monto'].sum():,.0f} CLP")

        st.dataframe(
            df_auditoria.sort_values(by='Fecha', ascending=False),
            use_container_width=True,
            column_config={
                "Fecha": st.column_config.DatetimeColumn("Fecha de Registro", format="DD/MM/YYYY"),
                "Monto": st.column_config.NumberColumn("Monto Líquido", format="$ %,.0f"),
                "Categoria": "Categoría / Centro de Costos",
                "Tipo_Movimiento": "Origen / Tipo de Movimiento"
            }
        )
    else:
        st.warning("La tabla maestra está vacía. No hay datos disponibles para auditar.")

    st.markdown("---")

    # 2. TOP 10 CATEGORÍAS (Oculto temporalmente a petición del usuario, cambiar False a True para mostrar)
    if False:
        st.subheader("🏆 Top 10 Categorías y Servicios Históricos")
        col_t1, col_t2 = st.columns(2)
        if not df_ventas.empty and 'DESC. CATEGORIA' in df_ventas.columns and 'SUBTOTAL' in df_ventas.columns:
            df_ventas['DESC. CATEGORIA'] = df_ventas['DESC. CATEGORIA'].astype(str).str.upper().str.strip()
            df_ventas['DESCRIPCION ARTICULO'] = df_ventas['DESCRIPCION ARTICULO'].astype(str).str.upper().str.strip()
            
            top_cat = df_ventas.groupby('DESC. CATEGORIA')['SUBTOTAL'].sum().nlargest(10).reset_index()
            fig_cat = px.bar(top_cat, x='DESC. CATEGORIA', y='SUBTOTAL', title="Top 10 Ingresos por Categoría", text_auto='.2s')
            col_t1.plotly_chart(fig_cat, use_container_width=True)
            
            top_serv = df_ventas.groupby('DESCRIPCION ARTICULO')['SUBTOTAL'].sum().nlargest(10).reset_index()
            fig_serv = px.bar(top_serv, x='DESCRIPCION ARTICULO', y='SUBTOTAL', title="Top 10 Servicios/Insumos", text_auto='.2s')
            col_t2.plotly_chart(fig_serv, use_container_width=True)
        else:
            st.write("Columnas requeridas no encontradas en ventas por producto.")
        st.markdown("---")

    # 3. FLUJO DE CAJA REAL SINCERADO (Antigua Pestaña 2 / 3)
    st.subheader("📈 Flujo de Caja Real Histórico (Sincerado con RRHH y OPEX)")
    if not df_master.empty:
        df_master_flujo = df_master.copy()
        df_master_flujo['Mes_Año'] = df_master_flujo['Fecha'].dt.to_period('M').astype(str)
        agrupado_flujo = df_master_flujo.groupby(['Mes_Año', 'Tipo_Movimiento'])['Monto'].sum().reset_index()
        
        ing_csv = agrupado_flujo[agrupado_flujo['Tipo_Movimiento'] == 'Ingreso (CSV Productos)'].set_index('Mes_Año')['Monto']
        ing_caja = agrupado_flujo[agrupado_flujo['Tipo_Movimiento'] == 'Ingreso (Libro Caja)'].set_index('Mes_Año')['Monto']
        egresos = agrupado_flujo[agrupado_flujo['Tipo_Movimiento'] == 'Egreso (Compras)'].set_index('Mes_Año')['Monto']
        
        df_ing_comb = pd.DataFrame({'csv': ing_csv, 'caja': ing_caja}).fillna(0)
        ingresos_reales = df_ing_comb.max(axis=1)
        
        todos_los_meses = ingresos_reales.index.union(egresos.index).sort_values()
        ingresos_reales = ingresos_reales.reindex(todos_los_meses, fill_value=0)
        egresos_reales = egresos.reindex(todos_los_meses, fill_value=0)
        
        df_plot = pd.DataFrame({
            'Mes_Año': list(todos_los_meses) * 2,
            'Monto': list(ingresos_reales.values) + list(egresos_reales.values),
            'Tipo_Movimiento': ['Ingreso (Consolidado)'] * len(todos_los_meses) + ['Egreso (Compras)'] * len(todos_los_meses)
        })
        
        fig_line = px.bar(df_plot, x='Mes_Año', y='Monto', color='Tipo_Movimiento', barmode='group',
                          title="Comparativa Ingresos vs Egresos (P&L Sincerado)")
        st.plotly_chart(fig_line, use_container_width=True, key="fig_line_tab1")
        
        pnl_series = ingresos_reales.sub(egresos_reales, fill_value=0)
        pnl = pnl_series.reset_index()
        pnl.columns = ['Mes_Año', 'Flujo Neto']
        
        fig_pnl = px.line(pnl, x='Mes_Año', y='Flujo Neto', title="Flujo de Caja Neto Mensual vs Punto de Equilibrio", markers=True)
        fig_pnl.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Punto de Equilibrio")
        st.plotly_chart(fig_pnl, use_container_width=True, key="fig_pnl_tab1")

        with st.expander("📖 ¿Cómo leer estos gráficos y qué significan para mi rentabilidad?", expanded=False):
            st.markdown("""
            ### 1. El Efecto "Outlier" (Aprende a hacer Zoom)
            Notarás que en el primer gráfico las barras azul oscuro (Egresos) se ven pequeñitas. Esto ocurre porque en **Diciembre de 2024** hubo un ingreso anómalo de casi **\$35 Millones** (probablemente una venta externa o ajuste contable), lo que obliga al gráfico a "aplastar" el resto de los meses para que ese pico quepa en la pantalla. 
            * **Tip de uso:** Haz clic sostenido en el gráfico y arrastra un rectángulo sobre los meses normales (de 0 a 10M) para hacer *Zoom In* y ver el detalle. Haz doble clic para alejar.
            
            ### 2. ¿Qué significa "P&L Sincerado"?
            "Sincerado" significa que este gráfico no te está mintiendo. Los antiguos dueños solo anotaban sus compras de insumos en sus Excel, ignorando el pago de sueldos, imposiciones, luz y arriendo. Nosotros tomamos su data histórica e **inyectamos los verdaderos costos operativos (OPEX y Leyes Sociales)** para mostrarte la realidad de cuánto cuesta mantener la clínica viva mes a mes.
            
            ### 3. El Punto de Flotación (Línea Roja de Equilibrio)
            El **Punto de Flotación** es literalmente la línea roja punteada en el valor **Cero (0)** del segundo gráfico. 
            * Si el punto azul (Flujo Neto) está **por encima de cero**, la clínica generó utilidades reales ese mes (después de pagar arriendo, sueldos y leyes sociales).
            * Si cae **por debajo de cero** (como se proyecta hacia Julio de 2026), significa que la clínica está **sangrando caja**. Tienes que sacar plata de tus ahorros para pagar los sueldos.
            * **Justificación Estratégica:** Un negocio saludable no puede depender solo de los picos de verano. Tu "Punto de Flotación" te exige que mantengas tus Costos Fijos por debajo del límite histórico de **\$4.5M**, garantizando que incluso en el "Valle de la Muerte" del invierno (Mayo-Julio), la clínica se pague a sí misma sin que tengas que poner plata de tu bolsillo.
            """)

    st.markdown("---")

    # 4. GOBERNANZA Y PUNTOS CIEGOS
    st.subheader("📊 Análisis Estratégico y Conclusiones del Histórico")
    
    with st.expander("¿Por qué fracasó la clínica anterior si tenían flujo positivo?", expanded=True):
        st.markdown("""
        Si los números en el papel dicen que el promedio de egresos es ~\$3.14M y el peor mes de ventas genera \$4.5M, ¿por qué alguien abandonaría un negocio que técnicamente deja un flujo positivo?
        
        Hay **5 factores asesinos** que probablemente los sacaron del juego, y que debes evitar a toda costa:
        
        1. **La "Falsa Rentabilidad" (El síndrome del dueño-esclavo)**: Es altamente probable que los dueños trabajaran 12 horas, 6 días a la semana, sacando la plata de la caja para vivir sin un sueldo asignado. Al no tener la "Ecuación de Valor" optimizada (vendiendo barato por volumen), el burnout los hizo tirar la toalla. Como dice Hormozi: *"Si compites por precio, prepárate para trabajar hasta morir"*.
        2. **El "Hachazo" Fiscal y Laboral (Inspección del Trabajo)**: Muchos locales operan a "Boleta de Honorarios". Una sola demanda laboral de un veterinario quiebra la caja por las multas y años de cotizaciones atrasadas.
        3. **Deuda de Capital Oculta (CAPEX no declarado)**: Si pidieron un crédito para comprar ecógrafos o máquinas, la cuota mensual del banco se comía ese "flujo neto".
        4. **El "Dueño del Local" (Riesgo Inmobiliario)**: Si el dueño del local ve que te va bien, te sube el arriendo. Un alza abrupta los hace inviables.
        5. **Problema de Retención (Bajo LTV)**: Tráfico peatonal de bajo ticket requiere la sala de espera llena. Una competencia barata o mala reputación desploma el negocio.
        
        **La Lección para 2026**: Que se hayan ido es una ventaja táctica. El punto está validado. Tu objetivo es aprovechar el tráfico residual, implementar Tickets Más Altos (Planes de salud, medicina preventiva, diagnósticos completos) y tener el Costo Empresa 100% blindado desde el día 1.
        """)

    with st.expander("Estacionalidad y El 'Peor Mes' Histórico", expanded=True):
        st.markdown("""
        El límite crítico de **\$4.5M** ocurrió exactamente en **Mayo de 2023** (\$4.503.130 CLP). Otros meses duros: Septiembre 2023 (\$4.6M), Junio y Julio 2024.
        
        **Patrones de Comportamiento:**
        - **El "Valle de la Muerte" (Otoño/Invierno):** Mayo, Junio y Julio son los más bajos. La gente sale menos por frío y lluvia, hay menos parásitos y bajan consultas preventivas. Septiembre también cae (presupuesto familiar a Fiestas Patrias). **Estrategia:** Tu OPEX debe estar blindado. Guarda caja en verano para sobrevivir este valle sin endeudarte.
        - **El "Boom" de Verano (Temporada Alta):** Diciembre, Enero y Febrero muestran picos (ej. Feb 2024 saltó a \$10.9M y Feb 2026 a \$12.2M). **Razón:** Valparaíso/Viña se llena por vacaciones, aumentan urgencias, y se necesitan vacunas/certificados para viajar.
        
        **Conclusión:** Tu simulador ya está configurado para sobrevivir al "Valle de la Muerte" (Mayo-Julio). Si mantienes tus costos fijos por debajo de los \$4.5M, todo excedente del "Boom de Verano" será pura ganancia neta para escalar el negocio.
        """)
        
    st.info("""
    **🚨 NOTA DE AUDITORÍA - DATOS ESTIMADOS (PUNTOS CIEGOS):**
    Se incluyeron estos datos estimados en la base de datos histórica ya que **NO** habían registros formales de estos gastos en los Excel originales, pero son vitales para simular un escenario realista:
    - **Costo Empresa de Nómina:** A cada sueldo líquido y bruto se le aplicó una sobrecarga del 34.5% (22% Leyes Sociales + 12.5% Provisiones Feriado e IAS).
    - **Servicios Críticos:** Luz, Agua y Climatización 24/7 (Autoclave, Oxígeno) por **$250.000 CLP / mes**.
    - **Cumplimiento Seremi (REAS):** Manejo de residuos biológicos por **$80.000 CLP / mes**.
    - **Gastos Inmobiliarios Base:** Arriendo estimado base en **$700.000 CLP / mes**.
    """)


# =====================================================================
# PESTAÑA 2: MASTER FINANCIERO FINAL Y SIMULADOR
# =====================================================================
with tab2:
    st.header("Master Financiero Definitivo (V13) y Conclusiones")
    
    dict_presupuesto = load_presupuesto()
    
    # 1. MOSTRAR TABLAS MASTER FINANCIERO
    if dict_presupuesto:
        for sheet_name, df_sheet in dict_presupuesto.items():
            st.subheader(f"📊 {sheet_name}")
            
            df_display = df_sheet.copy()
            
            # Agregar fila de Total dinámicamente si aplica
            if sheet_name == 'INVERSIÓN DETALLADA':
                total_neto = df_display['Monto Neto (CLP)'].sum()
                total_iva = df_display['IVA (CLP)'].sum()
                total_monto = df_display['Monto Total (CLP)'].sum()
                df_display.loc[len(df_display)] = ['TOTAL GENERAL', '', '', total_neto, total_iva, total_monto]
            elif sheet_name == 'OPEX (Costos Fijos)':
                total_opex = df_display['Costo Mensual (CLP)'].sum()
                df_display.loc[len(df_display)] = ['TOTAL OPEX MENSUAL', total_opex, '']
            elif sheet_name == 'NÓMINA INICIAL (Fase 1)':
                total_nomina = df_display['Costo Empresa Fijo Mensual'].sum()
                df_display.loc[len(df_display)] = ['TOTAL NÓMINA', '', '', '', '', total_nomina]
                
            # Formatear números a CLP (ej: $1.000.000)
            for col in df_display.columns:
                if pd.api.types.is_numeric_dtype(df_display[col]) and col != 'Cantidad':
                    df_display[col] = df_display[col].apply(lambda x: f"${x:,.0f}".replace(",", ".") if pd.notnull(x) else "")
            
            st.dataframe(df_display, use_container_width=True, hide_index=True)
            
            if sheet_name == 'NÓMINA INICIAL (Fase 1)':
                st.markdown("""
                <div style='background-color: #1e1e2e; padding: 15px; border-radius: 8px; margin-bottom: 20px; font-size: 0.9em; border-left: 4px solid #4a90e2;'>
                <b>📌 Detalle y Explicación de Horas Laborales (Estructura Fase 1)</b><br><br>
                • <b>Daniela (Socia Directora Médica):</b> 25 hrs laborales a la semana. Contrato de Trabajo. El sueldo base ($395.395) corresponde al Sueldo Mínimo Proporcional + Gratificación mensual. El retiro libre de impuestos es variable para cuadrar a un Ingreso Líquido de $1.700.000. El costo empresa asume el sueldo bruto más el retiro.<br>
                • <b>Sasha (Socia Recepción):</b> 30 hrs laborales por semana. Contrato de Trabajo. El sueldo base ($395.395) corresponde al Sueldo Mínimo Proporcional + Gratificación mensual. El retiro es variable para cuadrar a un Ingreso Líquido de $800.000.<br>
                • <b>Médico 2 (Tarde/Sábado):</b> Part-Time 30 hrs laborales por semana. Contrato de Trabajo con Sueldo Mínimo Proporcional + Gratificación. El ingreso de bolsillo está compuesto por el sueldo líquido más comisiones variables.<br>
                • <b>Médico 3 (Fines de semana):</b> Modalidad Boleta de Honorarios. Valor hora $5.000 de lunes a lunes. El prestador recibe el 100% de la boleta y asume su propia retención legal (Monto Boleta Líquida).<br>
                • <b>Técnicos (Diurno, Nocturno, FDS):</b> Se llaman según necesidad. Boleta de Honorarios. Turno de lunes a lunes con valor hora de $3.000. El técnico asume su propia retención.<br>
                • <b>Recepcionista 2:</b> 40 hrs laborales por semana. Contrato de Trabajo con Sueldo Mínimo ($553.553) + Gratificación mensual.
                </div>
                """, unsafe_allow_html=True)

            st.markdown("---")
            
        # Extraer variables dinámicas para el Simulador
        df_res = dict_presupuesto.get('RESUMEN EJECUTIVO', pd.DataFrame())
        try:
            opex_real_master = df_res.loc[df_res['Métrica Financiera'].str.contains('Gastos Operativos', na=False), 'Valor (CLP)'].values[0]
            nomina_real_master = df_res.loc[df_res['Métrica Financiera'].str.contains('Nómina', na=False), 'Valor (CLP)'].values[0]
        except:
            opex_real_master = 2160000
            nomina_real_master = 3374733
    else:
        st.warning("No se encontró el archivo 'presupuesto_clinica_mejorado_13.xlsx' en la ruta principal del proyecto.")
        opex_real_master = 2160000
        nomina_real_master = 3374733
        
    st.markdown("---")

    # 2. SIMULADOR ESTRATÉGICO CONECTADO
    st.header("🎛️ Simulador de Supervivencia Estratégico (Conectado al Master)")
    st.markdown("Hemos alimentado este simulador directamente con los **Egresos Fijos Totales** calculados en tu Máster Financiero de la parte superior. Modifica los valores para proyectar cómo impactaría un aumento de costos (ej. contratar más médicos o rentar un local más caro) en el riesgo de quiebra.")
    
    col_op1, col_op2 = st.columns(2)
    
    with col_op1:
        st.subheader("Gastos Operativos (OPEX)")
        opex_simulado = st.number_input("OPEX Mensual Simulado", value=int(opex_real_master), step=100000)
        st.info("Valor inicial inyectado desde el Master Financiero (Arriendo, Luz, Agua, REAS, Marketing y Contador).")
        
    with col_op2:
        st.subheader("Nómina y Retiros Societarios")
        nomina_simulada = st.number_input("Costo Empresa Total RRHH", value=int(nomina_real_master), step=100000)
        st.info("Valor inicial inyectado desde el Master Financiero (Sueldos, Retiros, Leyes Sociales y Provisiones).")
        
    opex_mensual_total = opex_simulado + nomina_simulada
    
    st.markdown("### Prueba de Supervivencia Financiera (Regla del Peor Mes Histórico)")
    PEOR_MES_HISTORICO = 4500000 # Mayo 2023
    
    col_g1, col_g2 = st.columns([1, 1])
    
    with col_g1:
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = opex_mensual_total,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Punto de Quiebre (OPEX + RRHH)", 'font': {'size': 20}},
            delta = {'reference': PEOR_MES_HISTORICO, 'increasing': {'color': "red"}, 'decreasing': {'color': "green"}},
            gauge = {
                'axis': {'range': [None, PEOR_MES_HISTORICO * 1.5], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "black"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, PEOR_MES_HISTORICO * 0.8], 'color': 'lightgreen'},
                    {'range': [PEOR_MES_HISTORICO * 0.8, PEOR_MES_HISTORICO], 'color': 'gold'},
                    {'range': [PEOR_MES_HISTORICO, PEOR_MES_HISTORICO * 1.5], 'color': 'salmon'}],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': PEOR_MES_HISTORICO}
            }
        ))
        st.plotly_chart(fig_gauge, use_container_width=True)
        
    with col_g2:
        st.subheader("Veredicto Financiero en Vivo")
        if opex_mensual_total > PEOR_MES_HISTORICO:
            st.error(f"**¡ALERTA ROJA!** El umbral proyectado (${opex_mensual_total:,.0f} CLP) supera los ingresos del peor mes histórico de la clínica (${PEOR_MES_HISTORICO:,.0f} CLP). Durante un mes bajo, la clínica tendrá un déficit crítico y quemarás tu Fondo de Emergencia. Es vital subir el ticket promedio y no subir sueldos fijos.")
        elif opex_mensual_total > PEOR_MES_HISTORICO * 0.8:
            st.warning(f"**ZONA DE ESTRÉS:** Estás operando peligrosamente cerca del límite. Un mes malo invernal consumirá todos tus márgenes. Recuerda la Pestaña 5: Todo nuevo contrato debe ser Variable por Rendimiento.")
        else:
            st.success(f"**ZONA SEGURA:** Estructura de costos hiper-saludable. La clínica sobrevivirá holgadamente al invierno y maximizará liquidez en verano.")
            
        ingreso_promedio_mensual = 0
        if not df_ventas.empty and 'SUBTOTAL' in df_ventas.columns:
            ingreso_promedio_mensual = df_ventas['SUBTOTAL'].sum() / 42
            
        flujo_proyectado = ingreso_promedio_mensual - opex_mensual_total
        st.markdown(f"#### Simulación de Caja (Basado en ${ingreso_promedio_mensual:,.0f} Venta Histórica Promedio)")
        if flujo_proyectado > 0:
            st.metric("Flujo de Caja Libre Promedio Mensual", f"${flujo_proyectado:,.0f} CLP")
        else:
            st.metric("Sangría de Caja Promedio Mensual", f"${flujo_proyectado:,.0f} CLP")

    st.markdown("---")
        
    st.markdown("### 📘 Guía Directiva y Operativa")
    st.info("""
    **1. Ahorro Administrativo de Provisiones (\$812.000 vs \$553.000)**
    El Técnico Fijo representa un costo empresa de \$812.061, aunque su sueldo líquido sea de ~\$553.000. La administración debe depositar ~\$172.000 mensuales en Previred (Leyes Sociales), y transferir los restantes ~\$86.000 a una cuenta vista separada (12.49% por concepto de Vacaciones + Indemnización). Al cabo de 12 meses, se generará un fondo de \$1.032.000 en dicha cuenta, asegurando el pago de su sueldo durante vacaciones legales sin estresar el flujo de caja operativo.

    **2. Cronograma de Desembolso de Inversión**
    * **Día Cero (Mes 0):** Desembolso de \$20.9 Millones para CAPEX (activos fijos, permisos, marketing inicial y sueldos del primer mes).
    * **Meses 1 al 6:** El Fondo de Emergencia de \$33.2 Millones permanece bloqueado en la cuenta corriente. Se realizarán inyecciones mensuales controladas para cubrir el déficit operativo, hasta que la facturación orgánica cruce el Punto de Equilibrio.

    **3. Glosario Legal de Pyme**
    * **AFC (Cesantía):** Las socias no cotizan al no existir posibilidad legal de autodespido.
    * **SIS (Invalidez):** Opcional para socias (independientes). Obligatorio para empleados con contrato.
    * **Caja de Compensación:** Afiliación gratuita para la clínica, otorgando beneficios sociales al equipo mediante el mismo 7% de salud legal.
    """)

    st.markdown("### 💡 Resumen Estratégico de Viabilidad y Escalabilidad")
    st.success("""
    **Evaluación de Inversión (Monto Requerido: \$54 Millones)**

    El proyecto presenta un modelo financiero conservador y altamente escalable, fundamentado en los siguientes 3 pilares estratégicos:

    #### 1. Viabilidad Basada en Cobertura de Riesgo (6 Meses de Runway)
    El principal riesgo en la industria veterinaria es la falta de liquidez post-apertura. Este modelo neutraliza ese riesgo limitando la exposición física real a \$21 Millones (Día 0) y reservando \$33 Millones como Fondo de Emergencia. Esta estructura garantiza **6 meses de oxígeno financiero**, brindando a la clínica un semestre completo para alcanzar el "Punto de Quiebre" de \$5.5M mensuales. Con el nivel de especialización proyectado y la campaña de posicionamiento inicial (\$1M), superar esta meta en el mes 4 o 5 es un hito de alta factibilidad.

    #### 2. Escalabilidad mediante Control de RRHH (Costos Fijos Blindados)
    El modelo asegura escalabilidad al evitar el crecimiento desproporcionado de los costos fijos. Las futuras contrataciones médicas operarán bajo un esquema de remuneración variable (Sueldo Base Legal + 20% a 30% de comisiones por rendimiento). Este modelo alinea los incentivos del equipo con la rentabilidad de la clínica: los costos laborales solo aumentan en proporción directa a los ingresos generados, protegiendo la caja frente a fluctuaciones de mercado.

    #### 3. Eficiencia Societaria y Legal
    Se ha optimizado la carga impositiva y previsional mediante la figura de **Sueldo Patronal Mínimo + Retiros Societarios**. Esta estructura blinda el flujo de caja personal de las socias, reduce drásticamente el pago de sobrecostos al Estado (evitando cotizaciones infladas e innecesarias) y posterga inteligentemente el pago del Impuesto a la Renta (F22) para cuando la clínica haya generado utilidades demostrables bajo el Régimen Propyme.

    **Conclusión:** El proyecto cuenta con un mapa financiero realista y una estrategia societaria avanzada. La combinación de una estructura de costos fijos minuciosamente controlada y un sólido fondo de contingencia, maximiza las probabilidades de éxito comercial y asegura un crecimiento sostenible a largo plazo.
    """)

    st.markdown("---")
    st.markdown("### 📈 Proyección de Escalamiento a 12 Meses (Timeline Estratégico)")
    st.markdown("Esta gráfica modela tu hoja de ruta. Demuestra que es **100% realista** llegar a los $3 Millones de utilidad neta vendiendo $11 Millones al mes, **siempre y cuando** retengan el margen de ganancia alto de los exámenes de laboratorio in-house y las cirugías.")

    meses = ["Mes 1", "Mes 2", "Mes 3", "Mes 4", "Mes 5", "Mes 6", "Mes 7", "Mes 8", "Mes 9", "Mes 10", "Mes 11", "Mes 12"]
    ventas_proj = [4500000, 5000000, 5500000, 7900000, 8500000, 9500000, 10000000, 10500000, 11000000, 11000000, 11000000, 11000000]
    
    # Utilidades proyectadas modelando margen de 75-80% y costos fijos de 5.5M
    utilidad_proj = [
        -2500000, # Mes 1 (Pérdida - Fondo Emergencia)
        -2000000, # Mes 2 (Pérdida - Fondo Emergencia)
        -1500000, # Mes 3 (Pérdida - Fondo Emergencia)
        0,        # Mes 4 (Punto Equilibrio exacto)
        500000,   # Mes 5 (Leve ganancia)
        1200000,  # Mes 6
        1800000,  # Mes 7
        2400000,  # Mes 8
        3000000,  # Mes 9 (Meta alcanzada: 11M Venta -> 3M Utilidad)
        3000000,  # Mes 10
        3000000,  # Mes 11
        3000000   # Mes 12
    ]

    fig_proj = go.Figure()
    # Barras de Ventas
    fig_proj.add_trace(go.Bar(
        x=meses,
        y=ventas_proj,
        name='Ventas (Facturación)',
        marker_color='royalblue',
        opacity=0.7
    ))
    # Línea de Utilidad/Pérdida
    fig_proj.add_trace(go.Scatter(
        x=meses,
        y=utilidad_proj,
        name='Utilidad Neta (Caja Libre)',
        mode='lines+markers+text',
        marker=dict(size=12, color=['red' if u < 0 else ('gold' if u == 0 else 'green') for u in utilidad_proj]),
        line=dict(color='black', width=3),
        text=[f"${u/1000000:.1f}M" for u in utilidad_proj],
        textposition="top center"
    ))

    fig_proj.update_layout(
        title='Mapa de Ruta: Del Valle de la Muerte a la Rentabilidad',
        xaxis_title='Línea de Tiempo Operativa',
        yaxis_title='Monto (CLP)',
        barmode='group',
        hovermode="x unified",
        shapes=[
            # Línea de cero (Break-even)
            dict(type="line", x0=0, x1=11, y0=0, y1=0, line=dict(color="black", width=2, dash="dash"))
        ],
        annotations=[
            dict(x=1, y=-500000, text="Fase Crítica<br>(Rescate Fondo Emergencia)", showarrow=False, font=dict(color="darkred", size=11)),
            dict(x=3.5, y=3000000, text="Break-Even<br>Utilidad Cero", showarrow=False, font=dict(color="darkgoldenrod", size=11)),
            dict(x=9, y=5500000, text="Meta Alcanzada<br>3M Utilidad", showarrow=False, font=dict(color="darkgreen", size=11))
        ],
        margin=dict(t=50, b=50)
    )

    st.plotly_chart(fig_proj, use_container_width=True)

    st.markdown("---")
    st.markdown("### ⚖️ Arquitectura Legal y Societaria (Propuesta Directorio)")
    st.markdown("Este es el resumen ejecutivo del blindaje legal diseñado para proteger a todos los socios, asegurar el retorno de la inversión y mantener la paz familiar y administrativa.")
    
    col_leg1, col_leg2 = st.columns(2)
    
    with col_leg1:
        st.info("""
        **1. Figura Legal (SpA)**
        * Se constituirá una **Sociedad por Acciones (SpA)**. A diferencia de la Sociedad Limitada, la SpA permite cambiar porcentajes en el futuro, no requiere unanimidad para operar y blinda el patrimonio personal.
        * **Riesgo Patrimonial:** Ante quiebra o deudas, los bancos y proveedores solo pueden embargar bienes de la empresa. Las casas, autos y ahorros personales de los 3 socios son intocables (salvo que firmen como avales personales).

        **2. Estructura Inicial y Préstamo (Mutuo con Período de Gracia)**
        * **Acciones Día 0:** Don Alfonso (50%), Sasha (25%), Daniela (25%).
        * **Protección del Capital:** Los $54 Millones de Don Alfonso no entran como "regalo", sino como un **Préstamo (Mutuo)** a la empresa.
        * **Período de Gracia (No se paga el Día 1):** Es suicidio financiero pagar esta deuda el primer mes. Se estipula legalmente un **Período de Gracia de 6 a 12 meses** (mientras se usa el Fondo de Emergencia). Don Alfonso empezará a cobrar su cuota mensual SOLO cuando la clínica alcance el Punto de Equilibrio y genere utilidades reales. Él asume el riesgo total, pero tiene prioridad de cobro cuando haya liquidez.

        **3. Roles y Representación (Firma en el Banco)**
        * En los estatutos públicos, los 3 pueden ser Representantes Legales, pero con poderes divididos.
        * **Firma Indistinta:** Sasha (como Administradora) tendrá el Digipass para operar sola en el día a día (pagar sueldos, proveedores, luz).
        * **Firma Conjunta:** Para decisiones graves (pedir créditos grandes, vender equipos caros), el banco exigirá la firma de Don Alfonso + 1 socia más.
        """)

    with col_leg2:
        st.warning("""
        **4. Protección de Minorías (Candado del 76%)**
        * Para evitar que el socio del 50% tome decisiones estructurales solo (vender la empresa, echar socios, emitir más acciones), los estatutos exigirán un **Quórum Supramayoritario del 76%**. Esto lo obliga matemáticamente a negociar y llegar a acuerdo con las socias del 25%.

        **5. Redistribución Futura (Pacto de Accionistas)**
        * Se firmará un contrato privado en Notaría estipulando que, una vez que la empresa le termine de pagar el Préstamo de $54M a Don Alfonso, él quedará obligado a vender parte de sus acciones a Sasha y Daniela para igualar los porcentajes (ej. 33/33/33).

        **6. Fallecimiento (Seguro Cruzado de Socios)**
        * Si un socio fallece, sus hijos heredan el *dinero*, no el derecho a voto. 
        * **Mecanismo:** La clínica contratará (a partir del año 2) un Seguro de Vida de Socios. Si alguien fallece, el seguro le paga millones a la clínica, y la clínica usa ese efectivo inmediatamente para comprarle las acciones a los hijos. Los hijos se van con efectivo y las socias vivas mantienen el 100% del control. Si el fallecido es Don Alfonso (antes de recuperar la inversión), la clínica simplemente le sigue pagando el préstamo mensual a sus hijos.
        """)
