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