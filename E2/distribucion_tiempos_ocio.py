import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Cargar los datos desde el archivo CSV
ruta_archivo = 'tiempos_ocio.txt'  # Ajusta esta ruta según sea necesario
df = pd.read_csv(ruta_archivo)

# Filtrar los datos solo para el Machine_ID que comienza con 'AWO'
df_awo = df[df['Machine_ID'].str.startswith('AWOU5IMX')]

# Crear los bins con un rango de 1
bins = np.arange(0, df_awo['TOcio'].max() + 1, 1)

# Crear el histograma
plt.hist(df_awo['TOcio'], bins=bins, edgecolor='black')

# Añadir títulos y etiquetas
plt.title('Histograma de TOcio para Machine_ID que empieza con AWO')
plt.xlabel('Tiempo')
plt.ylabel('Frecuencia')

# Mostrar el gráfico
plt.show()