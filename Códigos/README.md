# Extractor adaptativo de texto desde documentos PDF

## Descripción

El archivo `extraer_texto_adaptativo.py` implementa un módulo de extracción automática de texto desde documentos PDF utilizados como fuentes para la construcción del corpus paralelo español–shuar.

El script incorpora un mecanismo de análisis estructural que permite identificar automáticamente la organización interna de cada página y seleccionar una estrategia de extracción adecuada según sus características. Esta capacidad permite procesar documentos con diferentes formatos de presentación, incluyendo estructuras lineales, tabulares y mixtas.

El objetivo del módulo es transformar documentos PDF en archivos de texto procesables, conservando la mayor cantidad posible de información relevante para las etapas posteriores de limpieza, estructuración y generación del corpus.


## Objetivo del módulo

Este script forma parte de la etapa de **extracción y transformación de datos** dentro del pipeline de construcción del corpus paralelo español–shuar.

Sus principales objetivos son:

- Extraer contenido textual desde documentos PDF bilingües.
- Analizar automáticamente la estructura visual de cada página.
- Seleccionar estrategias de extracción según el tipo de contenido detectado.
- Reducir errores ocasionados por tablas, columnas o distribución irregular del texto.
- Generar archivos de salida con información extraída y reportes técnicos.


## Características principales

### Detección automática de estructura

El sistema analiza cada página del documento para determinar su tipo de organización:

| Tipo de estructura | Descripción |
|---|---|
| `lineal` | Páginas con contenido organizado principalmente mediante párrafos consecutivos. |
| `tabular` | Páginas donde el contenido presenta tablas, columnas o distribución estructurada. |
| `mixto` | Páginas que combinan elementos lineales y tabulares. |


### Extracción adaptativa

Según el resultado del análisis estructural, el script selecciona automáticamente una estrategia de extracción:

- **Extracción lineal:** utilizada para documentos con distribución convencional de párrafos.
- **Extracción tabular:** utilizada para documentos con columnas o tablas.
- **Extracción mixta:** utiliza un enfoque híbrido para páginas con estructuras combinadas.


### Análisis estructural por página

Durante el procesamiento se recopilan indicadores internos del documento:

- Número de palabras detectadas.
- Cantidad de tablas identificadas.
- Número estimado de columnas.
- Densidad de contenido.
- Distribución de tamaños de fuente.
- Nivel de confianza de la clasificación.


### Limpieza del texto extraído

El módulo incorpora procesos básicos de normalización:

- Eliminación de marcadores de página.
- Normalización de espacios.
- Reducción de saltos de línea excesivos.
- Eliminación de líneas con posibles artefactos de extracción.


## Dependencias

El script utiliza las siguientes librerías de Python:

| Librería | Uso |
|---|---|
| `pdfplumber` | Extracción de texto, palabras y tablas desde documentos PDF. |
| `pathlib` | Administración de rutas y archivos. |
| `re` | Aplicación de expresiones regulares para limpieza textual. |
| `collections` | Agrupación y conteo de elementos durante el análisis. |
| `dataclasses` | Definición de estructuras para almacenar resultados del procesamiento. |
| `typing` | Definición de tipos de datos utilizados en funciones y estructuras. |


## Flujo de procesamiento

```text
Documento PDF
      │
      ▼
Extracción de información de página
      │
      ▼
Análisis de estructura
      │
      ▼
Clasificación automática
(lineal / tabular / mixto)
      │
      ▼
Aplicación de estrategia de extracción
      │
      ▼
Limpieza y consolidación del texto
      │
      ▼
Generación de archivos de salida
```


## Uso

El script puede ejecutarse mediante línea de comandos:

```bash
python extraer_texto_adaptativo.py documento.pdf
```

También permite proporcionar únicamente el nombre del archivo cuando el documento se encuentra dentro del directorio de fuentes:

```bash
python extraer_texto_adaptativo.py nombre_documento.pdf
```


En caso de no proporcionar argumentos, el programa busca automáticamente documentos PDF disponibles dentro del directorio:

```text
Fuentes_de_datos/
```


## Archivos generados

Después del procesamiento se generan dos archivos dentro del directorio:

```text
Datos/
│
├── documento_EXTRAIDO.txt
└── documento_REPORTE.txt
```


### Archivo EXTRAIDO

Formato:

```text
documento_EXTRAIDO.txt
```

Contiene el texto obtenido desde el documento PDF después del proceso de extracción y limpieza.


### Archivo REPORTE

Formato:

```text
documento_REPORTE.txt
```

Contiene información detallada del análisis estructural realizado:

- Distribución de tipos de estructura.
- Clasificación por página.
- Nivel de confianza del análisis.
- Número de tablas detectadas.
- Número de columnas estimadas.
- Cantidad de palabras extraídas.
- Tamaños de fuente encontrados.


## Parámetros configurables

El comportamiento del extractor puede modificarse mediante las constantes definidas al inicio del script:

| Parámetro | Descripción |
|---|---|
| `UMBRAL_SHUAR` | Define el tamaño de fuente considerado como texto grande. |
| `UMBRAL_TITULO` | Define el tamaño mínimo para identificar posibles títulos. |
| `TOLERANCIA_Y` | Controla la agrupación de palabras según su posición vertical. |
| `MARGEN_BBOX` | Define el margen utilizado durante la detección de áreas. |


## Consideraciones

