import pandas as pd
import matplotlib.pyplot as plt

# Leer el archivo CSV
df = pd.read_csv('frecuencias_por_year.txt')
# Crear un gráfico de barras
plt.figure(figsize=(12, 6))
plt.bar(df['Year'], df['Frecuencia'], color='b', edgecolor='black')
plt.xlabel('Año')
plt.ylabel('Frecuencia de Reparación')
plt.title('Frecuencia de Reparación por Año')
plt.grid(True, axis='y')

# Mostrar el gráfico
plt.show()
