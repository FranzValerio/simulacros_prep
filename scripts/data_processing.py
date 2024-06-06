import numpy as np
import pandas as pd
import plotly.express as px
import os
import warnings
import sys
from datetime import datetime, timedelta
import plotly.graph_objects as go

sim_or_prep = str(input("¿Qué desea analizar? ¿Simulacros o el PREP?: ")).lower()

simulacro = None

if sim_or_prep == 'simulacros' or sim_or_prep == 'sim':

    simulacro = str(input("¿Qué simulacro desea analizar?: "))


tipo_eleccion = str(input("Indique el tipo de elección: 'GUB', 'DIP_LOC' o 'AYUN': ")).upper()

if simulacro == '1':

    folder_path = 'C:/Users/Francisco Valerio/Desktop/INE/Simulacros/simulacros_prep/BDD_Simulacro_1' #Desktop

    #folder_path = 'C:/Users/franz/Desktop/simulacros_prep/BDD_Simulacro_1' # Laptop

    inicio_intervalo = pd.to_datetime('2024-05-12 10:00')

    fin_intervalo = pd.to_datetime('2024-05-12 20:00')

    hora_inicio = datetime(2024, 5, 12, 10, 00)

    fecha_corte = datetime(2024, 5, 12, 21, 00)

elif simulacro == '1.2':

    folder_path = 'C:/Users/Francisco Valerio/Desktop/INE/Simulacros/simulacros_prep/BDD_Simulacro_1_rep'

    #folder_path = 'C:/Users/franz/Desktop/simulacros_prep/BDD_Simulacro_1_rep' # Laptop

    inicio_intervalo = pd.to_datetime('2024-05-17 20:00')

    fin_intervalo = pd.to_datetime('2024-05-17 20:40')

    hora_inicio = datetime(2024, 5, 17, 10, 30)

    fecha_corte = datetime(2024, 5, 17, 21, 00)

elif simulacro == '2':

    folder_path = 'C:/Users/Francisco Valerio/Desktop/INE/Simulacros/simulacros_prep/BDD_Simulacro_2'

    #folder_path = 'C:/Users/franz/Desktop/simulacros_prep/BDD_Simulacro_2' # Laptop

    inicio_intervalo = pd.to_datetime('2024-05-19 17:00')

    fin_intervalo = pd.to_datetime('2024-05-19 19:30')

    hora_inicio = datetime(2024, 5, 19, 10, 00)

    fecha_corte = datetime(2024, 5, 19, 21, 00)


elif simulacro == '3':

    folder_path = 'C:/Users/Francisco Valerio/Desktop/INE/Simulacros/simulacros_prep/BDD_Simulacro_3'  #Desktop

    #folder_path = 'C:/Users/franz/Desktop/simulacros_prep/BDD_Simulacro_3' # Laptop

    inicio_intervalo = pd.to_datetime('2024-05-26 14:00')

    fin_intervalo = pd.to_datetime('2024-05-26 14:40')

    hora_inicio = datetime(2024, 5, 26, 10, 20)

    fecha_corte = datetime(2024, 5, 26, 16,40)

else: 

    folder_path = 'C:/Users/franz/Desktop/simulacros_prep/BDD' # Laptop

    #folder_path = 'C:/Users/Francisco Valerio/Desktop/INE/Simulacros/simulacros_prep/BDD'  #Desktop

    inicio_intervalo = pd.to_datetime('2024-06-03 00:20')

    fin_intervalo = pd.to_datetime('2024-06-03 01:00')

    hora_inicio = datetime(2024, 6, 2, 20, 00)

    fecha_corte = datetime(2024, 6, 3, 20, 00)


totales = {'GUB': 8334,
               'DIP_LOC': 8423,
               'AYUN': 8352}


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

def generar_titulo(sim_or_prep, tipo):
    """
    Genera el título para un documento del Instituto Electoral del Estado de Puebla
    relacionado con el Proceso Electoral 2023-2024.

    Args:
        tipo (str): El tipo de elección para la cual se generará el título. Debe corresponder
                    a una clave en el diccionario 'titulo_elecciones'.

    Returns:
        str: El título completo que incluye el nombre del instituto, el proceso electoral,
             el simulacro y el nombre de la elección correspondiente al tipo proporcionado.
    """

    if sim_or_prep == 'simulacro' or sim_or_prep == 'sim':

        primera = "Instituto Electoral del Estado de Puebla - Proceso Electoral 2023-2024 "

        segunda = "(Tercer Simulacro PREP 26 de mayo del 2024) - "

        nombre_eleccion = titulo_elecciones.get(tipo, 'Tipo de elección desconocido')

        return primera + segunda + nombre_eleccion 
    
    else:

        primera = "Instituto Electoral del Estado de Puebla - "

        segunda = "Programa de Resultados Electorales Preliminares (2 de junio de 2024) - "

        nombre_eleccion = titulo_elecciones.get(tipo, "Tipo de elección desconocido")

        return primera + segunda + nombre_eleccion

def save_csv(df):
    """
    Guarda el archivo CSV que ha sido pre procesado y limpiado para análisis posteriores
    
    Args:
    df (pd.DataFrame): el dataframe que se va a guardar en formato CSV.
    
    Returns:
    saved_file (.CSV): archivo CSV"""

    saved_file = df.to_csv(f'C:/Users/Francisco Valerio/Desktop/INE/Simulacros/simulacros_prep/Data_final/BDD_Simulacro_3/data_sim_3_{tipo_eleccion}.csv', index = False) # Desktop

    # saved_file = df.to_csv(f'C:/Users/franz/Desktop/simulacros_prep/Data_clean/data_clean_{tipo_eleccion}_laptop.csv') # Laptop