El extractor fue diseñado para trabajar con documentos PDF heterogéneos utilizados como fuentes lingüísticas. Debido a la diversidad de formatos presentes en documentos educativos, culturales y literarios, el análisis adaptativo permite mejorar la recuperación del contenido textual antes de las fases de limpieza, estructuración y construcción del corpus paralelo.

----

# OCR avanzado para extracción y reconstrucción de tablas

## Descripción

El script implementa un sistema de reconocimiento óptico de caracteres (OCR) orientado a la extracción de información desde imágenes provenientes de documentos físicos o páginas digitalizadas.

El módulo utiliza técnicas de procesamiento digital de imágenes y reconocimiento de texto para recuperar contenido textual, especialmente información organizada en tablas. Además, incorpora un proceso de reconstrucción estructural basado en coordenadas espaciales obtenidas durante la detección OCR.

Este componente forma parte de la etapa de **recolección y transformación de datos**, permitiendo convertir fuentes documentales no editables en texto estructurado para su posterior incorporación al corpus paralelo español–shuar.


## Objetivo del módulo

El propósito principal del script es:

- Extraer texto desde imágenes mediante OCR.
- Mejorar la calidad de reconocimiento mediante preprocesamiento de imágenes.
- Detectar la posición espacial de cada palabra identificada.
- Reconstruir tablas conservando la distribución original del contenido.
- Generar archivos de salida en formato de texto estructurado.


## Características principales


### Reconocimiento óptico de caracteres

El módulo utiliza la biblioteca `EasyOCR` para identificar texto dentro de imágenes.

Características:

- Reconocimiento en español e inglés.
- Procesamiento mediante CPU o GPU según disponibilidad.
- Obtención de texto y coordenadas espaciales de cada elemento detectado.


### Preprocesamiento de imágenes

Antes de ejecutar el reconocimiento OCR, las imágenes pasan por una etapa de mejora:

1. Conversión a escala de grises.
2. Redimensionamiento cuando la resolución es insuficiente.
3. Aplicación de filtro bilateral para reducción de ruido.
4. Umbralización adaptativa para mejorar el contraste.

Flujo:

```text
Imagen original
      │
      ▼
Conversión escala de grises
      │
      ▼
Aumento de resolución
      │
      ▼
Reducción de ruido
      │
      ▼
Binarización adaptativa
      │
      ▼
Imagen optimizada para OCR
```


## Reconstrucción de tablas

El script incorpora un método de reconstrucción basado en las coordenadas obtenidas por OCR.

El proceso consiste en:

1. Obtener las coordenadas de cada palabra detectada.
2. Calcular el centro geométrico del bloque de texto.
3. Agrupar palabras según su posición vertical.
4. Ordenar elementos horizontalmente dentro de cada fila.
5. Determinar el número aproximado de columnas.
6. Generar una representación de tabla en formato Markdown.


Ejemplo de transformación:

Entrada:

```text
Palabra A       Palabra B       Palabra C
Dato 1          Dato 2          Dato 3
```

Salida:

```markdown
| Columna1 | Columna2 | Columna3 |
|---|---|---|
| Palabra A | Palabra B | Palabra C |
| Dato 1 | Dato 2 | Dato 3 |
```


## Funciones principales


### `preprocesar_imagen(ruta_imagen)`

Realiza el acondicionamiento de la imagen antes del reconocimiento OCR.

**Entrada:**

- Ruta del archivo de imagen.

**Procesos realizados:**

- Lectura de imagen.
- Conversión a escala de grises.
- Escalamiento automático.
- Filtrado de ruido.
- Umbralización adaptativa.

**Salida:**

- Imagen procesada lista para OCR.


---

### `extraer_tabla_con_coordenadas(ruta_imagen, tolerancia_y)`

Realiza la extracción OCR manteniendo la ubicación espacial del texto.

**Entrada:**

- Imagen con contenido textual o tabular.
- Tolerancia vertical para agrupación de filas.

**Proceso:**

- Reconocimiento de caracteres.
- Obtención de coordenadas.
- Limpieza de caracteres no válidos.
- Agrupación de palabras por filas.
- Ordenamiento por columnas.
- Reconstrucción de tabla.


**Salida:**

Tabla reconstruida en formato Markdown.


---

### `extraer_texto_normal(ruta_imagen)`

Realiza extracción OCR convencional cuando la reconstrucción tabular no obtiene resultados adecuados.

Características:

- Ignora la estructura espacial.
- Recupera bloques completos de texto.
- Utiliza detección de párrafos.


**Salida:**

Texto plano.


---

### `seleccionar_imagenes()`

Permite seleccionar imágenes mediante una interfaz gráfica.

Formatos soportados:

- PNG
- JPG
- JPEG
- BMP
- TIFF


---

### `main()`

Controla la ejecución completa del proceso:

1. Selección de imágenes.
2. Procesamiento individual.
3. Evaluación del resultado OCR.
4. Cambio automático entre modo tabla y modo texto.
5. Generación del archivo final.


## Dependencias

| Librería | Función |
|---|---|
| `easyocr` | Reconocimiento óptico de caracteres. |
| `opencv-python` (`cv2`) | Procesamiento y mejora de imágenes. |
| `numpy` | Operaciones matemáticas y cálculo de coordenadas. |
| `tkinter` | Selección gráfica de archivos. |
| `re` | Limpieza mediante expresiones regulares. |
| `os` | Gestión de archivos y rutas. |
| `torch` | Detección de disponibilidad de GPU. |


## Flujo de procesamiento

