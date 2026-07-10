"""
extraer_texto_adaptativo.py
═══════════════════════════════════════════════════════════════════════════════

Detecta automáticamente la estructura de cada página y aplica la estrategia
óptima de extracción. Funciona con documentos completos de múltiples secciones.

Características:
  • Detección automática de estructura (lineal/tabular/mixto)
  • Generación de reporte detallado por página
  • Manejo robusto de errores
  • Logs de debugging

Uso:
    python extraer_texto_adaptativo.py documento.pdf
    
Salida:
    → documento_EXTRAIDO.txt
    → documento_REPORTE.txt (análisis de estructura)
═══════════════════════════════════════════════════════════════════════════════
"""

import sys
import re
import pdfplumber
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Tuple
from dataclasses import dataclass


# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN GLOBAL
# ═══════════════════════════════════════════════════════════════════════════

UMBRAL_SHUAR = 9.0      # Tamaño que separa texto más grande (posibles títulos) del texto normal
UMBRAL_TITULO = 13.0    # Tamaños mayores son títulos
TOLERANCIA_Y = 3        # Píxeles de tolerancia para agrupar líneas
MARGEN_BBOX = 5         # Margen para detección de áreas


# ═══════════════════════════════════════════════════════════════════════════
# CLASES DE DATOS
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class AnalisisPagina:
    """Resultado del análisis de estructura de una página."""
    numero: int
    tipo_estructura: str  # 'lineal', 'tabular', 'mixto'
    num_tablas: int
    num_columnas: int
    num_palabras: int
    densidad: float
    tamaños_fuente: Dict[float, int]
    confianza: float  # 0-1, qué tan seguro está el clasificador


@dataclass
class ContenidoBilingue:
    """Contenido extraído de una página."""
    numero_pagina: int
    texto: str
    tipo_estructura: str


# ═══════════════════════════════════════════════════════════════════════════
# UTILIDADES
# ═══════════════════════════════════════════════════════════════════════════

def clasificar_por_tamano(size: float) -> str:
    """Clasifica una palabra según su tamaño de fuente."""
    if size >= UMBRAL_TITULO:
        return "titulo"
    elif size >= UMBRAL_SHUAR:
        return "texto_grande"
    else:
        return "texto_normal"


def limpiar_texto(texto: str) -> str:
    """Limpieza general de texto extraído."""
    # Eliminar marcadores de página [ 33 ]
    texto = re.sub(r'\[\s*\d+\s*\]', '', texto)
    
    # Normalizar espacios
    texto = re.sub(r'[ \t]+', ' ', texto)
    texto = re.sub(r'\n{3,}', '\n\n', texto)
    
    # Eliminar líneas muy cortas (probables artefactos)
    lineas = texto.split('\n')
    lineas_limpias = [l for l in lineas if len(l.strip()) > 2 or l.strip() == '']
    
    return '\n'.join(lineas_limpias).strip()





# ═══════════════════════════════════════════════════════════════════════════
# ANÁLISIS DE ESTRUCTURA
# ═══════════════════════════════════════════════════════════════════════════

