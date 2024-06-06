import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
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

# Cargar y preprocesar los datos
df = pd.read_csv('C:/Users/franz/Desktop/simulacros_prep/Data_clean/data_clean_GUB.csv', low_memory=False)

variables_relevantes = ['CONTABILIZADA', 'ORIGEN', 'DIGITALIZACION', 'TIPO_DOCUMENTO', 'MECANISMOS_TRASLADO', 'TIEMPO_PROCESAMIENTO_MINUTOS']

for col in variables_relevantes:
    df[col] = df[col].replace('-', '0')

df = df[variables_relevantes]

df = pd.get_dummies(df, columns=['ORIGEN', 'DIGITALIZACION', 'TIPO_DOCUMENTO', 'MECANISMOS_TRASLADO'])

df.dropna(inplace=True)

X = df.drop(columns=['TIEMPO_PROCESAMIENTO_MINUTOS'])
y = df['TIEMPO_PROCESAMIENTO_MINUTOS']

columnas_esperadas = X.columns

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Escalar los datos
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Construir el modelo de la red neuronal
model = Sequential()
model.add(Dense(128, input_dim=X_train_scaled.shape[1], activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(1))  # Salida de regresión

model.compile(optimizer=Adam(learning_rate=0.001), loss='mean_squared_error')

# Entrenar el modelo
history = model.fit(X_train_scaled, y_train, validation_split=0.2, epochs=100, batch_size=32, verbose=2)

# Evaluación del modelo
y_pred = model.predict(X_test_scaled)
print('MSE:', mean_squared_error(y_test, y_pred))
print('MAE:', mean_absolute_error(y_test, y_pred))
print('R²:', r2_score(y_test, y_pred))

# Preparar los nuevos datos
columnas_relevantes = ['CONTABILIZADA', 'ORIGEN', 'DIGITALIZACION', 'TIPO_DOCUMENTO', 'MECANISMOS_TRASLADO']
columnas_categoricas = ['ORIGEN', 'DIGITALIZACION', 'TIPO_DOCUMENTO', 'MECANISMOS_TRASLADO']

ruta_archivo_nuevo = 'C:/Users/franz/Desktop/simulacros_prep/Data_clean/data_clean_DIP_LOC.csv'
nuevos_datos_preparados = preparar_nuevos_datos(ruta_archivo_nuevo, columnas_relevantes, columnas_categoricas, columnas_esperadas)

nuevos_datos_preparados_scaled = scaler.transform(nuevos_datos_preparados)

# Tomar una muestra aleatoria de los nuevos datos
muestra_nuevos_datos = nuevos_datos_preparados_scaled.sample(n=10, random_state=42)

# Realizar predicciones con el modelo entrenado
predicciones = model.predict(muestra_nuevos_datos)

# Mostrar las predicciones
print('Predicciones para la muestra aleatoria de nuevos datos:')
for i, pred in enumerate(predicciones):
    print(f'Acta {i+1}: {pred[0]} minutos')

# Opcional: Unir las predicciones con los datos originales para mayor claridad
muestra_nuevos_datos_original = nuevos_datos_preparados.sample(n=10, random_state=42)
muestra_nuevos_datos_original['Prediccion_Tiempo_Procesamiento'] = predicciones
print(muestra_nuevos_datos_original)