```text
Imagen escaneada
        │
        ▼
Preprocesamiento digital
        │
        ▼
Reconocimiento OCR
        │
        ▼
Obtención de texto y coordenadas
        │
        ▼
Análisis de distribución espacial
        │
        ▼
Reconstrucción de tabla
        │
        ▼
Validación del resultado
        │
        ▼
Generación de archivo TXT
```


## Archivos generados

El script genera un archivo de salida con extensión `.txt`:

```text
nombre_salida.txt
```

El archivo contiene:

- Nombre de la imagen procesada.
- Texto extraído.
- Tablas reconstruidas.
- Separación entre documentos procesados.


## Consideraciones

El módulo está diseñado para procesar documentos digitalizados que no contienen una capa de texto editable. Su aplicación permite recuperar información proveniente de fuentes físicas o imágenes escaneadas, integrándola posteriormente al flujo de preparación del corpus.

La reconstrucción automática de tablas depende de la calidad de la imagen original, resolución, distribución espacial del contenido y precisión del reconocimiento OCR.

# Limpieza, normalización y validación de pares lingüísticos

## Descripción

El script implementa un módulo de limpieza y validación de archivos de texto utilizados para la construcción del corpus paralelo español–shuar.

Su función principal es procesar archivos que contienen pares de segmentos lingüísticos separados mediante un delimitador (`|`), aplicando técnicas de normalización textual, detección de codificación, eliminación de ruido y verificación de alineación estructural.

Este componente corresponde a la etapa de **preprocesamiento y estructuración de datos**, donde los textos extraídos desde diferentes fuentes son transformados en una representación uniforme antes de su incorporación al corpus final.


## Objetivo del módulo

El script tiene como objetivos:

- Detectar y corregir problemas de codificación de caracteres.
- Convertir archivos de texto a formato UTF-8.
- Eliminar caracteres no deseados y elementos generados durante la extracción.
- Normalizar espacios y saltos de línea.
- Eliminar registros vacíos y duplicados.
- Validar la presencia del separador entre segmentos paralelos.
- Calcular la tasa de alineación de los pares lingüísticos.
- Generar una versión limpia del archivo procesado.


## Formato de entrada esperado

El módulo trabaja con archivos de texto donde cada línea representa un par paralelo:

```text
Texto en español | Texto en shuar
```

Ejemplo:

```text
La casa es grande | Jea penker nekata
```

Cada línea debe contener:

| Elemento | Descripción |
|---|---|
| Segmento izquierdo | Texto correspondiente al idioma español. |
| Separador `|` | Marcador utilizado para identificar la correspondencia entre segmentos. |
| Segmento derecho | Texto correspondiente al idioma shuar. |


## Características principales


### Detección y conversión de codificación

El módulo identifica automáticamente la codificación original del archivo mediante la biblioteca `chardet`.

Proceso:

```text
Archivo de texto
       │
       ▼
Detección de codificación
       │
       ▼
Lectura con codificación identificada
       │
       ▼
Conversión a UTF-8
       │
       ▼
Archivo compatible con procesamiento posterior
```

Si la codificación no puede ser determinada, se utiliza `latin-1` como alternativa.


---

### Limpieza de ruido textual

El script aplica filtros para eliminar elementos innecesarios generados durante procesos de extracción.

Procesos realizados:

- Eliminación de caracteres no permitidos.
- Eliminación de números de página.
- Eliminación de líneas compuestas únicamente por numeración o símbolos.
- Conservación de caracteres lingüísticos necesarios:
  - tildes,
  - diéresis,
  - caracteres propios del español.


---

### Normalización del contenido

El módulo realiza ajustes de formato:

- Reducción de espacios consecutivos.
- Eliminación de saltos de línea innecesarios.
- Eliminación de espacios al inicio y final de cada línea.
- Homogeneización de la estructura del archivo.


---

### Eliminación de duplicados

El proceso elimina líneas repetidas para evitar registros duplicados dentro del corpus.

Ejemplo:

Entrada:

```text
La casa es grande | Jea penker nekata
La casa es grande | Jea penker nekata
```

Salida:

```text
La casa es grande | Jea penker nekata
```


---

### Normalización de mayúsculas

El script identifica segmentos escritos completamente en mayúsculas y los convierte a minúsculas.

Ejemplo:

Entrada:

```text
LA CASA ES GRANDE | JEA PENKER NEKATA
```

Salida:

```text
la casa es grande | jea penker nekata
```

La conversión únicamente se aplica cuando todas las letras del segmento están en mayúsculas.


## Validación de alineación

El módulo verifica la estructura de los pares lingüísticos mediante la presencia del separador `|`.

Indicadores calculados:

| Indicador | Descripción |
|---|---|
| Total de pares | Cantidad total de líneas procesadas. |
| Pares alineados | Líneas que contienen el separador `|`. |
| Pares sin alineación | Líneas que no presentan separación entre idiomas. |
| Tasa de alineación | Proporción de pares correctamente estructurados. |


Fórmula:

\[
Tasa\ de\ alineación = \frac{Pares\ alineados}{Total\ de\ pares}
\]


Ejemplo:

```text
Total de pares: 1000
Pares alineados: 980

Tasa de alineación: 98%
```


## Funciones principales


### `detectar_codificacion(ruta_archivo)`

Detecta la codificación utilizada por un archivo de texto.

**Entrada:**

- Ruta del archivo.

**Salida:**

- Nombre de la codificación detectada.


---

### `convertir_a_utf8(ruta_entrada, ruta_salida)`

Convierte archivos con diferentes codificaciones al estándar UTF-8.

**Entrada:**

- Archivo original.
- Ruta opcional de salida.

