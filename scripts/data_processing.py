import numpy as np
import pandas as pd
import plotly.express as px
import os
import warnings
import sys
import plotly.graph_objects as go

tipo_eleccion = 'DIP_LOC' # 'GUB', 'AYUN' o 'DIP_LOC, cambiar según la base de datos a analizar

inicio_intervalo = pd.to_datetime('2024-05-17 10:30')

fin_intervalo = pd.to_datetime('2024-05-17 21:00')

folder_path = 'C:/Users/franz/Desktop/simulacros_prep/BDD_Simulacro_1_rep' # Laptop

#folder_path = 'C:/Users/Francisco Valerio/Desktop/INE/Simulacros/simulacros_prep/BDD_Simulacro_1_rep' # Desktop

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

titulo_elecciones = {'GUB': 'Gubernatura',
                     'DIP_LOC': 'Diputaciones Locales',
                     'AYUN': 'Ayuntamientos'}

def generar_titulo(tipo):

    primera = "Instituto Electoral del Estado de Puebla - Proceso Electoral 2023-2024 "

    segunda = "(Segundo simulacro PREP 19 de mayo del 2024) - "

    nombre_eleccion = titulo_elecciones.get(tipo, 'Tipo de elección desconocido')

    return primera + segunda + nombre_eleccion 

def save_csv(df):
    """
    Guarda el archivo CSV que ha sido pre procesado y limpiado para análisis posteriores
    
    Args:
    df (pd.DataFrame): el dataframe que se va a guardar en formato CSV.
    
    Returns:
    saved_file (.CSV): archivo CSV"""

    saved_file = df.to_csv(f'C:/Users/Francisco Valerio/Desktop/INE/Simulacros/simulacros_prep/Data_clean/data_clean_{tipo_eleccion}.csv') # Desktop

    # saved_file = df.to_csv(f'C:/Users/franz/Desktop/simulacros_prep/Data_clean/data_clean_{tipo_eleccion}_laptop.csv') # Laptop

def digit_stop(df):

    last_time = df['FECHA_HORA_ACOPIO'].max()

    print(f"La última fecha y hora de acopio registrada fue a las {last_time}")

def acopio_serie_tiempo(df):

    df['Fecha_Acopio'] = df['FECHA_HORA_ACOPIO']

    df.set_index('Fecha_Acopio', inplace = True)

    df_resampled = df.resample('20T').count()

    line_color = 'blue'
    hist_color = '#EF553B'

    fig_line = go.Figure()

    fig_line.add_trace(go.Scatter(x=df_resampled.index, y = df_resampled.CODIGO_INTEGRIDAD,
                       mode = 'lines+markers', name='Actas Acopiadas',line = dict(color = line_color)))
    fig_line.update_layout(
        title = f"{generar_titulo(tipo_eleccion)}<br>Evolución temporal del Acopio de Actas de Escrutinio y Cómputo</br>",
        xaxis_title = 'Fecha y Hora',
        yaxis_title = 'Número de Actas Procesadas',
        template ='plotly_white'
    )

    fig_line.show()

    fig_hist = px.histogram(df.reset_index(), x = 'Fecha_Acopio', 
                            nbins = 20, 
                            title = f"{generar_titulo(tipo_eleccion)}<br>Histograma del Flujo de Acopio de Actas de Escrutinio y Cómputo</br>",
                            color_discrete_sequence=[hist_color])
    
    fig_hist.update_layout(
        xaxis_title='Fecha y Hora de Acopio',
        yaxis_title='Número de Actas',
        template='plotly_white'
    )
    fig_hist.show()

def captura_serie_tiempo(df):

    df['Fecha_Captura'] = df['FECHA_HORA_CAPTURA']

    df.set_index('Fecha_Captura', inplace = True)

    df_resampled = df.resample('20T').count()

    line_color = '#B82E2E'
    hist_color = '#990099'

    fig_line = go.Figure()

    fig_line.add_trace(go.Scatter(x=df_resampled.index, y = df_resampled.CODIGO_INTEGRIDAD,
                       mode = 'lines+markers', name='Actas Capturadas', line = dict(color = line_color)))
    fig_line.update_layout(
        title = f"{generar_titulo(tipo_eleccion)}<br>Evolución temporal de la Captura de Actas de Escrutinio y Cómputo</br>",
        xaxis_title = 'Fecha y Hora',
        yaxis_title = 'Número de Actas Capturadas',
        template ='plotly_white'
    )

    fig_line.show()

    fig_hist = px.histogram(df.reset_index(), x = 'Fecha_Captura', 
                            nbins = 20, 
                            title = f"{generar_titulo(tipo_eleccion)}<br>Histograma del Flujo de Captura de Actas de Escrutinio y Cómputo</br>",
                            color_discrete_sequence=[hist_color])
    
    fig_hist.update_layout(
        xaxis_title='Fecha y Hora de Captura',
        yaxis_title='Número de Actas',
        template='plotly_white'
    )
    fig_hist.show()

