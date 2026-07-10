import os
import re
import chardet
from pathlib import Path

# ------------------------------------------------------------
# Funciones de limpieza y análisis (sin cambios)
# ------------------------------------------------------------
def detectar_codificacion(ruta_archivo):
    with open(ruta_archivo, 'rb') as f:
        raw_data = f.read()
        resultado = chardet.detect(raw_data)
        return resultado['encoding']

def convertir_a_utf8(ruta_entrada, ruta_salida=None):
    encoding_original = detectar_codificacion(ruta_entrada)
    if encoding_original is None:
        encoding_original = 'latin-1'
    with open(ruta_entrada, 'r', encoding=encoding_original, errors='replace') as f:
        contenido = f.read()
    if encoding_original.lower() == 'utf-8':
        return ruta_entrada
    if ruta_salida is None:
        base, ext = os.path.splitext(ruta_entrada)
        ruta_salida = f"{base}_utf8{ext}"
    with open(ruta_salida, 'w', encoding='utf-8') as f:
        f.write(contenido)
    print(f"✓ Convertido a UTF-8: {ruta_salida}")
    return ruta_salida

def limpiar_ruido(texto):
    caracteres_validos = r'[^a-zA-ZáéíóúüñÁÉÍÓÚÜÑ0-9\s\.\,\;\:\?\!\¿\¡\(\)\[\]\{\}\-\_\/\@\#\$\%\&\=\+\*\~`\'\"\|]'
    texto = re.sub(caracteres_validos, ' ', texto)
    lineas = texto.splitlines()
    lineas_limpias = []
    for linea in lineas:
        linea_strip = linea.strip()
        if re.fullmatch(r'[\d\s\.\-]+', linea_strip):
            continue
        if re.match(r'^(página|page|pg|pag\.?)\s*\d+', linea_strip, re.IGNORECASE):
            continue
        lineas_limpias.append(linea)
    return '\n'.join(lineas_limpias)

def normalizar_espacios_y_saltos(texto):
    texto = re.sub(r'[ \t]+', ' ', texto)
    texto = re.sub(r'\n\s*\n', '\n', texto)
    lineas = [linea.strip() for linea in texto.splitlines()]
    return '\n'.join(lineas)

def eliminar_vacios_y_duplicados(lineas):
    lineas_no_vacias = [linea for linea in lineas if linea.strip() != '']
    vistos = set()
    lineas_unicas = []
    for linea in lineas_no_vacias:
        if linea not in vistos:
            vistos.add(linea)
            lineas_unicas.append(linea)
    return lineas_unicas

def analizar_separador(lineas):
    total_pares = len(lineas)
    alineados = 0
    sin_pipe = []
    for idx, linea in enumerate(lineas, start=1):
        if '|' in linea:
            alineados += 1
        else:
            sin_pipe.append((idx, linea))
    return sin_pipe, total_pares, alineados

def calcular_tasa_alineacion(alineados, total_pares):
    if total_pares == 0:
        return 0.0
    return alineados / total_pares

def eliminar_puntos_finales_en_linea(linea):
    """
    Elimina puntos finales en cada frase de una línea con separador '|'.
    - Parte izquierda: puntos justo antes de '|' (incluyendo espacios opcionales).
    - Parte derecha: puntos al final de la línea.
    - Si no hay '|', elimina puntos al final de toda la línea.
    """
    if '|' not in linea:
        # Sin separador: eliminar puntos y espacios al final
        return re.sub(r'\.+\s*$', '', linea.rstrip('\n'))
    
    # Dividir por el primer '|' (puede haber más, pero tomamos el principal)
    partes = linea.split('|', 1)
    izquierda = partes[0]
    derecha = partes[1] if len(partes) > 1 else ''
    
    # Eliminar puntos y espacios al final de la parte izquierda (justo antes de '|')
    izquierda_limpia = re.sub(r'[\.\s]+$', '', izquierda)
    
    # Eliminar puntos y espacios al final de la parte derecha
    derecha_limpia = re.sub(r'[\.\s]+$', '', derecha)
    
    # Reconstruir la línea (se añade un espacio alrededor de '|' por legibilidad)
    return f"{izquierda_limpia} | {derecha_limpia}"

def es_completamente_mayuscula(texto):
    """
    Verifica si un texto contiene SOLO mayúsculas (ignorando números y caracteres especiales).
    Retorna True solo si todas las LETRAS son mayúsculas.
    """
    # Extraer solo las letras del texto
    letras = [c for c in texto if c.isalpha()]
    # Si no hay letras, retornar False
    if not letras:
        return False
    # Verificar que todas las letras sean mayúsculas
    return all(c.isupper() for c in letras)

def convertir_mayusculas_a_minusculas(texto):
    """
    Convierte un texto a minúsculas si está completamente en mayúsculas.
    Si no está completamente en mayúsculas, retorna el texto sin cambios.
    """
    if es_completamente_mayuscula(texto):
        return texto.lower()
    return texto

def procesar_mayusculas_en_linea(linea):
    """
    Procesa una línea para convertir a minúsculas las partes completamente en mayúsculas.
    Considera el separador '|' si existe.
    """
    if '|' not in linea:
        return convertir_mayusculas_a_minusculas(linea)
    
    # Dividir por el separador '|'
    partes = linea.split('|', 1)
    izquierda = partes[0]
    derecha = partes[1] if len(partes) > 1 else ''
    
    # Aplicar conversión a ambas partes
    izquierda_convertida = convertir_mayusculas_a_minusculas(izquierda)
    derecha_convertida = convertir_mayusculas_a_minusculas(derecha)
    
    # Reconstruir la línea
    return f"{izquierda_convertida} | {derecha_convertida}"