def analizar_estructura_pagina(pagina, num_pagina: int) -> AnalisisPagina:
    """
    Analiza una página para determinar su tipo de estructura.
    
    Returns:
        AnalisisPagina con toda la información del análisis
    """
    
    # 1. Extraer información básica
    words = pagina.extract_words(extra_attrs=["size"])
    bbox = pagina.bbox
    area_total = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])
    
    # 2. Detectar tablas
    tablas = pagina.extract_tables()
    num_tablas = len([t for t in tablas if t and len(t) > 2])
    
    # 3. Analizar distribución de columnas
    if words:
        posiciones_x = [w['x0'] for w in words]
        # Redondear a grupos de 50px para detectar columnas
        grupos_x = set(round(x / 50) * 50 for x in posiciones_x)
        num_columnas = len(grupos_x)
    else:
        num_columnas = 0
    
    # 4. Calcular densidad de contenido
    num_palabras = len(words)
    densidad = num_palabras / area_total if area_total > 0 else 0
    
    # 5. Analizar tamaños de fuente
    tamaños = Counter()
    for w in words:
        size = round(float(w.get('size', 0)), 1)
        tamaños[size] += 1
    
    # 6. CLASIFICACIÓN DE ESTRUCTURA
    # Reglas de clasificación con scores
    score_tabular = 0
    score_lineal = 0
    
    # Evidencia de estructura tabular
    if num_tablas > 0:
        score_tabular += 40
    if num_columnas >= 3:
        score_tabular += 30
    if densidad > 0.003:  # Alta densidad = contenido compacto (tablas)
        score_tabular += 20
    
    # Evidencia de estructura lineal
    if num_columnas <= 2:
        score_lineal += 30
    if densidad < 0.002:  # Baja densidad = párrafos espaciados
        score_lineal += 30
    if num_tablas == 0:
        score_lineal += 40
    
    # Determinar tipo
    if score_tabular > score_lineal + 20:
        tipo = 'tabular'
        confianza = min(score_tabular / 100, 1.0)
    elif score_lineal > score_tabular + 20:
        tipo = 'lineal'
        confianza = min(score_lineal / 100, 1.0)
    else:
        tipo = 'mixto'
        confianza = 0.5
    
    return AnalisisPagina(
        numero=num_pagina,
        tipo_estructura=tipo,
        num_tablas=num_tablas,
        num_columnas=num_columnas,
        num_palabras=num_palabras,
        densidad=densidad,
        tamaños_fuente=dict(tamaños),
        confianza=confianza
    )


# ═══════════════════════════════════════════════════════════════════════════
# ESTRATEGIAS DE EXTRACCIÓN
# ═══════════════════════════════════════════════════════════════════════════

def extraer_lineal(pagina, num_pagina: int) -> ContenidoBilingue:
    """
    Estrategia para páginas con texto lineal (párrafos consecutivos).
    Extrae todo el texto sin diferenciación de idioma.
    """
    words = pagina.extract_words(extra_attrs=["size"])

    # Agrupar por línea (posición Y)
    lineas = defaultdict(lambda: {'texto': [], 'titulo': []})

    for w in words:
        size = float(w.get('size', 0))
        y_key = round(w['top'] / TOLERANCIA_Y) * TOLERANCIA_Y
        if size >= UMBRAL_TITULO:
            lineas[y_key]['titulo'].append(w['text'])
        else:
            lineas[y_key]['texto'].append(w['text'])

    texto_completo = []

    for y_key in sorted(lineas.keys()):
        linea = lineas[y_key]

        if linea['titulo']:
            titulo = ' '.join(linea['titulo'])
            texto_completo.append(f"\n{titulo}")

        texto_linea = ' '.join(linea['texto']).strip()
        if texto_linea:
            texto_completo.append(texto_linea)

    return ContenidoBilingue(
        numero_pagina=num_pagina,
        texto='\n'.join(texto_completo),
        tipo_estructura='lineal'
    )


def extraer_tabular(pagina, num_pagina: int) -> ContenidoBilingue:
    """
    Estrategia para páginas con tablas.
    Extrae todo el texto sin diferenciación de idioma.
    """
    words = pagina.extract_words(extra_attrs=["size"])

    # Agrupar por línea con más tolerancia (las tablas tienen espaciado irregular)
    lineas = defaultdict(list)

    for w in words:
        y_key = round(w['top'] / 5) * 5
        lineas[y_key].append(w)

    texto_completo = []

    for y_key in sorted(lineas.keys()):
        fila = sorted(lineas[y_key], key=lambda w: w['x0'])
        if not fila:
            continue

        # Separar segmentos por cambios grandes en la coordenada X
        segmentos_fila = []
        segmento_actual = []
        ultimo_final = None

        for w in fila:
            if segmento_actual and ultimo_final is not None and w['x0'] - ultimo_final > 50:
                segmentos_fila.append(segmento_actual)
                segmento_actual = []
            segmento_actual.append(w)
            ultimo_final = w['x1']

        if segmento_actual:
            segmentos_fila.append(segmento_actual)

        for segmento in segmentos_fila:
            texto_segmento = ' '.join(w['text'] for w in segmento).strip()
            if not texto_segmento:
                continue

            if any(float(w.get('size', 0)) >= UMBRAL_TITULO for w in segmento):
                texto_completo.append(f"\n{texto_segmento}")
            else:
                texto_completo.append(texto_segmento)

    return ContenidoBilingue(
        numero_pagina=num_pagina,
        texto='\n'.join(texto_completo),
        tipo_estructura='tabular'
    )


