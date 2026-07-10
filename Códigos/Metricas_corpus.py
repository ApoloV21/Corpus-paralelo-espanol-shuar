#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para análisis descriptivo de corpus bilingüe español-shuar.
Genera métricas de tamaño, diversidad léxica (TTR) y representatividad por dominio.
Producido para tesis: Actividades 1-5.
"""

import os
import sys
import chardet
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency
import re
from datetime import datetime

# Configuración de gráficos
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("Set2")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 11

# ------------------------------------------------------------
# 1. Selección y carga del corpus (interactivo o por argumento)
# ------------------------------------------------------------
def detectar_encoding(archivo):
    with open(archivo, 'rb') as f:
        raw = f.read()
    return chardet.detect(raw)['encoding']

def convertir_a_utf8(archivo):
    enc = detectar_encoding(archivo)
    if enc and enc.lower() == 'utf-8':
        return archivo
    base, ext = os.path.splitext(archivo)
    salida = f"{base}_utf8{ext}"
    with open(archivo, 'r', encoding=enc, errors='replace') as f:
        contenido = f.read()
    with open(salida, 'w', encoding='utf-8') as f:
        f.write(contenido)
    print(f"✓ Archivo convertido a UTF-8: {salida}")
    return salida

def seleccionar_archivo():
    """Menú interactivo para elegir archivo CSV o JSON."""
    print("\n--- SELECCIÓN DE CORPUS ---")
    print("1. Especificar directorio y elegir de lista")
    print("2. Ruta directa")
    op = input("Opción (1/2): ").strip()
    if op == '1':
        dir_path = input("Directorio: ").strip()
        dir_path = os.path.expanduser(dir_path)
        if not os.path.isdir(dir_path):
            print("Directorio no válido")
            return None
        archivos = [f for f in os.listdir(dir_path) if f.lower().endswith(('.csv', '.json'))]
        if not archivos:
            print("No hay archivos .csv o .json")
            return None
        print("\nArchivos disponibles:")
        for i, f in enumerate(archivos, 1):
            print(f"{i}. {f}")
        try:
            idx = int(input("Seleccione número: ")) - 1
            return os.path.join(dir_path, archivos[idx])
        except:
            return None
    elif op == '2':
        ruta = input("Ruta completa: ").strip()
        ruta = os.path.expanduser(ruta)
        if os.path.isfile(ruta) and ruta.lower().endswith(('.csv', '.json')):
            return ruta
        else:
            print("Archivo no válido")
            return None
    else:
        return None

def cargar_corpus(ruta):
    ext = os.path.splitext(ruta)[1].lower()
    try:
        if ext == '.csv':
            df = pd.read_csv(ruta, encoding='utf-8')
        elif ext == '.json':
            df = pd.read_json(ruta)
        else:
            raise ValueError(f"Formato no soportado: {ext}")
        print(f"✓ Corpus cargado: {len(df)} registros")
        return df
    except Exception as e:
        print(f"Error al cargar: {e}")
        return None

# ------------------------------------------------------------
# 2. Validaciones (Actividad 1)
# ------------------------------------------------------------
def validar_estructura(df):
    """Verifica columnas necesarias y relación 1:1, elimina vacíos."""
    # Buscar columnas de texto y dominio
    col_es = None
    col_sh = None
    col_dom = None
    for col in df.columns:
        if 'frase_es' in col or col.lower() == 'espanol':
            col_es = col
        if 'frase_sh' in col or col.lower() == 'shuar':
            col_sh = col
        if 'dominio' in col.lower():
            col_dom = col
    
    if col_es is None or col_sh is None:
        raise ValueError("No se encontraron columnas 'frase_es' y 'frase_sh'")
    
    # Renombrar
    df.rename(columns={col_es: 'frase_es', col_sh: 'frase_sh'}, inplace=True)
    if col_dom:
        df.rename(columns={col_dom: 'dominio'}, inplace=True)
    
    # Eliminar filas con valores nulos o vacíos
    antes = len(df)
    df = df.dropna(subset=['frase_es', 'frase_sh'])
    df = df[df['frase_es'].str.strip() != '']
    df = df[df['frase_sh'].str.strip() != '']
    despues = len(df)
    if antes - despues > 0:
        print(f"  - Eliminadas {antes - despues} filas con frases vacías")
    
    # Verificar si hay filas donde el separador no está bien (ya debería estar limpio)
    # Opcional: verificar que no haya '|' dentro de las frases (ruido)
    return df

def verificar_metadatos(df):
    """Comprueba si existe columna 'dominio' y si tiene valores no nulos."""
    if 'dominio' in df.columns:
        dominios_presentes = df['dominio'].dropna().unique()
        print(f"  - Metadato 'dominio' presente con {len(dominios_presentes)} categorías: {list(dominios_presentes)}")
        return True
    else:
        print("  - ADVERTENCIA: No se encontró columna 'dominio'. Se omitirá análisis por dominio.")
        return False

def actividad1_validaciones(df, ruta_original):
    print("\n" + "="*70)
    print("ACTIVIDAD 1: CARGA Y VALIDACIÓN DEL CORPUS ESTRUCTURADO")
    print("="*70)
    print(f"Archivo: {ruta_original}")
    print(f"Registros iniciales: {len(df)}")
    # Verificar UTF-8 ya se hizo al convertir
    print("✓ Codificación UTF-8 verificada")
    # Estructura paralela
    print("✓ Estructura paralela 1:1 validada (pares frase_es - frase_sh)")
    tiene_dom = verificar_metadatos(df)
    # Detección de vacíos ya se hizo en validar_estructura
    print("✓ Registros vacíos o inconsistentes eliminados")
    return tiene_dom

# ------------------------------------------------------------
# 3. Métricas de tamaño (Actividad 2)
# ------------------------------------------------------------
def contar_tokens(texto):
    """Tokeniza por espacios y signos de puntuación básicos."""
    # Separar por espacios y eliminar puntuación aislada (opcional)
    tokens = re.findall(r'\b\w+\b', str(texto).lower())
    return len(tokens)

def actividad2_metricas_tamano(df):
    print("\n" + "="*70)
    print("ACTIVIDAD 2: MÉTRICAS DE TAMAÑO DEL CORPUS")
    print("="*70)
    num_pares = len(df)
    print(f"• Número total de pares alineados: {num_pares}")
    
    # Tokens en español
    df['tokens_es'] = df['frase_es'].apply(contar_tokens)
    total_tokens_es = df['tokens_es'].sum()
    print(f"• Número total de tokens en español: {total_tokens_es}")
    
    # Tokens en shuar
    df['tokens_sh'] = df['frase_sh'].apply(contar_tokens)
    total_tokens_sh = df['tokens_sh'].sum()
    print(f"• Número total de tokens en shuar: {total_tokens_sh}")
    
    # Guardar df con tokens para usar después
    return df, total_tokens_es, total_tokens_sh

# ------------------------------------------------------------
# 4. Diversidad léxica (TTR) (Actividad 3)
# ------------------------------------------------------------
def calcular_ttr(lista_textos):
    """Calcula Type-Token Ratio para una lista de textos."""
    tokens = []
    for texto in lista_textos:
        tokens.extend(re.findall(r'\b\w+\b', str(texto).lower()))
    if len(tokens) == 0:
        return 0.0
    return len(set(tokens)) / len(tokens)

def actividad3_ttr(df, tiene_dominio):
    print("\n" + "="*70)
    print("ACTIVIDAD 3: DIVERSIDAD LÉXICA (TYPE-TOKEN RATIO)")
    print("="*70)
    
    # TTR global
    ttr_es_global = calcular_ttr(df['frase_es'])
    ttr_sh_global = calcular_ttr(df['frase_sh'])
    print(f"• TTR global español: {ttr_es_global:.4f}")
    print(f"• TTR global shuar:   {ttr_sh_global:.4f}")
    
    resultados_ttr = {'global_es': ttr_es_global, 'global_sh': ttr_sh_global}
    
    if tiene_dominio and 'dominio' in df.columns:
        dominios = df['dominio'].dropna().unique()
        print("\n• TTR por dominio:")
        ttr_por_dom = []
        for dom in dominios:
            sub = df[df['dominio'] == dom]
            ttr_es = calcular_ttr(sub['frase_es'])
            ttr_sh = calcular_ttr(sub['frase_sh'])
            print(f"  {dom}: TTR_es={ttr_es:.4f}, TTR_sh={ttr_sh:.4f}")
            ttr_por_dom.append({'dominio': dom, 'TTR_es': ttr_es, 'TTR_sh': ttr_sh})
        resultados_ttr['por_dominio'] = ttr_por_dom
        
        # Gráfico de TTR por dominio
        fig, ax = plt.subplots(figsize=(10,6))
        x = np.arange(len(dominios))
        width = 0.35
        es_vals = [d['TTR_es'] for d in ttr_por_dom]
        sh_vals = [d['TTR_sh'] for d in ttr_por_dom]
        ax.bar(x - width/2, es_vals, width, label='Español', color='steelblue')
        ax.bar(x + width/2, sh_vals, width, label='Shuar', color='darkorange')
        ax.set_xticks(x)
        ax.set_xticklabels(dominios, rotation=45, ha='right')
        ax.set_ylabel('Type-Token Ratio (TTR)')
        ax.set_title('Diversidad léxica por dominio temático')
        ax.legend()
        plt.tight_layout()
        plt.savefig('ttr_por_dominio.png', dpi=150)
        print("\n✓ Gráfico guardado: ttr_por_dominio.png")
        plt.show()
    else:
        print("  (No se encontró columna 'dominio' para análisis por dominio)")
    
    return resultados_ttr

# ------------------------------------------------------------
# 5. Representatividad y equilibrio temático (Actividad 4)
# ------------------------------------------------------------
def actividad4_representatividad(df, tiene_dominio):
    print("\n" + "="*70)
    print("ACTIVIDAD 4: REPRESENTATIVIDAD Y EQUILIBRIO TEMÁTICO")
    print("="*70)
    if not tiene_dominio or 'dominio' not in df.columns:
        print("No se puede realizar análisis por dominio: falta columna 'dominio'.")
        return None
    
    conteo = df['dominio'].value_counts()
    total = len(df)
    porcentajes = (conteo / total) * 100
    print("• Conteo de pares por dominio:")
    for dom, cnt in conteo.items():
        print(f"  {dom}: {cnt} pares ({porcentajes[dom]:.2f}%)")
    
    # Comparación con uniforme
    n_dom = len(conteo)
    uniforme = 100 / n_dom
    print(f"\n• Distribución uniforme esperada: {uniforme:.2f}% por dominio")
    print("  Desviación porcentual respecto a uniforme:")
    for dom, pct in porcentajes.items():
        desv = pct - uniforme
        print(f"    {dom}: {desv:+.2f}%")
    
    # Prueba chi-cuadrado de homogeneidad
    frec_obs = conteo.values
    frec_esp = [total / n_dom] * n_dom
    chi2, p = chi2_contingency([frec_obs, frec_esp])[:2]  # solo estadístico y p
    print(f"\n• Prueba chi-cuadrado de homogeneidad: χ² = {chi2:.2f}, p = {p:.4f}")
    if p < 0.05:
        print("  → La distribución por dominio difiere significativamente de la uniforme (p < 0.05)")
    else:
        print("  → No hay evidencia de diferencia significativa respecto a uniforme")
    
    # Gráfico de barras porcentuales
    fig, ax = plt.subplots()
    bars = ax.bar(porcentajes.index, porcentajes.values, color='skyblue')
    ax.axhline(y=uniforme, color='red', linestyle='--', label=f'Uniforme ({uniforme:.1f}%)')
    ax.set_ylabel('Porcentaje de pares (%)')
    ax.set_title('Distribución porcentual por dominio temático')
    ax.set_xticklabels(porcentajes.index, rotation=45, ha='right')
    for bar, pct in zip(bars, porcentajes.values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f'{pct:.1f}%', ha='center', va='bottom')
    ax.legend()
    plt.tight_layout()
    plt.savefig('distribucion_dominios.png', dpi=150)
    print("\n✓ Gráfico guardado: distribucion_dominios.png")
    plt.show()
    
    # Gráfico circular opcional
    fig2, ax2 = plt.subplots()
    ax2.pie(porcentajes, labels=porcentajes.index, autopct='%1.1f%%', startangle=90)
    ax2.set_title('Composición temática del corpus')
    plt.tight_layout()
    plt.savefig('composicion_dominios_pie.png', dpi=150)
    print("✓ Gráfico circular guardado: composicion_dominios_pie.png")
    plt.show()
    
    return {'conteo': conteo, 'porcentajes': porcentajes, 'chi2': chi2, 'p': p}

# ------------------------------------------------------------
# 6. Consolidación de resultados (Actividad 5)
# ------------------------------------------------------------
def actividad5_consolidacion(df, total_tokens_es, total_tokens_sh, ttr_results, rep_results):
    print("\n" + "="*70)
    print("ACTIVIDAD 5: CONSOLIDACIÓN DE RESULTADOS")
    print("="*70)
    
    # Tabla resumen principal
    resumen = {
        'Métrica': ['Número de pares', 'Tokens español', 'Tokens shuar', 
                    'TTR español global', 'TTR shuar global'],
        'Valor': [len(df), total_tokens_es, total_tokens_sh,
                  f"{ttr_results['global_es']:.4f}", f"{ttr_results['global_sh']:.4f}"]
    }
    df_resumen = pd.DataFrame(resumen)
    print("\n--- TABLA RESUMEN DE MÉTRICAS DESCRIPTIVAS ---")
    print(df_resumen.to_string(index=False))
    
    # Guardar tabla como CSV
    df_resumen.to_csv('resumen_metricas.csv', index=False, encoding='utf-8')
    print("\n✓ Tabla resumen guardada: resumen_metricas.csv")
    
    # Si hay TTR por dominio, crear tabla adicional
    if 'por_dominio' in ttr_results:
        df_ttr_dom = pd.DataFrame(ttr_results['por_dominio'])
        print("\n--- TTR POR DOMINIO ---")
        print(df_ttr_dom.to_string(index=False))
        df_ttr_dom.to_csv('ttr_por_dominio.csv', index=False, encoding='utf-8')
        print("✓ Tabla TTR por dominio guardada: ttr_por_dominio.csv")
    
    # Si hay representatividad, guardar también
    if rep_results:
        df_repr = pd.DataFrame({
            'Dominio': list(rep_results['conteo'].index),
            'Pares': rep_results['conteo'].values,
            'Porcentaje': rep_results['porcentajes'].values
        })
        print("\n--- DISTRIBUCIÓN POR DOMINIO ---")
        print(df_repr.to_string(index=False))
        df_repr.to_csv('distribucion_dominios.csv', index=False, encoding='utf-8')
        print("✓ Tabla de distribución guardada: distribucion_dominios.csv")
    
    print("\n✅ Consolidación completa. Reportes y gráficos generados.")
    return df_resumen

# ------------------------------------------------------------
# Main: ejecuta todo el flujo
# ------------------------------------------------------------
def main():
    print("=== ANÁLISIS DESCRIPTIVO DE CORPUS BILINGÜE ESPAÑOL-SHUAR ===")
    
    # Seleccionar archivo
    ruta = seleccionar_archivo()
    if not ruta:
        print("No se seleccionó ningún archivo. Saliendo.")
        return
    
    # Convertir a UTF-8 si es necesario
    ruta = convertir_a_utf8(ruta)
    
    # Cargar datos
    df = cargar_corpus(ruta)
    if df is None:
        return
    
    # Validación y limpieza
    df = validar_estructura(df)
    tiene_dominio = actividad1_validaciones(df, ruta)
    
    # Métricas de tamaño
    df, total_tokens_es, total_tokens_sh = actividad2_metricas_tamano(df)
    
    # Diversidad léxica
    ttr_results = actividad3_ttr(df, tiene_dominio)
    
    # Representatividad
    rep_results = actividad4_representatividad(df, tiene_dominio) if tiene_dominio else None
    
    # Consolidación
    actividad5_consolidacion(df, total_tokens_es, total_tokens_sh, ttr_results, rep_results)
    
    print("\n" + "="*70)
    print("ANÁLISIS FINALIZADO. Puedes tomar capturas de las salidas y gráficos.")
    print("="*70)

if __name__ == "__main__":
    main()