# Corpus Paralelo Español–Shuar

Repositorio oficial del proyecto de titulación:

**Construcción de un corpus paralelo español–shuar mediante técnicas de ingeniería de datos para aplicaciones de Procesamiento del Lenguaje Natural**

---

## Descripción

Este repositorio contiene un corpus paralelo **Español–Shuar** construido a partir de documentos bilingües oficiales provenientes de instituciones públicas del Ecuador.

El corpus tiene como finalidad proporcionar un recurso lingüístico documentado, interoperable y reutilizable para investigaciones relacionadas con el Procesamiento del Lenguaje Natural (PLN) y otras aplicaciones de lingüística computacional en lenguas indígenas de bajo recurso.

---

## Objetivo

Construir un corpus paralelo español–shuar mediante técnicas de ingeniería de datos para aplicaciones de Procesamiento del Lenguaje Natural.

---

## DOI

https://doi.org/10.5281/zenodo.18483848

---

## Características del corpus

- **Idiomas:** Español – Shuar
- **Tipo de corpus:** Paralelo
- **Unidad de alineación:** Oración–Oración (1:1)
- **Codificación:** UTF-8
- **Formatos:** CSV y JSON
- **Dominios temáticos:**
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
│   └── Corpus-paralelo-espanol-shuar.json
│
├── Codigos/
│   ├── Creacion_corpus.py
│   ├── Detectar_duplicados.py
│   ├── Extraer_imagenes_ocr.py
│   ├── Extraer_texto_adaptativo.py
│   ├── Limpieza_normalizacion.py
│   └── Metricas_corpus.py
│
├── README.md
├── SCHEMA.md
├── LICENSE
└── CITATION.cff
```

---

## Estructura del corpus

Cada registro representa un par de oraciones alineadas (1:1).

Los campos disponibles son:

- `id`
- `frase_es`
- `frase_sh`
- `dominio`
- `fecha_recoleccion`
- `origen`

La especificación técnica completa, incluyendo tipos de datos, restricciones y ejemplos, se encuentra en **SCHEMA.md**.

---

## Metodología de construcción

El corpus fue construido mediante un pipeline de ingeniería de datos compuesto por cuatro fases:

1. Definición del corpus.
2. Recolección de documentos bilingües.
3. Limpieza, normalización y alineación.
4. Medición de métricas descriptivas.

---

## Requisitos de software

- Python 3.12 o superior.

### Bibliotecas principales

- pdfplumber
- easyocr
- opencv-python
- pandas
- numpy
- chardet
- regex

---

## Principios FAIR

El corpus fue diseñado considerando los principios FAIR.

- **Findable:** documentación y metadatos estructurados.
- **Accessible:** formatos abiertos (CSV y JSON).
- **Interoperable:** codificación UTF-8 y esquema de datos documentado.
- **Reusable:** documentación técnica y licencia abierta.

---

## Posibles aplicaciones

Este recurso puede utilizarse en investigaciones relacionadas con:

- Traducción automática.
- Modelos de lenguaje.
- Sistemas de recuperación de información.
- Sistemas de búsqueda bilingüe.
- Lingüística computacional.
- Procesamiento del Lenguaje Natural para lenguas indígenas.
- Construcción de embeddings.
- Fine-tuning de modelos neuronales.

---

## Fuentes documentales

El corpus fue construido a partir de documentos bilingües publicados por instituciones oficiales del Ecuador:

- Secretaría de Educación Intercultural Bilingüe y la Etnoeducación (SEIBE).
- Ministerio de Educación del Ecuador.
- Instituto Nacional de Patrimonio Cultural (INPC).

Los derechos de autor de dichos documentos pertenecen a sus respectivos titulares.

---

## Limitaciones

- El corpus fue construido exclusivamente a partir de documentos bilingües oficiales.
- No representa la totalidad de las variantes dialectales del idioma shuar.
- La distribución temática depende de la disponibilidad documental existente.
- No incorpora traducciones automáticas.
- Puede ampliarse en futuras versiones mediante la incorporación de nuevas fuentes documentales.

---

## Citación

Si utiliza este corpus en una investigación, cite el recurso de la siguiente manera:

```bibtex
@misc{Vega2026,
  author = {Vega Chiriap, Ares Apolo},
  title = {Corpus Paralelo Español--Shuar},
  year = {2026},
  publisher = {Escuela Superior Politécnica de Chimborazo},
  doi = {10.5281/zenodo.18483848}
}
```

---

## Licencia

Este proyecto se distribuye bajo la licencia descrita en el archivo **LICENSE**.

La licencia **CC BY 4.0** aplica a:

- documentación técnica;
- scripts;
- metadatos;
- estructura del corpus;
- procesos de alineación y normalización desarrollados por el autor.

Los documentos originales utilizados como fuente mantienen los derechos de autor de sus respectivas instituciones.

---

## Autor

**Ares Apolo Vega Chiriap**

Escuela Superior Politécnica de Chimborazo  
Sede Morona Santiago

2026