def extraer_mixto(pagina, num_pagina: int) -> ContenidoBilingue:
    """
    Estrategia híbrida para páginas con estructura mixta.
    Usa un enfoque conservador que funciona en ambos casos.
    """
    # Por ahora, usar la estrategia tabular que es más robusta
    return extraer_tabular(pagina, num_pagina)


# ═══════════════════════════════════════════════════════════════════════════
# PROCESADOR PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════

def procesar_pdf_adaptativo(ruta_pdf: str) -> Tuple[str, List[AnalisisPagina]]:
    """
    Procesa un PDF completo con detección automática de estructura.
    
    Returns:
        (texto_combinado, lista_analisis)
    """
    
    contenido_total = []
    analisis_paginas = []
    
    with pdfplumber.open(ruta_pdf) as pdf:
        total_paginas = len(pdf.pages)
        
        print(f"\n{'═'*70}")
        print(f" Procesando: {Path(ruta_pdf).name}")
        print(f" Total de páginas: {total_paginas}")
        print(f"{'═'*70}\n")
        
        for num_pag, pagina in enumerate(pdf.pages, start=1):
            print(f" [{num_pag:3d}/{total_paginas}] Analizando estructura...", end='')
            
            # 1. ANÁLISIS DE ESTRUCTURA
            analisis = analizar_estructura_pagina(pagina, num_pag)
            analisis_paginas.append(analisis)
            
            print(f" → {analisis.tipo_estructura.upper():8s} "
                  f"(confianza: {analisis.confianza:.0%})", end='')
            
            # 2. SELECCIONAR Y APLICAR ESTRATEGIA
            try:
                if analisis.tipo_estructura == 'lineal':
                    contenido = extraer_lineal(pagina, num_pag)
                elif analisis.tipo_estructura == 'tabular':
                    contenido = extraer_tabular(pagina, num_pag)
                else:  # mixto
                    contenido = extraer_mixto(pagina, num_pag)
                
                # 3. AÑADIR ENCABEZADO DE PÁGINA
                contenido_total.append(f"\n{'─'*70}\nPÁGINA {num_pag}\n{'─'*70}\n")
                
                # 4. AGREGAR TEXTO EXTRAÍDO
                contenido_total.append(contenido.texto)
                
            except Exception as e:
                print(f" ERROR: {str(e)[:40]}")
                contenido_total.append(f"\n[ERROR EN PÁGINA {num_pag}]\n")
    
    # 5. CONSOLIDAR Y LIMPIAR
    texto_combinado = limpiar_texto('\n'.join(contenido_total))
    
    return texto_combinado, analisis_paginas


# ═══════════════════════════════════════════════════════════════════════════
# GENERACIÓN DE REPORTES
# ═══════════════════════════════════════════════════════════════════════════

def generar_reporte(analisis_paginas: List[AnalisisPagina], ruta_pdf: Path) -> str:
    """Genera un reporte detallado del análisis de estructura."""
    
    lineas = [
        "═" * 80,
        "  REPORTE DE ANÁLISIS DE ESTRUCTURA",
        "═" * 80,
        f"\nDocumento: {ruta_pdf.name}",
        f"Total de páginas: {len(analisis_paginas)}\n",
        "─" * 80,
    ]
    
    # Resumen por tipo
    tipos = Counter(a.tipo_estructura for a in analisis_paginas)
    lineas.append("\n DISTRIBUCIÓN DE ESTRUCTURAS:\n")
    for tipo, cantidad in tipos.most_common():
        porcentaje = (cantidad / len(analisis_paginas)) * 100
        lineas.append(f"  {tipo.capitalize():10s} : {cantidad:3d} páginas ({porcentaje:5.1f}%)")
    
    # Detalle por página
    lineas.append("\n" + "─" * 80)
    lineas.append("\n DETALLE POR PÁGINA:\n")
    lineas.append(f"{'Pág':>4} | {'Tipo':>8} | {'Conf':>5} | {'Tablas':>6} | "
                  f"{'Cols':>4} | {'Palabras':>8} | {'Densidad':>9}")
    lineas.append("─" * 80)
    
    for a in analisis_paginas:
        lineas.append(
            f"{a.numero:4d} | {a.tipo_estructura:>8s} | {a.confianza:>4.0%} | "
            f"{a.num_tablas:>6d} | {a.num_columnas:>4d} | {a.num_palabras:>8d} | "
            f"{a.densidad:>9.6f}"
        )
    
    # Tamaños de fuente más comunes
    lineas.append("\n" + "─" * 80)
    lineas.append("\n TAMAÑOS DE FUENTE DETECTADOS:\n")
    
    todos_tamaños = Counter()
    for a in analisis_paginas:
        todos_tamaños.update(a.tamaños_fuente)
    
    for size, count in sorted(todos_tamaños.items(), key=lambda x: x[1], reverse=True)[:10]:
        clasificacion = clasificar_por_tamano(size)
        lineas.append(f"  {size:5.1f}pt → {count:6d} palabras ({clasificacion})")
    
    lineas.append("\n" + "═" * 80)
    
    return '\n'.join(lineas)


