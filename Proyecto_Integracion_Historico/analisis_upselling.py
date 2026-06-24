import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Configuracion de graficos
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

def main():
    db_path = r'd:\Data Science\GitHub\PET\Proyecto_Integracion_Historico\pet_historico.db'
    conn = sqlite3.connect(db_path)

    print("Cargando datos de TBL_INFORME_DETALLEDE_VENTAS...")
    # Cargar detalle de ventas, excluyendo posibles anulaciones o totales en 0
    query = """
    SELECT 
        CLIENTE,
        FECHA,
        CATEGORIA,
        DESCRIPCION,
        TOTAL,
        CANTIDAD
    FROM TBL_INFORME_DETALLEDE_VENTAS
    WHERE CLIENTE IS NOT NULL AND TOTAL > 0
    """
    df = pd.read_sql(query, conn)
    conn.close()

    if df.empty:
        print("No se encontraron datos válidos para el análisis.")
        return

    # Limpieza basica
    df['FECHA'] = pd.to_datetime(df['FECHA'])
    df['CLIENTE'] = df['CLIENTE'].astype(str).str.strip()
    df['CATEGORIA'] = df['CATEGORIA'].fillna('SIN CATEGORIA').str.strip().str.upper()

    # Identificar visitas unicas por cliente y dia (Tickets)
    df['FECHA_DIA'] = df['FECHA'].dt.date
    
    # Agregar por cliente
    clientes_agrupados = df.groupby('CLIENTE').agg(
        Total_Gasto=('TOTAL', 'sum'),
        Total_Visitas_Unicas=('FECHA_DIA', 'nunique'),
        Primera_Visita=('FECHA', 'min'),
        Ultima_Visita=('FECHA', 'max')
    ).reset_index()

    # Calcular meses activos (minimo 1)
    clientes_agrupados['Meses_Activos'] = ((clientes_agrupados['Ultima_Visita'] - clientes_agrupados['Primera_Visita']).dt.days / 30).apply(np.ceil).replace(0, 1)

    # Calcular gasto mensual y anualizado
    clientes_agrupados['Gasto_Promedio_Mensual'] = clientes_agrupados['Total_Gasto'] / clientes_agrupados['Meses_Activos']
    clientes_agrupados['Gasto_Promedio_Anualizado'] = clientes_agrupados['Gasto_Promedio_Mensual'] * 12

    # Segmentacion: Esporádico (1 visita) vs Recurrente (>1 visita)
    clientes_agrupados['Segmento'] = np.where(clientes_agrupados['Total_Visitas_Unicas'] > 1, 'Recurrente', 'Esporádico')

    # Deteccion de Outliers (Top 1% de gasto)
    limite_outlier = clientes_agrupados['Total_Gasto'].quantile(0.99)
    outliers = clientes_agrupados[clientes_agrupados['Total_Gasto'] > limite_outlier]
    clientes_normales = clientes_agrupados[clientes_agrupados['Total_Gasto'] <= limite_outlier]

    print("\n--- ANÁLISIS DE OUTLIERS ---")
    print(f"Límite del percentil 99 (Outliers): ${limite_outlier:,.0f}")
    print(f"Cantidad de clientes Outliers: {len(outliers)}")
    print(f"Gasto promedio de Outliers (Anual): ${outliers['Gasto_Promedio_Anualizado'].mean():,.0f}")

    print("\n--- RESUMEN POR SEGMENTO (Sin Outliers) ---")
    resumen = clientes_normales.groupby('Segmento').agg(
        Clientes=('CLIENTE', 'count'),
        Gasto_Promedio_Anual=('Gasto_Promedio_Anualizado', 'mean'),
        Gasto_Promedio_Mensual=('Gasto_Promedio_Mensual', 'mean')
    ).reset_index()
    print(resumen)

    # --- GRÁFICO 1: Gasto Promedio Anual por Segmento ---
    plt.figure()
    sns.barplot(data=resumen, x='Segmento', y='Gasto_Promedio_Anual', palette='viridis')
    plt.title('Gasto Promedio Anual por Perfil de Cliente (Sin Outliers)')
    plt.ylabel('Gasto Promedio Anual ($)')
    for i, val in enumerate(resumen['Gasto_Promedio_Anual']):
        plt.text(i, val + (val*0.02), f'${val:,.0f}', ha='center', fontweight='bold')
    plt.tight_layout()
    plt.savefig('gasto_por_perfil.png')
    plt.close()

    # --- ANÁLISIS DE CATEGORÍAS Y UPSELLING ---
    print("\n--- OPORTUNIDADES DE UPSELLING (BASKET ANALYSIS) ---")
    # Qué categorías compran los recurrentes vs los esporádicos?
    cat_ventas = df.groupby(['CLIENTE', 'CATEGORIA']).size().reset_index(name='Veces_Comprada')
    cat_ventas = pd.merge(cat_ventas, clientes_agrupados[['CLIENTE', 'Segmento']], on='CLIENTE')

    # % de clientes de cada segmento que compran una categoria
    cat_penetracion = cat_ventas.groupby(['Segmento', 'CATEGORIA']).agg(
        Clientes_Compradores=('CLIENTE', 'nunique')
    ).reset_index()
    
    total_clientes_seg = clientes_agrupados.groupby('Segmento')['CLIENTE'].nunique().to_dict()
    cat_penetracion['Total_Clientes_Segmento'] = cat_penetracion['Segmento'].map(total_clientes_seg)
    cat_penetracion['Penetracion_%'] = (cat_penetracion['Clientes_Compradores'] / cat_penetracion['Total_Clientes_Segmento']) * 100

    # Filtrar solo categorias relevantes (>5% penetracion)
    cat_penetracion = cat_penetracion[cat_penetracion['Penetracion_%'] >= 5]
    
    # Pivotear para comparar
    pivot_pen = cat_penetracion.pivot(index='CATEGORIA', columns='Segmento', values='Penetracion_%').fillna(0)
    pivot_pen['Brecha_Recurrente_vs_Esporadico'] = pivot_pen['Recurrente'] - pivot_pen['Esporádico']
    pivot_pen = pivot_pen.sort_values(by='Brecha_Recurrente_vs_Esporadico', ascending=False)
    
    print("\nDiferencia en penetración de servicios (Recurrentes vs Esporádicos):")
    print(pivot_pen.head(10))

    # --- GRÁFICO 2: Brecha de Upselling ---
    plt.figure(figsize=(12, 8))
    pivot_pen['Brecha_Recurrente_vs_Esporadico'].head(10).sort_values().plot(kind='barh', color='coral')
    plt.title('Brecha de Adquisición: Recurrentes vs Esporádicos\n(Qué consumen más los clientes frecuentes)')
    plt.xlabel('Diferencia de Penetración (%)')
    plt.tight_layout()
    plt.savefig('oportunidades_upselling.png')
    plt.close()

    print("\n¡Análisis completado! Gráficos guardados: gasto_por_perfil.png y oportunidades_upselling.png")

    # Escribir un archivo markdown temporal para que el agente lea los resultados
    with open('resultados_temp.txt', 'w') as f:
        f.write("RESUMEN DE OUTLIERS\n")
        f.write(f"Limite 99%: {limite_outlier}\n")
        f.write(f"N Outliers: {len(outliers)}\n")
        f.write("\nRESUMEN POR SEGMENTO (Sin Outliers)\n")
        f.write(resumen.to_string())
        f.write("\n\nBRECHA DE CATEGORIAS (Top 10)\n")
        f.write(pivot_pen.head(10).to_string())

if __name__ == "__main__":
    main()
