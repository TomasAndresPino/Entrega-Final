import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import uniform

# Cargar los datos desde el archivo CSV
ruta_archivo = 'truck_operational_data.csv'  # Ajusta esta ruta según sea necesario
df = pd.read_csv(ruta_archivo)

# Filtrar los datos para Machine_ID que empieza con 'AWO'
df_awo = df[df['Machine_ID'].str.startswith('AWOU5IMX')]

# Filtrar los datos para el rango de 5-15 toneladas
df_rango1 = df_awo[(df_awo['Tons_Loaded'] >= 20) & (df_awo['Tons_Loaded'] <= 45)]

# Crear los bins para el rango de 5-15 toneladas
bins_rango1 = np.arange(20, 46, 0.5)  # Rango 20-46 toneladas, con intervalos de 0.5

# Crear el gráfico
plt.hist(df_rango1['Tons_Loaded'], bins=bins_rango1, density=True, edgecolor='black', alpha=0.6)
plt.title('Histograma de 20-45 Toneladas')
plt.xlabel('Toneladas')
plt.ylabel('Frecuencia')

# Ajuste de la distribución uniforme para el rango de 5-15 toneladas
rango1_min, rango1_max = 20, 41
x_rango1 = np.linspace(rango1_min, rango1_max, 100)
pdf_rango1 = uniform.pdf(x_rango1, rango1_min, rango1_max - rango1_min)
plt.plot(x_rango1, pdf_rango1, 'r-', label='Distribución Uniforme')
plt.legend()

# Mostrar el gráfico
plt.show()