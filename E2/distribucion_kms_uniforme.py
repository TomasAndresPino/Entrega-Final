import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import uniform

# Cargar los datos desde el archivo CSV
ruta_archivo = 'truck_operational_data.csv'  # Ajusta esta ruta según sea necesario
df = pd.read_csv(ruta_archivo)

# Filtrar los datos para Machine_ID que empieza con 'AWO'
df_awo = df[df['Machine_ID'].str.startswith('AWOU5IMX')]

# Filtrar los datos para el rango de 8-22 kilometros
df_rango1 = df_awo[(df_awo['Distance_Traveled_km'] >= 8) & (df_awo['Distance_Traveled_km'] <= 22)]

# Crear los bins para el rango de 8-22
bins_rango1 = np.arange(8, 23, 0.5)  # Rango 8-22 kilometros, con intervalos de 0.5

# Crear el gráfico
plt.hist(df_rango1['Distance_Traveled_km'], bins=bins_rango1, density=True, edgecolor='black', alpha=0.6)
plt.title('Histograma de 8-22 Kilometros')
plt.xlabel('Kilometros')
plt.ylabel('Frecuencia')

# Ajuste de la distribución uniforme para el rango de 8-22 Kms
rango1_min, rango1_max = 8, 22
x_rango1 = np.linspace(rango1_min, rango1_max, 100)
pdf_rango1 = uniform.pdf(x_rango1, rango1_min, rango1_max - rango1_min)
plt.plot(x_rango1, pdf_rango1, 'r-', label='Distribución Uniforme')
plt.legend()

# Mostrar el gráfico
plt.show()