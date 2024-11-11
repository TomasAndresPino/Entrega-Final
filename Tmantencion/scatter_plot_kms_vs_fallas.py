""""
from mantenimiento import counter_kms_por_camion

with open("../truck_operational_data.csv", 'r') as archivo:
        # Contar la frecuencia de cada falla
        imprimir = counter_kms_por_camion(archivo)

print(imprimir)
"""


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

# Cargar los datos
truck_operational_data = pd.read_csv("../truck_operational_data.csv")
maintenance_data = pd.read_csv("../maintenance_data.csv")

# Calcular kilómetros recorridos por camión
kms_per_truck = truck_operational_data.groupby('Machine_ID')['Distance_Traveled_km'].sum().reset_index()

# Calcular la cantidad de fallas por camión
failures_per_truck = maintenance_data.groupby('Machine_ID')['Failure_Mode'].count().reset_index()

# Unir los datos en un solo DataFrame
combined_data = pd.merge(kms_per_truck, failures_per_truck, on='Machine_ID', suffixes=('_kms', '_failures'))

# Crear el scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(combined_data['Distance_Traveled_km'], combined_data['Failure_Mode'], alpha=0.7, label='Camiones')

# Calcular la línea de regresión lineal
slope, intercept, r_value, p_value, std_err = linregress(combined_data['Distance_Traveled_km'], combined_data['Failure_Mode'])

# Crear los valores de la línea de regresión
x_values = np.linspace(combined_data['Distance_Traveled_km'].min(), combined_data['Distance_Traveled_km'].max(), 100)
y_values = slope * x_values + intercept

# Dibujar la línea de regresión
plt.plot(x_values, y_values, color='red', label='Línea de Regresión', linewidth=2)

# Etiquetas y título
plt.title('Kilómetros Recorridos vs. Cantidad de Fallas por Camión')
plt.xlabel('Kilómetros Recorridos')
plt.ylabel('Cantidad de Fallas')
plt.grid(True)
plt.legend()

# Mostrar el gráfico
plt.show()



