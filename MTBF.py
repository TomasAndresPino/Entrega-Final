import pandas as pd
import numpy as np

# Cargar los datos desde el archivo CSV
archivo = 'caso_reactivo.csv'  # Reemplaza con el nombre de tu archivo
datos = pd.read_csv(archivo)

# Seleccionar la columna "Tiempo promedio entre fallas"
tiempo_promedio = datos['Tiempo promedio entre fallas']

# Calcular las métricas
media = tiempo_promedio.mean()
percentil_25 = np.percentile(tiempo_promedio, 25)
percentil_75 = np.percentile(tiempo_promedio, 75)

# Imprimir los resultados
print(f"Media: {media}")
print(f"Percentil 25: {percentil_25}")
print(f"Percentil 75: {percentil_75}")