import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings

warnings.filterwarnings('ignore')

sim_or_prep = str(input("¿Qué desea analizar? ¿Simulacros o el PREP?: ")).lower()

tipo_eleccion = str(input("Indique el tipo de elección: 'GUB', 'DIP_LOC' o 'AYUN': ")).upper()

titulo_elecciones = {'GUB': 'Gubernatura',
                     'DIP_LOC': 'Diputaciones Locales',
                     'AYUN': 'Ayuntamientos'}

data_gub = pd.read_csv('C:/Users/Francisco Valerio/Desktop/INE/Simulacros/simulacros_prep/Data_final/PREP/data_GUB.csv', low_memory= False)

data_dip = pd.read_csv('C:/Users/Francisco Valerio/Desktop/INE/Simulacros/simulacros_prep/Data_final/PREP/data_DIP_LOC.csv', low_memory= False)

data_ayun = pd.read_csv('C:/Users/Francisco Valerio/Desktop/INE/Simulacros/simulacros_prep/Data_final/PREP/data_AYUN.csv', low_memory=False)

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
    
def series_de_tiempo(df, columna_tiempo, nombre_serie, color_serie):

    df[f'Fecha_{nombre_serie}'] = pd.to_datetime(df[columna_tiempo])

    df.set_index(f'Fecha_{nombre_serie}', inplace = True)

    df_resampled = df.resample('20t').count()

    df.reset_index(inplace = True)

    return go.Scatter(x = df_resampled.index, y = df_resampled['CODIGO_INTEGRIDAD'],
                      mode = 'lines', name=nombre_serie, line = dict(color=color_serie))

def subplots_series(df, sim_or_prep, tipo_eleccion):

    fig = make_subplots(rows=3, cols=1,
                        subplot_titles=("Evolución temporal del Acopio de AEC",
                                        "Evolución temporal de la Captura de AEC",
                                        "Evolución temporal de la Verificación de AEC"))
    
    colores = {'Acopio': 'blue', 'Captura': 'green', 'Verificacion': 'red'}

    fig.add_trace(series_de_tiempo(df, 'FECHA_HORA_ACOPIO', 'Acopio', colores['Acopio']),
                  row=1, col = 1)
    fig.add_trace(series_de_tiempo(df, 'FECHA_HORA_CAPTURA', 'Captura', colores['Captura']),
                  row = 2, col = 1)
    fig.add_trace(series_de_tiempo(df, 'FECHA_HORA_VERIFICACION', 'Verificación', colores['Verificacion']),
                  row = 3, col = 1)
    
    fig.update_layout(
        height = 1020,
        width = 1980,
        title={
            'text': f"{generar_titulo(sim_or_prep, tipo_eleccion)}",
            'font': {'size': 25}  # Aumentar el tamaño del título
        },
        xaxis_title='Fecha y Hora',
        yaxis_title='Número de Actas Procesadas',
        xaxis=dict(
            title_font_size=20  # Aumentar tamaño de título del eje X
        ),
        yaxis=dict(
            title_font_size=20  # Aumentar tamaño de título del eje Y
        ),
        legend_title_text='Observaciones',
        legend=dict(
            font_size=18,  # Aumentar el tamaño de la fuente de la leyenda
            title_font_size=20  # Aumentar el tamaño de la fuente del título de la leyenda
        ),
        template='presentation'
    )


    width = 1980
    height = 1020
    fig.write_image(f"C:/Users/Francisco Valerio/Desktop/INE/Simulacros/simulacros_prep/Final plots/series_tiempo_{tipo_eleccion}.png", format='png', width=width, height=height, scale=1)

    fig.show()

def promedio_por_categorias(df, sim_or_prep, tipo_eleccion):
    group_obs = df.groupby('OBSERVACIONES', as_index=False)['TIEMPO_PROCESAMIENTO_MINUTOS'].mean().round(2)
    group_metodo = df.groupby('DIGITALIZACION', as_index=False)['TIEMPO_PROCESAMIENTO_MINUTOS'].mean().round(2)

    fig = make_subplots(rows=1, cols=2)

    fig_1 = px.bar(group_obs, x='OBSERVACIONES', y='TIEMPO_PROCESAMIENTO_MINUTOS',
                   labels={'TIEMPO_PROCESAMIENTO_MINUTOS': 'Promedio de tiempo (minutos)', 'OBSERVACIONES': 'Observaciones'},
                   color='OBSERVACIONES', text='TIEMPO_PROCESAMIENTO_MINUTOS', text_auto=True,
                   color_discrete_sequence=px.colors.qualitative.T10)

    fig_1.update_traces(textfont_size=20)

    fig_1.update_layout(
        legend_title_text='Observaciones',
        legend=dict(font_size=18, title_font_size=20),
        xaxis_title_font_size=20,
        yaxis_title_font_size=20
    )

    fig.add_trace(go.Bar(x=group_obs['OBSERVACIONES'], y=group_obs['TIEMPO_PROCESAMIENTO_MINUTOS'],
                         text=group_obs['TIEMPO_PROCESAMIENTO_MINUTOS'], marker_color=px.colors.qualitative.T10,
                         name='Tiempo promedio de procesamiento por observación'), row=1, col=1)

    fig_2 = px.bar(group_metodo, x='DIGITALIZACION', y='TIEMPO_PROCESAMIENTO_MINUTOS',
                   labels={'TIEMPO_PROCESAMIENTO_MINUTOS': 'Promedio de tiempo (minutos)', 'DIGITALIZACION': 'Método'},
                   color='DIGITALIZACION', text='TIEMPO_PROCESAMIENTO_MINUTOS', text_auto=True,
                   color_discrete_sequence=px.colors.qualitative.Pastel2)

    fig_2.update_traces(textfont_size=20)

    fig_2.update_layout(
        legend_title_text='Digitalización',
        legend=dict(font_size=18, title_font_size=20),
        xaxis_title_font_size=20,
        yaxis_title_font_size=20
    )

    fig.add_trace(go.Bar(x=group_metodo['DIGITALIZACION'], y=group_metodo['TIEMPO_PROCESAMIENTO_MINUTOS'],
                         text=group_metodo['TIEMPO_PROCESAMIENTO_MINUTOS'], marker_color=px.colors.qualitative.Pastel2,
                         name='Tiempo promedio de procesamiento por método de digitalización'), row=1, col=2)

    fig.update_layout(
        height=600,
        width=1200,
        title={
            'text': generar_titulo(sim_or_prep, tipo_eleccion),
            'font': {'size': 25}
        },
        legend=dict(
            font_size=18,
            title_font_size=20
        ),
        template='presentation'
    )

    width = 1980
    height = 1020
    fig.write_image(f"C:/Users/Francisco Valerio/Desktop/INE/Simulacros/simulacros_prep/Final plots/prom_tiempo_categorias{tipo_eleccion}.png", format='png', width=width, height=height, scale=1)

    fig.show()



if tipo_eleccion == 'GUB':

    subplots_series(data_gub, sim_or_prep, tipo_eleccion)

    promedio_por_categorias(data_gub, sim_or_prep, tipo_eleccion)

elif tipo_eleccion == 'DIP_LOC':

    subplots_series(data_dip, sim_or_prep, tipo_eleccion)

    promedio_por_categorias(data_dip, sim_or_prep, tipo_eleccion)

elif tipo_eleccion == 'AYUN':

    subplots_series(data_ayun, sim_or_prep, tipo_eleccion)

    promedio_por_categorias(data_ayun, sim_or_prep, tipo_eleccion)