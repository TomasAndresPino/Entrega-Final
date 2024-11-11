import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Cargar los datos desde el archivo CSV
ruta_archivo = 'truck_operational_data.csv'  # Ajusta esta ruta según sea necesario
df = pd.read_csv(ruta_archivo)

# Filtrar los datos solo para el Machine_ID que comienza con 'AWO'
df_awo = df[df['Machine_ID'].str.startswith('AWOU5IMX')]

# Crear los bins con un rango de 0.5
bins = np.arange(0, df_awo['Distance_Traveled_km'].max() + 0.5, 0.5)

# Crear el histograma
plt.hist(df_awo['Distance_Traveled_km'], bins=bins, edgecolor='black')

# Añadir títulos y etiquetas
plt.title('Histograma de Kms para Machine_ID que empieza con AWO')
plt.xlabel('Toneladas')
plt.ylabel('Frecuencia')

# Mostrar el gráfico
plt.show()
