import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.api import SARIMAX
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings('ignore')

data = pd.read_csv('C:/Users/Francisco Valerio/Desktop/INE/Simulacros/simulacros_prep/data_series/data_sim_3_GUB.csv')

data['FECHA_HORA_ACOPIO'] = pd.to_datetime(data['FECHA_HORA_ACOPIO'])
data['FECHA_HORA_CAPTURA'] = pd.to_datetime(data['FECHA_HORA_CAPTURA'])
data['FECHA_HORA_VERIFICACION'] = pd.to_datetime(data['FECHA_HORA_VERIFICACION'])

inicio_intervalo = pd.to_datetime('2024-05-26 10:20')

fin_intervalo = pd.to_datetime('2024-05-26 18:00')

def analisis_serie_capturas(df, start, stop):

    capturas_intervalo = df[(df['FECHA_HORA_CAPTURA'] >= start) & (df['FECHA_HORA_CAPTURA'] <= stop)]

    num_capturas_intervalo = capturas_intervalo.shape[0]

    print(f"El número de capturas en el intervalo de {start} a {stop} es de: {num_capturas_intervalo}")

    capturas_intervalo['Tiempo_Acopio_Captura'] = (capturas_intervalo['FECHA_HORA_CAPTURA'] - capturas_intervalo['FECHA_HORA_ACOPIO']).dt.total_seconds()

    capturas_intervalo['Tiempo_Captura_Verificacion'] = (capturas_intervalo['FECHA_HORA_VERIFICACION'] - capturas_intervalo['FECHA_HORA_CAPTURA']).dt.total_seconds()

    df['HORA_CAPTURA'] = df['FECHA_HORA_CAPTURA'].dt.floor('T')

    conteo_capturas = df.groupby('HORA_CAPTURA').size()

     # Crear la gráfica
    line_color = '#AB63FA'
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=conteo_capturas.index, y=conteo_capturas.values,
                             mode='lines+markers',
                             name='Capturas',
                             line=dict(color=line_color)))

    fig.update_layout(
        title={
            'text': "Instituto Electoral del Estado de Puebla - Proceso Electoral 2023-2024 (Segundo Simulacro PREP 19 de mayo del 2024) - Gubernatura<br>Captura de Actas de Escrutinio y Cómputo</br>",
            'font': {'size': 20}
        },
        xaxis_title='Fecha y Hora',
        yaxis_title='Número de Actas Procesadas',
        xaxis=dict(title_font_size=18),
        yaxis=dict(title_font_size=18),
        legend_title_text='Observaciones',
        legend=dict(font_size=18, title_font_size=20),
        template='plotly_white'
    )

    fig.add_vline(x=start, line=dict(color='green', dash='dash'), name='Inicio del intervalo')
    fig.add_vline(x=stop, line=dict(color='red', dash='dash'), name='Fin del intervalo')

    fig.show()

    return conteo_capturas



def check_stationarity(series, max_diff = 3):
    """
    Prueba la estacionariedad de una serie de tiempo usando la prueba ADF y realiza diferenciaciones 
    hasta que la serie se vuelva estacionaria. Guarda la serie estacionaria en un nuevo DataFrame.

    Args:
        series (pd.Series): Serie de tiempo original.
        max_diff (int): Número máximo de diferenciaciones a aplicar para lograr la estacionariedad. 
                        Por defecto es 3.

    Returns:
        pd.DataFrame: DataFrame que contiene la serie estacionaria.
        int: Número de diferenciaciones aplicadas.
    """

    print("Test de estacionalidad de series de tiempo con la prueba de Dickey-Fuller Aumentada (ADF)")
    print()
    print()

    p_value_treshold = 0.05
    diff_count = 0
    stationary_series = series.copy()

    adf_result = adfuller(stationary_series.dropna())

    print(f"Valor inicial del estadístico ADF: {adf_result[0]}")
    print(f"Valor inicial del p-value: {adf_result[1]}")
    print()

    while adf_result[1] > p_value_treshold and diff_count < max_diff:

        print("La serie no es estacionaria, se aplican transformaciones para hacerla estacionaria")
        print()

        stationary_series = stationary_series.diff().dropna()

        diff_count += 1

        adf_result = adfuller(stationary_series)

        print(f"Nivel de diferenciación: {diff_count}")
        print(f"Valor del estadístico ADF: {adf_result[0]}")
        print(f"Valor del p-value: {adf_result[1]}")

        for key, value in adf_result[4].items():

            print(f" Valor crítico {key}: {value}")

    if adf_result[1] > p_value_treshold:
        print(F"La serie no es estacionaria después de {max_diff} derivadas.")
        print()

    else:
        print(f"La serie es estacionaria después de {diff_count} derivadas.")
        print()

    return stationary_series, diff_count

