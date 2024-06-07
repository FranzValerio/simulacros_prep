import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.api import SARIMAX
import plotly.graph_objects as go
import warnings

warnings.filterwarnings('ignore')

inicio_intervalo = pd.to_datetime('2024-06-02 20:00')
fin_intervalo = pd.to_datetime('2024-06-03 20:00')

data = pd.read_csv('C:/Users/Francisco Valerio/Desktop/INE/Simulacros/simulacros_prep/BDD/PUE_GUB_2024.csv', skiprows=5, low_memory=False)

def serie_capturas(df):

   df['Fecha_Captura'] = df['FECHA_HORA_CAPTURA']

   df.set_index('Fecha_Captura', inplace = True)

   df_resampled = df.resample('20T').count()

   return df_resampled['FECHA_HORA_CAPTURA']

def serie_plot(series):

    line_color = '#B82E2E'

    fig_line = go.Figure()

    fig_line.add_trace(go.Scatter(x = series.index, y = series,
                                  mode = 'lines', name = 'Actas Capturadas', line = dict(color = line_color)))
    
    fig_line.update_layout(
        title={
        'text': f"Programa de Resultados Electorales Preliminares (2 de junio de 2024) <br>Evolución temporal de la Captura de Actas de Escrutinio y Cómputo</br>",
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

def inverse_transform(predictions, original_series, diff_count):

    last_original_value = original_series[-diff_count]

    inverted_predictions = predictions.copy()

    for i in range(diff_count, 0, -1):

        inverted_predictions = inverted_predictions.cumsum() + original_series[-i]

    return inverted_predictions


data['FECHA_HORA_ACOPIO'] = pd.to_datetime(data['FECHA_HORA_ACOPIO'], format='%d/%m/%Y %H:%M:%S', errors='coerce')
data['FECHA_HORA_CAPTURA'] = pd.to_datetime(data['FECHA_HORA_CAPTURA'], format='%d/%m/%Y %H:%M:%S', errors='coerce')
data['FECHA_HORA_VERIFICACION'] = pd.to_datetime(data['FECHA_HORA_VERIFICACION'], format='%d/%m/%Y %H:%M:%S', errors='coerce')

data['TIEMPO_PROCESAMIENTO'] = data['FECHA_HORA_CAPTURA'] - data['FECHA_HORA_ACOPIO']
data['TIEMPO_PROCESAMIENTO_MINUTOS'] = data['TIEMPO_PROCESAMIENTO'].dt.total_seconds()/60
data['TIEMPO_PROCESAMIENTO_MINUTOS'] = data['TIEMPO_PROCESAMIENTO_MINUTOS'].round(2)

data['TIEMPO_PROCESAMIENTO_VERIFICACION'] = data['FECHA_HORA_VERIFICACION'] - data['FECHA_HORA_CAPTURA']
data['TIEMPO_PROCESAMIENTO_VERIFICACION_MINUTOS'] = data['TIEMPO_PROCESAMIENTO_VERIFICACION'].dt.total_seconds()/60
data['TIEMPO_PROCESAMIENTO_VERIFICACION_MINUTOS'] = data['TIEMPO_PROCESAMIENTO_VERIFICACION_MINUTOS'].round(2)

serie = serie_capturas(data)

serie_plot(serie)

print(f"Total de datos en la serie: {len(serie)}")

print()

serie_estacionaria, diff_count = check_stationarity(serie)

print()
print("La serie estacionaria es ahora: \n")
print(serie_estacionaria.head())

fig, ax = plt.subplots(1, 1, figsize = (8,6), dpi = 80)
ax.plot(serie_estacionaria)
plt.show()

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

inverted_forecast_values = inverse_transform(forecasted_values, serie, diff_count)
print(inverted_forecast_values)
print(confidence_intervals)

# Plot the predictions
fig = go.Figure()
fig.add_trace(go.Scatter(x=serie.index, y=serie.values,
                         mode='lines+markers',
                         name='Capturas',
                         line=dict(color='#AB63FA')))
fig.add_trace(go.Scatter(x=inverted_forecast_values.index, y=inverted_forecast_values.values,
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