**Salida:**

- Archivo convertido a UTF-8.


---

### `limpiar_ruido(texto)`

Elimina elementos no deseados del contenido textual.

Incluye:

- Caracteres inválidos.
- Números de página.
- Líneas generadas por errores de extracción.


---

### `normalizar_espacios_y_saltos(texto)`

Estandariza la distribución del texto.

Funciones:

- Reducir espacios consecutivos.
- Eliminar líneas vacías innecesarias.
- Normalizar saltos de línea.


---

### `eliminar_vacios_y_duplicados(lineas)`

Filtra registros repetidos o vacíos.

**Salida:**

Lista de líneas únicas y válidas.


---

### `analizar_separador(lineas)`

Evalúa la estructura del archivo mediante el separador paralelo.

Retorna:

- Líneas sin separador.
- Total de pares.
- Cantidad de pares alineados.


---

### `calcular_tasa_alineacion(alineados, total_pares)`

Calcula el porcentaje de pares correctamente estructurados.


---

### `procesar_archivo(ruta_archivo)`

Ejecuta el flujo completo de procesamiento:

1. Conversión de codificación.
2. Limpieza textual.
3. Normalización.
4. Eliminación de duplicados.
5. Conversión de mayúsculas.
6. Validación de alineación.
7. Generación del archivo limpio.


---

### `seleccionar_archivo()`

Permite seleccionar archivos mediante menú interactivo.

Opciones disponibles:

1. Seleccionar archivo desde un directorio.
2. Introducir una ruta directa.
3. Salir del programa.


## Dependencias

| Librería | Función |
|---|---|
| `chardet` | Detección automática de codificación de archivos. |
| `os` | Gestión de archivos y rutas. |
| `re` | Aplicación de expresiones regulares para limpieza. |
| `pathlib` | Manejo de rutas del sistema. |


## Flujo de procesamiento

```text
Archivo TXT inicial
        │
        ▼
Detección de codificación
        │
        ▼
Conversión UTF-8
        │
        ▼
Eliminación de ruido
        │
        ▼
Normalización textual
        │
        ▼
Eliminación de duplicados
        │
        ▼
Validación de pares paralelos
        │
        ▼
Cálculo de tasa de alineación
        │
        ▼
Archivo limpio del corpus
```


## Archivos generados

Cuando el usuario confirma la operación, se genera un nuevo archivo:

```text
archivo_limpio.txt
```

Este archivo contiene:

- Pares lingüísticos normalizados.
- Segmentos sin duplicados.
- Codificación UTF-8.
- Estructura compatible con procesos posteriores.


## Consideraciones

El módulo está diseñado para preparar datos textuales antes de la generación del corpus paralelo definitivo. Las operaciones realizadas buscan mejorar la consistencia del conjunto de datos, reducir errores introducidos durante la extracción y garantizar que cada segmento mantenga una estructura compatible con procesos posteriores de análisis y evaluación.

# Importador y gestión del corpus paralelo

## Descripción

El script implementa un sistema de importación, administración y conversión de datos para el corpus paralelo español–shuar.

El módulo permite incorporar nuevos pares lingüísticos almacenados en archivos de texto (`.txt`) hacia un archivo principal en formato CSV, asignando metadatos asociados como dominio temático, fecha de incorporación y origen de la información.

Además, proporciona herramientas para consultar estadísticas del corpus, visualizar registros, validar la estructura de entrada y generar una versión equivalente en formato JSON para facilitar la interoperabilidad con diferentes aplicaciones de procesamiento del lenguaje natural.

Este componente corresponde a la etapa de **estructuración y almacenamiento del corpus**, donde los segmentos lingüísticos previamente limpiados son transformados en un conjunto de datos organizado y reutilizable.


## Objetivo del módulo

El script tiene como objetivos:

- Importar pares de frases español–shuar desde archivos de texto.
- Validar la estructura de los datos antes de incorporarlos al corpus.
- Mantener identificadores únicos para cada registro.
- Asociar metadatos descriptivos a cada segmento.
- Gestionar dominios temáticos del corpus.
- Generar formatos compatibles con herramientas de análisis posteriores.


## Estructura del corpus generado

El archivo principal utiliza formato CSV con la siguiente estructura:

| Campo | Descripción |
|---|---|
| `ID` | Identificador único del segmento dentro del corpus. |
| `frase_es` | Segmento correspondiente al idioma español. |
| `frase_sh` | Segmento correspondiente al idioma shuar. |
| `dominio` | Clasificación temática del segmento. |
| `fecha` | Fecha de incorporación del registro. |
| `origen` | Fuente o documento de procedencia. |


Ejemplo de registro:

```csv
ID,frase_es,frase_sh,dominio,fecha,origen
1,La casa es grande,Jea penker nekata,Cultural,10-07-2026,Documento bilingüe
```


## Formato de entrada

El módulo recibe archivos `.txt` con pares lingüísticos separados por el carácter `|`.

Ejemplo:

```text
La casa es grande | Jea penker nekata
El niño estudia | Uun uchich unuimiatain
```

Cada línea representa una unidad paralela independiente.


## Características principales


### Validación de archivos

Antes de realizar una importación, el sistema verifica:

- Existencia del archivo.
- Tipo de archivo (`.txt`).
- Disponibilidad de lectura.
- Codificación UTF-8.

Esto evita la incorporación de archivos incompatibles o dañados al corpus.


---

### Importación de pares lingüísticos

El proceso de importación realiza:

