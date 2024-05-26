import pandas as pd
import os

tipo_eleccion = 'AYUN' # 'DIP_LOC' o 'AYUN'

titulo_elecciones = {'GUB': 'Gubernatura',
                     'DIP_LOC': 'Diputaciones Locales',
                     'AYUN': 'Ayuntamientos'}

folder_path_sim1 = 'C:/Users/Francisco Valerio/Desktop/INE/Simulacros/simulacros_prep/Data_final/BDD_Simulacro_1'

folder_path_sim1_2 = 'C:/Users/Francisco Valerio/Desktop/INE/Simulacros/simulacros_prep/Data_final/BDD_Simulacro_1_2'

folder_path_sim2 = 'C:/Users/Francisco Valerio/Desktop/INE/Simulacros/simulacros_prep/Data_final/BDD_Simulacro_2'

totales = {'GUB': 8338,
           'DIP_LOC': 8414,
           'AYUN': 8356}

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

        return pd.read_csv(file_path, low_memory=False)
    
    else:

        print("No se encontró ningún archivo CSV.")

    return None

def comparar_promedios(df1, df2, nombre_df1, nombre_df2):
    promedio_procesamiento_df1 = df1['TIEMPO_PROCESAMIENTO_MINUTOS'].mean()
    promedio_procesamiento_df2 = df2['TIEMPO_PROCESAMIENTO_MINUTOS'].mean()
    
    porcentaje_cambio = ((promedio_procesamiento_df2 - promedio_procesamiento_df1) / promedio_procesamiento_df1) * 100
    
    if porcentaje_cambio > 0:
        resultado = f"El tiempo de procesamiento de {nombre_df2} empeoró en un {porcentaje_cambio:.2f}% respecto a {nombre_df1}."
    else:
        resultado = f"El tiempo de procesamiento de {nombre_df2} mejoró en un {abs(porcentaje_cambio):.2f}% respecto a {nombre_df1}."
    
    return resultado

def calcular_incremento_actas(df1, df2, nombre_df1, nombre_df2, tipo_eleccion):
    actas_capturadas_df1 = df1.shape[0]
    actas_capturadas_df2 = df2.shape[0]
    
    incremento = actas_capturadas_df2 - actas_capturadas_df1
    porcentaje_incremento = (incremento / totales[tipo_eleccion]) * 100
    
    return f"El número de actas capturadas en {nombre_df2} aumentó en {incremento} actas ({porcentaje_incremento:.2f}%) respecto a {nombre_df1}."

def check_nans(df):
    """Revisa si existen valores NaNs en las columnas de FECHA_HORA_ACOPIO, FECHA_HORA_CAPTURA y
    FECHA_HORA_VERIFICACION. Se aplica previo a la conversión de datos tipo object a datetime para
    poder calcular el tiempo de procesamiento
    
    Args:
    df (pd.DataFrame): La dataframe que se va a utilizar
    
    Returns:
    df_no_nans (pd.DataFrame): La dataframe sin valores NaNs en esas columnas"""

    df_no_nans = df.dropna(subset = ['FECHA_HORA_ACOPIO', 'FECHA_HORA_CAPTURA', 'FECHA_HORA_VERIFICACION'])

    df_tiempos_validos = df_no_nans[~df_no_nans['FECHA_HORA_CAPTURA'].isin(['-', 'N/A'])]

    df_contabilizadas = df_tiempos_validos[~df_tiempos_validos['CONTABILIZADA'].isin([0, 2])]

    df_filtrada = df_contabilizadas[~df_contabilizadas['OBSERVACIONES'].str.startswith('SIN ACTA')]

    return df_filtrada

print(f"Tipo de elección: {titulo_elecciones.get(tipo_eleccion)}")

csv_file_path_1 = find_csv(folder_path_sim1, tipo_eleccion)

csv_file_path_1_2 = find_csv(folder_path_sim1_2, tipo_eleccion)

csv_file_path_2 = find_csv(folder_path_sim2, tipo_eleccion)

df_sim_1 = load_csv(csv_file_path_1)

df_sim_1_2 = load_csv(csv_file_path_1_2)

df_sim_2 = load_csv(csv_file_path_2)

df_clean_sim_1 = check_nans(df_sim_1)

df_clean_sim_1_2 = check_nans(df_sim_1_2)

df_clean_sim_2 = check_nans(df_sim_2)

print(comparar_promedios(df_clean_sim_1, df_clean_sim_1_2, "Simulacro 1", "Simulacro 1.2"))
print(comparar_promedios(df_clean_sim_1_2, df_clean_sim_2, "Simulacro 1.2", "Simulacro 2"))

print(calcular_incremento_actas(df_clean_sim_1, df_clean_sim_1_2, "Simulacro 1", "Simulacro 1.2", tipo_eleccion))
print(calcular_incremento_actas(df_clean_sim_1_2, df_clean_sim_2, "Simulacro 1.2", "Simulacro 2", tipo_eleccion))

print(f"La cantidad de actas capturadas en el Primer Simulacro PREP fue de: {df_clean_sim_1.shape[0]} actas")
print(f"La cantidad de actas capturadas en la Repetición del Primer Simulacro PREP fue de: {df_clean_sim_1_2.shape[0]} actas")
print(f"La cantidad de actas capturadas en el Segundo Simulacro PREP fue de: {df_clean_sim_2.shape[0]} actas")