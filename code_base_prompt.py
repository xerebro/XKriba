import os

# Extensiones permitidas
ALLOWED_EXTENSIONS = {".js", ".html", ".json", ".css", ".ts", ".tsx", ".vue", ".yaml", ".yml"}

# Directorio base donde se encuentran los archivos
base_dir = r"/Users/pruebas/Documents/Magik/XKriba/"

# Archivo de salida
OUTPUT_FILE = "codigo_fuente.txt"

# Carpetas y archivos a excluir
EXCLUDE_FOLDERS = {"public", "node_modules", "dist"}
EXCLUDE_FILES = {"package-lock.json", "yarn.lock", "README.md", "LICENSE", "CHANGELOG.md"}

# Contenido inicial del archivo
HEADER = """Eres un ingeniero de software de élite especializado en el desarrollo de extensiones para navegadores, particularmente Chrome. Tienes una vasta experiencia en la implementación de tecnologías de Inteligencia Artificial en el navegador utilizando bibliotecas como transformers.js. Tu enfoque es la excelencia, la precisión y la optimización de rendimiento con baja latencia. 
Tu objetivo es mejorar y optimizar la base de código proporcionada, identificando y resolviendo problemas, creando nuevas funcionalidades y mejorando el rendimiento general del proyecto. 
A continuación, se presenta la base de código del proyecto. Cada archivo de código fuente está marcado con un indicador de inicio y fin, junto con el nombre y la ruta relativa del archivo:\n\n"""
FOOTER = """\n\n\n\nIMPORTANTE:

* Siempre proporciona respuestas completas y detalladas.
* Planifica tus pasos de manera estructurada antes de comenzar cualquier tarea.
* Asegúrate de que tus respuestas sean técnicamente precisas y de alta calidad.

A continuación, las tareas a completar:: \n\n"""

def is_allowed_file(filename):
    """Verifica si el archivo tiene una extensión permitida."""
    return any(filename.endswith(ext) for ext in ALLOWED_EXTENSIONS)


def build_file_block(relative_path, content):
    """Construye el bloque de texto para cada archivo."""
    return f"/{relative_path}:\n------BEGIN OF FILE----\n{content}\n------END OF FILE----\n\n"


def should_exclude_folder(folder_name):
    """Determina si la carpeta debe ser excluida."""
    return folder_name.lower() in EXCLUDE_FOLDERS


def main():
    output_path = os.path.join(base_dir, OUTPUT_FILE)

    with open(output_path, "w", encoding="utf-8") as output:
        output.write(HEADER)
        process_folder(base_dir, output)
        output.write(FOOTER)
        # Recorre recursivamente desde base_dir
        

    print(f"Archivo generado: {output_path}")

def process_folder(folder_path, output):
    for root, dirs, files in os.walk(folder_path, topdown=True):
            # Elimina carpetas excluidas antes de procesarlas
            dirs[:] = [d for d in dirs if not should_exclude_folder(d)]

            for filename in files:
                # Saltar archivos excluidos
                if filename in EXCLUDE_FILES:
                    continue

                # Verificar extensión
                if not is_allowed_file(filename):
                    continue

                full_path = os.path.join(root, filename)
                relative_path = os.path.relpath(full_path, base_dir)

                try:
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                    output.write(build_file_block(relative_path, content))
                except Exception as e:
                    print(f"Error leyendo {relative_path}: {e}")
            for dir_name in dirs:
                # Procesar subcarpetas
                subfolder_path = os.path.join(root, dir_name)
                process_folder(subfolder_path, output)
if __name__ == "__main__":
    main()