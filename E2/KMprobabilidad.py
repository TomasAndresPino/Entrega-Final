import pandas as pd
from lifelines import KaplanMeierFitter

# Cargar los datos desde un archivo CSV
df = pd.read_csv('base_de_datos')

# Crear el modelo Kaplan-Meier
kmf = KaplanMeierFitter()

# Ajustar el modelo Kaplan-Meier con los datos de "Edad" y "Falla"
kmf.fit(df['Edad'], event_observed=df['Falla'])

# Ejemplo de cómo predecir la probabilidad de supervivencia en un tiempo específico
t = 1000  # Tiempo en el que quieres predecir la probabilidad de supervivencia
probabilidad_supervivencia = kmf.predict(t)

print(f'La probabilidad de supervivencia en el tiempo {t} es {probabilidad_supervivencia:.4f}')
