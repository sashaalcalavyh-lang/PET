import os
import zipfile
import tempfile
import shutil
import pandas as pd
import sqlite3
import re
from pathlib import Path

def clean_column_name(col):
    """Limpia el nombre de las columnas (remueve espacios y caracteres especiales)."""
    col = str(col).strip().upper()
    # Reemplazar espacios por guiones bajos
    col = re.sub(r'\s+', '_', col)
    # Remover caracteres no alfanumericos (mantener guiones bajos)
    col = re.sub(r'[^A-Z0-9_]', '', col)
    return col

def clean_data(df):
    """Aplica limpiezas generales a todo el DataFrame."""
    # Limpiar nombres de columnas
    df.columns = [clean_column_name(col) for col in df.columns]
    
    for col in df.columns:
        # Strip whitespace de columnas tipo string
        if df[col].dtype == 'object':
            df[col] = df[col].astype(str).str.strip()
            # Convertir 'nan' o 'None' de vuelta a NaN de Pandas
            df[col] = df[col].replace({'nan': None, 'None': None, '': None})
            
        # Intentar convertir fechas si el nombre de la columna sugiere fecha
        if 'FECHA' in col:
            try:
                # pandas datetime parsing, intentamos dd-mm-yyyy o yyyy-mm-dd
                # coerce convertira a NaT lo que no se pueda procesar
                df[col] = pd.to_datetime(df[col], errors='coerce', dayfirst=True)
            except Exception as e:
                print(f"No se pudo convertir a fecha la columna {col}: {e}")

    return df

def clean_table_name(filename):
    """Genera un nombre de tabla SQL seguro a partir del nombre del archivo."""
    name = Path(filename).stem
    name = str(name).strip().upper()
    name = re.sub(r'\s+', '_', name)
    name = re.sub(r'[^A-Z0-9_]', '', name)
    # Algunos nombres tienen prefijos raros, intentemos dejarlos limpios
    return "TBL_" + name

def process_csv(filepath, conn):
    """Lee, limpia y carga un archivo CSV en SQLite."""
    table_name = clean_table_name(filepath.name)
    print(f"Procesando CSV: {filepath.name} -> Tabla: {table_name}")
    
    try:
        # Intentar utf-8 primero, luego latin1
        try:
            df = pd.read_csv(filepath, sep=',', encoding='utf-8', on_bad_lines='skip')
        except UnicodeDecodeError:
            df = pd.read_csv(filepath, sep=',', encoding='latin1', on_bad_lines='skip')
        except Exception as e:
            # Quizás esté separado por punto y coma
            df = pd.read_csv(filepath, sep=';', encoding='utf-8', on_bad_lines='skip')
            
        if df.empty:
            print(f"  El archivo {filepath.name} está vacío. Saltando.")
            return
            
        df = clean_data(df)
        
        # Cargar a base de datos
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"  Cargados {len(df)} registros exitosamente.")
    except Exception as e:
        print(f"Error procesando {filepath.name}: {e}")

def main():
    base_dir = Path(r"d:\Data Science\GitHub\PET\historico")
    db_path = Path(r"d:\Data Science\GitHub\PET\pet_historico.db")
    
    # Conexión SQLite
    conn = sqlite3.connect(db_path)
    
    # 1. Crear un directorio temporal para extraer ZIPs
    temp_dir = tempfile.mkdtemp(prefix="pet_historico_")
    print(f"Directorio temporal creado: {temp_dir}")
    
    try:
        # 2. Descomprimir todos los ZIPs
        zip_files = list(base_dir.rglob("*.zip"))
        for zip_file in zip_files:
            print(f"Extrayendo: {zip_file.name}")
            try:
                with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                    # Extraer en subcarpeta para no mezclar nombres
                    extract_path = Path(temp_dir) / zip_file.stem
                    extract_path.mkdir(exist_ok=True)
                    zip_ref.extractall(extract_path)
            except zipfile.BadZipFile:
                 print(f"Archivo zip corrupto o invalido: {zip_file.name}")
            except Exception as e:
                 print(f"Error extrayendo {zip_file.name}: {e}")
                 
        # 3. Recopilar todos los CSVs
        # De la carpeta principal
        all_csvs = list(base_dir.rglob("*.csv"))
        # De la carpeta temporal (zippeados)
        all_csvs.extend(list(Path(temp_dir).rglob("*.csv")))
        
        # Filtrar duplicados (por nombre de archivo)
        # Esto previene que un CSV extraido sobreescriba o sea sobreescrito por el mismo CSV
        processed_names = set()
        for csv_file in all_csvs:
            if csv_file.name not in processed_names:
                process_csv(csv_file, conn)
                processed_names.add(csv_file.name)
            else:
                print(f"Saltando CSV duplicado: {csv_file.name}")
            
    finally:
        # Limpiar
        print(f"Limpiando directorio temporal: {temp_dir}")
        shutil.rmtree(temp_dir, ignore_errors=True)
        conn.close()
        
    print("¡Proceso de integración finalizado! Base de datos guardada en:", db_path)

if __name__ == "__main__":
    main()