def verificacion_serie_tiempo(df):

    df['Fecha_Verificacion'] = df['FECHA_HORA_VERIFICACION']

    df.set_index('Fecha_Verificacion', inplace = True)

    df_resampled = df.resample('20T').count()

    line_color = '#FF7F0E'
    hist_color = '#00CC96'

    fig_line = go.Figure()

    fig_line.add_trace(go.Scatter(x=df_resampled.index, y = df_resampled.CODIGO_INTEGRIDAD,
                       mode = 'lines+markers', name='Actas Verificadas', line = dict(color = line_color)))
    fig_line.update_layout(
        title = f"{generar_titulo(tipo_eleccion)}<br>Evolución temporal de la Verificación de Actas de Escrutinio y Cómputo</br>",
        xaxis_title = 'Fecha y Hora',
        yaxis_title = 'Número de Actas Verificadas',
        template ='plotly_white'
    )

    fig_line.show()

    fig_hist = px.histogram(df.reset_index(), x = 'Fecha_Verificacion', 
                            nbins = 20, 
                            title = f"{generar_titulo(tipo_eleccion)}<br>Histograma del Flujo de Verificacion de Actas de Escrutinio y Cómputo</br>",
                            color_discrete_sequence=[hist_color])
    
    fig_hist.update_layout(
        xaxis_title='Fecha y Hora de Verificacion',
        yaxis_title='Número de Actas',
        template='plotly_white'
    )
    fig_hist.show()

def analisis_serie_capturas(df, start, stop):

    capturas_intervalo = df[(df['FECHA_HORA_CAPTURA'] >= start) & (df['FECHA_HORA_CAPTURA'] <= stop)]

    num_capturas_intervalo = capturas_intervalo.shape[0]

    print(f"El número de capturas en el intervalo de {start} a {stop} es de: {num_capturas_intervalo}")

    capturas_intervalo['Tiempo_Acopio_Captura'] = (capturas_intervalo['FECHA_HORA_CAPTURA'] - capturas_intervalo['FECHA_HORA_ACOPIO']).dt.total_seconds()

    capturas_intervalo['Tiempo_Captura_Verificacion'] = (capturas_intervalo['FECHA_HORA_VERIFICACION'] - capturas_intervalo['FECHA_HORA_CAPTURA']).dt.total_seconds()

    print()
    print()

    print(capturas_intervalo[['Tiempo_Acopio_Captura', 'Tiempo_Captura_Verificacion']].describe())

    df['HORA_CAPTURA'] = df['FECHA_HORA_CAPTURA'].dt.floor('T')

    conteo_capturas = df.groupby('HORA_CAPTURA').size()

    fig = px.line(x = conteo_capturas.index, y = conteo_capturas.values,
                  labels = {'x': 'Hora', 'y': 'Número de capturas'},
                            title = f"{generar_titulo(tipo_eleccion)}<br>Captura de Actas a lo largo del día</br>")
    
    fig.add_vline(x = start, line = dict(color = 'green', dash = 'dash'), name ='Inicio del intervalo')
    fig.add_vline(x = stop, line = dict(color = 'red', dash = 'dash'), name = 'Fin del intervalo')

    fig.show()

def tiempos_finales(df, tipo_eleccion):

    df['HORA_CAPTURA'] = df['FECHA_HORA_CAPTURA'].dt.floor('T')

    conteo_capturas = df.groupby('HORA_CAPTURA').size().cumsum()

    totales = {'GUB': 8338,
               'DIP_LOC': 8414,
               'AYUN': 8356}
    
    porcentaje_captura = conteo_capturas/totales.get(tipo_eleccion) * 100

    def momento_captura_completa(porcentaje_captura):

        completo = porcentaje_captura[porcentaje_captura == 100]

        if not completo.empty:

            return completo.index[0]
    
        else:

            return "No se ha alcanzado el 100% de la captura de las actas"
    
    momento_100 = momento_captura_completa(porcentaje_captura)

    porcentaje_real = porcentaje_captura.iloc[-1]

    print(f"El momento en el que se alancazó el 100% de actas capturadas fue el: {momento_100}")

    print(f"El porcentaje actual de actas capturadas es: {porcentaje_real:.2f}%")



print(f"Tipo de elección: {titulo_elecciones.get(tipo_eleccion)}")

csv_file_path = find_csv(folder_path, tipo_eleccion)

df = load_csv(csv_file_path)

print()
print()

if df is not None:

    print(df.head())

data_no_nan = check_nans(df)

print()
print()

