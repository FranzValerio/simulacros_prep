import pandas as pd
import os

tipo_eleccion = 'GUB' # 'DIP_LOC' o 'AYUN'

titulo_elecciones = {'GUB': 'Gubernatura',
                     'DIP_LOC': 'Diputaciones Locales',
                     'AYUN': 'Ayuntamientos'}

folder_path_sim1 = 'C:/Users/Francisco Valerio/Desktop/INE/Simulacros/simulacros_prep/Data_final/BDD_Simulacro_1'

folder_path_sim1_2 = 'C:/Users/Francisco Valerio/Desktop/INE/Simulacros/simulacros_prep/Data_final/BDD_Simulacro_1_2'

folder_path_sim2 = 'C:/Users/Francisco Valerio/Desktop/INE/Simulacros/simulacros_prep/Data_final/BDD_Simulacro_2'

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

print(f"Tipo de elección: {titulo_elecciones.get(tipo_eleccion)}")

csv_file_path_1 = find_csv(folder_path_sim1, tipo_eleccion)

csv_file_path_1_2 = find_csv(folder_path_sim1_2, tipo_eleccion)

csv_file_path_2 = find_csv(folder_path_sim2, tipo_eleccion)

df_sim_1 = load_csv(csv_file_path_1)

df_sim_1_2 = load_csv(csv_file_path_1_2)

df_sim_2 = load_csv(csv_file_path_2)

print(comparar_promedios(df_sim_1, df_sim_1_2, "Simulacro 1", "Simulacro 1.2"))
print(comparar_promedios(df_sim_1_2, df_sim_2, "Simulacro 1.2", "Simulacro 2"))