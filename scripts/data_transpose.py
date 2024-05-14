import pandas as pd

df = pd.read_csv('C:/Users/Francisco Valerio/Desktop/INE/Simulacros/simulacros_prep/Data adicional/totales_simulacro_1.csv')

df_transpuesto = df.T

df_transpuesto.to_csv('C:/Users/Francisco Valerio/Desktop/INE/Simulacros/simulacros_prep/Data adicional/totales_simulacro_1_T.csv', header = False)