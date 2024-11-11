import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

# Cargar los datos
truck_operational_data = pd.read_csv("../truck_operational_data.csv")
maintenance_data = pd.read_csv("../maintenance_data.csv")
truck_data = pd.read_csv("../truck_data.csv")

# Agrupar datos por Machine_ID
tons_per_truck = truck_operational_data.groupby('Machine_ID')['Tons_Loaded'].sum().reset_index()
failures_per_truck = maintenance_data.groupby('Machine_ID')['Failure_Mode'].count().reset_index()

# Renombrar las columnas para facilitar la fusión
tons_per_truck.rename(columns={'Tons_Loaded': 'Total_Tons'}, inplace=True)
failures_per_truck.rename(columns={'Failure_Mode': 'Total_Failures'}, inplace=True)

# Fusionar los datos
data = pd.merge(tons_per_truck, failures_per_truck, on='Machine_ID')
data = pd.merge(data, truck_data, on='Machine_ID')  # Fusionar con los datos del modelo

# Ajustar la línea de regresión por modelo
model_a_data = data[data['Model'] == 'Model_A']
model_b_data = data[data['Model'] == 'Model_B']

# Regresión para Model_A
slope_a, intercept_a, r_value_a, p_value_a, std_err_a = linregress(model_a_data['Total_Tons'], model_a_data['Total_Failures'])

# Regresión para Model_B
slope_b, intercept_b, r_value_b, p_value_b, std_err_b = linregress(model_b_data['Total_Tons'], model_b_data['Total_Failures'])

# Crear el gráfico de dispersión
plt.figure(figsize=(10, 6))

# Graficar puntos para Model_A y Model_B
plt.scatter(model_a_data['Total_Tons'], model_a_data['Total_Failures'], alpha=0.7, color='blue', label='Model_A')
plt.scatter(model_b_data['Total_Tons'], model_b_data['Total_Failures'], alpha=0.7, color='green', label='Model_B')

# Trazar las líneas de regresión para Model_A y Model_B
plt.plot(model_a_data['Total_Tons'], slope_a * model_a_data['Total_Tons'] + intercept_a, color='blue', linestyle='--', label='Regresión Model_A')
plt.plot(model_b_data['Total_Tons'], slope_b * model_b_data['Total_Tons'] + intercept_b, color='green', linestyle='--', label='Regresión Model_B')

# Añadir el ID del camión a cada punto
for i in range(len(data)):
    plt.annotate(data['Machine_ID'].iloc[i], (data['Total_Tons'].iloc[i], data['Total_Failures'].iloc[i]), 
                 textcoords="offset points", xytext=(0, 5), ha='center', fontsize=8)

# Configurar etiquetas y título
plt.xlabel('Toneladas Cargadas')
plt.ylabel('Cantidad de Fallas')
plt.title('Scatter Plot: Fallas vs Toneladas Cargadas por Camión')
plt.legend()
plt.grid()

# Mostrar el gráfico
plt.show()
