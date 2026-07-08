import os
import pandas as pd
import sqlite3
import glob
import zipfile
import shutil
import re
from datetime import datetime

# Diccionario de meses
MESES = {
    'ENERO': 1, 'FEBRERO': 2, 'MARZO': 3, 'ABRIL': 4, 'MAYO': 5, 'JUNIO': 6,
    'JULIO': 7, 'AGOSTO': 8, 'SEPTIEMBRE': 9, 'OCTUBRE': 10, 'NOVIEMBRE': 11, 'DICIEMBRE': 12
}

def get_month_year(filename):
    name = os.path.basename(filename).upper()
    year = None
    month = None
    for m in MESES:
        if m in name:
            month = MESES[m]
            break
    match = re.search(r'(20\d{2})', name)
    if match:
        year = int(match.group(1))
        
    return year, month

def build_database():
    print("Iniciando construcción de base de datos robusta...")
    base_dir = os.path.dirname(__file__)
    historico_dir = os.path.abspath(os.path.join(base_dir, '..', '..', 'historico'))
    db_path = os.path.join(base_dir, 'clinica_historico.db')
    
    # Lista para guardar los archivos que dan error
    errores_log = []
    
    conn = sqlite3.connect(db_path)
    
    # --- 1. VENTAS POR PRODUCTO (CSV) ---
    csv_files = glob.glob(os.path.join(historico_dir, '*.csv'))
    ventas_df = pd.DataFrame()
    for f in csv_files:
        try:
            df = pd.read_csv(f, encoding='utf-8', on_bad_lines='skip')
            ventas_df = pd.concat([ventas_df, df], ignore_index=True)
        except Exception as e:
            errores_log.append(f"ERROR CSV - {os.path.basename(f)}: {e}")
            
    if not ventas_df.empty:
        if 'FECHA' in ventas_df.columns:
            ventas_df['FECHA'] = pd.to_datetime(ventas_df['FECHA'], errors='coerce')
        ventas_df.fillna({'CANTIDAD': 0, 'SUBTOTAL': 0, 'MARGEN': 0}, inplace=True)
        ventas_df.to_sql('ventas_historicas', conn, if_exists='replace', index=False)
        print(f"-> Insertadas {len(ventas_df)} filas en 'ventas_historicas'.")

    # --- 2. LIBROS DE COMPRAS (Versión Multi-Pestaña) ---
    facturas_dir = os.path.join(historico_dir, 'extracted_facturas', 'Facturas')
    # Buscar TODOS los Excel para evitar fallos de mayúsculas
    todos_compras = glob.glob(os.path.join(facturas_dir, '**', '*.xls*'), recursive=True)
    compras_archivos = [f for f in todos_compras if 'COMPRAS' in os.path.basename(f).upper()]
    compras_list = []
    
    for f in compras_archivos:
        try:
            # sheet_name=None fuerza a Pandas a leer TODAS las pestañas del Excel
            todas_las_hojas = pd.read_excel(f, sheet_name=None, header=None)
            
            for nombre_hoja, df_temp in todas_las_hojas.items():
                if len(df_temp) < 5: continue # Saltar hojas vacías
                
                header_idx = -1
                for idx, row in df_temp.head(15).iterrows():
                    row_str = " ".join(str(v).upper() for v in row.values)
                    if 'TOTAL' in row_str or 'MONTO' in row_str:
                        header_idx = idx
                        break
                
                if header_idx != -1:
                    df_compra = df_temp.iloc[header_idx + 1:].copy()
                    df_compra.columns = df_temp.iloc[header_idx].astype(str).str.upper().str.strip()
                    
                    if 'MONTO TOTAL' in df_compra.columns:
                        df_compra['MONTO TOTAL'] = pd.to_numeric(df_compra['MONTO TOTAL'], errors='coerce')
                        df_compra = df_compra.dropna(subset=['MONTO TOTAL'])
                        df_compra = df_compra[df_compra['MONTO TOTAL'] != 0]
                        compras_list.append(df_compra)
        except Exception as e:
            errores_log.append(f"ERROR Compras - {os.path.basename(f)}: {e}")
            
    if compras_list:
        compras_df = pd.concat(compras_list, ignore_index=True)
        if 'FECHA EMISION' in compras_df.columns:
            compras_df['FECHA'] = pd.to_datetime(compras_df['FECHA EMISION'], errors='coerce')
        compras_df.to_sql('compras_historicas', conn, if_exists='replace', index=False)
        print(f"-> Insertadas {len(compras_df)} filas en 'compras_historicas'.")

    # --- 3. LIBROS DE VENTAS DIARIAS (ZIP) ---
    zip_path = os.path.join(historico_dir, 'Calendario_Historico.zip')
    temp_zip_dir = os.path.join(base_dir, 'temp_unzip')
    if os.path.exists(zip_path) and os.path.isfile(zip_path):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_zip_dir)
            
    # Búsqueda a prueba de case-sensitive
    todos_ventas = glob.glob(os.path.join(temp_zip_dir, '**', '*.xls*'), recursive=True)
    todos_ventas.extend(glob.glob(os.path.join(historico_dir, 'Calendario_Historico.zip', '**', '*.xls*'), recursive=True))
    ventas_archivos = [f for f in todos_ventas if 'VENTAS' in os.path.basename(f).upper()]
    
    ventas_diarias_list = []
    
    for f in set(ventas_archivos): 
        try:
            year, month = get_month_year(f)
            if not year or not month:
                errores_log.append(f"OMITIDO Ventas Diarias - {os.path.basename(f)}: No se pudo deducir Año/Mes.")
                continue
                
            # Dropna elimina columnas 100% vacías
            df_venta = pd.read_excel(f, header=None).dropna(how='all', axis=1)
            
            # CAZADOR DE TOTALES: Buscar dinámicamente la columna "TOTAL" en las cabeceras (primeras 5 filas)
            col_total_idx = -1
            for col_idx in range(df_venta.shape[1]):
                col_data = df_venta.iloc[0:5, col_idx].astype(str).str.upper()
                if any(col_data.str.contains('TOTAL')):
                    col_total_idx = col_idx
                    break
            
            # Si no encuentra la palabra "TOTAL", usamos la última columna (-1) como plan B
            if col_total_idx == -1:
                col_total_idx = -1
            
            for idx, row in df_venta.iterrows():
                if idx < 4: continue # Saltar cabeceras
                try:
                    dia = int(row.iloc[0])
                    # Extraemos el valor usando la columna que encontramos dinámicamente
                    total = row.iloc[col_total_idx]
                    total = pd.to_numeric(total, errors='coerce')
                    
                    if pd.notna(total) and total > 0:
                        try:
                            fecha = datetime(year, month, dia)
                            ventas_diarias_list.append({'FECHA': fecha, 'VENTA_TOTAL': total, 'ARCHIVO': os.path.basename(f)})
                        except ValueError:
                            pass # Ignorar días inválidos (ej. 31 de febrero)
                except (ValueError, TypeError):
                    continue
        except Exception as e:
            errores_log.append(f"ERROR Ventas Diarias - {os.path.basename(f)}: {e}")
            
    if ventas_diarias_list:
        ventas_diarias_df = pd.DataFrame(ventas_diarias_list)
        ventas_diarias_df.to_sql('ventas_diarias', conn, if_exists='replace', index=False)
        print(f"-> Insertadas {len(ventas_diarias_df)} filas en 'ventas_diarias'.")

    # =========================================================
    # 4. CREACIÓN DEL "ONE BIG TABLE" (MASTER FINANCIERO GOLD)
    # =========================================================
    print("Consolidando datos en la tabla maestra (Gold Layer)...")
    
    # 4.1 Extraer solo lo esencial de Egresos
    if not compras_df.empty and 'MONTO TOTAL' in compras_df.columns:
        df_egresos = compras_df[['FECHA', 'MONTO TOTAL', 'CENTRO DE COSTOS']].copy()
        df_egresos.columns = ['Fecha', 'Monto', 'Categoria']
        df_egresos['Tipo_Movimiento'] = 'Egreso (Compras)'
    else:
        df_egresos = pd.DataFrame(columns=['Fecha', 'Monto', 'Categoria', 'Tipo_Movimiento'])

    # 4.2 Extraer solo lo esencial de Ventas por Producto (CSV)
    if not ventas_df.empty and 'SUBTOTAL' in ventas_df.columns:
        df_ingresos_csv = ventas_df[['FECHA', 'SUBTOTAL', 'DESC. CATEGORIA']].copy()
        df_ingresos_csv.columns = ['Fecha', 'Monto', 'Categoria']
        df_ingresos_csv['Tipo_Movimiento'] = 'Ingreso (CSV Productos)'
    else:
        df_ingresos_csv = pd.DataFrame(columns=['Fecha', 'Monto', 'Categoria', 'Tipo_Movimiento'])

    # 4.3 Extraer solo lo esencial de Ventas Diarias (Caja)
    if not ventas_diarias_df.empty and 'VENTA_TOTAL' in ventas_diarias_df.columns:
        df_ingresos_caja = ventas_diarias_df[['FECHA', 'VENTA_TOTAL']].copy()
        df_ingresos_caja['Categoria'] = 'Caja Diaria'
        df_ingresos_caja.columns = ['Fecha', 'Monto', 'Categoria']
        df_ingresos_caja['Tipo_Movimiento'] = 'Ingreso (Libro Caja)'
    else:
        df_ingresos_caja = pd.DataFrame(columns=['Fecha', 'Monto', 'Categoria', 'Tipo_Movimiento'])

    # 🔥 NUEVO PASO 4.4: GENERADOR AUTOMÁTICO DE COSTOS RRHH Y OPEX HISTÓRICOS 🔥
    print("Generando registros históricos de RRHH y OPEX (2024-08 a 2026-07)...")
    meses_rrhh = pd.date_range(start='2024-08-01', end='2026-07-01', freq='MS')
    rrhh_rows = []
    
    for mes in meses_rrhh:
        # --- A. RECURSOS HUMANOS ---
        # 1. Gasto Recepcionista (Lunes a Viernes)
        rrhh_rows.append({'Fecha': mes, 'Monto': 521033 + 130258, 'Categoria': 'SUELDOS - RECEPCIONISTA (L-V)', 'Tipo_Movimiento': 'Egreso (Compras)'})
        # 2. Gasto Recepcionista (Solo Sábados - ESTIMADO)
        rrhh_rows.append({'Fecha': mes, 'Monto': 100000 + 25000, 'Categoria': 'SUELDOS - RECEPCIONISTA (SABADOS)', 'Tipo_Movimiento': 'Egreso (Compras)'})
        # 3. Gasto Médico Veterinaria (TURNO AM)
        rrhh_rows.append({'Fecha': mes, 'Monto': 326667 + 81667 + 826000, 'Categoria': 'SUELDOS - MEDICO VETERINARIA (TURNO AM)', 'Tipo_Movimiento': 'Egreso (Compras)'})
        # 4. Gasto Médico Veterinaria (TURNO PM)
        rrhh_rows.append({'Fecha': mes, 'Monto': 326667 + 81667 + 826000, 'Categoria': 'SUELDOS - MEDICO VETERINARIA (TURNO PM)', 'Tipo_Movimiento': 'Egreso (Compras)'})
        # 5. Gasto Enfermera (Boleta de Honorarios)
        rrhh_rows.append({'Fecha': mes, 'Monto': 241537, 'Categoria': 'HONORARIOS - ENFERMERA (TURNOS)', 'Tipo_Movimiento': 'Egreso (Compras)'})
        
        # --- B. COSTOS OPERATIVOS AUSENTES (OPEX) ---
        # Inyectamos valores mensuales estimados para sincerar el Flujo de Caja
        rrhh_rows.append({'Fecha': mes, 'Monto': 200000, 'Categoria': 'OPEX - SERVICIOS BASICOS (LUZ/AGUA/CLIMATIZACION)', 'Tipo_Movimiento': 'Egreso (Compras)'})
        rrhh_rows.append({'Fecha': mes, 'Monto': 75000, 'Categoria': 'OPEX - SEGUROS Y RETIRO RESIDUOS (REAS)', 'Tipo_Movimiento': 'Egreso (Compras)'})
        # Estimación de ~22% de leyes sociales sobre sueldos base + provisión de vacaciones/indemnización
        rrhh_rows.append({'Fecha': mes, 'Monto': 450000, 'Categoria': 'OPEX - LEYES SOCIALES Y PROVISIONES LABORALES', 'Tipo_Movimiento': 'Egreso (Compras)'})

    df_rrhh = pd.DataFrame(rrhh_rows)

    # 4.5 Unir todo en una sola gran tabla unificada
    master_df = pd.concat([df_egresos, df_ingresos_csv, df_ingresos_caja, df_rrhh], ignore_index=True)
    
    # Limpieza final de seguridad sobre el Master
    master_df = master_df.dropna(subset=['Fecha', 'Monto'])
    master_df['Monto'] = pd.to_numeric(master_df['Monto'], errors='coerce').fillna(0)
    master_df['Fecha'] = pd.to_datetime(master_df['Fecha'], errors='coerce')
    master_df['Categoria'] = master_df['Categoria'].astype(str).str.upper().str.strip()

    # Guardar en la base de datos
    master_df.to_sql('master_financiero', conn, if_exists='replace', index=False)
    print(f"-> ¡Master Financiero creado con éxito! ({len(master_df)} registros totales).")
    # =========================================================

    # Limpieza final y Log de Auditoría
    if os.path.exists(temp_zip_dir):
        shutil.rmtree(temp_zip_dir)
        
    conn.close()
    print("\n=== CONSTRUCCIÓN FINALIZADA ===")
    
    # Escribir el reporte de errores en un archivo de texto en la misma carpeta
    log_path = os.path.join(base_dir, 'reporte_archivos_ignorados.txt')
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write("REPORTE DE ARCHIVOS NO PROCESADOS O CON ERRORES\n")
        f.write("="*50 + "\n")
        if errores_log:
            for error in errores_log:
                f.write(error + "\n")
            print(f"[ALERTA] Se encontraron {len(errores_log)} problemas. Revisa el archivo 'reporte_archivos_ignorados.txt'")
        else:
            f.write("¡Todos los archivos se procesaron con éxito sin errores aparentes!\n")
            print("[EXITO] 100% de archivos procesados sin errores.")

if __name__ == '__main__':
    build_database()
