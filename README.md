# Corpus Paralelo Español–Shuar

## Construcción de un corpus paralelo español–shuar mediante técnicas de ingeniería de datos para aplicaciones de Procesamiento del Lenguaje Natural

---

## Descripción

Este repositorio contiene un corpus paralelo **Español–Shuar** construido a partir de documentos bilingües oficiales provenientes de instituciones públicas del Ecuador.

El corpus fue desarrollado como parte del proyecto de titulación:

> **Construcción de un corpus paralelo español–shuar mediante técnicas de ingeniería de datos para aplicaciones de Procesamiento del Lenguaje Natural.**

Su propósito es proporcionar un recurso lingüístico documentado, interoperable y reutilizable para investigaciones relacionadas con el Procesamiento del Lenguaje Natural (PLN) en lenguas indígenas de bajo recurso.

---

## Objetivo

Construir un corpus paralelo Español–Shuar mediante técnicas de ingeniería de datos que permita disponer de un recurso estructurado para futuras aplicaciones de procesamiento del lenguaje natural.

---

## Características del corpus

- Idiomas: Español – Shuar
- Tipo de corpus: Paralelo
- Unidad de alineación: Oración–Oración (1:1)
- Codificación: UTF-8
- Formatos disponibles:
  - CSV
  - JSON
- Dominios:
  - Educativo
  - Cultural
  - Literario
  - Médico

---

## Estadísticas generales

| Métrica | Valor |
|----------|------:|
| Documentos utilizados | 24 |
| Pares alineados | 5762 |
| Tokens (Español) | 35976 |
| Tokens (Shuar) | 22704 |
| Tasa de alineación | >90 % |

---

## Estructura del repositorio

```text
Corpus-paralelo-espanol-shuar/
│
├── Corpus/
│   ├── Corpus-paralelo-espanol-shuar.csv
│   ├── Corpus-paralelo-espanol-shuar.json
|
├── Códigos/
│   ├── Creacion_corpus.py
│   ├── Detectar_duplicados.py
│   ├── Extraer_imagenes_ocr.py
│   ├── Extraer_texto_adaptativo.py
│   └── Limpieza_normalizacion.py
│   └── Metricas_corpus.py
|
├── README.md
├── SCHEMA.md
├── LICENSE
```

---

## Estructura del corpus

Cada registro representa un par de oraciones alineadas.

| Campo | Descripción |
|--------|-------------|
| id | Identificador único |
| frase_es | Oración en español |
| frase_sh | Oración en shuar |
| dominio | Dominio temático |
| fecha | Fecha de incorporación |
| origen | Documento fuente |

Ejemplo:

| id | frase_es | frase_sh | dominio |
|----|-----------|-----------|----------|
|1|Buenos días|Penker pujustin|Educativo|

---

## Metodología de construcción

La construcción del corpus se desarrolló en cuatro fases:

1. Definición del corpus.
2. Recolección de documentos bilingües.
3. Limpieza, normalización y alineación.
4. Cálculo de métricas descriptivas.

---

## Requisitos

Python 3.12 o superior.

---

## Dependencias principales

- pdfplumber
- easyocr
- opencv-python
- pandas
- numpy
- chardet
- regex

---

## Principios FAIR

El corpus fue diseñado considerando los principios FAIR:

- **Findable**: estructura documentada y metadatos.
- **Accessible**: formatos abiertos (CSV y JSON).
- **Interoperable**: codificación UTF-8 y esquema documentado.
- **Reusable**: documentación técnica y licencia abierta.

---

## Posibles aplicaciones

Este recurso puede utilizarse en investigaciones relacionadas con:

- Traducción automática
- Modelos de lenguaje
- Recuperación de información
- Sistemas de búsqueda bilingüe
- Lingüística computacional
- Procesamiento del lenguaje natural para lenguas indígenas
- Construcción de embeddings
- Fine-tuning de modelos neuronales

---

## Citación

Si utiliza este corpus en una investigación, cite el proyecto correspondiente.

Ejemplo:

```
Vega, A. (2026). Construcción de un corpus paralelo español–shuar mediante técnicas de ingeniería de datos para aplicaciones de procesamiento del lenguaje natural. Ecuela Superior Politécnica de Chimborazo Sede Morona Santiago.
```

---

## Licencia

Este proyecto se distribuye bajo la licencia especificada en el archivo **LICENSE**.

---

## Autor

**Ares Vega**

Escuela Superior Politécnica de Chimborazo

2026