1. Lectura del archivo fuente.
2. Separación de segmentos mediante `|`.
3. Validación de campos vacíos.
4. Generación de identificadores consecutivos.
5. Incorporación al archivo CSV principal.


Flujo:

```text
Archivo TXT
     │
     ▼
Validación del formato
     │
     ▼
Lectura de pares español-shuar
     │
     ▼
Asignación de metadatos
     │
     ▼
Generación de registros CSV
     │
     ▼
Actualización del corpus
```


---

### Gestión de dominios

El módulo permite clasificar cada registro según su temática.

Dominios disponibles:

- Educativo.
- Cultural.
- Médico.
- Literario.
- Otro.


Esta clasificación permite realizar análisis posteriores de distribución temática del corpus.


---

### Generación de identificadores

Cada nuevo registro recibe un identificador único.

Ejemplo:

```text
Último ID existente: 3500

Nuevos registros:
3501
3502
3503
```


Esto garantiza la trazabilidad individual de cada segmento lingüístico.


## Clase principal


# `CorpusImporter`

Clase encargada de controlar todo el proceso de administración del corpus.


### Inicialización

```python
CorpusImporter(corpus_file)
```

Crea o carga el archivo principal del corpus.

Parámetro:

| Parámetro | Descripción |
|---|---|
| `corpus_file` | Nombre del archivo CSV donde se almacenarán los datos. |


Si el archivo no existe, genera automáticamente la estructura inicial.


## Métodos principales


### `_inicializar_corpus()`

Crea el archivo CSV inicial con los encabezados requeridos.

Campos generados:

```text
ID
frase_es
frase_sh
dominio
fecha
origen
```


---

### `_validar_archivo_txt(ruta_archivo)`

Comprueba que el archivo de entrada cumple los requisitos necesarios.

Validaciones:

- Ruta válida.
- Extensión `.txt`.
- Archivo accesible.
- Codificación compatible.


---

### `_leer_txt_fuente_simple(archivo_fuente)`

Lee archivos de texto con estructura:

```text
español | shuar
```

Devuelve una lista de pares lingüísticos:

```python
[
    ("texto español", "texto shuar"),
    ("texto español", "texto shuar")
]
```


---

### `_obtener_proximo_id()`

Calcula el siguiente identificador disponible dentro del corpus.


---

### `importar_desde_txt(archivo_txt, dominio, origen)`

Realiza la importación completa de datos.

Proceso:

1. Validación del archivo.
2. Validación del dominio.
3. Lectura de pares.
4. Vista previa de registros.
5. Confirmación del usuario.
6. Inserción en CSV.
7. Generación de resumen.


Salida:

```text
Cantidad de frases importadas
```


---

### `mostrar_estadisticas()`

Genera estadísticas descriptivas del corpus actual.

Indicadores:

- Total de frases.
- Distribución por dominio.
- Distribución por origen.


Ejemplo:

```text
Total de frases: 5000

Distribución por dominio:

Educativo: 1500 (30%)
Cultural: 2000 (40%)
Literario: 1500 (30%)
```


---

### `convertir_a_json()`

Convierte el corpus CSV a formato JSON.

Salida:

```text
corpus.json
```

Este formato facilita el uso del corpus en aplicaciones de procesamiento del lenguaje natural.


---

### `menu_principal()`

Proporciona una interfaz interactiva para administrar el corpus.

Opciones disponibles:

1. Importar frases desde TXT.
2. Consultar estadísticas.
3. Convertir a JSON.
4. Cambiar archivo del corpus.
5. Visualizar registros.
6. Salir.


## Dependencias

| Librería | Función |
|---|---|
| `csv` | Lectura y escritura del corpus en formato CSV. |
| `os` | Gestión de archivos y rutas. |
| `datetime` | Registro de fecha de incorporación. |
| `sys` | Control del entorno de ejecución. |
| `json` | Conversión del corpus a formato JSON. |


## Flujo general del procesamiento

```text
Archivo TXT limpio
        │
        ▼
Validación del formato
        │
        ▼
Lectura de pares paralelos
        │
        ▼
Asignación de dominio y origen
        │
        ▼
Generación de IDs
        │
        ▼
Almacenamiento en CSV
        │
        ▼
Conversión opcional a JSON
        │
        ▼
Corpus estructurado
```


## Archivos generados

El módulo genera o modifica los siguientes archivos:

```text
corpus.csv
```

Archivo principal de almacenamiento del corpus.


```text
corpus.json
```

Versión del corpus en formato JSON para interoperabilidad.


## Consideraciones

Este módulo representa la etapa final de estructuración del corpus, permitiendo consolidar los segmentos lingüísticos previamente extraídos y limpiados en un conjunto de datos organizado.

La incorporación de metadatos como dominio y origen permite mantener la trazabilidad de cada registro, facilitando posteriormente procesos de análisis estadístico, evaluación de calidad y reutilización del corpus en aplicaciones de procesamiento del lenguaje natural.

# Eliminación y control de duplicados del corpus

## Descripción

Este módulo implementa un proceso de depuración de datos para identificar y eliminar registros duplicados dentro del corpus paralelo español–shuar.

Su función principal es garantizar que cada par lingüístico sea único, evitando redundancias que puedan afectar los análisis estadísticos posteriores, la evaluación de calidad del corpus o el entrenamiento de modelos de procesamiento del lenguaje natural.

El script trabaja sobre archivos estructurados en formato CSV o JSON y realiza una comparación basada en los campos `frase_es` y `frase_sh`.

Cuando encuentra registros repetidos, permite eliminarlos y reconstruir los identificadores del corpus.

