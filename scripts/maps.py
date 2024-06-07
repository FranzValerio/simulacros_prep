import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import warnings
import sys
from datetime import datetime, timedelta
import json

warnings.filterwarnings('ignore')

tipo_eleccion = str(input("Indique el tipo de elección a analizar: 'GUB', 'DIP_LOC', o 'AYUN': ")).upper()

folder_path = 'C:/Users/Francisco Valerio/Desktop/INE/Simulacros/simulacros_prep/BDD'

geo_mun_path = 'C:/Users/Francisco Valerio/Desktop/INE/Simulacros/simulacros_prep/geodata/geo_mun_pue.csv'

geo_json_path = 'C:/Users/Francisco Valerio/Desktop/INE/Simulacros/simulacros_prep/geodata/Puebla.json'



inicio_intervalo = pd.to_datetime('2024-06-03 00:20')
fin_intervalo = pd.to_datetime('2024-06-03 01:00')

hora_inicio = datetime(2024,6, 2, 20, 00)
fecha_corte = datetime(2024, 6, 3, 20, 00)

totales = {'GUB': 8334,
            'DIP_LOC': 8423,
            'AYUN': 8352}

def find_csv(folder_path, identifier):
    """Busca archivos CSV en la carpeta especificada y que coincide
     con el identificador de elección declarado en la variable tipo_eleccion

     Args:
     folder_path (str): Ruta al directorio donde va a buscar los archivos
     identifier (str): Identificador del tipo de elección

     Returns:
     str: Ruta completa al archivo si lo encuentra, None en caso contrario"""

    for file in os.listdir(folder_path):

        if file.endswith('.csv') and identifier in file:

            return os.path.join(folder_path, file)

    return None

def load_csv(file_path):
    """Carga un archivo CSV en un DataFrame de Pandas, debido a la estructura
    de las BDD, se omiten las primeras 5 filas, se incluye el parámetro low_memory = False
    para optimizar la memoria

    Args:
    file_path (str): La ruta completa al archivo CSV que se desea cargar. Si el archivo no existe o
                         el valor es None, la función imprimirá un mensaje de error y retornará None.

    Returns:
        pd.DataFrame: Un DataFrame que contiene los datos del archivo CSV especificado. Retorna None si no
                      se proporciona una ruta de archivo válida o si el archivo no se encuentra."""

    if file_path:

        with open(file_path, 'r', encoding='utf-8') as file:

            lines = file.readlines()

        if len(lines) > 5:

            info_rows = lines[4:5]

            column_names = lines[3].strip().split(',')

            second_line = lines[1].strip().split(',')

            data_info_rows = [line.strip().split(',') for line in info_rows]

            info = pd.DataFrame(data_info_rows, columns=column_names)

            info.insert(0, 'Fecha_corte', second_line[0])

            df = pd.read_csv(file_path, skiprows = 5, low_memory=False)

            return df, info

    else:

        print("No se encontró ningún archivo CSV.")

        return None, None

def check_nans(df):
    """Revisa si existen valores NaNs en las columnas de FECHA_HORA_ACOPIO, FECHA_HORA_CAPTURA y
    FECHA_HORA_VERIFICACION. Se aplica previo a la conversión de datos tipo object a datetime para
    poder calcular el tiempo de procesamiento

    Args:
    df (pd.DataFrame): La dataframe que se va a utilizar

    Returns:
    df_no_nans (pd.DataFrame): La dataframe sin valores NaNs en esas columnas"""

    if tipo_eleccion == 'GUB':

        df_no_nans = df.dropna(subset = ['ID_DISTRITO','FECHA_HORA_ACOPIO', 'FECHA_HORA_CAPTURA', 'FECHA_HORA_VERIFICACION'])

        df_no_nans = df[df['CONTABILIZADA'] != 2]

    elif tipo_eleccion == 'DIP_LOC':

        df_no_nans = df.dropna(subset = ['ID_DISTRITO_LOCAL','FECHA_HORA_ACOPIO', 'FECHA_HORA_CAPTURA', 'FECHA_HORA_VERIFICACION'])

        df_no_nans = df[df['CONTABILIZADA'] != 2]

    else:

        df_no_nans = df.dropna(subset = ['ID_MUNICIPIO','FECHA_HORA_ACOPIO', 'FECHA_HORA_CAPTURA', 'FECHA_HORA_VERIFICACION'])

        df_no_nans = df[df['CONTABILIZADA'] != 2]

    return df_no_nans