def digit_stop(df):
    """
    Imprime las últimas fechas y horas registradas de acopio, captura y verificación
    en un DataFrame dado.

    Args:
        df (pandas.DataFrame): DataFrame que contiene las columnas 'FECHA_HORA_ACOPIO',
                               'FECHA_HORA_CAPTURA' y 'FECHA_HORA_VERIFICACION' con 
                               las respectivas fechas y horas.

    Returns:
        None

    Prints:
        La última fecha y hora de acopio, captura y verificación registradas en el DataFrame.
    """

    last_time_acopio = df['FECHA_HORA_ACOPIO'].max()

    last_time_captura = df['FECHA_HORA_CAPTURA'].max()

    last_time_verificacion = df['FECHA_HORA_VERIFICACION'].max()

    print(f"La última fecha y hora de acopio registrada fue a las {last_time_acopio}")
    print(f"La última fecha y hora de captura registrada fue a las {last_time_captura}")
    print(f"La última fecha y hora de verificación registrada fue a las {last_time_verificacion}")

def acopio_serie_tiempo(df):
    """
    Genera y muestra una serie temporal y un histograma del flujo de acopio de actas
    de escrutinio y cómputo, utilizando datos de un DataFrame dado.

    Args:
        df (pandas.DataFrame): DataFrame que contiene la columna 'FECHA_HORA_ACOPIO' con
                               las fechas y horas del acopio de actas, y 'CODIGO_INTEGRIDAD'
                               que representa el número de actas procesadas.

    Returns:
        None

    Generates:
        Una gráfica de líneas que muestra la evolución temporal del acopio de actas, y
        un histograma que muestra la distribución del flujo de acopio de actas.
    """
    
    df['Fecha_Acopio'] = df['FECHA_HORA_ACOPIO']

    df.set_index('Fecha_Acopio', inplace = True)

    df_resampled = df.resample('20T').count()

    line_color = 'blue'
    hist_color = '#EF553B'

    fig_line = go.Figure()

    fig_line.add_trace(go.Scatter(x=df_resampled.index, y = df_resampled.CODIGO_INTEGRIDAD,
                       mode = 'lines+markers', name='Actas Acopiadas',line = dict(color = line_color)))
    
    fig_line.update_layout(
        title={
        'text': f"{generar_titulo(sim_or_prep, tipo_eleccion)}<br>Evolución temporal del Acopio de Actas de Escrutinio y Cómputo</br>",
        'font': {'size': 20}  # Aumentar el tamaño del título
    },
    xaxis_title='Fecha y Hora',
    yaxis_title='Número de Actas Procesadas',
    xaxis=dict(
        title_font_size=18  # Aumentar tamaño de título del eje X
    ),
    yaxis=dict(
        title_font_size=18  # Aumentar tamaño de título del eje Y
    ),
    legend_title_text='Observaciones',
    legend=dict(
        font_size=18,  # Aumentar el tamaño de la fuente de la leyenda
        title_font_size=20  # Aumentar el tamaño de la fuente del título de la leyenda
    ),
    template='plotly_white'
    )

    fig_line.show()

    fig_hist = px.histogram(df.reset_index(), x = 'Fecha_Acopio', 
                            nbins = 20, 
                            title = f"{generar_titulo(sim_or_prep, tipo_eleccion)}<br>Histograma del Flujo de Acopio de Actas de Escrutinio y Cómputo</br>",
                            color_discrete_sequence=[hist_color])
    
    fig_hist.update_layout(
        xaxis_title='Fecha y Hora de Acopio',
        yaxis_title='Número de Actas',
        template='plotly_white'
    )
    #fig_hist.show()

def captura_serie_tiempo(df):
    """
      Genera y muestra una serie temporal y un histograma del flujo de captura de actas
    de escrutinio y cómputo, utilizando datos de un DataFrame dado.

    Args:
        df (pandas.DataFrame): DataFrame que contiene la columna 'FECHA_HORA_CAPTURA' con
                               las fechas y horas de la captura de actas, y 'CODIGO_INTEGRIDAD'
                               que representa el número de actas procesadas.

    Returns:
        None

    Generates:
        Una gráfica de líneas que muestra la evolución temporal de la captura de actas, y
        un histograma que muestra la distribución del flujo de captura de actas.

    """

    df['Fecha_Captura'] = df['FECHA_HORA_CAPTURA']

    df.set_index('Fecha_Captura', inplace = True)

    df_resampled = df.resample('20T').count()

    line_color = '#B82E2E'
    hist_color = '#990099'

    fig_line = go.Figure()

    fig_line.add_trace(go.Scatter(x=df_resampled.index, y = df_resampled.CODIGO_INTEGRIDAD,
                       mode = 'lines+markers', name='Actas Capturadas', line = dict(color = line_color)))
    fig_line.update_layout(
        title={
        'text': f"{generar_titulo(sim_or_prep,tipo_eleccion)}<br>Evolución temporal de la Captura de Actas de Escrutinio y Cómputo</br>",
        'font': {'size': 20}  # Aumentar el tamaño del título
    },
    xaxis_title='Fecha y Hora',
    yaxis_title='Número de Actas Capturadas',
    xaxis=dict(
        title_font_size=18  # Aumentar tamaño de título del eje X
    ),
    yaxis=dict(
        title_font_size=18  # Aumentar tamaño de título del eje Y
    ),
    legend_title_text='Observaciones',
    legend=dict(
        font_size=18,  # Aumentar el tamaño de la fuente de la leyenda
        title_font_size=20  # Aumentar el tamaño de la fuente del título de la leyenda
    ),
    template='plotly_white'
    )

    fig_line.show()

    fig_hist = px.histogram(df.reset_index(), x = 'Fecha_Captura', 
                            nbins = 20, 
                            title = f"{generar_titulo(sim_or_prep, tipo_eleccion)}<br>Histograma del Flujo de Captura de Actas de Escrutinio y Cómputo</br>",
                            color_discrete_sequence=[hist_color])
    
    fig_hist.update_layout(
        xaxis_title='Fecha y Hora de Captura',
        yaxis_title='Número de Actas',
        template='plotly_white'
    )
    #fig_hist.show()

