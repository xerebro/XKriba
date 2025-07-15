import os

# Extensiones permitidas
ALLOWED_EXTENSIONS = {".js", ".html", ".json", ".css", ".ts", ".tsx", ".vue", ".yaml", ".yml"}

# Directorio base donde se encuentran los archivos
base_dir = r"/Users/pruebas/Documents/Magik/XMeet/"

# Archivo de salida
OUTPUT_FILE = "codigo_fuente.txt"

# Carpetas y archivos a excluir
EXCLUDE_FOLDERS = {"public", "node_modules", "dist"}
EXCLUDE_FILES = {"package-lock.json", "yarn.lock", "README.md", "LICENSE", "CHANGELOG.md"}

# Contenido inicial del archivo
HEADER = "Eres un desarrollador experto en extensiones para browser particularmente chrome, eres proactivo, inteligente, enfocado al detalle y a la calidad, te caracterizas por tomardesiciones autonomas y acertadas de cara a completar tus tareas, siempre entregas tustareas con alta calidad y alto nivel tecnico, tienes aplios conocimientos en ejecutar modelos de Gen AI en el browser usando transformers.js con baja latenciay usando el estado del arte en modelos,debes trabajar en la siguiente base de codigo:\n\n"
FOOTER = "\n\nIMPORTATE:\n\n* Siempre sa como respuesta el archivo completo\nnComo comptente desarrollador debes ayudarme a completar satisfactoriamente usa serie de tareas, antes de iniciar tu trabajo en una tarea planifica la serie de pasos que te permnita completar la tarea con alta calidad.\n\nA continuacion la tareas a completar: \n\n"

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