## Objetivo del módulo

El módulo tiene como objetivos:

* Detectar pares lingüísticos duplicados.
* Comparar registros considerando o ignorando diferencias entre mayúsculas y minúsculas.
* Normalizar frases completamente escritas en mayúsculas.
* Eliminar redundancias del corpus.
* Reasignar identificadores consecutivos.
* Mantener la integridad estructural del dataset.

## Ubicación dentro del pipeline

Este script corresponde a la etapa de validación y control de calidad del corpus.

```text
Extracción de documentos
          │
          ▼
Limpieza y normalización textual
          │
          ▼
Estructuración del corpus CSV/JSON
          │
          ▼
Detección de duplicados
          │
          ▼
Corpus depurado
          │
          ▼
Evaluación de métricas
```

## Formatos compatibles

El módulo acepta los siguientes formatos:

| Formato | Extensión | Lectura  |
| ------- | --------- | -------- |
| CSV     | `.csv`    | `pandas` |
| JSON    | `.json`   | `pandas` |

Ejemplo de estructura esperada:

```csv
ID,frase_es,frase_sh,dominio,fecha,origen
1,La casa es grande,Jea penker nekata,Cultural,10-07-2026,Documento bilingüe
2,El niño estudia,Uchich unuimiatain,Educativo,10-07-2026,Guía educativa
```

## Características principales

### Detección de codificación

Antes de procesar el corpus, el script verifica la codificación del archivo mediante la biblioteca `chardet`.

```text
Archivo CSV/JSON
        │
        ▼
Detección de encoding
        │
        ▼
¿Es UTF-8?
        │
   ┌────┴────┐
   │         │
 Sí        No
   │         │
   ▼         ▼
Procesar   Convertir
directo    a UTF-8
```

Esto evita errores relacionados con caracteres propios del idioma shuar como:

```text
á é í ó ú ü ñ
```

### Selección del corpus

El usuario puede seleccionar el archivo mediante dos métodos:

#### Opción 1: Buscar dentro de un directorio

El sistema lista automáticamente archivos `.csv` y `.json`.

Ejemplo:

```text
Archivos de corpus:

1. corpus_principal.csv
2. corpus_final.json
3. corpus_limpio.csv
```

#### Opción 2: Ruta directa

Permite ingresar directamente la ubicación del archivo.

Ejemplo:

```text
C:\Proyecto\Corpus\corpus.csv
```

### Detección de duplicados

La detección utiliza las columnas:

```python
[
    "frase_es",
    "frase_sh"
]
```

Dos registros son considerados duplicados cuando ambos segmentos lingüísticos coinciden.

Ejemplo:

Registro 1:

```text
La casa es grande | Jea penker nekata
```

Registro 2:

```text
La casa es grande | Jea penker nekata
```

Resultado:

```text
Duplicado detectado
```

### Sensibilidad de comparación

El usuario puede decidir si las diferencias entre mayúsculas y minúsculas afectan la comparación.

#### Comparación sensible

Ejemplo:

```text
Jímiapetek
jímiapetek
```

Son considerados diferentes.

#### Comparación no sensible

Ejemplo:

```text
Jímiapetek
jímiapetek
```

Son considerados equivalentes.

Esta opción permite adaptar la limpieza según el nivel de normalización requerido.

### Normalización de mayúsculas

El script permite transformar únicamente textos completamente escritos en mayúsculas.

Ejemplo:

Entrada:

```text
LA CASA GRANDE
```

Salida:

```text
la casa grande
```

No modifica textos con escritura mixta:

```text
La Casa Grande
```

permanece sin cambios.

### Eliminación de duplicados

Cuando el usuario confirma la eliminación, el proceso realiza:

1. Conserva la primera aparición del registro.
2. Elimina las repeticiones posteriores.
3. Recalcula los identificadores.
4. Guarda el corpus actualizado.

Ejemplo:

Antes:

```text
ID | frase_es | frase_sh

1 | La casa | Jea
2 | El niño | Uchich
3 | La casa | Jea
```

Después:

```text
ID | frase_es | frase_sh

1 | La casa | Jea
2 | El niño | Uchich
```

### Reindexación de IDs

Después de eliminar registros, los identificadores son reconstruidos desde 1.

Ejemplo:

Antes:

```text
ID:
1
2
5
8
```

Después:

```text
ID:
1
2
3
4
```

Esto evita espacios vacíos dentro del identificador principal del corpus.

## Funciones principales

### `detectar_encoding(file_path)`

Detecta la codificación del archivo utilizando análisis binario.

**Entrada:**

* Ruta del archivo.

**Salida:**

* Codificación detectada.

### `convertir_a_utf8_si_necesario(ruta_entrada)`

Convierte archivos con codificaciones incompatibles a UTF-8.

**Salida:**

* Archivo UTF-8.

### `detectar_duplicados(df, case_sensitive=True)`

Busca registros repetidos dentro del `DataFrame`.

**Parámetros:**

| Parámetro        | Descripción                     |
| ---------------- | ------------------------------- |
| `df`             | Dataset del corpus              |
| `case_sensitive` | Define si diferencia mayúsculas |

**Retorna:**

* `DataFrame` con los registros duplicados.

### `eliminar_duplicados_y_reindexar(df, case_sensitive=True)`

Ejecuta la limpieza completa:

* Eliminación de duplicados.
* Conservación de primera ocurrencia.
* Reasignación de IDs.

**Retorna:**

* `DataFrame` limpio.

