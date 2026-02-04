# SCHEMA.md - Estructura y Metadatos del Corpus Paralelo Español–Shuar

## Descripción general
Este archivo describe la estructura de datos del corpus paralelo español–shuar construido mediante técnicas de ingeniería de datos. El corpus contiene pares de oraciones alineadas (1:1) extraídos de fuentes oficiales pre-validadas del Ministerio de Educación del Ecuador (materiales EIB/CNIB).  

**Formato principal**: CSV (con opción de exportación a JSON)  
**Codificación**: UTF-8 (obligatoria para caracteres del shuar)  
**Licencia del corpus derivado**: Creative Commons Attribution 4.0 International (CC BY 4.0)  
**Licencia de textos originales**: Institucional – Ministerio de Educación del Ecuador (EIB/CNIB) – Uso educativo autorizado  
**DOI (al publicar)**: [insertar DOI de Zenodo/GitHub]  
**Última actualización**: Enero 2026

## Estructura del archivo CSV principal (corpus.csv)

| Columna          | Tipo de dato     | Descripción                                                                 | Ejemplo de valor                              | Obligatorio | Notas / Restricciones                              |
|------------------|------------------|-----------------------------------------------------------------------------|-----------------------------------------------|-------------|----------------------------------------------------|
| id               | String           | Identificador único del par oración–oración                                 | 1                                             | Sí          | Generado automáticamente                           |
| frase_es         | String           | Oración en español (texto original)                                         | "Las dos niñas tienen pilche"                 | Sí          | Texto limpio, sin caracteres de control            |
| frase_sh         | String           | Oración en shuar (texto original)                                           | "Jimiara uchi tsapan achiakainiawai"          | Sí          | Texto limpio, preservando morfología aglutinante   |
| dominio          | String           | Dominio temático del texto                                                  | Educativo / Cultural / Literario / Médico     | Sí          | Valores controlados (lista predefinida)            |
| fecha_recoleccion| Date (ISO 8601)  | Fecha de incorporación del texto al corpus                                  | 2026-01-21                                    | Sí          | Formato YYYY-MM-DD                                 |
| origen_id        | String           | Identificador de la fuente original                                         | MINEDUC-EIB-2023-Curriculo-Shuar-001          | Sí          | Referencia al documento oficial del Ministerio     |
| licencia         | String           | Licencia de uso del texto original                                          | Institucional – Ministerio de Educación (EIB/CNIB) | Sí     | No modificable – respeta derechos de la fuente     |

## Convenciones adicionales
- Todos los textos están en codificación UTF-8 (soporte para diacríticos y caracteres del shuar).
- No se incluyen traducciones automáticas ni modificaciones semánticas; los pares son extraídos directamente de fuentes oficiales.
- Revisión manual por el investigador (no hablantes nativos) para garantizar fidelidad semántica.
- El corpus derivado (pares alineados + metadatos agregados) se libera bajo **CC BY 4.0**; citar como: Vega Chiriap, A. A. (2026). Corpus paralelo español–shuar. ESPOCH. DOI: [insertar].

## Ejemplo de fila CSV (encabezado + una fila)

```csv
id,frase_es,frase_sh,dominio,fecha_recoleccion,origen_id,licencia
1,"Las dos niñas tienen pilche","Jimiara uchi tsapan achiakainiawai","Educativo","2026-01-21","MINEDUC-EIB-2023-001","Institucional – Ministerio de Educación (EIB/CNIB)"