def verificacion_serie_tiempo(df):
    """
    Genera y muestra una serie temporal y un histograma del flujo de verificación de actas
    de escrutinio y cómputo, utilizando datos de un DataFrame dado.

    Args:
        df (pandas.DataFrame): DataFrame que contiene la columna 'FECHA_HORA_VERIFICACION' con
                               las fechas y horas de la verificación de actas, y 'CODIGO_INTEGRIDAD'
                               que representa el número de actas procesadas.

    Returns:
        None

    Generates:
        Una gráfica de líneas que muestra la evolución temporal de la verificación de actas, y
        un histograma que muestra la distribución del flujo de verificación de actas.
    """

    df['Fecha_Verificacion'] = df['FECHA_HORA_VERIFICACION']

    df.set_index('Fecha_Verificacion', inplace = True)

    df_resampled = df.resample('20T').count()

    line_color = '#109618'
    hist_color = '#00CC96'

    fig_line = go.Figure()

    fig_line.add_trace(go.Scatter(x=df_resampled.index, y = df_resampled.CODIGO_INTEGRIDAD,
                       mode = 'lines+markers', name='Actas Verificadas', line = dict(color = line_color)))
    fig_line.update_layout(
       title={
        'text': f"{generar_titulo(sim_or_prep, tipo_eleccion)}<br>Evolución temporal de la Verificación de Actas de Escrutinio y Cómputo</br>",
        'font': {'size': 20}  # Aumentar el tamaño del título
    },
    xaxis_title='Fecha y Hora',
    yaxis_title='Número de Actas Verificadas',
    xaxis=dict(
        title_font_size=18  # Aumentar tamaño de título del eje X
    ),
    yaxis=dict(
        title_font_size=18  # Aumentar tamaño de título del eje Y
    ),
    legend_title_text='Observaciones',
    legend=dict(
        font_size=18,  # Aumentar el tamaño de la fuente de la leyenda
        title_font_size=20  # Aumentar el tamaño de la fuente del título de la leyenda
    ),
    template='plotly_white'
    )

    fig_line.show()

    fig_hist = px.histogram(df.reset_index(), x = 'Fecha_Verificacion', 
                            nbins = 20, 
                            title = f"{generar_titulo(sim_or_prep, tipo_eleccion)}<br>Histograma del Flujo de Verificacion de Actas de Escrutinio y Cómputo</br>",
                            color_discrete_sequence=[hist_color])
    
    fig_hist.update_layout(
        xaxis_title='Fecha y Hora de Verificacion',
        yaxis_title='Número de Actas',
        template='plotly_white'
    )
    #fig_hist.show()

def analisis_serie_acopio(df, start, stop):

    acopio_intervalo = df[(df['FECHA_HORA_ACOPIO'] >= start) & (df['FECHA_HORA_ACOPIO'] <= stop)]

    num_acopio_intervalo = acopio_intervalo.shape[0]

    print(f"El número de capturas en el intervalo de {start} a {stop} es de: {num_acopio_intervalo}")

    acopio_intervalo['Tiempo_Acopio_Captura'] = (acopio_intervalo['FECHA_HORA_CAPTURA'] - acopio_intervalo['FECHA_HORA_ACOPIO']).dt.total_seconds()

    acopio_intervalo['Tiempo_Captura_Verificacion'] = (acopio_intervalo['FECHA_HORA_VERIFICACION'] - acopio_intervalo['FECHA_HORA_CAPTURA']).dt.total_seconds()

    print()
    print()

    #print(capturas_intervalo[['Tiempo_Acopio_Captura', 'Tiempo_Captura_Verificacion']].describe())

    df['HORA_ACOPIO'] = df['FECHA_HORA_ACOPIO'].dt.floor('T')

    conteo_acopio = df.groupby('HORA_ACOPIO').size()

    line_color = '#2E91E5'

    fig = go.Figure()

    fig.add_trace(go.Scatter(x = conteo_acopio.index, y = conteo_acopio.values,
                             mode = 'lines+markers',
                             name = 'Acopiadas',
                             line=dict(color= line_color)))

    
    fig.update_layout(title={
        'text': f"{generar_titulo(sim_or_prep, tipo_eleccion)}<br>Acopio de Actas de Escrutinio y Cómputo</br>",
        'font': {'size': 20}  # Aumentar el tamaño del título
    },
    xaxis_title='Fecha y Hora',
    yaxis_title='Número de Actas Digitalizadas',
    xaxis=dict(
        title_font_size=18  # Aumentar tamaño de título del eje X
    ),
    yaxis=dict(
        title_font_size=18  # Aumentar tamaño de título del eje Y
    ),
    legend_title_text='Observaciones',
    legend=dict(
        font_size=18,  # Aumentar el tamaño de la fuente de la leyenda
        title_font_size=20  # Aumentar el tamaño de la fuente del título de la leyenda
    ),
    template='plotly_white')
    
    fig.add_vline(x = start, line = dict(color = 'green', dash = 'dash'), name ='Inicio del intervalo')
    fig.add_vline(x = stop, line = dict(color = 'red', dash = 'dash'), name = 'Fin del intervalo')

    fig.show()

