import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# Leer los datos desde el CSV (reemplaza 'ruta_al_archivo.csv' con tu archivo real)
df = pd.read_csv("C:/Users/manue/OneDrive/Escritorio/Proyecto-Capstone-1/E2/KMs/km.engine.csv")

# Extraer los tiempos (la primera columna del CSV)
tiempos = df['time'].values

# Aplicar KDE usando scipy
kde = gaussian_kde(tiempos)

# Crear un rango de valores donde se evaluará la densidad
x_range = np.linspace(min(tiempos), max(tiempos), 6800)

# Evaluar la KDE en ese rango de valores
kde_values = kde(x_range)

# Graficar la densidad estimada
plt.plot(x_range, kde_values, label='Densidad estimada (KDE)')
plt.xlabel('Tiempo')
plt.ylabel('Densidad')
plt.title('Función de Densidad estimada con KDE')
plt.legend()
plt.show()
