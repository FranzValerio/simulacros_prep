import numpy as np
import pandas as pd
import plotly.express as px
import os
import warnings
import sys

tipo_eleccion = 'AYUN' # 'AYUN' o 'DIP_LOC

#folder_path = 'C:/Users/franz/Desktop/Prueba de funcionalidad/prueba_funcionalidad/BDD_Simulacro_1' # Laptop

folder_path = 'C:/Users/Francisco Valerio/Desktop/INE/Simulacros/simulacros_prep/BDD_Simulacro_1'

warnings.filterwarnings('ignore')

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

        return pd.read_csv(file_path, skiprows = 5, low_memory=False)
    
    else:

        print("No se encontró ningún archivo CSV.")

    return None

def check_nans(df):
    """Revisa si existen valores NaNs en las columnas de FECHA_HORA_ACOPIO, FECHA_HORA_CAPTURA y
    FECHA_HORA_VERIFICACION. Se aplica previo a la conversión de datos tipo object a datetime para
    poder calcular el tiempo de procesamiento
    
    Args:
    df (pd.DataFrame): La dataframe que se va a utilizar
    
    Returns:
    df_no_nans (pd.DataFrame): La dataframe sin valores NaNs en esas columnas"""

    df_no_nans = df.dropna(subset = ['FECHA_HORA_ACOPIO', 'FECHA_HORA_CAPTURA', 'FECHA_HORA_VERIFICACION'])

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

        print("Los registros negativos son los siguientes:")

        registros_negativos = np.where(df[cols] < 0)[0]

        print(df.iloc[registros_negativos])

    if cantidad_negativos > 0:

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

titulo_elecciones = {'GUB': 'Gubernatura',
                     'DIP_LOC': 'Diputaciones Locales',
                     'AYUN': 'Ayuntamientos'}

def generar_titulo(tipo):

    primera = "Instituto Electoral del Estado de Puebla - Proceso Electoral 2024 "

    segunda = "(Primer simulacro realizado el 12 de mayo del 2024) - "

    nombre_eleccion = titulo_elecciones.get(tipo, 'Tipo de elección desconocido')

    return primera + segunda + nombre_eleccion 

def save_csv(df):
    """
    Guarda el archivo CSV que ha sido pre procesado y limpiado para análisis posteriores
    
    Args:
    df (pd.DataFrame): el dataframe que se va a guardar en formato CSV.
    
    Returns:
    saved_file (.CSV): archivo CSV"""

    saved_file = df.to_csv(f'C:/Users/Francisco Valerio/Desktop/INE/Simulacros/simulacros_prep/Data_clean/data_clean_{tipo_eleccion}.csv')

def save_output(func):
    """
    Decorador que captura la salida de una función y la guarda en un archivo de texto.

    Args:
        func (function): La función cuya salida será capturada y guardada.

    Returns:
        function: Función decorada que escribe su salida a un archivo.
    """

    def wrapper(*args, **kwargs):

        original_stdout = sys.stdout

        with open(f'output_{tipo_eleccion}.txt', 'w') as f:

            sys.stdout = f

            func(*args, **kwargs)

            sys.stdout = original_stdout

        print("Los datos de salida han sido almacenados.")

    return wrapper

print(f"Tipo de elección: {titulo_elecciones.get(tipo_eleccion)}")

csv_file_path = find_csv(folder_path, tipo_eleccion)

df = load_csv(csv_file_path)

if df is not None:

    print(df.head())

data_no_nan = check_nans(df)

print(f"Número de datos nulos en FECHA_HORA_ACOPIO: {data_no_nan.FECHA_HORA_ACOPIO.isna().sum()}")
print(f"Número de datos nulos en FECHA_HORA_CAPTURA: {data_no_nan.FECHA_HORA_CAPTURA.isna().sum()}")
print(f"Número de datos nulos en FECHA_HORA_VERIFICACION: {data_no_nan.FECHA_HORA_VERIFICACION.isna().sum()}")

print("Tipos de datos antes de la conversión: ")
print(data_no_nan[['FECHA_HORA_ACOPIO', 'FECHA_HORA_CAPTURA', 'FECHA_HORA_VERIFICACION']].dtypes)

data_no_nan['FECHA_HORA_ACOPIO'] = pd.to_datetime(data_no_nan['FECHA_HORA_ACOPIO'], format = '%d/%m/%Y %H:%M:%S',  errors='coerce')
data_no_nan['FECHA_HORA_CAPTURA'] = pd.to_datetime(data_no_nan['FECHA_HORA_CAPTURA'], format = '%d/%m/%Y %H:%M:%S', errors='coerce')
data_no_nan['FECHA_HORA_VERIFICACION'] = pd.to_datetime(data_no_nan['FECHA_HORA_VERIFICACION'], format = '%d/%m/%Y %H:%M:%S', errors='coerce')

