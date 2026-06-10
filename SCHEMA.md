# SCHEMA.md - Estructura y Metadatos del Corpus Paralelo Español–Shuar

## Descripción general
Este archivo describe la estructura de datos del corpus paralelo español–shuar construido mediante técnicas de ingeniería de datos. El corpus contiene pares de oraciones alineadas (1:1) extraídos de fuentes oficiales pre-validadas del Ministerio de Educación del Ecuador (materiales EIB/CNIB).  

**Formato principal**: CSV (con opción de exportación a JSON)  
**Codificación**: UTF-8 (obligatoria para caracteres del shuar)  
**Licencia del corpus derivado**: Creative Commons Attribution 4.0 International (CC BY 4.0)    
**DOI (al publicar)**: 10.5281/zenodo.18483848  
**Última actualización**: Enero 2026

## Estructura del archivo CSV principal (corpus.csv)

| Columna          | Tipo de dato     | Descripción                                                                 | Ejemplo de valor                              | Obligatorio | Notas / Restricciones                              |
|------------------|------------------|-----------------------------------------------------------------------------|-----------------------------------------------|-------------|----------------------------------------------------|
| id               | String           | Identificador único del par oración–oración                                 | 1                                             | Sí          | Generado automáticamente                           |
| frase_es         | String           | Oración en español (texto original)                                         | "Las dos niñas tienen pilche"                 | Sí          | Texto limpio, sin caracteres de control            |
| frase_sh         | String           | Oración en shuar (texto original)                                           | "Jimiara uchi tsapan achiakainiawai"          | Sí          | Texto limpio, preservando morfología aglutinante   |
| dominio          | String           | Dominio temático del texto                                                  | Educativo / Cultural / Literario / Médico     | Sí          | Valores controlados (lista predefinida)            |
| fecha_recoleccion| Date (ISO 8601)  | Fecha de incorporación del texto al corpus                                  | 2026-01-21                                    | Sí          | Formato YYYY-MM-DD                                 |
| origen        | String           | Fuente original                                         | SEIBE - Secretaría de Educación Intercultural Bilingüe y la Etnoeducación          | Sí          | Referencia a la fuente oficial del Ministerio     |

## Convenciones adicionales
- Todos los textos están en codificación UTF-8 (soporte para diacríticos y caracteres del shuar).
- No se incluyen traducciones automáticas ni modificaciones semánticas; los pares son extraídos directamente de fuentes oficiales.
- Revisión manual por el investigador (no hablantes nativos) para garantizar fidelidad semántica.
- El corpus derivado (pares alineados + metadatos agregados) se libera bajo **CC BY 4.0**; citar como: Vega Chiriap, A. A. (2026). Corpus paralelo español–shuar. ESPOCH. DOI: 10.5281/zenodo.18483848

## Ejemplo de fila CSV (encabezado + una fila)

```csv
id,frase_es,frase_sh,dominio,fecha_recoleccion,origen
1,"Las dos niñas tienen pilche","Jimiara uchi tsapan achiakainiawai","Educativo","2026-01-21","Instituto Nacional de Patrimonio Cultural"
