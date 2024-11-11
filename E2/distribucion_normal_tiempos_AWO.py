import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

# Cargar los datos desde el archivo CSV
ruta_archivo = 'tiempos_operaciones.txt'  # Ajusta esta ruta según sea necesario
df = pd.read_csv(ruta_archivo)

# Filtrar los datos solo para el Machine_ID que comienza con 'AWO'
df_awo = df[df['Machine_ID'].str.startswith('AWOU5IMX')]

# Crear los bins con un rango de 0.5
bins = np.arange(0, df_awo['Tiempo'].max() + 0.5, 0.5)

# Crear el histograma
plt.hist(df_awo['Tiempo'], bins=bins, edgecolor='black', density=True, alpha=0.6, color='g')

# Calcular los parámetros de la distribución normal (media y desviación estándar)
mu, std = norm.fit(df_awo['Tiempo'])

# Generar los valores de la curva de la distribución normal
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, mu, std)

# Graficar la curva de la distribución normal
plt.plot(x, p, 'k', linewidth=2)

# Añadir títulos y etiquetas
plt.title(f'Histograma y Curva Normal Ajustada\nMachine_ID que empieza con AWO\n$\mu={mu:.2f},\ \sigma={std:.2f}$')
plt.xlabel('Tiempo')
plt.ylabel('Densidad de Frecuencia')

# Mostrar el gráfico
plt.show()
