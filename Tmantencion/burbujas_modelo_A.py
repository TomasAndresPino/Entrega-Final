import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress
from matplotlib.lines import Line2D
import numpy as np

# Cargar los datos
truck_operational_data = pd.read_csv("truck_operational_data.csv")
maintenance_data = pd.read_csv("maintenance_data.csv")
truck_data = pd.read_csv("truck_data.csv")

# Agrupar datos por Machine_ID
kms_per_truck = truck_operational_data.groupby('Machine_ID')['Distance_Traveled_km'].sum().reset_index()
tons_per_truck = truck_operational_data.groupby('Machine_ID')['Tons_Loaded'].sum().reset_index()
failures_per_truck = maintenance_data.groupby('Machine_ID')['Failure_Mode'].count().reset_index()

# Renombrar las columnas para facilitar la fusión
kms_per_truck.rename(columns={'Distance_Traveled_km': 'Total_Kms'}, inplace=True)
tons_per_truck.rename(columns={'Tons_Loaded': 'Total_Tons'}, inplace=True)
failures_per_truck.rename(columns={'Failure_Mode': 'Total_Failures'}, inplace=True)

# Fusionar los datos
data = pd.merge(kms_per_truck, tons_per_truck, on='Machine_ID', how='inner')
data = pd.merge(data, failures_per_truck, on='Machine_ID', how='inner')
data = pd.merge(data, truck_data, on='Machine_ID', how='inner')

# Filtrar los datos solo para el modelo A
model_b_data = data[data['Model'] == 'Model_B']

# Crear el gráfico de burbujas con un color distinto para cada Machine_ID
plt.figure(figsize=(14, 8))

# Generar colores más oscuros y diferenciados
dark_colors = plt.cm.get_cmap('Dark2', len(model_b_data))  # Colores oscuros del cmap Dark2

# Lista para almacenar los elementos de la leyenda
legend_elements = []

# Dibujar cada camión como una burbuja de distinto color
for i in range(len(model_b_data)):
    plt.scatter(model_b_data['Total_Tons'].iloc[i], model_b_data['Total_Kms'].iloc[i], 
                s=model_b_data['Total_Failures'].iloc[i] * 20, color=dark_colors(i), alpha=0.7)
    
    # Añadir cada camión a la leyenda como una línea de color correspondiente
    legend_elements.append(Line2D([0], [0], marker='o', color='w', markerfacecolor=dark_colors(i), 
                                  label=f"Camión {model_b_data['Machine_ID'].iloc[i]}", markersize=10))

# Trazar la línea de regresión para Model_A
# Trazar la línea de regresión para Model_B
slope_b, intercept_b, _, _, _ = linregress(model_b_data['Total_Tons'], model_b_data['Total_Kms'])
plt.plot(model_b_data['Total_Tons'], slope_b * model_b_data['Total_Tons'] + intercept_b, 
         color='green', linestyle='--', label='Regresión Model_B')

# Añadir texto a cada burbuja para indicar la cantidad de fallas
for i in range(len(model_b_data)):
    plt.text(model_b_data['Total_Tons'].iloc[i], model_b_data['Total_Kms'].iloc[i], 
             f"Fallas Totales: {model_b_data['Total_Failures'].iloc[i]}", fontsize=10, ha='center')

# Configurar la grilla para que muestre una sola línea de color (sin interferir con las burbujas)
plt.grid(True, which='both', color='gray', linestyle='-', linewidth=0.5)
plt.minorticks_on()

# Configurar etiquetas y título
plt.xlabel('Toneladas Cargadas')
plt.ylabel('Kilómetros Andados')
plt.title('Gráfico de Burbujas: Tons vs Kms vs Fallas para Model_B')
plt.tick_params(axis='both', which='both', direction='in')

# Agregar los camiones y la línea de regresión a la leyenda
legend_elements.append(Line2D([0], [0], color='blue', linestyle='--', label='Regresión Model_A'))

# Mostrar la leyenda con los nombres de los camiones y la regresión
plt.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1, 1), fontsize=10)

# Mostrar el gráfico
plt.tight_layout()
plt.show()