# ═══════════════════════════════════════════════════════════════════════════
# FUNCIÓN PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════

def buscar_pdf_en_fuentes(nombre_archivo):
    """
    Busca un PDF en todos los subdirectorios de Fuentes_de_datos/.
    
    Args:
        nombre_archivo: Nombre del PDF a buscar (ej: 'archivo.pdf')
    
    Returns:
        Path al archivo encontrado, o None si no existe
    """
    fuentes = Path("Fuentes_de_datos")
    
    if not fuentes.exists():
        return None
    
    # Buscar el archivo en todos los subdirectorios
    resultados = list(fuentes.glob(f"**/{nombre_archivo}"))
    
    return resultados if resultados else None


def seleccionar_pdf(pdfs):
    """
    Muestra un menú para seleccionar un PDF de una lista.
    
    Args:
        pdfs: Lista de rutas Path a archivos PDF
    
    Returns:
        Path al archivo seleccionado
    """
    print("\n PDFs encontrados:\n")
    for i, pdf in enumerate(pdfs, 1):
        tamano = pdf.stat().st_size / (1024*1024)  # Tamaño en MB
        print(f"  {i}. {pdf.name:40s} ({pdf.parent.name:15s}) {tamano:.2f} MB")
    
    while True:
        try:
            seleccion = input("\n Ingresa el número del archivo a procesar: ").strip()
            indice = int(seleccion) - 1
            if 0 <= indice < len(pdfs):
                return pdfs[indice]
            else:
                print(f" Número inválido. Por favor, ingresa un número entre 1 y {len(pdfs)}")
        except ValueError:
            print(" Ingresa un número válido")


