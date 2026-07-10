import easyocr
import cv2
import numpy as np
import os
import re
import tkinter as tk
from tkinter import filedialog
from collections import defaultdict

def preprocesar_imagen(ruta_imagen):
    img = cv2.imread(ruta_imagen)
    if img is None:
        return None
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Escalar para mejorar detalle
    h, w = gray.shape
    if w < 1500:
        scale = 1500 / w
        new_w = int(w * scale)
        new_h = int(h * scale)
        gray = cv2.resize(gray, (new_w, new_h), interpolation=cv2.INTER_CUBIC)
    # Filtro bilateral para reducir ruido
    gray = cv2.bilateralFilter(gray, 9, 75, 75)
    # Umbral adaptativo
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 15, 2)
    return thresh

def extraer_tabla_con_coordenadas(ruta_imagen, tolerancia_y=35):
    # Forzar CPU
    reader = easyocr.Reader(['es', 'en'], gpu=False, verbose=False)
    img_proc = preprocesar_imagen(ruta_imagen)
    if img_proc is None:
        return "No se pudo leer la imagen"
    resultado = reader.readtext(img_proc, detail=1, paragraph=False)
    if not resultado:
        return "No se detectaron palabras"
    
    # Obtener coordenadas
    datos = []
    for coords, texto, conf in resultado:
        xs = [p[0] for p in coords]
        ys = [p[1] for p in coords]
        x_center = np.mean(xs)
        y_center = np.mean(ys)
        # Limpiar caracteres extraños básicos
        texto = re.sub(r'[^\w\sáéíóúñüÁÉÍÓÚÑÜ\,\.\;\(\)\¿\?\!\¡]', '', texto)
        if len(texto.strip()) > 1:
            datos.append((y_center, x_center, texto.strip()))
    
    if not datos:
        return "No hay palabras válidas"
    
    # Ordenar por Y
    datos.sort(key=lambda p: p[0])
    
    # Agrupar filas por diferencia en Y
    filas = []
    fila_actual = []
    ultima_y = datos[0][0]
    for y, x, texto in datos:
        if abs(y - ultima_y) <= tolerancia_y:
            fila_actual.append((x, texto))
        else:
            fila_actual.sort(key=lambda p: p[0])
            filas.append([p[1] for p in fila_actual])
            fila_actual = [(x, texto)]
            ultima_y = y
    if fila_actual:
        fila_actual.sort(key=lambda p: p[0])
        filas.append([p[1] for p in fila_actual])
    
    # Detectar número de columnas (usar la fila más ancha)
    max_cols = max(len(fila) for fila in filas)
    # Si la primera fila tiene menos de 4 columnas, puede ser un título
    if len(filas[0]) < 4 and len(filas) > 1:
        # Combinar las dos primeras filas si son títulos
        if len(filas[1]) >= 4:
            filas[0] = filas[1][:4]  # reemplazar con la fila que tiene más columnas
    
    # Reconstruir tabla Markdown
    markdown = "| " + " | ".join([f"Columna{i+1}" for i in range(max_cols)]) + " |\n"
    markdown += "|" + "---|" * max_cols + "\n"
    for fila in filas:
        while len(fila) < max_cols:
            fila.append("")
        markdown += "| " + " | ".join(fila) + " |\n"
    return markdown

# El resto del código (seleccionar imágenes, main) se mantiene igual, pero forzando CPU

def extraer_texto_normal(ruta_imagen):
    """OCR simple sin estructura de tabla."""
    try:
        import torch
        use_gpu = torch.cuda.is_available()
    except:
        use_gpu = False
    reader = easyocr.Reader(['es', 'en'], gpu=use_gpu, verbose=False)
    resultado = reader.readtext(ruta_imagen, detail=0, paragraph=True)
    return '\n'.join(resultado)

def seleccionar_imagenes():
    root = tk.Tk()
    root.withdraw()
    rutas = filedialog.askopenfilenames(
        title="Seleccione imágenes (tablas o texto)",
        filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.bmp *.tiff")]
    )
    return rutas

def main():
    print("=== OCR AVANZADO: RECONSTRUCCIÓN DE TABLAS (GPU si disponible) ===")
    rutas = seleccionar_imagenes()
    if not rutas:
        print("No se seleccionó ninguna imagen.")
        return
    
    texto_total = ""
    for i, ruta in enumerate(rutas, 1):
        print(f"Procesando ({i}/{len(rutas)}): {os.path.basename(ruta)}")
        texto = extraer_tabla_con_coordenadas(ruta)
        # Si la tabla parece muy dispersa, usar modo normal
        lineas = texto.split('\n')
        if len(lineas) < 3 or (len(lineas[0].split('|')) < 3 if lineas else True):
            texto = extraer_texto_normal(ruta)
        bloque = f"--- {os.path.basename(ruta)} ---\n{texto}\n\n"
        texto_total += bloque
    
    nombre_base = input("\nNombre del archivo de salida (sin extensión): ").strip()
    if not nombre_base:
        nombre_base = "tabla_extraida"
    archivo_salida = f"{nombre_base}.txt"
    
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        f.write(texto_total)
    
    print(f"\n✅ Documento guardado: {archivo_salida}")

if __name__ == "__main__":
    main()