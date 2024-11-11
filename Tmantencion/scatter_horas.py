import matplotlib.pyplot as plt

import pandas as pd
from datetime import datetime
import numpy as np


df_hours = pd.read_csv("truck_operational_data.csv")

# Convertir las columnas 'Start' y 'End' a formato de fecha y hora
df_hours['Start'] = pd.to_datetime(df_hours['Start'])
df_hours['End'] = pd.to_datetime(df_hours['End'])

# Calcular las horas trabajadas para cada fila
df_hours['Hours_Worked'] = (df_hours['End'] - df_hours['Start']).dt.total_seconds() / 3600.0

# Sumar todas las horas trabajadas por cada camión
hours_per_machine = df_hours.groupby('Machine_ID')['Hours_Worked'].sum().reset_index()
print(hours_per_machine)


df_fallas = pd.read_csv('maintenance_data.csv')
fallas_per_machine = df_fallas.groupby('Machine_ID').size().reset_index(name='Fallas')


df_combined = pd.merge(hours_per_machine, fallas_per_machine, on='Machine_ID')

colores = np.random.rand(12) 
# Crear el scatter plot
plt.scatter(df_combined['Hours_Worked'], df_combined['Fallas'], c=colores, cmap='PuRd', alpha=0.7)

# Etiquetas y título
plt.xlabel('Horas Trabajadas')
plt.ylabel('Número de Fallas')
plt.title('Relación entre Horas Trabajadas y Fallas por Camión')


for i in range(len(df_combined)):
    plt.text(df_combined['Hours_Worked'][i]-10, df_combined['Fallas'][i]+3, 
             df_combined['Machine_ID'][i], fontsize=7)
    
x = df_combined['Hours_Worked']
y = df_combined['Fallas']

# Ajuste lineal
m, b = np.polyfit(x, y, 1)  # m = pendiente, b = intersección

# Crear la línea de regresión
x_fit = np.linspace(x.min(), x.max(), 100)
y_fit = m * x_fit + b

# Trazar la línea de regresión
plt.plot(x_fit, y_fit, color='pink', linestyle='--', label='Regresión Lineal')

# Mostrar el gráfico
plt.show()