### `normalizar_mayusculas_completas(df, cols)`

Transforma cadenas completamente en mayúsculas dentro de las columnas indicadas.

**Columnas procesadas:**

```python
[
    "frase_es",
    "frase_sh"
]
```

### `guardar_corpus(df, ruta_original, formato)`

Guarda el resultado final del corpus.

**Opciones:**

```text
1. Sobrescribir archivo original
2. Crear archivo nuevo:
   corpus_limpio.csv
```

**Formatos disponibles:**

* CSV
* JSON

## Resultados generados

Cuando existen duplicados y son eliminados, el módulo genera un archivo limpio como:

```text
corpus_principal_limpio.csv
```

Contenido de ejemplo:

```csv
ID,frase_es,frase_sh,dominio,fecha,origen
1,La casa es grande,Jea penker nekata,Cultural,10-07-2026,Documento
2,El niño estudia,Uchich unuimiatain,Educativo,10-07-2026,Documento
```

## Estadísticas mostradas

Durante la ejecución se muestran resultados como los siguientes:

### Antes de limpieza

```text
Total de pares en el corpus: 5000
Pares duplicados encontrados: 35
```

### Después de limpieza

```text
Pares únicos después de eliminar duplicados: 4965
Nuevo rango de IDs:
1 a 4965
```

## Dependencias

| Librería  | Uso                         |
| --------- | --------------------------- |
| `os`      | Gestión de archivos y rutas |
| `pandas`  | Manipulación de datasets    |
| `chardet` | Detección de codificación   |

## Consideraciones técnicas

La eliminación de duplicados es una etapa importante dentro del control de calidad del corpus, debido a que registros repetidos pueden alterar:

* Conteos de frecuencia léxica.
* Distribuciones por dominio.
* Cálculos de diversidad lingüística.
* Evaluaciones posteriores del conjunto de datos.

Este módulo permite garantizar que cada par español–shuar represente una unidad lingüística única antes de realizar análisis estadísticos o utilizar el corpus en aplicaciones de procesamiento del lenguaje natural.


# Análisis descriptivo de corpus bilingüe español–shuar

## Descripción

Este script implementa un módulo de análisis descriptivo para el corpus bilingüe español–shuar.

Su finalidad es calcular métricas cuantitativas que permitan caracterizar el corpus desde tres perspectivas principales: tamaño, diversidad léxica y representatividad temática. Para ello, el módulo carga archivos en formato CSV o JSON, valida su estructura, realiza cálculos sobre los segmentos lingüísticos y genera tablas y gráficos de salida para facilitar la interpretación de los resultados.

Este componente corresponde a la etapa de **evaluación y caracterización del corpus** dentro del flujo general del proyecto.

## Objetivo del módulo

El script tiene como objetivos:

* Cargar corpus bilingües en formato CSV o JSON.
* Verificar la estructura básica de los datos.
* Validar la existencia de columnas lingüísticas y metadatos.
* Calcular métricas de tamaño del corpus.
* Estimar la diversidad léxica mediante Type-Token Ratio (TTR).
* Analizar la distribución por dominio temático.
* Evaluar la representatividad y el equilibrio de las categorías.
* Generar tablas y gráficos de apoyo para el informe final.

## Ubicación dentro del pipeline

Este módulo se ejecuta después de la construcción y limpieza del corpus.

```text
Extracción de documentos
          │
          ▼
Limpieza y normalización textual
          │
          ▼
Estructuración del corpus
          │
          ▼
Análisis descriptivo
          │
          ▼
Generación de métricas, tablas y gráficos
```

## Formatos compatibles

El script acepta corpus en los siguientes formatos:

| Formato | Extensión | Carga                |
| ------- | --------- | -------------------- |
| CSV     | `.csv`    | `pandas.read_csv()`  |
| JSON    | `.json`   | `pandas.read_json()` |

## Características principales

### Selección interactiva del archivo

El módulo permite seleccionar el corpus mediante dos modalidades:

1. Especificar un directorio y elegir un archivo desde una lista.
2. Ingresar directamente la ruta completa del archivo.

---

### Detección y conversión de codificación

Antes del análisis, el script verifica la codificación del archivo con `chardet`.

Si el archivo no está en UTF-8, se genera una versión convertida para evitar errores durante la lectura o el procesamiento de caracteres especiales.

---

### Validación estructural

El sistema verifica que el corpus contenga al menos las columnas necesarias para el análisis:

* `frase_es`
* `frase_sh`

También identifica la columna `dominio` cuando está disponible, ya que esta permite realizar análisis por categoría temática.

Durante esta fase se eliminan:

* filas con valores nulos,
* filas con frases vacías,
* registros inconsistentes.

---

### Cálculo de métricas de tamaño

El módulo calcula indicadores básicos del corpus:

* número total de pares alineados,
* total de tokens en español,
* total de tokens en shuar.

---

### Cálculo de diversidad léxica

Se utiliza la métrica **Type-Token Ratio (TTR)** para medir la relación entre tipos léxicos distintos y cantidad total de tokens.

El cálculo se realiza:

* de forma global para español y shuar,
* por dominio temático cuando existe la columna `dominio`.

---

### Análisis de representatividad temática

Cuando el corpus contiene la columna `dominio`, el script calcula:

* frecuencia absoluta por dominio,
* porcentaje por dominio,
* comparación frente a una distribución uniforme,
* desviación porcentual de cada categoría.

Además, aplica una prueba de chi-cuadrado para evaluar si la distribución observada difiere significativamente de una distribución uniforme.

---