print(f"Número de datos nulos en FECHA_HORA_ACOPIO: {data_no_nan.FECHA_HORA_ACOPIO.isna().sum()}")
print(f"Número de datos nulos en FECHA_HORA_CAPTURA: {data_no_nan.FECHA_HORA_CAPTURA.isna().sum()}")
print(f"Número de datos nulos en FECHA_HORA_VERIFICACION: {data_no_nan.FECHA_HORA_VERIFICACION.isna().sum()}")

print()
print()

print("Tipos de datos antes de la conversión: ")
print(data_no_nan[['FECHA_HORA_ACOPIO', 'FECHA_HORA_CAPTURA', 'FECHA_HORA_VERIFICACION']].dtypes)

data_no_nan['FECHA_HORA_ACOPIO'] = pd.to_datetime(data_no_nan['FECHA_HORA_ACOPIO'], format = '%d/%m/%Y %H:%M:%S',  errors='coerce')
data_no_nan['FECHA_HORA_CAPTURA'] = pd.to_datetime(data_no_nan['FECHA_HORA_CAPTURA'], format = '%d/%m/%Y %H:%M:%S', errors='coerce')
data_no_nan['FECHA_HORA_VERIFICACION'] = pd.to_datetime(data_no_nan['FECHA_HORA_VERIFICACION'], format = '%d/%m/%Y %H:%M:%S', errors='coerce')

print()
print()

print("Tipos de datos después de la conversión: ")
print(data_no_nan[['FECHA_HORA_ACOPIO', 'FECHA_HORA_CAPTURA', 'FECHA_HORA_VERIFICACION']].dtypes)

# Tiempo de procesamiento con solo capturas

data_no_nan['TIEMPO_PROCESAMIENTO'] = data_no_nan['FECHA_HORA_CAPTURA'] - data_no_nan['FECHA_HORA_ACOPIO']

data_no_nan['TIEMPO_PROCESAMIENTO_MINUTOS'] = data_no_nan['TIEMPO_PROCESAMIENTO'].dt.total_seconds()/60

data_no_nan['TIEMPO_PROCESAMIENTO_MINUTOS'] = data_no_nan['TIEMPO_PROCESAMIENTO_MINUTOS'].round(2)

# Tiempo de procesamiento para actas con verificacion

data_no_nan['TIEMPO_PROCESAMIENTO_VERIFICACION'] = data_no_nan['FECHA_HORA_VERIFICACION'] - data_no_nan['FECHA_HORA_ACOPIO']

data_no_nan['TIEMPO_PROCESAMIENTO_VERIFICACION_MINUTOS'] = data_no_nan['TIEMPO_PROCESAMIENTO_VERIFICACION'].dt.total_seconds()/60

data_no_nan['TIEMPO_PROCESAMIENTO_VERIFICACION_MINUTOS'] = data_no_nan['TIEMPO_PROCESAMIENTO_VERIFICACION_MINUTOS'].round(2)

print()
print()

print(data_no_nan[['FECHA_HORA_ACOPIO', 'FECHA_HORA_CAPTURA', 'TIEMPO_PROCESAMIENTO_MINUTOS','TIEMPO_PROCESAMIENTO_VERIFICACION_MINUTOS' ]].head())

print()
print()

data_plot = change_names(data_no_nan)

data_plot = check_negs(data_plot, 'TIEMPO_PROCESAMIENTO_MINUTOS')

print()
print()

print(f"El tiempo de procesamiento promedio, en minutos, fue de: {data_plot['TIEMPO_PROCESAMIENTO_MINUTOS'].mean().round(2)}")
print(f"La mediana del tiempo de procesamiento, en minutos, fue de: {data_plot['TIEMPO_PROCESAMIENTO_MINUTOS'].median().round(2)}")
print(f"La desviación estándar del tiempo de procesamiento, en minutos, fue de: {data_plot['TIEMPO_PROCESAMIENTO_MINUTOS'].std().round(2)}")
print(f"El tiempo mínimo de procesamiento, en minutos, fue de: {data_plot['TIEMPO_PROCESAMIENTO_MINUTOS'].min().round(2)}")
print(f"El tiempo máximo de procesamiento, en minutos, fue de: {data_plot['TIEMPO_PROCESAMIENTO_MINUTOS'].max().round(2)}")

print()
print()


print(f"El tiempo de verificación promedio, en minutos, fue de: {data_plot['TIEMPO_PROCESAMIENTO_VERIFICACION_MINUTOS'].mean().round(2)}")
print(f"La mediana del tiempo de verificación, en minutos, fue de: {data_plot['TIEMPO_PROCESAMIENTO_VERIFICACION_MINUTOS'].median().round(2)}")
print(f"La desviación estándar del tiempo de verificación, en minutos, fue de: {data_plot['TIEMPO_PROCESAMIENTO_VERIFICACION_MINUTOS'].std().round(2)}")
print(f"El tiempo mínimo de verificación, en minutos, fue de: {data_plot['TIEMPO_PROCESAMIENTO_VERIFICACION_MINUTOS'].min().round(2)}")
print(f"El tiempo máximo de verificación, en minutos, fue de: {data_plot['TIEMPO_PROCESAMIENTO_VERIFICACION_MINUTOS'].max().round(2)}")