def main():
    """Punto de entrada principal del script."""
    
    ruta_pdf = None
    
    # Obtener ruta del PDF
    if len(sys.argv) > 1:
        ruta_input = Path(sys.argv[1])
        
        # Si es una ruta completa existente, usarla directamente
        if ruta_input.is_absolute() and ruta_input.exists():
            ruta_pdf = ruta_input
            print(f" Usando PDF: {ruta_pdf}")
        
        # Si es un nombre de archivo (sin barras), buscar en Fuentes_de_datos
        elif "/" not in str(sys.argv[1]) and "\\" not in str(sys.argv[1]):
            nombre_archivo = sys.argv[1]
            resultados = buscar_pdf_en_fuentes(nombre_archivo)
            
            if resultados:
                if len(resultados) == 1:
                    ruta_pdf = resultados[0]
                    print(f"  Encontrado: {ruta_pdf}")
                else:
                    # Múltiples resultados, permitir selección
                    print(f"\n  Se encontraron {len(resultados)} archivos con ese nombre:")
                    ruta_pdf = seleccionar_pdf(resultados)
                    print(f"\n Seleccionado: {ruta_pdf}")
            else:
                # No encontrado, mostrar PDFs disponibles
                fuentes = Path("Fuentes_de_datos")
                if fuentes.exists():
                    pdfs_disponibles = sorted(list(fuentes.glob("**/*.pdf")))
                    if pdfs_disponibles:
                        print(f"\n ERROR: '{nombre_archivo}' no encontrado en Fuentes_de_datos")
                        print("\n PDFs disponibles:")
                        ruta_pdf = seleccionar_pdf(pdfs_disponibles)
                        print(f"\n Seleccionado: {ruta_pdf}")
                    else:
                        print(" ERROR: No hay PDFs en Fuentes_de_datos")
                        sys.exit(1)
                else:
                    print(" ERROR: Directorio 'Fuentes_de_datos' no existe")
                    sys.exit(1)
        
        # Si es una ruta relativa/directorio
        elif ruta_input.is_dir():
            pdfs = sorted(list(ruta_input.glob("**/*.pdf")))
            if not pdfs:
                print(f" ERROR: No se encontró ningún PDF en: {ruta_input}")
                sys.exit(1)
            
            if len(pdfs) == 1:
                ruta_pdf = pdfs[0]
                print(f"  Usando: {ruta_pdf}")
            else:
                ruta_pdf = seleccionar_pdf(pdfs)
                print(f"\n Seleccionado: {ruta_pdf}")
        else:
            # Intenta como ruta relativa o completa
            if ruta_input.exists():
                ruta_pdf = ruta_input
                print(f"  Usando: {ruta_pdf}")
            else:
                print(f" ERROR: No se encontró: {ruta_input}")
                sys.exit(1)
    
    else:
        # Si no hay argumentos, buscar en Fuentes_de_datos
        fuentes = Path("Fuentes_de_datos")
        if not fuentes.exists():
            print(" ERROR: Directorio 'Fuentes_de_datos' no existe")
            print("\nUso: python extraer_bilingue_adaptativo.py nombre_archivo.pdf")
            sys.exit(1)
        
        pdfs = sorted(list(fuentes.glob("**/*.pdf")))
        if not pdfs:
            print(" ERROR: No hay PDFs en Fuentes_de_datos")
            sys.exit(1)
        
        ruta_pdf = seleccionar_pdf(pdfs)
        print(f"\n Seleccionado: {ruta_pdf}")
    
    # Validar que se encontró un PDF
    if ruta_pdf is None or not ruta_pdf.exists():
        print(f" ERROR: No se encontró el archivo: {ruta_pdf}")
        sys.exit(1)
    
    # Procesar PDF
    try:
        texto_combinado, analisis = procesar_pdf_adaptativo(str(ruta_pdf))
    except Exception as e:
        print(f"\n ERROR FATAL: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Generar archivos de salida
    directorio_salida = Path("Datos")
    directorio_salida.mkdir(parents=True, exist_ok=True)
    
    base = ruta_pdf.stem.replace(" ", "_")
    
    # Archivo de texto único
    archivo_salida = directorio_salida / f"{base}_EXTRAIDO.txt"
    archivo_reporte = directorio_salida / f"{base}_REPORTE.txt"
    
    # Encabezado
    #encabezado = (
    #    "═" * 80 + "\n"
    #    "  CONTENIDO EXTRAÍDO DEL PDF\n"
    #    f"  Documento: {ruta_pdf.name}\n"
    #    f"  Páginas procesadas: {len(analisis)}\n"
    ##    "  Extracción: Adaptativa con detección automática de estructura\n"
    #    "═" * 80 + "\n\n"
    #)
    
    # Guardar archivo
    print(f"\n{'═'*70}")
    print(" Guardando archivo...")
    print(f"{'═'*70}\n")
    
    #encabezado + 

    archivo_salida.write_text(texto_combinado, encoding='utf-8')
    print(f" {archivo_salida.name:50s} {archivo_salida.stat().st_size:>10,} bytes")
    
    # Generar y guardar reporte
    reporte = generar_reporte(analisis, ruta_pdf)
    archivo_reporte.write_text(reporte, encoding='utf-8')
    print(f" {archivo_reporte.name:50s} {archivo_reporte.stat().st_size:>10,} bytes")
    
    # Estadísticas finales
    print(f"\n{'═'*70}")
    print(" ESTADÍSTICAS FINALES")
    print(f"{'═'*70}")
    
    tipos = Counter(a.tipo_estructura for a in analisis)
    for tipo, cantidad in sorted(tipos.items()):
        print(f"  Páginas {tipo:8s} : {cantidad:3d}")
    
    print(f"\n  Caracteres totales   : {len(texto_combinado):>10,}")
    print(f"  Palabras totales     : {len(texto_combinado.split()):>10,}")
    
    print(f"\n{'═'*70}")
    print(" Extracción completada exitosamente")
    print(f"{'═'*70}\n")


if __name__ == "__main__":
    main()