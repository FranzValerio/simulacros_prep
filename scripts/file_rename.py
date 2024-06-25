import os

def renombrar_archivos_a_minusculas(ruta_carpeta):
    # Verificar si la ruta de la carpeta es válida
    if not os.path.isdir(ruta_carpeta):
        print(f"La ruta {ruta_carpeta} no es válida.")
        return

    # Obtener la lista de archivos en la carpeta
    archivos = os.listdir(ruta_carpeta)

    # Recorrer cada archivo en la carpeta
    for archivo in archivos:
        ruta_completa = os.path.join(ruta_carpeta, archivo)
        # Verificar si es un archivo (y no una carpeta)
        if os.path.isfile(ruta_completa):
            # Obtener el nuevo nombre en minúsculas
            nuevo_nombre = archivo.lower()
            ruta_nueva = os.path.join(ruta_carpeta, nuevo_nombre)
            # Renombrar el archivo
            os.rename(ruta_completa, ruta_nueva)
            print(f"Renombrado: {archivo} -> {nuevo_nombre}")
        else:
            print(f"{ruta_completa} no es un archivo. Se omite.")

# Ruta de la carpeta que contiene los archivos
ruta_carpeta = 'C:/Users/Francisco Valerio/Desktop/INE/Simulacros/simulacros_prep/img/ayun'

# Llamar a la función para renombrar los archivos
renombrar_archivos_a_minusculas(ruta_carpeta)