print("Tipos de datos después de la conversión: ")
print(data_no_nan[['FECHA_HORA_ACOPIO', 'FECHA_HORA_CAPTURA', 'FECHA_HORA_VERIFICACION']].dtypes)

data_no_nan['TIEMPO_PROCESAMIENTO'] = data_no_nan['FECHA_HORA_CAPTURA'] - data_no_nan['FECHA_HORA_ACOPIO']

data_no_nan['TIEMPO_PROCESAMIENTO_MINUTOS'] = data_no_nan['TIEMPO_PROCESAMIENTO'].dt.total_seconds()/60

data_no_nan['TIEMPO_PROCESAMIENTO_MINUTOS'] = data_no_nan['TIEMPO_PROCESAMIENTO_MINUTOS'].round(2)

print(data_no_nan[['FECHA_HORA_ACOPIO', 'FECHA_HORA_CAPTURA', 'TIEMPO_PROCESAMIENTO', 'TIEMPO_PROCESAMIENTO_MINUTOS']].head())

data_plot = change_names(data_no_nan)

data_plot = check_negs(data_plot, 'TIEMPO_PROCESAMIENTO_MINUTOS')

print(f"El tiempo de procesamiento promedio, en minutos, fue de: {data_plot['TIEMPO_PROCESAMIENTO_MINUTOS'].mean().round(2)}")
print(f"La mediana del tiempo de procesamiento, en minutos, fue de: {data_plot['TIEMPO_PROCESAMIENTO_MINUTOS'].median().round(2)}")
print(f"La desviación estándar del tiempo de procesamiento, en minutos, fue de: {data_plot['TIEMPO_PROCESAMIENTO_MINUTOS'].std().round(2)}")
print(f"El tiempo mínimo de procesamiento, en minutos, fue de: {data_plot['TIEMPO_PROCESAMIENTO_MINUTOS'].min().round(2)}")
print(f"El tiempo máximo de procesamiento, en minutos, fue de: {data_plot['TIEMPO_PROCESAMIENTO_MINUTOS'].max().round(2)}")

group_obs = data_plot.groupby('OBSERVACIONES', as_index=False)['TIEMPO_PROCESAMIENTO_MINUTOS'].mean().round(2)

group_metodo = data_plot.groupby('DIGITALIZACION', as_index = False)['TIEMPO_PROCESAMIENTO_MINUTOS'].mean().round(2)

conteo_metodos = data_plot['DIGITALIZACION'].value_counts()

print(conteo_metodos)

fig_1 = px.bar(group_obs, x = 'OBSERVACIONES', y = 'TIEMPO_PROCESAMIENTO_MINUTOS',
             title = generar_titulo(tipo_eleccion) + '<br>Tiempo promedio de procesamiento de actas por observación </br>',
             labels = {'TIEMPO_PROCESAMIENTO_MINUTOS': 'Promedio de tiempo (minutos)', 'OBSERVACIONES': 'Observaciones'},
             color = 'OBSERVACIONES',
             text='TIEMPO_PROCESAMIENTO_MINUTOS',
             text_auto=True,
             color_discrete_sequence=px.colors.qualitative.Pastel1)

fig_1.update_traces(textfont_size = 20)

fig_1.show()


fig_2 = px.bar(group_metodo, x = 'DIGITALIZACION', y = 'TIEMPO_PROCESAMIENTO_MINUTOS',
             title = generar_titulo(tipo_eleccion) + '<br>Tiempo promedio de procesamiento de actas por método de digitalización </br>',
             labels = {'TIEMPO_PROCESAMIENTO_MINUTOS': 'Promedio de tiempo (minutos)', 'DIGITALIZACION': 'Método'},
             color = 'DIGITALIZACION',
             text = 'TIEMPO_PROCESAMIENTO_MINUTOS',
             text_auto=True,
             color_discrete_sequence=px.colors.qualitative.Pastel2)

fig_2.update_traces(textfont_size = 20)

fig_2.show()

fig_3 = px.box(data_plot, x = 'TIEMPO_PROCESAMIENTO_MINUTOS',
               title = generar_titulo(tipo_eleccion) + '<br>Distribución del tiempo de procesamiento de actas</br>', 
               labels = {'TIEMPO_PROCESAMIENTO_MINUTOS': 'Tiempo de procesamiento'},
               color_discrete_sequence=px.colors.qualitative.Prism)


fig_3.show()

print(data_plot['TIEMPO_PROCESAMIENTO_MINUTOS'].sum())

save_csv(data_plot)