print()
print()

print(digit_stop(data_plot))

print()
print()

acopio_serie_tiempo(data_plot)

captura_serie_tiempo(data_plot)

verificacion_serie_tiempo(data_plot)


group_obs = data_plot.groupby('OBSERVACIONES', as_index=False)['TIEMPO_PROCESAMIENTO_MINUTOS'].mean().round(2)

group_metodo = data_plot.groupby('DIGITALIZACION', as_index = False)['TIEMPO_PROCESAMIENTO_MINUTOS'].mean().round(2)

conteo_metodos = data_plot['DIGITALIZACION'].value_counts()

print(f"La cantidad de actas procesadas por método de digitalización es de: \n")

print(conteo_metodos)

fig_1 = px.bar(group_obs, x = 'OBSERVACIONES', y = 'TIEMPO_PROCESAMIENTO_MINUTOS',
             title = generar_titulo(tipo_eleccion) + '<br>Tiempo promedio de procesamiento de actas por observación </br>',
             labels = {'TIEMPO_PROCESAMIENTO_MINUTOS': 'Promedio de tiempo (minutos)', 'OBSERVACIONES': 'Observaciones'},
             color = 'OBSERVACIONES',
             text='TIEMPO_PROCESAMIENTO_MINUTOS',
             text_auto=True,
             color_discrete_sequence=px.colors.qualitative.Pastel1)

fig_1.update_traces(textfont_size = 20)

fig_1.update_layout(
    title={
        'text': generar_titulo(tipo_eleccion) + '<br>Tiempo promedio de procesamiento de actas por observación</br>',
        'font': {'size': 20}  # Aumentar el tamaño del título
    },
    legend_title_text='Observaciones',
    legend=dict(
        font_size=18,  # Aumentar el tamaño de la fuente de la leyenda
        title_font_size=20  # Aumentar el tamaño de la fuente del título de la leyenda
    ),
    xaxis_title_font_size=18,  # Aumentar tamaño de título del eje X
    yaxis_title_font_size=18   # Aumentar tamaño de título del eje Y
)

fig_1.show()

fig_2 = px.bar(group_metodo, x = 'DIGITALIZACION', y = 'TIEMPO_PROCESAMIENTO_MINUTOS',
             title = generar_titulo(tipo_eleccion) + '<br>Tiempo promedio de procesamiento de actas por método de digitalización </br>',
             labels = {'TIEMPO_PROCESAMIENTO_MINUTOS': 'Promedio de tiempo (minutos)', 'DIGITALIZACION': 'Método'},
             color = 'DIGITALIZACION',
             text = 'TIEMPO_PROCESAMIENTO_MINUTOS',
             text_auto=True,
             color_discrete_sequence=px.colors.qualitative.Pastel2)

fig_2.update_traces(textfont_size = 20)

fig_2.update_layout(
    title={
        'text': generar_titulo(tipo_eleccion) + '<br>Tiempo promedio de procesamiento de actas por observación</br>',
        'font': {'size': 20}  # Aumentar el tamaño del título
    },
    legend_title_text='Observaciones',
    legend=dict(
        font_size=18,  # Aumentar el tamaño de la fuente de la leyenda
        title_font_size=20  # Aumentar el tamaño de la fuente del título de la leyenda
    ),
    xaxis_title_font_size=18,  # Aumentar tamaño de título del eje X
    yaxis_title_font_size=18   # Aumentar tamaño de título del eje Y
)


fig_2.show()

fig_3 = px.box(data_plot, x = 'TIEMPO_PROCESAMIENTO_MINUTOS',
               title = generar_titulo(tipo_eleccion) + '<br>Distribución del tiempo de procesamiento de actas</br>', 
               labels = {'TIEMPO_PROCESAMIENTO_MINUTOS': 'Tiempo de procesamiento'},
               color_discrete_sequence=px.colors.qualitative.Prism)

fig_3.update_layout(
    title = {
        'text': generar_titulo(tipo_eleccion) + '<br>Distribución del tiempo de procesamiento de actas</br>',
        'font': {'size': 20}
    },
    xaxis_title='Tiempo de procesamiento (minutos)',
    yaxis_title='Frecuencia',
    xaxis_title_font={'size': 16},  # Aumentar tamaño del título del eje X
    yaxis_title_font={'size': 16}   # Aumentar tamaño del título del eje Y
)

fig_3.show()

print()
print()

analisis_serie_capturas(data_plot, start = inicio_intervalo, stop = fin_intervalo)

print()
print()
tiempos_finales(data_plot, tipo_eleccion)

#save_csv(data_plot)