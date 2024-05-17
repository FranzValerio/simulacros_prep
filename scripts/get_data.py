import requests
import os
import zipfile

def download_file(url, path_file):

    respuesta = requests.get(url)

    respuesta.raise_for_status()

    with open(path_file, 'wb') as f:

        f.write(respuesta.content)

    print(f'Archivo descargado y guardado en: {path_file}')

def decompress_save_file(zip_file, destiny_folder):

    if not os.path.exists(destiny_folder):

        os.makedirs(destiny_folder)

    with zipfile.ZipFile(zip_file, 'r') as archivo:

        archivo.extractall(destiny_folder)

    print(f'Archivos descomprimidos en: {destiny_folder}')

