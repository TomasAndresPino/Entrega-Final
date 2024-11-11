import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Lee el archivo CSV
df = pd.read_csv('maintenance_data.csv')

# Convierte las columnas de tiempo a tipo datetime
df['Start_Time'] = pd.to_datetime(df['Start_Time'], format='%m/%d/%Y %H:%M')
df['End_Time'] = pd.to_datetime(df['End_Time'], format='%m/%d/%Y %H:%M')

# Ordena los datos por Machine_ID y Start_Time
df = df.sort_values(by=['Machine_ID', 'Start_Time'])

# Calcula el tiempo entre fallas
df['Time_Between_Failures'] = df.groupby('Machine_ID')['Start_Time'].shift(-1) - df['End_Time']

# Filtra las filas donde 'Time_Between_Failures' es positivo (para asegurar que haya una siguiente falla)
df_filtered = df[df['Time_Between_Failures'] > pd.Timedelta(0)]

# Calcula el tiempo promedio entre fallas por máquina
average_time_between_failures = df_filtered.groupby('Machine_ID')['Time_Between_Failures'].mean().reset_index()

# Convierte el tiempo promedio a días
average_time_between_failures['Time_Between_Failures'] = average_time_between_failures['Time_Between_Failures'].dt.total_seconds() / (3600 * 24)

# Define una paleta de colores
colors = plt.cm.viridis(np.linspace(0, 1, len(average_time_between_failures)))

# Ordena los datos para aplicar colores de forma gradual
sorted_data = average_time_between_failures.sort_values('Time_Between_Failures')

# Asigna colores según el orden de duración
colors_sorted = plt.cm.viridis(np.linspace(0, 1, len(sorted_data)))

# Grafica el tiempo promedio entre fallas por máquina con colores graduales
plt.figure(figsize=(10, 6))
bars = plt.bar(sorted_data['Machine_ID'], sorted_data['Time_Between_Failures'], color=colors_sorted)

# Añade etiquetas y título
plt.xlabel('Machine ID')
plt.ylabel('Tiempo Promedio entre Fallas (días)')
plt.title('Tiempo Promedio entre Fallas por Máquina')

# Añade una leyenda con los colores
sm = plt.cm.ScalarMappable(cmap='viridis', norm=plt.Normalize(vmin=sorted_data['Time_Between_Failures'].min(), vmax=sorted_data['Time_Between_Failures'].max()))
cbar = plt.colorbar(sm, orientation='vertical')
cbar.set_label('Tiempo Promedio entre Fallas (días)')

plt.xticks(rotation=45)
plt.show()
