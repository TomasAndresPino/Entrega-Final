import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

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

# Ajustar líneas de regresión por modelo
model_a_data = data[data['Model'] == 'Model_A']
model_b_data = data[data['Model'] == 'Model_B']

# Crear el gráfico de burbujas
plt.figure(figsize=(14, 8))
bubble_a = plt.scatter(model_a_data['Total_Tons'], model_a_data['Total_Kms'], 
                       s=model_a_data['Total_Failures']*20, alpha=0.5, color='blue', label='Model_A')
bubble_b = plt.scatter(model_b_data['Total_Tons'], model_b_data['Total_Kms'], 
                       s=model_b_data['Total_Failures']*20, alpha=0.5, color='green', label='Model_B')

# Trazar las líneas de regresión
slope_a, intercept_a, _, _, _ = linregress(model_a_data['Total_Tons'], model_a_data['Total_Kms'])
slope_b, intercept_b, _, _, _ = linregress(model_b_data['Total_Tons'], model_b_data['Total_Kms'])

plt.plot(model_a_data['Total_Tons'], slope_a * model_a_data['Total_Tons'] + intercept_a, 
         color='blue', linestyle='--', label='Regresión Model_A')
plt.plot(model_b_data['Total_Tons'], slope_b * model_b_data['Total_Tons'] + intercept_b, 
         color='green', linestyle='--', label='Regresión Model_B')

# Añadir texto a cada burbuja para indicar la cantidad de fallas
for i in range(len(data)):
    plt.text(data['Total_Tons'].iloc[i], data['Total_Kms'].iloc[i], 
             f"Fallas Totales: {data['Total_Failures'].iloc[i]}", fontsize=10, ha='center')

# Crear manejadores personalizados para la leyenda
from matplotlib.lines import Line2D
legend_elements = [Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10, label='Model_A'),
                   Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=10, label='Model_B'),
                   Line2D([0], [0], color='blue', linestyle='--', label='Regresión Model_A'),
                   Line2D([0], [0], color='green', linestyle='--', label='Regresión Model_B')]

# Configurar etiquetas y título
plt.xlabel('Toneladas Cargadas')
plt.ylabel('Kilómetros Andados')
plt.title('Gráfico de Burbujas: Tons vs Kms vs Fallas por Camión')
plt.legend(handles=legend_elements)
plt.grid()

# Mostrar el gráfico
plt.show()