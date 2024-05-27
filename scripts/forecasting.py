import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.api import SARIMAX


def analisis_serie_capturas(df, start, stop):

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
        'text': f"{generar_titulo(tipo_eleccion)}<br>Captura de Actas de Escrutinio y Cómputo</br>",
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