def analisis_serie_capturas(df, start, stop):
    """
    Realiza un análisis de la serie temporal de capturas de actas de escrutinio y cómputo 
    dentro de un intervalo de tiempo especificado, y genera una gráfica de líneas que 
    muestra el número de capturas por hora en el DataFrame dado.

    Args:
        df (pandas.DataFrame): DataFrame que contiene las columnas 'FECHA_HORA_ACOPIO',
                               'FECHA_HORA_CAPTURA' y 'FECHA_HORA_VERIFICACION' con 
                               las respectivas fechas y horas, y 'CODIGO_INTEGRIDAD' 
                               que representa el número de actas procesadas.
        start (datetime): Fecha y hora de inicio del intervalo.
        stop (datetime): Fecha y hora de fin del intervalo.

    Returns:
        None

    Generates:
        Imprime el número de capturas en el intervalo especificado, calcula el tiempo 
        entre acopio y captura y entre captura y verificación, y muestra una gráfica de 
        líneas con el número de capturas por hora y líneas verticales que indican el 
        inicio y fin del intervalo.

    """

    capturas_intervalo = df[(df['FECHA_HORA_CAPTURA'] >= start) & (df['FECHA_HORA_CAPTURA'] <= stop)]

    num_capturas_intervalo = capturas_intervalo.shape[0]

    print(f"El número de capturas en el intervalo de {start} a {stop} es de: {num_capturas_intervalo}")

    capturas_intervalo['Tiempo_Acopio_Captura'] = (capturas_intervalo['FECHA_HORA_CAPTURA'] - capturas_intervalo['FECHA_HORA_ACOPIO']).dt.total_seconds()

    capturas_intervalo['Tiempo_Captura_Verificacion'] = (capturas_intervalo['FECHA_HORA_VERIFICACION'] - capturas_intervalo['FECHA_HORA_CAPTURA']).dt.total_seconds()

    print()
    print()

    #print(capturas_intervalo[['Tiempo_Acopio_Captura', 'Tiempo_Captura_Verificacion']].describe())

    df['HORA_CAPTURA'] = df['FECHA_HORA_CAPTURA'].dt.floor('T')

    conteo_capturas = df.groupby('HORA_CAPTURA').size()

    line_color = '#AB63FA'

    fig = go.Figure()

    fig.add_trace(go.Scatter(x = conteo_capturas.index, y = conteo_capturas.values,
                             mode = 'lines+markers',
                             name = 'Capturas',
                             line=dict(color= line_color)))

    
    fig.update_layout(title={
        'text': f"{generar_titulo(sim_or_prep, tipo_eleccion)}<br>Captura de Actas de Escrutinio y Cómputo</br>",
        'font': {'size': 20}  # Aumentar el tamaño del título
    },
    xaxis_title='Fecha y Hora',
    yaxis_title='Número de Actas Procesadas',
    xaxis=dict(
        title_font_size=18  # Aumentar tamaño de título del eje X
    ),
    yaxis=dict(
        title_font_size=18  # Aumentar tamaño de título del eje Y
    ),
    legend_title_text='Observaciones',
    legend=dict(
        font_size=18,  # Aumentar el tamaño de la fuente de la leyenda
        title_font_size=20  # Aumentar el tamaño de la fuente del título de la leyenda
    ),
    template='plotly_white')
    
    fig.add_vline(x = start, line = dict(color = 'green', dash = 'dash'), name ='Inicio del intervalo')
    fig.add_vline(x = stop, line = dict(color = 'red', dash = 'dash'), name = 'Fin del intervalo')

    fig.show()

def analisis_serie_verificaciones(df, start, stop):
    """
    Realiza un análisis de la serie temporal de verificaciones de actas de escrutinio y cómputo
    dentro de un intervalo de tiempo especificado, y genera una gráfica de líneas que 
    muestra el número de verificaciones por hora en el DataFrame dado.

    Args:
        df (pandas.DataFrame): DataFrame que contiene las columnas 'FECHA_HORA_ACOPIO',
                               'FECHA_HORA_CAPTURA' y 'FECHA_HORA_VERIFICACION' con 
                               las respectivas fechas y horas, y 'CODIGO_INTEGRIDAD' 
                               que representa el número de actas procesadas.
        start (datetime): Fecha y hora de inicio del intervalo.
        stop (datetime): Fecha y hora de fin del intervalo.

    Returns:
        None

    Generates:
        Imprime el número de verificaciones en el intervalo especificado, calcula el tiempo 
        entre acopio y captura y entre captura y verificación, y muestra una gráfica de 
        líneas con el número de verificaciones por hora y líneas verticales que indican el 
        inicio y fin del intervalo.
    """

    verificaciones_intervalo = df[(df['FECHA_HORA_VERIFICACION'] >= start) & (df['FECHA_HORA_VERIFICACION'] <= stop)]

    num_verificaciones_intervalo = verificaciones_intervalo.shape[0]

    print(f"El número de verificaciones en el intervalo de {start} a {stop} es de: {num_verificaciones_intervalo}")

    verificaciones_intervalo['Tiempo_Acopio_Captura'] = (verificaciones_intervalo['FECHA_HORA_CAPTURA'] - verificaciones_intervalo['FECHA_HORA_ACOPIO']).dt.total_seconds()

    verificaciones_intervalo['Tiempo_Captura_Verificacion'] = (verificaciones_intervalo['FECHA_HORA_VERIFICACION'] - verificaciones_intervalo['FECHA_HORA_CAPTURA']).dt.total_seconds()

    print()
    print()

    print(verificaciones_intervalo[['Tiempo_Acopio_Captura', 'Tiempo_Captura_Verificacion']].describe())

    df['HORA_VERIFICACION'] = df['FECHA_HORA_VERIFICACION'].dt.floor('T')

    conteo_verificaciones = df.groupby('HORA_VERIFICACION').size()

    line_color = 'rgb(228,26,28)'

    fig = go.Figure()

    fig.add_trace(go.Scatter(x = conteo_verificaciones.index, y = conteo_verificaciones.values,
                             mode = 'lines+markers',
                             name = 'Verificaciones',
                             line = dict(color = line_color)))

    fig.update_layout(title={
        'text': f"{generar_titulo(sim_or_prep, tipo_eleccion)}<br>Verificación de Actas de Escrutinio y Cómputo</br>",
        'font': {'size': 20}  # Aumentar el tamaño del título
    },
    xaxis_title='Fecha y Hora',
    yaxis_title='Número de Actas Verificadas',
    xaxis=dict(
        title_font_size=18  # Aumentar tamaño de título del eje X
    ),
    yaxis=dict(
        title_font_size=18  # Aumentar tamaño de título del eje Y
    ),
    legend_title_text='Observaciones',
    legend=dict(
        font_size=18,  # Aumentar el tamaño de la fuente de la leyenda
        title_font_size=20  # Aumentar el tamaño de la fuente del título de la leyenda
    ),
    template='plotly_white')

    fig.add_vline(x=start, line=dict(color='green', dash='dash'), name='Inicio del intervalo')
    fig.add_vline(x=stop, line=dict(color='red', dash='dash'), name='Fin del intervalo')

    fig.show()

