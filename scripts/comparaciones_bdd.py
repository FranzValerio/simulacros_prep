import pandas as pd

def compare_csv(file1, file2):
    df1 = pd.read_csv(file1, skiprows=5, low_memory=False)
    df2 = pd.read_csv(file2, skiprows=5, low_memory=False)

    print("Programa de comparación de archivos de Bases de Datos \n")

    summary = {}

    # Identificar registros añadidos y quitados
    merged_df = df1.merge(df2, indicator=True, how='outer')

    added = merged_df[merged_df['_merge'] == 'right_only']
    removed = merged_df[merged_df['_merge'] == 'left_only']

    summary['Registros Añadidos'] = len(added)
    summary['Registros Quitados'] = len(removed)

    # Identificar columnas añadidas y quitadas
    columns_added = df2.columns.difference(df1.columns)
    columns_removed = df1.columns.difference(df2.columns)

    summary['Columnas Añadidas'] = list(columns_added)
    summary['Columnas Quitadas'] = list(columns_removed)

    # Comparar columnas modificadas
    common_columns = df1.columns.intersection(df2.columns)
    modified_columns = []

    for col in common_columns:
        if not df1[col].equals(df2[col]):
            modified_columns.append(col)

    summary['Columnas Modificadas'] = modified_columns

    # Comparar fila por fila para detectar registros modificados
    modified_records = 0
    for i in range(len(df1)):
        if i >= len(df2):
            break
        row1 = df1.iloc[i]
        row2 = df2.iloc[i]
        if not row1.equals(row2):
            modified_records += 1

    summary['Registros Modificados'] = modified_records

    # Mostrar resumen
    print("Resumen de Cambios:")
    print(f"Dimensiones de la Base de Datos de Ayuntamientos del 3 de junio: {df1.shape}")
    print(f"Dimensiones de la Base de Datos de Ayuntamientos del 26 de junio: {df2.shape}")
    print(f"Columnas Añadidas: {summary['Columnas Añadidas']}")
    print(f"Columnas Quitadas: {summary['Columnas Quitadas']}")
    print(f"Columnas Modificadas: {summary['Columnas Modificadas']}")
    print(f"Registros Añadidos: {summary['Registros Añadidos']}")
    print(f"Registros Quitados: {summary['Registros Quitados']}")
    print(f"Registros Modificados: {summary['Registros Modificados']}")

# Rutas de los archivos CSV
ayun_3junio = 'C:/Users/Francisco Valerio/Desktop/INE/Simulacros/simulacros_prep/BDD/PUE_AYUN_2024.csv'
ayun_26junio = 'C:/Users/Francisco Valerio/Downloads/20240603_2000_PREP_PUE(1)/20240603_2000_PREP_AYUN_PUE/PUE_AYUN_2024.csv'
gub_3junio = 'C:/Users/Francisco Valerio/Desktop/INE/Simulacros/simulacros_prep/BDD/PUE_GUB_2024.csv'
gub_26junio = 'C:/Users/Francisco Valerio/Downloads/20240603_2000_PREP_PUE(1)/20240603_2000_PREP_GUB_PUE/PUE_GUB_2024.csv'

dip_3junio = 'C:/Users/Francisco Valerio/Desktop/INE/Simulacros/simulacros_prep/BDD/PUE_DIP_LOC_2024.csv'
dip_26junio = 'C:/Users/Francisco Valerio/Downloads/20240603_2000_PREP_PUE(1)/20240603_2000_PREP_DIP_LOC_PUE/PUE_DIP_LOC_2024.csv'

ayun_3junio = 'C:/Users/Francisco Valerio/Desktop/INE/Simulacros/simulacros_prep/BDD/PUE_AYUN_2024.csv'
ayun_26junio =  'C:/Users/Francisco Valerio/Downloads/20240603_2000_PREP_PUE(1)/20240603_2000_PREP_AYUN_PUE/PUE_AYUN_2024.csv'

# Comparar los archivos CSV y mostrar un resumen de los cambios
compare_csv(ayun_3junio, ayun_26junio)
