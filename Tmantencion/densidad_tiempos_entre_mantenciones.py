import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np  # Importar numpy
from scipy.stats import gaussian_kde

# Cargar los datos
maintenance_data = pd.read_csv("maintenance_data.csv")

# Convertir las columnas de fecha a datetime
maintenance_data['Start_Time'] = pd.to_datetime(maintenance_data['Start_Time'])
maintenance_data['End_Time'] = pd.to_datetime(maintenance_data['End_Time'])

# Ordenar los datos por Machine_ID y Start_Time
maintenance_data = maintenance_data.sort_values(by=['Machine_ID', 'Start_Time'])

# Calcular el tiempo entre mantenciones para cada camión
maintenance_data['Time_Between_Maintenances'] = maintenance_data['Start_Time'] - maintenance_data['End_Time'].shift()

# Convertir a días
maintenance_data['Time_Between_Maintenances'] = maintenance_data['Time_Between_Maintenances'].dt.total_seconds() / 86400  # en días

# Filtrar los tiempos entre mantenciones para eliminar valores NaN (primer registro de cada camión) y negativos
maintenance_data = maintenance_data[
    maintenance_data['Time_Between_Maintenances'].notnull() &
    (maintenance_data['Time_Between_Maintenances'] >= 0)
]

# Calcular la densidad
data = maintenance_data['Time_Between_Maintenances']
kde = gaussian_kde(data)
x = np.linspace(data.min(), data.max(), 100)
density = kde(x)

# Encontrar el valor en x con la máxima densidad
max_density_x = x[density.argmax()]
max_density_y = density.max()

# Crear el gráfico de densidad
plt.figure(figsize=(20, 15))
plt.fill_between(x, density, color='blue', alpha=0.7)
plt.axvline(x=max_density_x, color='red', linestyle='--')

# Configurar etiquetas y título
plt.xlabel('Tiempo Entre Mantenciones (días)')
plt.ylabel('Densidad')
plt.title('Densidad del Tiempo Entre Mantenciones por Camión')

# Configurar la leyenda
plt.legend(
    [f'Máxima Densidad: {max_density_x:.2f} días'],
    loc='upper right',
    frameon=True,
    fontsize=10,
    title='Leyenda',
    title_fontsize='12',
    shadow=True,
    borderpad=1,
    facecolor='white'
)

# Mostrar el gráfico
plt.show()