def tiempos_finales(df, tipo_eleccion):
    """
    Calcula y muestra el momento en que se alcanzó el 100% de capturas de actas de escrutinio y cómputo
    para un tipo de elección dado, junto con la cantidad y el porcentaje actual de actas capturadas.

    Args:
        df (pandas.DataFrame): DataFrame que contiene las columnas 'FECHA_HORA_CAPTURA' con las fechas y horas
                               de la captura de actas, y 'CONTABILIZADA' que indica si el acta fue contabilizada.
        tipo_eleccion (str): Tipo de elección ('GUB', 'DIP_LOC', 'AYUN') para la cual se realizará el análisis.

    Returns:
        None

    Prints:
        El momento en el que se alcanzó el 100% de actas capturadas, la cantidad actual de actas capturadas,
        y el porcentaje actual de actas capturadas.
    """

    df = df[df['CONTABILIZADA'] != 2] 

    df['HORA_CAPTURA'] = df['FECHA_HORA_CAPTURA'].dt.floor('T')

    conteo_capturas = df.groupby('HORA_CAPTURA').size().cumsum()

    totales = {'GUB': 8338,
               'DIP_LOC': 8414,
               'AYUN': 8356}

    
    porcentaje_captura = (conteo_capturas/totales.get(tipo_eleccion)) * 100


    def momento_captura_completa(porcentaje_captura):

        completo = porcentaje_captura[porcentaje_captura == 100]

        if not completo.empty:

            return completo.index[0]
    
        else:

            return "No se ha alcanzado el 100% de la captura de las actas"
    
    momento_100 = momento_captura_completa(porcentaje_captura)

    porcentaje_real = porcentaje_captura.iloc[-1]

    actas_capturadas_actual = conteo_capturas.iloc[-1]

    print(f"El momento en el que se alancazó el 100% de actas capturadas fue el: {momento_100}")

    print(f"La cantidad actual de actas capturadas es de: {actas_capturadas_actual} actas")

    print(f"El porcentaje actual de actas capturadas es: {porcentaje_real:.2f}%")

def proyeccion_tiempos(df, info, start, stop):

    diff_tiempo = stop - start

    total_actas = totales.get(tipo_eleccion)

    tiempo_procesamiento_disponible = diff_tiempo.total_seconds() / 60

    actas_capturadas = int(info['ACTAS_CAPTURADAS'].values[0])

    tiempo_procesamiento_prom = df['TIEMPO_PROCESAMIENTO_MINUTOS'].mean().round(2)

    actas_restantes = total_actas - actas_capturadas
    tiempo_restante_procesamiento = actas_restantes * tiempo_procesamiento_prom

    tiempo_restante = tiempo_restante_procesamiento / 60  # Convertir a horas

    hora_estimada_finalizacion = stop + timedelta(hours=tiempo_restante)

    print(f"La fecha estimada para terminar de procesar el 100% de las actas de {titulo_elecciones.get(tipo_eleccion)} al ritmo llevado en el simulacro sería: {hora_estimada_finalizacion}")
#     """
#     Calcula y proyecta la fecha y hora estimada para terminar de procesar el 100% de las actas
#     de escrutinio y cómputo, basado en el tiempo de procesamiento promedio observado y el intervalo de tiempo dado.

#     Args:
#         df (pandas.DataFrame): DataFrame que contiene la columna 'TIEMPO_PROCESAMIENTO_MINUTOS' con 
#                                los tiempos de procesamiento de actas en minutos.
#         info (dict): Diccionario que contiene la información de las actas capturadas con la clave 'ACTAS_CAPTURADAS'.
#         start (datetime): Fecha y hora de inicio del intervalo.
#         stop (datetime): Fecha y hora de fin del intervalo.

#     Returns:
#         None

#     Prints:
#         La fecha y hora estimada para terminar de procesar el 100% de las actas al ritmo observado en el intervalo.

#     """

#     diff_tiempo = stop - start

#     total_actas = totales.get(tipo_eleccion)

#     tiempo_procesamiento_disponible = diff_tiempo.total_seconds() / 60

#     actas_capturadas = info['ACTAS_CAPTURADAS']

#     tiempo_procesamiento_prom = df['TIEMPO_PROCESAMIENTO_MINUTOS'].mean().round(2)

#     tiempo_proyectado_total = tiempo_procesamiento_prom * total_actas

#     tiempo_restante = (tiempo_proyectado_total - tiempo_procesamiento_disponible)/60

#     hora_estimada_finalizacion = start + timedelta(minutes = tiempo_restante)

#     print(f"La fecha estimada para terminar de procesar el 100% de las actas de {titulo_elecciones.get(tipo_eleccion)} al ritmo llevado en el simulacro sería: {hora_estimada_finalizacion}")