def procesar_archivo(ruta_archivo):
    print(f"\n--- Procesando: {ruta_archivo} ---")
    ruta_utf8 = convertir_a_utf8(ruta_archivo)
    with open(ruta_utf8, 'r', encoding='utf-8') as f:
        contenido = f.read()
    contenido = limpiar_ruido(contenido)
    contenido = normalizar_espacios_y_saltos(contenido)
    
    # Eliminar puntos finales de cada frase
    lineas_temp = contenido.splitlines()
    lineas_sin_puntos = [eliminar_puntos_finales_en_linea(linea) for linea in lineas_temp]
    contenido = '\n'.join(lineas_sin_puntos)
    
    # Convertir a minúsculas los textos completamente en mayúsculas
    lineas_temp = contenido.splitlines()
    lineas_mayusculas_convertidas = [procesar_mayusculas_en_linea(linea) for linea in lineas_temp]
    contenido = '\n'.join(lineas_mayusculas_convertidas)
    
    lineas = contenido.splitlines()
    lineas = eliminar_vacios_y_duplicados(lineas)
    sin_pipe, total_pares, alineados = analizar_separador(lineas)
    tasa = calcular_tasa_alineacion(alineados, total_pares)
    
    if sin_pipe:
        print(f"\n⚠️ Se encontraron {len(sin_pipe)} pares sin el separador '|':")
        for num, linea in sin_pipe[:10]:
            preview = linea[:80] + "..." if len(linea) > 80 else linea
            print(f"  Par {num}: {preview}")
        if len(sin_pipe) > 10:
            print(f"  ... y {len(sin_pipe)-10} pares más.")
    else:
        print("\n✓ Todos los pares contienen el separador '|'.")
    
    guardar = input("\n¿Guardar el archivo limpio (con pares únicos y normalizados)? (s/n): ").lower()
    if guardar == 's':
        base, ext = os.path.splitext(ruta_archivo)
        ruta_limpio = f"{base}_limpio{ext}"
        with open(ruta_limpio, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lineas))
        print(f"✓ Archivo limpio guardado en: {ruta_limpio}")
    
    return {
        'total_pares': total_pares,
        'alineados': alineados,
        'tasa': tasa,
        'sin_pipe': sin_pipe
    }

# ------------------------------------------------------------
# NUEVA FUNCIÓN: seleccionar archivo mediante directorio o ruta directa
# ------------------------------------------------------------
def listar_txt_en_directorio(directorio):
    """Devuelve lista de archivos .txt en el directorio dado."""
    try:
        archivos = [f for f in os.listdir(directorio) if f.lower().endswith('.txt')]
        return sorted(archivos)
    except FileNotFoundError:
        return []

def elegir_archivo_de_directorio(directorio):
    """Muestra menú con archivos .txt de un directorio y retorna la ruta completa del elegido."""
    archivos = listar_txt_en_directorio(directorio)
    if not archivos:
        print(f"No se encontraron archivos .txt en el directorio: {directorio}")
        return None
    print(f"\nArchivos .txt en '{directorio}':")
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
    """
    Menú principal para seleccionar archivo:
    1. Ingresar ruta de un directorio y elegir archivo de la lista.
    2. Ingresar ruta directa de un archivo .txt.
    3. Salir.
    """
    while True:
        print("\n--- SELECCIÓN DE ARCHIVO ---")
        print("1. Especificar un DIRECTORIO y elegir un archivo .txt de la lista")
        print("2. Ingresar la RUTA DIRECTA de un archivo .txt")
        print("3. Salir del programa")
        opcion = input("Elige una opción (1/2/3): ").strip()
        
        if opcion == '1':
            ruta_dir = input("Ingresa la ruta del directorio: ").strip()
            ruta_dir = os.path.expanduser(ruta_dir)
            if not os.path.isdir(ruta_dir):
                print("Error: la ruta no es un directorio válido.")
                continue
            archivo_elegido = elegir_archivo_de_directorio(ruta_dir)
            if archivo_elegido:
                return archivo_elegido
            else:
                print("No se seleccionó ningún archivo.")
        
        elif opcion == '2':
            ruta_archivo = input("Ingresa la ruta completa del archivo .txt: ").strip()
            ruta_archivo = os.path.expanduser(ruta_archivo)
            if os.path.isfile(ruta_archivo) and ruta_archivo.lower().endswith('.txt'):
                return ruta_archivo
            else:
                print("Error: la ruta no es válida o no es un archivo .txt.")
        
        elif opcion == '3':
            return None
        
        else:
            print("Opción no válida. Intenta de nuevo.")

# ------------------------------------------------------------
# Main
# ------------------------------------------------------------
def main():
    print("=== ALGORITMO DE LIMPIEZA Y ALINEACIÓN DE TEXTOS ===")
    print("Cada línea del archivo debe representar un par (texto1 | texto2).")
    while True:
        archivo = seleccionar_archivo()
        if archivo is None:
            print("Saliendo del programa.")
            break
        procesar_archivo(archivo)

if __name__ == "__main__":
    main()