def change_names(df):
    """
    Cambia el valor de los registros que en la columna OBSERVACIONES aparezcan como '-' por SIN OBSERVACIONES

    Args:
    df (pd.DataFrame): La dataframe que se utilizará

    Returns:
    df (pd.DataFrame): La misma dataframe con los valores cambiados"""

    names = df.OBSERVACIONES.unique()

    for x in names:

        if x == '-':

            df.OBSERVACIONES = df.OBSERVACIONES.replace('-', 'SIN OBSERVACIONES')

    return df

def check_negs(df, cols):
    """
    Verifica y maneja registros negativos en una columna específica de un DataFrame.

    Args:
        df (pd.DataFrame): DataFrame que contiene los datos.
        cols (str): Nombre de la columna a verificar.

    Returns:
        pd.DataFrame: DataFrame original o modificado dependiendo de si el usuario decide eliminar los registros negativos.

    Note:
        La función primero imprime la cantidad de registros negativos y muestra sus detalles.
        Luego, pregunta al usuario si desea eliminar esos registros. Si el usuario responde afirmativamente,
        los registros negativos se eliminan; de lo contrario, se conservan.
    """

    if cols in df.columns:

        cantidad_negativos = (df[cols] < 0).sum()

        print(f"La cantidad de registros con tiempos de procesamiento negativos es de: {cantidad_negativos} registros.")

        if cantidad_negativos > 0:

            print("Los registros negativos son los siguientes:")

            registros_negativos = np.where(df[cols] < 0)[0]

            print(df.iloc[registros_negativos])

            respuesta = input("¿Deseas eliminar los registros negativos? (Y/N): ")

            if respuesta.lower() in ['y', 'Y']:

                df = df[df[cols] >= 0]

                print("Registros negativos eliminados.")

            else:

                print("Los registros negativos no fueron eliminados. Requiere análisis más profundo.")

        else:

            print(f"La columna {cols} no existe en el dataframe.")

        return df

    return df


def pre_process(df, identifier):

    if identifier == 'GUB':

        df['ID_DISTRITO'] = df['ID_DISTRITO'].str.extract(r'(\d+)')

        df['ID_DISTRITO'] = df['ID_DISTRITO'].fillna('').astype(str).apply(lambda x: x.zfill(3))

    elif identifier == 'DIP_LOC':

        df['ID_DISTRITO_LOCAL'] = df['ID_DISTRITO_LOCAL'].str.extract(r'(\d+)')

        df['ID_DISTRITO_LOCAL'] = df['ID_DISTRITO_LOCAL'].fillna('').astype(str).apply(lambda x: x.zfill(3))

    else:

        df['ID_MUNICIPIO'] = df['ID_MUNICIPIO'].str.extract(r'(\d+)')

        df['ID_MUNICIPIO'] = df['ID_MUNICIPIO'].fillna('').astype(str).apply(lambda x: x.zfill(3))

    return df


def merge_dfs(df, df_mun, json_file):

    df_mun['CVE_MUN'] = df_mun['CVE_MUN'].apply(lambda x: str(x).zfill(3))

    merged = df.merge(df_mun, left_on = 'ID_MUNICIPIO', right_on = 'CVE_MUN', how = 'right')

    with open(json_file, encoding = 'utf-8') as f:

        geojson_municipios = json.load(f)

    claves_merged = sorted(merged['CVE_MUN'].unique())

    claves_geojson = sorted([feature['properties']['CVE_MUN'] for feature in geojson_municipios['features']])

    print()
    print()

    print("Verificación de la coincidencia de las claves en los archivos: \n")
    print("Claves en el merged: ",claves_merged)
    print("Claves en el GeoJSON: ", claves_geojson)

    print()
    print()

    if claves_merged == claves_geojson:

        print("Todos los elementos de las listas son iguales.")

    else:

        print("No todos los elementos de la lista son iguales.")

        diferencias_merged = [clave for clave in claves_merged if clave not in claves_geojson]

        diferencias_geojson = [clave for clave in claves_geojson if clave not in claves_merged]

        print("Elementos en merged['CVE_MUN'] que no están en geojson_municipios['features']: ", diferencias_merged)
        print("Elementos en geojson_municipios['features'] que no están en merged['CVE_MUN']: ", diferencias_geojson)

    print()
    print()

    print("Verificación de los tipos de datos: \n")
    print(merged['CVE_MUN'].dtype)
    print(type(geojson_municipios['features'][0]['properties']['CVE_MUN']))

    return merged, geojson_municipios

