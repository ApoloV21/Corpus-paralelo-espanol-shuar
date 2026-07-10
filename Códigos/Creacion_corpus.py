import csv
import os
from datetime import datetime
import sys

class CorpusImporter:
    def __init__(self, corpus_file="corpus_principal.csv"):
        """
        Inicializa el importador.
        
        Args:
            corpus_file: Nombre del archivo del corpus principal
        """
        self.corpus_file = corpus_file
        self.dominios_validos = [
            "Educativo", "Cultural", "Médico",
            "Literario", "Otro"
        ]
        
        # Inicializar corpus si no existe
        self._inicializar_corpus()
    
    def _inicializar_corpus(self):
        """Crea el archivo del corpus si no existe"""
        if not os.path.exists(self.corpus_file):
            with open(self.corpus_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['ID', 'frase_es', 'frase_sh', 'dominio', 'fecha', 'origen'])
            print(f"✓ Corpus creado: {self.corpus_file}")
    
    def _validar_archivo_txt(self, ruta_archivo):
        """
        Valida que el archivo existe y es un TXT.
        
        Args:
            ruta_archivo: Ruta completa del archivo
            
        Returns:
            bool: True si es válido, False si no
        """
        # Verificar si es archivo (no carpeta)
        if not os.path.isfile(ruta_archivo):
            print(f"✗ Error: '{ruta_archivo}' no es un archivo (es una carpeta)")
            return False
        
        # Verificar extensión .txt
        if not ruta_archivo.lower().endswith('.txt'):
            print(f"✗ Error: '{ruta_archivo}' no tiene extensión .txt")
            return False
        
        # Verificar que existe
        if not os.path.exists(ruta_archivo):
            print(f"✗ Error: Archivo no encontrado: {ruta_archivo}")
            return False
        
        # Verificar que se puede leer
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                f.readline()
            return True
        except UnicodeDecodeError:
            print(f"✗ Error: El archivo no está en UTF-8. Conviértelo a UTF-8 primero.")
            return False
        except Exception as e:
            print(f"✗ Error al leer archivo: {e}")
            return False
    
    def _leer_txt_fuente_simple(self, archivo_fuente):
        """
        Lee un TXT con formato: frase_en|frase_sh por línea
        
        Args:
            archivo_fuente: Ruta del archivo TXT
            
        Returns:
            Lista de tuplas [(frase_es, frase_sh), ...]
        """
        pares_frases = []
        
        try:
            with open(archivo_fuente, 'r', encoding='utf-8') as f:
                for num_linea, linea in enumerate(f, 1):
                    linea = linea.strip()
                    if not linea:
                        continue
                    
                    # Dividir por |
                    partes = linea.split('|', 1)
                    if len(partes) == 2:
                        frase_es = partes[0].strip()
                        frase_sh = partes[1].strip()
                        
                        if frase_es and frase_sh:
                            pares_frases.append((frase_es, frase_sh))
                        else:
                            print(f"  ⚠ Línea {num_linea}: Campos vacíos, omitida")
                    else:
                        print(f"  ⚠ Línea {num_linea}: Formato incorrecto, se necesita 'frase_es|frase_sh'")
                
                print(f"  ✓ Líneas procesadas: {num_linea}")
                
        except Exception as e:
            print(f"✗ Error crítico al leer TXT: {e}")
            return []
        
        return pares_frases
    
    def _obtener_proximo_id(self):
        """Obtiene el próximo ID disponible en el corpus"""
        try:
            with open(self.corpus_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)  # Saltar encabezado
                
                ids = []
                for row in reader:
                    if row and row[0].strip().isdigit():
                        ids.append(int(row[0]))
                
                return max(ids) + 1 if ids else 1
        except Exception as e:
            print(f"  Nota: Error al leer IDs existentes: {e}")
            return 1
        
    def _listar_txt_en_directorio(self, directorio):
        """Devuelve lista de archivos .txt en el directorio dado."""
        try:
            archivos = [f for f in os.listdir(directorio) if f.lower().endswith('.txt')]
            return sorted(archivos)
        except FileNotFoundError:
            return []

    def _elegir_archivo_de_directorio(self, directorio):
        """Muestra menú con archivos .txt de un directorio y retorna la ruta completa del elegido."""
        archivos = self._listar_txt_en_directorio(directorio)
        if not archivos:
            print(f"No se encontraron archivos .txt en el directorio: {directorio}")
            return None
        print(f"\nArchivos .txt en '{directorio}':")
        for i, arch in enumerate(archivos, start=1):
            print(f"{i}. {arch}")
        while True:
            try:
                opcion = int(input("Elige el número del archivo (0 para cancelar): "))
                if opcion == 0:
                    return None
                if 1 <= opcion <= len(archivos):
                    return os.path.join(directorio, archivos[opcion-1])
                else:
                    print(f"Opción inválida. Elige entre 1 y {len(archivos)}.")
            except ValueError:
                print("Por favor, ingresa un número válido.")

    def importar_desde_txt(self, archivo_txt, dominio, origen):
        """
        Importa frases desde un TXT al corpus.
        
        Args:
            archivo_txt: Ruta del archivo TXT fuente
            dominio: Dominio para todas las frases
            origen: Origen para todas las frases
            
        Returns:
            int: Número de frases importadas
        """
        print(f"\n{'='*60}")
        print(f"IMPORTANDO DESDE TXT")
        print(f"{'='*60}")
        
        # 1. Validar archivo
        if not self._validar_archivo_txt(archivo_txt):
            return 0
        
        # 2. Validar dominio
        if dominio not in self.dominios_validos:
            print(f"\n⚠ Advertencia: '{dominio}' no está en la lista de dominios válidos.")
            print("Dominios válidos:")
            for i, dom in enumerate(self.dominios_validos, 1):
                print(f"  {i}. {dom}")
            
            usar_dominio = input(f"\n¿Usar '{dominio}' de todos modos? (s/n): ").lower()
            if usar_dominio != 's':
                print("Importación cancelada.")
                return 0
        
        # 3. Leer frases del TXT
        print(f"\nLeyendo archivo: {os.path.basename(archivo_txt)}")
        pares_frases = self._leer_txt_fuente_simple(archivo_txt)
        
        if not pares_frases:
            print("✗ No se encontraron frases válidas para importar.")
            return 0
        
        print(f"✓ Frases válidas encontradas: {len(pares_frases)}")
        
        # 4. Mostrar vista previa
        print("\n--- VISTA PREVIA (primeras 5 frases) ---")
        for i, (es, sh) in enumerate(pares_frases[:5], 1):
            es_preview = es[:60] + "..." if len(es) > 60 else es
            sh_preview = sh[:60] + "..." if len(sh) > 60 else sh
            print(f"{i}. Español: {es_preview}")
            print(f"   Indígena: {sh_preview}")
            print()
        
        if len(pares_frases) > 5:
            print(f"... y {len(pares_frases) - 5} frases más")
        
        # 5. Confirmar importación
        confirmar = input(f"\n¿Importar {len(pares_frases)} frases al corpus? (s/n): ").lower()
        if confirmar != 's':
            print("Importación cancelada.")
            return 0
        
        # 6. Preparar datos
        fecha_actual = datetime.now().strftime("%d-%m-%Y")
        id_inicial = self._obtener_proximo_id()
        frases_importadas = 0
        
        # 7. Importar al corpus
        print("\nImportando frases...")
        try:
            with open(self.corpus_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                for i, (frase_es, frase_sh) in enumerate(pares_frases, id_inicial):
                    entrada = [i, frase_es, frase_sh, dominio, fecha_actual, origen]
                    writer.writerow(entrada)
                    frases_importadas += 1
            
            print(f"✓ Importación exitosa!")
            
        except Exception as e:
            print(f"✗ Error durante la importación: {e}")
            return 0
        
        # 8. Mostrar resumen
        self._mostrar_resumen_importacion(frases_importadas, id_inicial)
        return frases_importadas
    
    def _mostrar_resumen_importacion(self, frases_importadas, id_inicial):
        """Muestra resumen de la importación"""
        print(f"\n{'='*60}")
        print(f"RESUMEN DE IMPORTACIÓN")
        print(f"{'='*60}")
        print(f"Frases importadas: {frases_importadas}")
        print(f"Rango de IDs: {id_inicial} - {id_inicial + frases_importadas - 1}")
        print(f"Archivo del corpus: {self.corpus_file}")
        
        # Contar frases totales en corpus
        total_frases = self._contar_frases_totales()
        print(f"Total de frases en corpus: {total_frases}")
        
        # Mostrar última entrada como ejemplo
        if frases_importadas > 0:
            print(f"\n--- Última entrada agregada ---")
            ultima_id = id_inicial + frases_importadas - 1
            self._mostrar_entrada(ultima_id)
    
    def _contar_frases_totales(self):
        """Cuenta total de frases en el corpus"""
        try:
            with open(self.corpus_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                # Restar 1 por el encabezado
                return sum(1 for row in reader) - 1
        except:
            return 0
    
    def _mostrar_entrada(self, id_entrada):
        """Muestra una entrada específica del corpus"""
        try:
            with open(self.corpus_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                encabezado = next(reader)
                
                for fila in reader:
                    if fila and fila[0] == str(id_entrada):
                        print(f"ID: {fila[0]}")
                        print(f"Español: {fila[1]}")
                        print(f"Indígena: {fila[2]}")
                        print(f"Dominio: {fila[3]}")
                        print(f"Fecha: {fila[4]}")
                        print(f"Origen: {fila[5]}")
                        return
            print(f"No se encontró la entrada con ID {id_entrada}")
        except Exception as e:
            print(f"Error al leer entrada: {e}")
    
    def mostrar_estadisticas(self):
        """Muestra estadísticas del corpus actual"""
        try:
            with open(self.corpus_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                datos = list(reader)
            
            if not datos:
                print("El corpus está vacío.")
                return
            
            print(f"\n{'='*60}")
            print(f"ESTADÍSTICAS DEL CORPUS")
            print(f"{'='*60}")
            print(f"Total de frases: {len(datos)}")
            
            # Estadísticas por dominio
            dominios = {}
            for fila in datos:
                dom = fila['dominio']
                dominios[dom] = dominios.get(dom, 0) + 1
            
            print("\nDistribución por dominio:")
            for dominio, cantidad in sorted(dominios.items()):
                porcentaje = (cantidad / len(datos)) * 100
                print(f"  {dominio}: {cantidad} ({porcentaje:.1f}%)")
            
            # Estadísticas por origen
            origenes = {}
            for fila in datos:
                org = fila['origen']
                origenes[org] = origenes.get(org, 0) + 1
            
            print("\nDistribución por origen:")
            for origen, cantidad in sorted(origenes.items(), key=lambda x: x[1], reverse=True):
                porcentaje = (cantidad / len(datos)) * 100
                print(f"  {origen}: {cantidad} ({porcentaje:.1f}%)")
                
        except Exception as e:
            print(f"Error al mostrar estadísticas: {e}")
    
    def convertir_a_json(self):
        """Convierte el corpus CSV a JSON"""
        try:
            import json
            
            json_file = self.corpus_file.replace('.csv', '.json')
            
            with open(self.corpus_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                datos = list(reader)
            
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(datos, f, ensure_ascii=False, indent=2)
            
            print(f"✓ Corpus convertido a JSON: {json_file}")
            print(f"  Total de entradas: {len(datos)}")
            
            return json_file
        except Exception as e:
            print(f"✗ Error al convertir a JSON: {e}")
            return None
    
    def menu_principal(self):
        """Menú principal interactivo"""
        while True:
            print(f"\n{'='*60}")
            print(f"IMPORTADOR DE CORPUS TXT")
            print(f"Corpus actual: {self.corpus_file}")
            print(f"{'='*60}")
            
            # Mostrar estado actual
            total = self._contar_frases_totales()
            print(f"Frases en corpus: {total}")
            
            print("\nOPCIONES:")
            print("1. Importar frases desde un archivo TXT")
            print("2. Ver estadísticas del corpus")
            print("3. Convertir corpus a JSON")
            print("4. Cambiar nombre del corpus")
            print("5. Ver primeras 10 entradas")
            print("6. Salir")
            
            opcion = input("\nSeleccione una opción (1-6): ").strip()
            
            if opcion == '1':
                self._ejecutar_importacion()
            elif opcion == '2':
                self.mostrar_estadisticas()
            elif opcion == '3':
                self.convertir_a_json()
            elif opcion == '4':
                self._cambiar_corpus()
            elif opcion == '5':
                self._ver_primeras_entradas()
            elif opcion == '6':
                print("¡Hasta luego!")
                break
            else:
                print("Opción no válida. Intente nuevamente.")
    
    def _ejecutar_importacion(self):
        """Ejecuta el proceso de importación paso a paso, permitiendo elegir archivo por directorio o ruta directa."""
        print("\n--- IMPORTAR DESDE TXT ---")
    
    # --- 1. SELECCIÓN DEL ARCHIVO TXT ---
        print("\n[1/3] ESPECIFICAR ARCHIVO TXT")
        print("Seleccione cómo desea indicar el archivo:")
        print("1. Especificar un DIRECTORIO y elegir un archivo .txt de la lista")
        print("2. Ingresar la RUTA DIRECTA de un archivo .txt")
        opcion_ruta = input("\nElige una opción (1/2): ").strip()
    
        archivo_txt = None
        if opcion_ruta == '1':
            # Seleccionar directorio
            ruta_dir = input("Ingresa la ruta del directorio: ").strip()
            ruta_dir = os.path.expanduser(ruta_dir)
            if not os.path.isdir(ruta_dir):
                print("Error: la ruta no es un directorio válido.")
                return
            archivo_txt = self._elegir_archivo_de_directorio(ruta_dir)
            if archivo_txt is None:
                print("No se seleccionó ningún archivo. Importación cancelada.")
                return
        elif opcion_ruta == '2':
            # Ruta directa
            print("Ejemplos de rutas:")
            print("  • frases.txt (si está en la misma carpeta)")
            print("  • datos/mis_frases.txt")
            print("  • C:\\Usuarios\\Nombre\\frases.txt")
            while True:
                ruta = input("\nRuta del archivo TXT: ").strip()
                # Si solo se ingresa un nombre, buscar en carpeta actual
                if not os.path.dirname(ruta):
                    ruta = os.path.join(os.getcwd(), ruta)
                if self._validar_archivo_txt(ruta):
                    archivo_txt = ruta
                    break
        else:
            print("Opción no válida. Importación cancelada.")
            return
        
        # Ya tenemos archivo_txt validado
        # --- 2. SELECCIONAR DOMINIO (igual que antes) ---
        print("\n[2/3] SELECCIONAR DOMINIO")
        print("Dominios disponibles:")
        for i, dominio in enumerate(self.dominios_validos, 1):
            print(f"  {i}. {dominio}")
        print("  0. Otro (escribir manualmente)")
        
        while True:
            opcion_dominio = input("\nSeleccione dominio (número) o '0' para otro: ").strip()
            if opcion_dominio == '0':
                dominio = input("Escriba el dominio: ").strip()
                break
            elif opcion_dominio.isdigit() and 1 <= int(opcion_dominio) <= len(self.dominios_validos):
                dominio = self.dominios_validos[int(opcion_dominio) - 1]
                break
            else:
                print("Opción no válida. Intente nuevamente.")
        
        # --- 3. ESPECIFICAR ORIGEN (igual que antes) ---
        print("\n[3/3] ESPECIFICAR ORIGEN")
        print("Ejemplos: 'Libro del MINEDUC', 'Entrevistas comunitarias 2023',")
        print("'Diccionario Shawi', 'Taller de revitalización lingüística'")
        origen = input("\nOrigen/fuente de los datos: ").strip()
        
        # --- 4. EJECUTAR IMPORTACIÓN ---
        print(f"\n{'='*60}")
        print("INICIANDO IMPORTACIÓN...")
        print(f"{'='*60}")
        
        resultado = self.importar_desde_txt(archivo_txt, dominio, origen)
        
        if resultado > 0:
            print(f"\n✓ Proceso completado exitosamente!")
        else:
            print(f"\n✗ No se importaron frases.")
    
    def _cambiar_corpus(self):
        """Permite cambiar el archivo del corpus"""
        nuevo_nombre = input("\nNuevo nombre para el corpus (ej: corpus_shawi.csv): ").strip()
        if not nuevo_nombre.lower().endswith('.csv'):
            nuevo_nombre += '.csv'
        
        self.corpus_file = nuevo_nombre
        self._inicializar_corpus()
        print(f"✓ Corpus cambiado a: {nuevo_nombre}")
    
    def _ver_primeras_entradas(self, cantidad=10):
        """Muestra las primeras entradas del corpus"""
        try:
            with open(self.corpus_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                encabezado = next(reader)
                
                print(f"\nPrimeras {min(cantidad, 10)} entradas del corpus:")
                print("-" * 60)
                
                for i, fila in enumerate(reader, 1):
                    if i > cantidad:
                        break
                    
                    print(f"ID: {fila[0]}")
                    print(f"Español: {fila[1][:50]}..." if len(fila[1]) > 50 else f"Español: {fila[1]}")
                    print(f"Indígena: {fila[2][:50]}..." if len(fila[2]) > 50 else f"Indígena: {fila[2]}")
                    print(f"Dominio: {fila[3]} | Fecha: {fila[4]} | Origen: {fila[5]}")
                    print("-" * 40)
                    
        except Exception as e:
            print(f"Error al leer corpus: {e}")


# EJEMPLO DE USO RÁPIDO
if __name__ == "__main__":
    print("INICIALIZANDO IMPORTADOR DE CORPUS TXT")
    print("=" * 60)
    
    # Preguntar por el nombre del corpus
    corpus_nombre = input("Nombre del archivo corpus (ENTER para 'corpus.csv'): ").strip()
    if not corpus_nombre:
        corpus_nombre = "corpus.csv"
    
    # Crear importador
    importador = CorpusImporter(corpus_nombre)
    
    # Iniciar menú principal
    importador.menu_principal()