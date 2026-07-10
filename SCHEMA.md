# SCHEMA.md

# Esquema de Datos del Corpus Paralelo Español–Shuar

## Descripción

Este documento describe la estructura del corpus paralelo español–shuar desarrollado mediante técnicas de ingeniería de datos para aplicaciones de Procesamiento del Lenguaje Natural (PLN).

El corpus está compuesto por pares de oraciones alineadas (1:1) obtenidas de documentos bilingües oficiales de la Educación Intercultural Bilingüe del Ecuador.

---

# Especificaciones generales

| Propiedad | Valor |
|-----------|-------|
| Formato principal | CSV |
| Formato alternativo | JSON |
| Codificación | UTF-8 |
| Unidad de alineación | Oración – Oración (1:1) |
| Licencia | CC BY 4.0 |
| DOI | 10.5281/zenodo.18483848 |
| Idiomas | Español (es), Shuar (jiv) |
| Última actualización | Enero 2026 |

---

# Archivo principal

```
Corpus-paralelo-espanol-shuar.csv
```

---

# Esquema del archivo

| Campo | Tipo | Obligatorio | Descripción |
|--------|------|-------------|-------------|
| id | Integer | Sí | Identificador único del par alineado. |
| frase_es | String | Sí | Oración en español. |
| frase_sh | String | Sí | Oración equivalente en shuar. |
| dominio | String | Sí | Dominio temático del documento. |
| fecha | Date | Sí | Fecha de incorporación al corpus (ISO 8601). |
| origen | String | Sí | Institución de procedencia del documento. |

---

# Restricciones

## id

- Entero positivo.
- No admite duplicados.

Ejemplo

```
1
```

---

## frase_es

- Texto UTF-8.
- Una única oración.
- No contiene saltos de línea.
- Sin espacios innecesarios.

Ejemplo

```
Las dos niñas tienen pilche.
```

---

## frase_sh

- Texto UTF-8.
- Una única oración.
- Conserva íntegramente la escritura original del idioma shuar.
- No contiene modificaciones lingüísticas.

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

Formato ISO 8601

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
SEIBE - Secretaría de Educación Intercultural Bilingüe y la Etnoeducación
Instituto Nacional de Patrimonio Cultural
Ministerio de Educación
```

---

# Ejemplo de registro

```csv
id,frase_es,frase_sh,dominio,fecha_recoleccion,origen
1,"Las dos niñas tienen pilche.","Jimiara uchi tsapan achiakainiawai.","Educativo","2026-01-21","Instituto Nacional de Patrimonio Cultural"
```

---

# Convenciones

- Todos los archivos utilizan codificación UTF-8.
- Cada registro representa un único par de oraciones.
- La alineación es estrictamente 1:1.
- No existen registros duplicados.
- No se incluyen líneas vacías.
- El corpus procede únicamente de documentos oficiales bilingües.
- No se realizaron traducciones automáticas.
- La correspondencia bilingüe fue verificada manualmente durante el proceso de construcción.

---

# Principios FAIR

## Findable

- Publicación mediante Zenodo.
- DOI permanente.

## Accessible

- Repositorio GitHub.
- Licencia CC BY 4.0.

## Interoperable

- Formatos abiertos (CSV y JSON).
- UTF-8.
- Esquema documentado.

## Reusable

- Documentación técnica completa.
- Metadatos normalizados.
- Licencia abierta.

---

# Archivos relacionados

```
README.md
LICENSE
Corpus-paralelo-espanol-shuar.csv
Corpus-paralelo-espanol-shuar.json
SCHEMA.md
```
