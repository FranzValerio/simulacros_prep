import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

def preparar_nuevos_datos(ruta_archivo, columnas_relevantes, columnas_categoricas, columnas_esperadas):
    # Cargar el archivo nuevo
    df_nuevo = pd.read_csv(ruta_archivo, low_memory=False)

    # Seleccionar solo las variables relevantes
    df_nuevo = df_nuevo[columnas_relevantes]

    # Reemplazar valores no numéricos
    for col in columnas_relevantes:
        df_nuevo[col] = df_nuevo[col].replace('-', 'DESCONOCIDO')

    # Realizar one-hot encoding para las variables categóricas
    df_nuevo = pd.get_dummies(df_nuevo, columns=columnas_categoricas)

    # Asegurarse de que las nuevas columnas codificadas coincidan con las del conjunto de entrenamiento
    df_nuevo = df_nuevo.reindex(columns=columnas_esperadas, fill_value=0)

    return df_nuevo

df = pd.read_csv('C:/Users/Francisco Valerio/Desktop/INE/Simulacros/simulacros_prep/Data_clean/data_clean_sim_2_GUB.csv', low_memory=False)

# Pre-procesamiento
variables_relevantes = ['CONTABILIZADA', 'ORIGEN', 'DIGITALIZACION', 'TIPO_DOCUMENTO', 'MECANISMOS_TRASLADO', 'TIEMPO_PROCESAMIENTO_MINUTOS', 'OBSERVACIONES']

# Reemplazar valores no numéricos
for col in variables_relevantes:
    df[col] = df[col].replace('-', 'DESCONOCIDO')

df = df[variables_relevantes]

df = pd.get_dummies(df, columns=['ORIGEN', 'DIGITALIZACION', 'TIPO_DOCUMENTO', 'MECANISMOS_TRASLADO', 'OBSERVACIONES'])

df.dropna(inplace=True)

X = df.drop(columns=['TIEMPO_PROCESAMIENTO_MINUTOS'])
y = df['TIEMPO_PROCESAMIENTO_MINUTOS']

# Guardar las columnas para asegurar que los datos nuevos tengan las mismas columnas
columnas_esperadas = X.columns

# División en conjunto de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modelo de Random Forest
rf = RandomForestRegressor()

# Ajuste de hiperparámetros
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_features': ['auto', 'sqrt'],
    'max_depth': [10, 20, 30, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=3, n_jobs=-1, verbose=2)
grid_search.fit(X_train, y_train)

# Mejor modelo
best_rf = grid_search.best_estimator_

# Evaluación del modelo
y_pred = best_rf.predict(X_test)
print('MSE:', mean_squared_error(y_test, y_pred))
print('MAE:', mean_absolute_error(y_test, y_pred))
print('R²:', r2_score(y_test, y_pred))

columnas_relevantes = ['CONTABILIZADA', 'ORIGEN', 'DIGITALIZACION', 'TIPO_DOCUMENTO', 'MECANISMOS_TRASLADO']
columnas_categoricas = ['ORIGEN', 'DIGITALIZACION', 'TIPO_DOCUMENTO', 'MECANISMOS_TRASLADO']

# Ruta al nuevo archivo de datos
ruta_archivo_nuevo = 'C:/Users/Francisco Valerio/Desktop/INE/Simulacros/simulacros_prep/Data_clean/data_clean_GUB.csv'

# Preparar los nuevos datos
nuevos_datos_preparados = preparar_nuevos_datos(ruta_archivo_nuevo, columnas_relevantes, columnas_categoricas, columnas_esperadas)

# Tomar una muestra aleatoria de los nuevos datos
muestra_nuevos_datos = nuevos_datos_preparados.sample(n=10, random_state=42)

# Realizar predicciones con el modelo entrenado
predicciones = best_rf.predict(muestra_nuevos_datos)

# Mostrar las predicciones
print('Predicciones para la muestra aleatoria de nuevos datos:')
for i, pred in enumerate(predicciones):
    print(f'Acta {i+1}: {pred} minutos')

# Opcional: Unir las predicciones con los datos originales para mayor claridad
muestra_nuevos_datos['Prediccion_Tiempo_Procesamiento'] = predicciones
print(muestra_nuevos_datos)
