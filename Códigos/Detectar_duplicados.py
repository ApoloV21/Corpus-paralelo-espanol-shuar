import os
import pandas as pd
import chardet

# ------------------------------------------------------------
# Utilidades de codificación (igual que en scripts anteriores)
# ------------------------------------------------------------
def detectar_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
    result = chardet.detect(raw_data)
    return result['encoding']

def convertir_a_utf8_si_necesario(ruta_entrada, ruta_salida=None):
    """Convierte a UTF-8 si no lo está, devuelve ruta del archivo UTF-8."""
    encoding = detectar_encoding(ruta_entrada)
    if encoding is None:
        encoding = 'latin-1'
    with open(ruta_entrada, 'r', encoding=encoding, errors='replace') as f:
        contenido = f.read()
    if encoding.lower() == 'utf-8':
        return ruta_entrada
    if ruta_salida is None:
        base, ext = os.path.splitext(ruta_entrada)
        ruta_salida = f"{base}_utf8{ext}"
    with open(ruta_salida, 'w', encoding='utf-8') as f:
        f.write(contenido)
    print(f"✓ Convertido a UTF-8: {ruta_salida}")
    return ruta_salida

# ------------------------------------------------------------
# Selección interactiva de archivo (CSV/JSON)
# ------------------------------------------------------------
def listar_archivos_corpus(directorio):
    try:
        archivos = [f for f in os.listdir(directorio) if f.lower().endswith(('.csv', '.json'))]
        return sorted(archivos)
    except FileNotFoundError:
        return []

def elegir_archivo_corpus(directorio):
    archivos = listar_archivos_corpus(directorio)
    if not archivos:
        print(f"No se encontraron archivos .csv o .json en: {directorio}")
        return None
    print(f"\nArchivos de corpus en '{directorio}':")
    for i, arch in enumerate(archivos, start=1):
        print(f"{i}. {arch}")
    while True:
        try:
            opcion = int(input("Elige el número del archivo (0 para cancelar): "))
            if opcion == 0:
                return None
            if 1 <= opcion <= len(archivos):
                return os.path.join(directorio, archivos[opcion-1])
            else:
                print(f"Opción inválida. Elige entre 1 y {len(archivos)}.")
        except ValueError:
            print("Por favor, ingresa un número válido.")

def seleccionar_archivo():
    while True:
        print("\n--- SELECCIÓN DE CORPUS ---")
        print("1. Especificar un DIRECTORIO y elegir archivo .csv/.json")
        print("2. Ingresar la RUTA DIRECTA de un archivo .csv o .json")
        print("3. Salir")
        opcion = input("Elige una opción (1/2/3): ").strip()
        if opcion == '1':
            ruta_dir = input("Ingresa la ruta del directorio: ").strip()
            ruta_dir = os.path.expanduser(ruta_dir)
            if not os.path.isdir(ruta_dir):
                print("Error: la ruta no es un directorio válido.")
                continue
            archivo = elegir_archivo_corpus(ruta_dir)
            if archivo:
                return archivo
        elif opcion == '2':
            ruta = input("Ingresa la ruta completa del archivo: ").strip()
            ruta = os.path.expanduser(ruta)
            if os.path.isfile(ruta) and ruta.lower().endswith(('.csv', '.json')):
                return ruta
            else:
                print("Error: la ruta no es válida o no es .csv/.json")
        elif opcion == '3':
            return None
        else:
            print("Opción no válida.")

# ------------------------------------------------------------
# Detección y eliminación de duplicados
# ------------------------------------------------------------
def detectar_duplicados(df, case_sensitive=True):
    """
    Detecta filas duplicadas basadas en 'frase_es' y 'frase_sh'.
    Retorna un DataFrame con las filas duplicadas (excepto la primera ocurrencia).
    """
    # Elegir columnas para comparar
    cols = ['frase_es', 'frase_sh']
    if not case_sensitive:
        # Crear versiones en minúsculas para comparación
        df_comp = df[cols].apply(lambda x: x.str.lower() if x.dtype == 'object' else x)
        duplicados = df_comp.duplicated(keep='first')
    else:
        duplicados = df[cols].duplicated(keep='first')
    return df[duplicados]

def reindexar_ids(df):
    """Reasigna IDs consecutivos empezando desde 1."""
    df = df.copy()
    df.reset_index(drop=True, inplace=True)
    
    # Eliminar columna ID si ya existe (para evitar duplicado)
    if 'ID' in df.columns:
        df = df.drop(columns=['ID'])
    
    # Insertar nueva ID al inicio
    df.insert(0, 'ID', range(1, len(df)+1))
    return df

def es_texto_mayusculas_completo(texto):
    """Retorna True si el texto es una cadena y está totalmente en mayúsculas."""
    return isinstance(texto, str) and texto.isupper()


def normalizar_mayusculas_completas(df, cols):
    """Convierte a minúsculas solo las cadenas que están completamente en mayúsculas."""
    df = df.copy()
    for col in cols:
        if col in df.columns and df[col].dtype == 'object':
            df[col] = df[col].apply(lambda x: x.lower() if es_texto_mayusculas_completo(x) else x)
    return df