def equipos_necesarios(df, horas_disponibles = 4, porcentaje_actas = 1.0):
    """
    Calcula y muestra el número mínimo de equipos necesarios para procesar un porcentaje especificado
    de actas de escrutinio y cómputo en el tiempo disponible dado.

    Args:
        df (pandas.DataFrame): DataFrame que contiene la columna 'TIEMPO_PROCESAMIENTO_MINUTOS' con 
                               los tiempos de procesamiento de actas en minutos.
        horas_disponibles (int, optional): Número de horas disponibles para procesar las actas. 
                                           Por defecto es 4.
        porcentaje_actas (float, optional): Porcentaje de actas que se desea procesar. 
                                            Por defecto es 1.0 (100%).

    Returns:
        None

    Prints:
        El número mínimo de equipos necesarios para procesar el porcentaje especificado de actas 
        en el tiempo disponible dado.

    """
    
    tiempo_prom_por_acta = df['TIEMPO_PROCESAMIENTO_MINUTOS'].mean().round(2)

    actas_a_procesar = totales.get(tipo_eleccion) * porcentaje_actas

    tiempo_disponible_min =  horas_disponibles * 60

    tiempo_total_requerido = actas_a_procesar * tiempo_prom_por_acta

    equipos_necesarios = tiempo_total_requerido/tiempo_disponible_min

    return print(f"El número mínimo de equipos necesarios para procesar el {porcentaje_actas*100}% de las actas de {titulo_elecciones.get(tipo_eleccion)} en {horas_disponibles} horas es de {int(equipos_necesarios)} equipos.")

