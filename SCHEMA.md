# SCHEMA.md

# Esquema del Corpus Paralelo Español–Shuar

## Descripción

Este documento especifica la estructura y las restricciones del conjunto de datos que conforma el corpus paralelo Español–Shuar.

El corpus contiene pares de oraciones alineadas (1:1), extraídos de documentos bilingües oficiales de la Educación Intercultural Bilingüe del Ecuador y estructurados mediante técnicas de ingeniería de datos.

---

## Información general

| Propiedad | Valor |
|-----------|-------|
| Formato principal | CSV |
| Formato alternativo | JSON |
| Codificación | UTF-8 |
| Unidad de alineación | Oración–Oración (1:1) |
| Idiomas | Español (es), Shuar (jiv) |
| Licencia | CC BY 4.0 |
| DOI | https://doi.org/10.5281/zenodo.18483848 |
| Versión | 1.0 |
| Última actualización | Julio 2026 |

---

# Archivo principal

```
Corpus/Corpus-paralelo-espanol-shuar.csv
```

---

# Esquema de datos

| Campo | Tipo | Obligatorio | Descripción |
|--------|------|:-----------:|-------------|
| id | Integer | Sí | Identificador único del par alineado. |
| frase_es | String | Sí | Oración original en español. |
| frase_sh | String | Sí | Oración equivalente en idioma shuar. |
| dominio | String | Sí | Dominio temático del documento fuente. |
| fecha | Date | Sí | Fecha de incorporación al corpus (ISO 8601). |
| origen | String | Sí | Institución responsable del documento fuente. |

---

# Restricciones por campo

## id

- Entero positivo.
- Valor único.
- Sin duplicados.

Ejemplo

```
1
```

---

## frase_es

- Texto codificado en UTF-8.
- Una única oración.
- Sin saltos de línea.
- Conserva la puntuación original.

Ejemplo

```
Las dos niñas tienen pilche.
```

---

## frase_sh

- Texto codificado en UTF-8.
- Una única oración.
- Conserva íntegramente la escritura original del idioma shuar.
- No presenta modificaciones lingüísticas.

Ejemplo

```
Jimiara uchi tsapan achiakainiawai.
```

---

## dominio

Valores permitidos

```
Educativo
Cultural
Literario
Médico
```

---

## fecha_recoleccion

Formato

```
YYYY-MM-DD
```

Ejemplo

```
2026-01-21
```

---

## origen

Valores esperados

```
SEIBE -Secretaría de Educación Intercultural Bilingüe y la Etnoeducación 

Ministerio de Educación del Ecuador

Instituto Nacional de Patrimonio Cultural
```

---

# Ejemplo de registro

```csv
id,frase_es,frase_sh,dominio,fecha_recoleccion,origen
1,"Las dos niñas tienen pilche.","Jimiara uchi tsapan achiakainiawai.","Educativo","2026-01-21","Instituto Nacional de Patrimonio Cultural"
```

---

# Reglas del corpus

- Cada registro representa exactamente un par de oraciones alineadas.
- La alineación es estrictamente 1:1.
- No existen registros duplicados.
- No se incluyen registros vacíos.
- Todos los archivos utilizan codificación UTF-8.
- Los textos proceden exclusivamente de documentos bilingües oficiales.
- No se incorporan traducciones automáticas.
- La correspondencia entre ambos idiomas fue verificada durante el proceso de construcción del corpus.

---

# Integridad de los datos

El corpus cumple las siguientes condiciones:

- Identificadores únicos.
- Sin pares duplicados.
- Sin líneas vacías.
- Codificación UTF-8 validada.
- Estructura uniforme en CSV y JSON.
- Correspondencia uno a uno entre ambos idiomas.

---

# Archivos relacionados

```
README.md
LICENSE
Corpus/
    Corpus-paralelo-espanol-shuar.csv
    Corpus-paralelo-espanol-shuar.json
```