### Consolidación de resultados

El módulo genera tablas resumen con las métricas calculadas y las guarda en archivos CSV.

También crea gráficos para representar visualmente:

* la diversidad léxica por dominio,
* la distribución porcentual de los dominios,
* la composición temática del corpus.

## Funciones principales

### `detectar_encoding(archivo)`

Detecta la codificación del archivo de entrada.

**Salida:**

* Codificación identificada por `chardet`.

---

### `convertir_a_utf8(archivo)`

Convierte el archivo a UTF-8 si su codificación original es distinta.

**Salida:**

* Archivo convertido, cuando corresponde.

---

### `seleccionar_archivo()`

Permite escoger el archivo del corpus mediante interfaz de texto.

Opciones:

* seleccionar desde un directorio,
* ingresar una ruta directa.

---

### `cargar_corpus(ruta)`

Carga el corpus en un `DataFrame` de `pandas`.

Formatos admitidos:

* CSV
* JSON

---

### `validar_estructura(df)`

Verifica y normaliza la estructura del corpus.

Tareas realizadas:

* detección de columnas equivalentes a `frase_es`, `frase_sh` y `dominio`,
* renombramiento estandarizado,
* eliminación de filas vacías,
* depuración de registros incompletos.

---

### `verificar_metadatos(df)`

Comprueba la presencia de la columna `dominio` y reporta las categorías encontradas.

---

### `actividad1_validaciones(df, ruta_original)`

Resume la primera actividad del análisis:

* carga del corpus,
* validación de la codificación,
* validación estructural,
* verificación de metadatos.

---

### `contar_tokens(texto)`

Cuenta tokens en un texto usando una expresión regular basada en palabras.

---

### `actividad2_metricas_tamano(df)`

Calcula métricas de tamaño del corpus:

* pares alineados,
* tokens en español,
* tokens en shuar.

---

### `calcular_ttr(lista_textos)`

Calcula el Type-Token Ratio para una serie de textos.

---

### `actividad3_ttr(df, tiene_dominio)`

Calcula la diversidad léxica:

* TTR global para español y shuar,
* TTR por dominio cuando existe la columna correspondiente.

---

### `actividad4_representatividad(df, tiene_dominio)`

Evalúa la distribución temática del corpus.

Incluye:

* conteo por dominio,
* porcentajes,
* desviación respecto a distribución uniforme,
* prueba chi-cuadrado,
* generación de gráficos.

---

### `actividad5_consolidacion(df, total_tokens_es, total_tokens_sh, ttr_results, rep_results)`

Consolida los resultados en tablas finales y los guarda en archivos CSV.

---

### `main()`

Ejecuta el flujo completo del análisis:

1. Selección del archivo.
2. Conversión a UTF-8 si es necesario.
3. Carga del corpus.
4. Validación estructural.
5. Cálculo de tamaño.
6. Cálculo de TTR.
7. Análisis de representatividad.
8. Consolidación de resultados.

## Dependencias

| Librería                       | Función                                  |
| ------------------------------ | ---------------------------------------- |
| `os`                           | Gestión de archivos y rutas.             |
| `sys`                          | Control del flujo de ejecución.          |
| `chardet`                      | Detección de codificación.               |
| `pandas`                       | Carga, limpieza y análisis de datos.     |
| `numpy`                        | Operaciones numéricas.                   |
| `matplotlib.pyplot`            | Generación de gráficos.                  |
| `seaborn`                      | Configuración visual de gráficos.        |
| `scipy.stats.chi2_contingency` | Prueba estadística de homogeneidad.      |
| `re`                           | Expresiones regulares para tokenización. |
| `datetime`                     | Manejo de fechas.                        |

## Métricas calculadas

### Tamaño del corpus

* Número total de pares.
* Número total de tokens en español.
* Número total de tokens en shuar.

### Diversidad léxica

* TTR global en español.
* TTR global en shuar.
* TTR por dominio.

### Representatividad temática

* Frecuencia por dominio.
* Porcentaje por dominio.
* Desviación respecto a distribución uniforme.
* Valor de chi-cuadrado.
* Valor p de significancia.

## Archivos generados

El script produce los siguientes archivos de salida:

| Archivo                        | Descripción                                       |
| ------------------------------ | ------------------------------------------------- |
| `ttr_por_dominio.png`          | Gráfico de diversidad léxica por dominio.         |
| `distribucion_dominios.png`    | Gráfico de barras de la distribución por dominio. |
| `composicion_dominios_pie.png` | Gráfico circular de la composición temática.      |
| `resumen_metricas.csv`         | Tabla resumen con las métricas principales.       |
| `ttr_por_dominio.csv`          | Tabla con los valores de TTR por dominio.         |
| `distribucion_dominios.csv`    | Tabla con la distribución porcentual por dominio. |

## Flujo general del procesamiento

```text
Archivo CSV o JSON
        │
        ▼
Detección y conversión de codificación
        │
        ▼
Carga del corpus
        │
        ▼
Validación de estructura y metadatos
        │
        ▼
Cálculo de métricas de tamaño
        │
        ▼
Cálculo de diversidad léxica (TTR)
        │
        ▼
Análisis de representatividad temática
        │
        ▼
Consolidación de tablas y gráficos
```

## Consideraciones

Este módulo permite caracterizar el corpus desde una perspectiva descriptiva y cuantitativa. Sus resultados sirven como evidencia técnica para evaluar la dimensión del conjunto de datos, la variabilidad léxica de ambos idiomas y la distribución temática de los segmentos incluidos.