def group_plots(df):
    """
    Genera y muestra varias gráficas basadas en los datos de un DataFrame dado,
    incluyendo el tiempo promedio de procesamiento y la cantidad de actas por 
    diferentes categorías (observaciones, método de digitalización, origen, y contabilización).

    Args:
        df (pandas.DataFrame): DataFrame que contiene las siguientes columnas:
                               'TIEMPO_PROCESAMIENTO_MINUTOS', 'OBSERVACIONES', 'DIGITALIZACION', 
                               'ORIGEN', y 'CONTABILIZADA'.

    Returns:
        None

    Generates:
        Varias gráficas de barras y una gráfica de cajas que muestran el tiempo promedio de procesamiento
        y la cantidad de actas por diferentes categorías, incluyendo observaciones, métodos de digitalización, 
        origen, y contabilización.
    """

    group_obs = df.groupby('OBSERVACIONES', as_index=False)['TIEMPO_PROCESAMIENTO_MINUTOS'].mean().round(2)

    group_metodo = df.groupby('DIGITALIZACION', as_index = False)['TIEMPO_PROCESAMIENTO_MINUTOS'].mean().round(2)

    #group_count_obs = df['OBSERVACIONES'].value_counts().reset_index(name = 'count')

    #group_count_metodos = df['DIGITALIZACION'].value_counts().reset_index(name = 'count')

    #group_count_origen = df['ORIGEN'].value_counts().reset_index(name = 'count')

    #group_count_cont = df['CONTABILIZADA'].value_counts().reset_index(name = 'count')


    #group_count_doc = df['TIPO_DOCUMENTO'].value_counts().reset_index(name = 'count')

    group_count_obs = df['OBSERVACIONES'].value_counts().reset_index(name='count').rename(columns={'index': 'OBSERVACIONES'})
    group_count_metodos = df['DIGITALIZACION'].value_counts().reset_index(name='count').rename(columns={'index': 'DIGITALIZACION'})
    group_count_origen = df['ORIGEN'].value_counts().reset_index(name='count').rename(columns={'index': 'ORIGEN'})
    group_count_cont = df['CONTABILIZADA'].value_counts().reset_index(name='count').rename(columns={'index': 'CONTABILIZADA'})
    group_count_cont['CONTABILIZADA'] = group_count_cont['CONTABILIZADA'].replace({0: 'No contabilizada', 1: 'Contabilizada'})


    fig_1 = px.bar(group_obs, x = 'OBSERVACIONES', y = 'TIEMPO_PROCESAMIENTO_MINUTOS',
             title = generar_titulo(sim_or_prep, tipo_eleccion) + '<br>Tiempo promedio de procesamiento de actas por observación </br>',
             labels = {'TIEMPO_PROCESAMIENTO_MINUTOS': 'Promedio de tiempo (minutos)', 'OBSERVACIONES': 'Observaciones'},
             color = 'OBSERVACIONES',
             text='TIEMPO_PROCESAMIENTO_MINUTOS',
             text_auto=True,
             color_discrete_sequence=px.colors.qualitative.T10)

    fig_1.update_traces(textfont_size = 20)

    fig_1.update_layout(
    title={
        'text': generar_titulo(sim_or_prep,tipo_eleccion) + '<br>Tiempo promedio de procesamiento de actas por observación</br>',
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
             title = generar_titulo(sim_or_prep, tipo_eleccion) + '<br>Tiempo promedio de procesamiento de actas por método de digitalización </br>',
             labels = {'TIEMPO_PROCESAMIENTO_MINUTOS': 'Promedio de tiempo (minutos)', 'DIGITALIZACION': 'Método'},
             color = 'DIGITALIZACION',
             text = 'TIEMPO_PROCESAMIENTO_MINUTOS',
             text_auto=True,
             color_discrete_sequence=px.colors.qualitative.Pastel2)

    fig_2.update_traces(textfont_size = 20)

    fig_2.update_layout(
    title={
        'text': generar_titulo(sim_or_prep, tipo_eleccion) + '<br>Tiempo promedio de procesamiento de actas por método de digitalización</br>',
        'font': {'size': 20}  # Aumentar el tamaño del título
    },
    legend_title_text='Digitalización',
    legend=dict(
        font_size=18,  # Aumentar el tamaño de la fuente de la leyenda
        title_font_size=20  # Aumentar el tamaño de la fuente del título de la leyenda
    ),
    xaxis_title_font_size=18,  # Aumentar tamaño de título del eje X
    yaxis_title_font_size=18   # Aumentar tamaño de título del eje Y
)


    fig_2.show()

    fig_3 = px.box(data_plot, x = 'TIEMPO_PROCESAMIENTO_MINUTOS',
               title = generar_titulo(sim_or_prep, tipo_eleccion) + '<br>Distribución del tiempo de procesamiento de actas</br>', 
               labels = {'TIEMPO_PROCESAMIENTO_MINUTOS': 'Tiempo de procesamiento'},
               color_discrete_sequence=px.colors.qualitative.Prism)

    fig_3.update_layout(
    title = {
        'text': generar_titulo(sim_or_prep, tipo_eleccion) + '<br>Distribución del tiempo de procesamiento de actas</br>',
        'font': {'size': 20}
    },
    xaxis_title='Tiempo de procesamiento (minutos)',
    yaxis_title='Frecuencia',
    xaxis_title_font={'size': 16},  # Aumentar tamaño del título del eje X
    yaxis_title_font={'size': 16}   # Aumentar tamaño del título del eje Y
)

    fig_3.show()

    fig_4 = px.bar(group_count_obs, x = 'OBSERVACIONES', y = 'count',
                   title = generar_titulo(sim_or_prep, tipo_eleccion) + '<br>Cantidad de actas por tipo de observación </br>',
             labels = {'count': 'Total de Actas', 'OBSERVACIONES': 'Observaciones'},
             color = 'OBSERVACIONES',
             text='count',
             text_auto=True,
             color_discrete_sequence=px.colors.qualitative.Alphabet)
    
    fig_4.update_traces(textfont_size = 20)

    fig_4.update_layout(
    title={
        'text': generar_titulo(sim_or_prep, tipo_eleccion) + '<br>Cantidad de actas por tipo de observación</br>',
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

    fig_4.show()

    fig_5 = px.bar(group_count_metodos, x = 'DIGITALIZACION', y = 'count',
                    title = generar_titulo(sim_or_prep, tipo_eleccion) + '<br>Cantidad de actas por tipo método de digitalización </br>',
             labels = {'count': 'Total de Actas', 'DIGITALIZACION': 'Método'},
             color = 'DIGITALIZACION',
             text='count',
             text_auto=True,
             color_discrete_sequence=px.colors.qualitative.Bold)
    
    fig_5.update_traces(textfont_size = 20)

    fig_5.update_layout(
    title={
        'text': generar_titulo(sim_or_prep, tipo_eleccion) + '<br>Cantidad de actas por tipo de método de digitalización</br>',
        'font': {'size': 20}  # Aumentar el tamaño del título
    },
    legend_title_text='Digitalización',
    legend=dict(
        font_size=18,  # Aumentar el tamaño de la fuente de la leyenda
        title_font_size=20  # Aumentar el tamaño de la fuente del título de la leyenda
    ),
    xaxis_title_font_size=18,  # Aumentar tamaño de título del eje X
    yaxis_title_font_size=18   # Aumentar tamaño de título del eje Y
)

    fig_5.show()

    fig_6 = px.bar(group_count_origen, x = 'ORIGEN', y = 'count',
                    title = generar_titulo(sim_or_prep, tipo_eleccion) + '<br>Cantidad de actas por tipo de origen </br>',
             labels = {'count': 'Total de Actas', 'ORIGEN': 'Origen'},
             color = 'ORIGEN',
             text='count',
             text_auto=True,
             color_discrete_sequence=px.colors.qualitative.D3)
    
    
    fig_6.update_traces(textfont_size = 20)

    fig_6.update_layout(
    title={
        'text': generar_titulo(sim_or_prep, tipo_eleccion) + '<br>Cantidad de actas por tipo de origen</br>',
        'font': {'size': 20}  # Aumentar el tamaño del título
    },
    legend_title_text='Origen',
    legend=dict(
        font_size=18,  # Aumentar el tamaño de la fuente de la leyenda
        title_font_size=20  # Aumentar el tamaño de la fuente del título de la leyenda
    ),
    xaxis_title_font_size=18,  # Aumentar tamaño de título del eje X
    yaxis_title_font_size=18   # Aumentar tamaño de título del eje Y
)

    fig_6.show()

    fig_7 = px.bar(group_count_cont, x = 'CONTABILIZADA', y = 'count',
                    title = generar_titulo(sim_or_prep, tipo_eleccion) + '<br>Cantidad de actas contabilizadas </br>',
             labels = {'count': 'Total de Actas', 'CONTABILIZADA': 'Contabilizada'},
             color = 'CONTABILIZADA',
             text='count',
             text_auto=True,
             color_discrete_sequence=px.colors.qualitative.Plotly)
    
    
    fig_7.update_traces(textfont_size = 20)

    fig_7.update_layout(
    title={
        'text': generar_titulo(sim_or_prep, tipo_eleccion) + '<br>Cantidad de actas contabilizadas</br>',
        'font': {'size': 20}  # Aumentar el tamaño del título
    },
    legend_title_text='Contabilizada',
    legend=dict(
        font_size=18,  # Aumentar el tamaño de la fuente de la leyenda
        title_font_size=20  # Aumentar el tamaño de la fuente del título de la leyenda
    ),
    xaxis_title_font_size=18,  # Aumentar tamaño de título del eje X
    yaxis_title_font_size=18   # Aumentar tamaño de título del eje Y
)

    fig_7.show()


csv_file_path = find_csv(folder_path, tipo_eleccion)

df, info = load_csv(csv_file_path)

if sim_or_prep == 'simulacro' or sim_or_prep == 'sim':

    print(f"Simulacro {simulacro} realizado el {hora_inicio}")

else:
    print("Programa de Resultados Electorales Preliminares - 2 de junio de 2024")
    print(f"Fecha de corte: {info['Fecha_corte'][0]}")

print(f"Tipo de elección: {titulo_elecciones.get(tipo_eleccion)}")

print()
print()

if df is not None and info is not None:
    print("Base de datos: \n")
    print(df.head())

    print()
    print()

    print("Información general de la base: \n")
    print(info)

    print()
    print()

    print(f"La cantidad de Actas Registradas es de {info['ACTAS_REGISTRADAS'][0]} actas.")
    print(f"La cantidad de Actas Fuera de Catálogo es de {info['ACTAS_FUERA_CATALOGO'][0]} actas.")
    print(f"La cantidad de Actas Capturadas es de {info['ACTAS_CAPTURADAS'][0]} actas, lo que representa un {info['PORCENTAJE_ACTAS_CAPTURADAS'][0]}% del total de Actas Esperadas.")
    print(f"La cantidad de Actas Contabilizadas es de {info['ACTAS_CONTABILIZADAS'][0]}, lo que representa un {info['PORCENTAJE_ACTAS_CONTABILIZADAS'][0]}%. del total de Actas Esperadas.")
    print(f"El Porcentaje de Participación Ciudadana es del {info['PORCENTAJE_PARTICIPACION_CIUDADANA'][0]}%.")


data_no_nan = check_nans(df)


print()
print()

print(f"Número de datos nulos en FECHA_HORA_ACOPIO: {data_no_nan.FECHA_HORA_ACOPIO.isna().sum()}")
print(f"Número de datos nulos en FECHA_HORA_CAPTURA: {data_no_nan.FECHA_HORA_CAPTURA.isna().sum()}")
print(f"Número de datos nulos en FECHA_HORA_VERIFICACION: {data_no_nan.FECHA_HORA_VERIFICACION.isna().sum()}")

print()
print()

#print("Tipos de datos antes de la conversión: ")
#print(data_no_nan[['FECHA_HORA_ACOPIO', 'FECHA_HORA_CAPTURA', 'FECHA_HORA_VERIFICACION']].dtypes)

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

print(data_no_nan[['FECHA_HORA_ACOPIO', 'FECHA_HORA_CAPTURA', 'TIEMPO_PROCESAMIENTO_MINUTOS','TIEMPO_PROCESAMIENTO_VERIFICACION_MINUTOS' ]].iloc[40:50])

print()
print()


data_plot = change_names(data_no_nan)

data_plot = check_negs(data_plot, 'TIEMPO_PROCESAMIENTO_MINUTOS')

data_plot = data_plot[data_plot['CONTABILIZADA'] != 2] # REMOVE IF DOESN'T WORK

print()
print()

print("Estadísticos descriptivos del tiempo de procesamiento: \n")
print()

print(f"El tiempo de procesamiento promedio, en minutos, fue de: {data_plot['TIEMPO_PROCESAMIENTO_MINUTOS'].mean().round(2)}")
print(f"La mediana del tiempo de procesamiento, en minutos, fue de: {data_plot['TIEMPO_PROCESAMIENTO_MINUTOS'].median().round(2)}")
print(f"La desviación estándar del tiempo de procesamiento, en minutos, fue de: {data_plot['TIEMPO_PROCESAMIENTO_MINUTOS'].std().round(2)}")
print(f"El tiempo mínimo de procesamiento, en minutos, fue de: {data_plot['TIEMPO_PROCESAMIENTO_MINUTOS'].min().round(2)}")
print(f"El tiempo máximo de procesamiento, en minutos, fue de: {data_plot['TIEMPO_PROCESAMIENTO_MINUTOS'].max().round(2)}")

print()
print()

print("Estadísticos descriptivos del tiempo de verificación: \n")
print()
print(f"El tiempo de verificación promedio, en minutos, fue de: {data_plot['TIEMPO_PROCESAMIENTO_VERIFICACION_MINUTOS'].mean().round(2)}")
print(f"La mediana del tiempo de verificación, en minutos, fue de: {data_plot['TIEMPO_PROCESAMIENTO_VERIFICACION_MINUTOS'].median().round(2)}")
print(f"La desviación estándar del tiempo de verificación, en minutos, fue de: {data_plot['TIEMPO_PROCESAMIENTO_VERIFICACION_MINUTOS'].std().round(2)}")
print(f"El tiempo mínimo de verificación, en minutos, fue de: {data_plot['TIEMPO_PROCESAMIENTO_VERIFICACION_MINUTOS'].min().round(2)}")
print(f"El tiempo máximo de verificación, en minutos, fue de: {data_plot['TIEMPO_PROCESAMIENTO_VERIFICACION_MINUTOS'].max().round(2)}")

print()
print()
print("Fecha y hora de los últimos registros del procesamiento: \n")
print()

print(digit_stop(data_plot))

print()
print()

print("Estimación de tiempos de finalización del Simulacro: \n")
print()

print(proyeccion_tiempos(data_plot, info, hora_inicio, fecha_corte))

print()
print()

print("Número mínimo de equipos necesarios: \n")
print()
print(equipos_necesarios(data_plot, 4, 0.9))

print()
print()

print("Porcentaje de actas contabilizadas capturadas: \n")
print()
tiempos_finales(data_plot, tipo_eleccion)

#save_csv(data_plot)

acopio_serie_tiempo(data_plot)

captura_serie_tiempo(data_plot)

verificacion_serie_tiempo(data_plot)

analisis_serie_acopio(data_plot, start = inicio_intervalo, stop = fin_intervalo)

analisis_serie_capturas(data_plot, start = inicio_intervalo, stop = fin_intervalo)

analisis_serie_verificaciones(data_plot, start=inicio_intervalo, stop=fin_intervalo)

group_plots(data_plot)