def make_map(df_merged, geojson_file):

    fig = px.choropleth_mapbox(df_merged,
                               geojson = geojson_file,
                               locations = "CVE_MUN",
                               featureidkey = "properties.CVE_MUN",
                               color = 'TIEMPO_PROCESAMIENTO_MINUTOS',
                               hover_name = 'NOM_MUN',
                               color_continuous_scale = 'Viridis',
                               mapbox_style = 'carto-positron',
                               zoom = 8,
                               center = {'lat': 19.0413, 'lon': -98.2062},
                               labels = {'TIEMPO_PROCESAMIENTO_MINUTOS': 'Tiempo de procesamiento promedio de actas'},
                               opacity = 0.7)

    fig.update_layout(margin = {"r":0, "t": 0, "l":0, "b": 0})
    fig.update_geos(fitbounds = "locations", visible = False)
    fig.show()


csv_file_path = find_csv(folder_path, tipo_eleccion)

df, info = load_csv(csv_file_path)

print("Instituto Electoral del Estado de Puebla")
print("Programa de Resultados Electorales Premilinares - 2 de junio de 2024")
print(f"Fecha de corte {info['Fecha_corte'][0]}")

print()
print()

print("Información general de la base: \n")

print(f"La cantidad de Actas Registradas es de {info['ACTAS_REGISTRADAS'][0]} actas.")
print(f"La cantidad de Actas Fuera de Catálogo es de {info['ACTAS_FUERA_CATALOGO'][0]} actas.")
print(f"La cantidad de Actas Capturadas es de {info['ACTAS_CAPTURADAS'][0]} actas, lo que representa un {info['PORCENTAJE_ACTAS_CAPTURADAS'][0]}% del total de Actas Esperadas.")
print(f"La cantidad de Actas Contabilizadas es de {info['ACTAS_CONTABILIZADAS'][0]}, lo que representa un {info['PORCENTAJE_ACTAS_CONTABILIZADAS'][0]}%. del total de Actas Esperadas.")
print(f"El Porcentaje de Participación Ciudadana es del {info['PORCENTAJE_PARTICIPACION_CIUDADANA'][0]}%.")

data_no_nan = check_nans(df)

data_no_nan['FECHA_HORA_ACOPIO'] = pd.to_datetime(data_no_nan['FECHA_HORA_ACOPIO'], format = '%d/%m/%Y %H:%M:%S',  errors='coerce')
data_no_nan['FECHA_HORA_CAPTURA'] = pd.to_datetime(data_no_nan['FECHA_HORA_CAPTURA'], format = '%d/%m/%Y %H:%M:%S', errors='coerce')
data_no_nan['FECHA_HORA_VERIFICACION'] = pd.to_datetime(data_no_nan['FECHA_HORA_VERIFICACION'], format = '%d/%m/%Y %H:%M:%S', errors='coerce')

# Tiempo de procesamiento con solo capturas

data_no_nan['TIEMPO_PROCESAMIENTO'] = data_no_nan['FECHA_HORA_CAPTURA'] - data_no_nan['FECHA_HORA_ACOPIO']

data_no_nan['TIEMPO_PROCESAMIENTO_MINUTOS'] = data_no_nan['TIEMPO_PROCESAMIENTO'].dt.total_seconds()/60

data_no_nan['TIEMPO_PROCESAMIENTO_MINUTOS'] = data_no_nan['TIEMPO_PROCESAMIENTO_MINUTOS'].round(2)

# Tiempo de procesamiento para actas con verificacion

data_no_nan['TIEMPO_PROCESAMIENTO_VERIFICACION'] = data_no_nan['FECHA_HORA_VERIFICACION'] - data_no_nan['FECHA_HORA_ACOPIO']

data_no_nan['TIEMPO_PROCESAMIENTO_VERIFICACION_MINUTOS'] = data_no_nan['TIEMPO_PROCESAMIENTO_VERIFICACION'].dt.total_seconds()/60

data_no_nan['TIEMPO_PROCESAMIENTO_VERIFICACION_MINUTOS'] = data_no_nan['TIEMPO_PROCESAMIENTO_VERIFICACION_MINUTOS'].round(2)

# Cambio de nombres

data_plot = change_names(data_no_nan)

data_plot = check_negs(data_plot, 'TIEMPO_PROCESAMIENTO_MINUTOS')

ready_data = pre_process(data_plot, tipo_eleccion)

df_mun = pd.read_csv(geo_mun_path)

df_merged, geojson = merge_dfs(ready_data, df_mun, geo_json_path)

exit()
make_map(df_merged, geojson)