def eliminar_duplicados_y_reindexar(df, case_sensitive=True):
    """
    Elimina filas duplicadas (conservando primera ocurrencia) y reindexa IDs.
    """
    cols = ['frase_es', 'frase_sh']
    if not case_sensitive:
        # Para el drop_duplicates también necesitamos ignorar mayúsculas
        df_comp = df[cols].apply(lambda x: x.str.lower() if x.dtype == 'object' else x)
        df_sin_dup = df[~df_comp.duplicated(keep='first')]
    else:
        df_sin_dup = df.drop_duplicates(subset=cols, keep='first')
    df_limpio = reindexar_ids(df_sin_dup)
    return df_limpio

def guardar_corpus(df, ruta_original, formato=None):
    """Guarda el corpus limpio, pregunta si sobrescribir o crear nuevo."""
    if formato is None:
        formato = 'csv' if ruta_original.lower().endswith('.csv') else 'json'
    
    print(f"\nGuardar como:")
    print(f"1. Sobrescribir el archivo original: {ruta_original}")
    print(f"2. Crear un nuevo archivo (ej: original_limpio.csv)")
    opcion = input("Elige (1/2): ").strip()
    
    if opcion == '1':
        salida = ruta_original
    else:
        base, ext = os.path.splitext(ruta_original)
        sufijo = "_limpio"
        salida = f"{base}{sufijo}{ext}"
    
    try:
        if formato == 'csv':
            df.to_csv(salida, index=False, encoding='utf-8')
        else:
            df.to_json(salida, orient='records', force_ascii=False, indent=2)
        print(f"✓ Corpus guardado en: {salida}")
        return salida
    except Exception as e:
        print(f"Error al guardar: {e}")
        return None

def mostrar_resumen_duplicados(df_original, df_duplicados, case_sensitive):
    """Muestra estadísticas de duplicados."""
    total_original = len(df_original)
    num_duplicados = len(df_duplicados)
    print("\n=== RESULTADOS DE DETECCIÓN ===")
    print(f"Total de pares en el corpus: {total_original}")
    print(f"Pares duplicados encontrados: {num_duplicados}")
    if num_duplicados > 0:
        print(f"Pares únicos después de eliminar duplicados: {total_original - num_duplicados}")
        print("\nEjemplos de duplicados (primeros 5):")
        for idx, row in df_duplicados.head(5).iterrows():
            print(f"  {row['frase_es']} | {row['frase_sh']}")
        if num_duplicados > 5:
            print(f"  ... y {num_duplicados-5} más.")
    else:
        print("✓ No hay pares duplicados. No es necesario eliminar nada.")
    return num_duplicados

def procesar_corpus_duplicados():
    """Función principal."""
    archivo = seleccionar_archivo()
    if archivo is None:
        print("Saliendo.")
        return
    
    # Asegurar UTF-8
    archivo = convertir_a_utf8_si_necesario(archivo)
    
    # Cargar datos
    ext = os.path.splitext(archivo)[1].lower()
    try:
        if ext == '.csv':
            df = pd.read_csv(archivo, encoding='utf-8')
        else:
            df = pd.read_json(archivo)
    except Exception as e:
        print(f"Error al cargar el archivo: {e}")
        return
    
    # Validar columnas necesarias
    col_es = None
    col_sh = None
    for col in df.columns:
        if 'frase_es' in col or col.lower() == 'espanol':
            col_es = col
        if 'frase_sh' in col or col.lower() == 'shuar':
            col_sh = col
    if col_es is None or col_sh is None:
        print("Error: No se encontraron columnas 'frase_es' y 'frase_sh'.")
        return
    # Renombrar para consistencia
    df.rename(columns={col_es: 'frase_es', col_sh: 'frase_sh'}, inplace=True)

    # Normalizar frases completamente en mayúsculas
    print("\n¿Deseas convertir a minúsculas solo las frases totalmente en mayúsculas?")
    print("Ejemplo: 'HOLA BUENOS DÍAS' -> 'hola buenos días', pero no 'Hola buenos días'")
    normalizar = input("Normalizar mayúsculas completas? (s/n, por defecto s): ").strip().lower()
    if normalizar != 'n':
        df = normalizar_mayusculas_completas(df, ['frase_es', 'frase_sh'])
    
    # Preguntar si considerar mayúsculas/minúsculas
    print("\n¿Debe considerarse la diferencia entre mayúsculas y minúsculas?")
    print("Ejemplo: 'Jímiapetek' vs 'jímiapetek'")
    case = input("¿Distingue mayúsculas? (s/n, por defecto s): ").strip().lower()
    case_sensitive = case != 'n'
    
    # Detectar duplicados
    duplicados_df = detectar_duplicados(df, case_sensitive)
    num_dup = mostrar_resumen_duplicados(df, duplicados_df, case_sensitive)
    
    if num_dup == 0:
        return
    
    # Preguntar si eliminar
    eliminar = input("\n¿Deseas eliminar los pares duplicados y reindexar los IDs? (s/n): ").strip().lower()
    if eliminar != 's':
        print("Operación cancelada.")
        return
    
    # Eliminar duplicados y reindexar
    df_limpio = eliminar_duplicados_y_reindexar(df, case_sensitive)
    
    # Guardar
    guardar_corpus(df_limpio, archivo, ext[1:])
    
    # Mostrar nuevo rango de IDs
    print(f"\nNuevo rango de IDs: 1 a {len(df_limpio)} (sin huecos)")

if __name__ == "__main__":
    print("=== ELIMINADOR DE DUPLICADOS EN CORPUS ===")
    procesar_corpus_duplicados()