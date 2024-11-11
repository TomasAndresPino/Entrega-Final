import pandas as pd
import matplotlib.pyplot as plt

# Cargar el archivo TXT, asumiendo que cada número está en una línea
df = pd.read_csv('tiempos_sin_outlayers.txt', header=None)

# Asignar un nombre a la única columna
df.columns = ['numero']

# Definir los rangos
bins = [i * 0.1 for i in range(800)]  # Rango de 0 a 10 con intervalos de 0.1
labels = [f'{bins[i]}-{bins[i+1]}' for i in range(len(bins)-1)]

# Crear una columna de categorías basadas en los rangos
df['rango'] = pd.cut(df['numero'], bins=bins, labels=labels, include_lowest=True)

# Contar la cantidad de números en cada rango
conteo_por_rango = df['rango'].value_counts().sort_index()

# Convertir el conteo por rango en un DataFrame
conteo_df = conteo_por_rango.reset_index()
conteo_df.columns = ['Rango', 'Cantidad']

# Guardar el DataFrame en un archivo CSV
conteo_df.to_csv('conteo_por_rango.csv', index=False)

# Crear el histograma a partir del DataFrame conteo_df
plt.figure(figsize=(12, 6))
plt.bar(conteo_df['Rango'], conteo_df['Cantidad'], color='blue')

# Ajustar las etiquetas del eje X
plt.xticks([])
plt.xlabel('Rango de Tiempo (horas)')
plt.ylabel('Cantidad')
plt.title('Histograma de Tiempos de Mantenimiento')

# Mejorar el layout para que las etiquetas no se solapen
plt.tight_layout()

# Mostrar el histograma
plt.show()