# def find_sarimax_params(series):
#     """
#     Encuentra los mejores parámetros SARIMAX (p, d, q, P, D, Q, s) usando gráficos ACF y PACF.

#     Args:
#         series (pd.Series): Serie de tiempo estacionaria.

#     Returns:
#         dict: Diccionario con los parámetros SARIMAX.
#     """

#     # ACF y PACF para determinar p y q
#     fig, axes = plt.subplots(1, 2, figsize=(16, 6))
#     plot_acf(series, ax=axes[0])
#     plot_pacf(series, ax=axes[1])
#     plt.show()

#     p = int(input("Ingrese el valor de p (AR term): "))
#     q = int(input("Ingrese el valor de q (MA term): "))

#     # Determinar estacionalidad s
#     s = int(input("Ingrese el valor de s (Seasonal period): "))

#     # ACF y PACF para la serie diferenciada estacionalmente para determinar P y Q
#     series_seasonal_diff = series.diff(s).dropna()

#     fig, axes = plt.subplots(1, 2, figsize=(16, 6))
#     plot_acf(series_seasonal_diff, ax=axes[0])
#     plot_pacf(series_seasonal_diff, ax=axes[1])
#     plt.show()

#     P = int(input("Ingrese el valor de P (Seasonal AR term): "))
#     Q = int(input("Ingrese el valor de Q (Seasonal MA term): "))

#     D = 1  # Asumimos una diferenciación estacional de 1

#     return {'p': p, 'd': diff_count, 'q': q, 'P': P, 'D': D, 'Q': Q, 's': s}

def find_sarimax_params(series):
    """
    Encuentra los mejores parámetros SARIMAX (p, d, q, P, D, Q, s) usando gráficos ACF y PACF.

    Args:
        series (pd.Series): Serie de tiempo estacionaria.

    Returns:
        dict: Diccionario con los parámetros SARIMAX.
    """

    # ACF y PACF para determinar p y q
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    plot_acf(series, ax=axes[0])
    plot_pacf(series, ax=axes[1])
    plt.show()

    # Sugiere los valores basados en el análisis
    p = 1  # basado en PACF
    q = 1  # basado en ACF

    # Determinar estacionalidad s
    s = int(input("Ingrese el valor de s (Seasonal period): "))

    # ACF y PACF para la serie diferenciada estacionalmente para determinar P y Q
    series_seasonal_diff = series.diff(s).dropna()

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    plot_acf(series_seasonal_diff, ax=axes[0])
    plot_pacf(series_seasonal_diff, ax=axes[1])
    plt.show()

    P = 1  # basado en el análisis visual de los gráficos ACF y PACF de la serie diferenciada estacionalmente
    Q = 1  # basado en el análisis visual de los gráficos ACF y PACF de la serie diferenciada estacionalmente
    D = 1  # Asumimos una diferenciación estacional de 1

    return {'p': p, 'd': diff_count, 'q': q, 'P': P, 'D': D, 'Q': Q, 's': s}

serie = analisis_serie_capturas(data, inicio_intervalo, fin_intervalo)

print(f"Total de datos en la serie: {len(serie)}")
print()

serie_estacionaria, diff_count = check_stationarity(serie)

print()
print("La serie estacionaria es ahora: \n")
print(serie_estacionaria.head())

print()
sarimax_params = find_sarimax_params(serie_estacionaria)

# Ajustar el modelo SARIMAX con los parámetros encontrados
model = SARIMAX(serie_estacionaria, 
                order=(sarimax_params['p'], sarimax_params['d'], sarimax_params['q']),
                seasonal_order=(sarimax_params['P'], sarimax_params['D'], sarimax_params['Q'], sarimax_params['s']))
results = model.fit()

# Hacer predicciones
forecast_steps = 10  # Número de pasos hacia adelante para predecir
predictions = results.get_forecast(steps=forecast_steps)
forecasted_values = predictions.predicted_mean
confidence_intervals = predictions.conf_int()

print(forecasted_values)
print(confidence_intervals)

# Plot the predictions
fig = go.Figure()
fig.add_trace(go.Scatter(x=serie_estacionaria.index, y=serie_estacionaria.values,
                         mode='lines+markers',
                         name='Capturas',
                         line=dict(color='#AB63FA')))
fig.add_trace(go.Scatter(x=forecasted_values.index, y=forecasted_values.values,
                         mode='lines+markers',
                         name='Predicciones',
                         line=dict(color='orange')))

fig.update_layout(
    title={
        'text': "Predicciones de Captura de Actas de Escrutinio y Cómputo",
        'font': {'size': 20}
    },
    xaxis_title='Fecha y Hora',
    yaxis_title='Número de Actas Procesadas',
    xaxis=dict(title_font_size=18),
    yaxis=dict(title_font_size=18),
    legend_title_text='Observaciones',
    legend=dict(font_size=18, title_font_size=20),
    template='plotly_white'
)

fig.show()
