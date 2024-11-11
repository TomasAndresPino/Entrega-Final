import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Lee el archivo CSV
df = pd.read_csv('maintenance_data.csv')

# Convierte las columnas de tiempo a tipo datetime
df['Start_Time'] = pd.to_datetime(df['Start_Time'], format='%m/%d/%Y %H:%M')
df['End_Time'] = pd.to_datetime(df['End_Time'], format='%m/%d/%Y %H:%M')

# Calcula la diferencia entre Start_Time y End_Time
df['Duration'] = df['End_Time'] - df['Start_Time']

# Agrupa por Machine_ID y calcula la duración promedio
grouped = df.groupby('Machine_ID')['Duration'].mean().reset_index()

# Muestra el tiempo promedio por máquina en horas
grouped['Duration'] = grouped['Duration'].dt.total_seconds() / 3600

# Define una paleta de colores
colors = plt.cm.viridis(np.linspace(0, 1, len(grouped)))

# Ordena los datos para aplicar colores de forma gradual
grouped_sorted = grouped.sort_values('Duration')

# Asigna colores según el orden de duración
colors_sorted = plt.cm.viridis(np.linspace(0, 1, len(grouped_sorted)))

# Grafica el tiempo promedio entre mantenimientos por máquina con colores graduales
plt.figure(figsize=(10, 6))
bars = plt.bar(grouped_sorted['Machine_ID'], grouped_sorted['Duration'], color=colors_sorted)

# Añade etiquetas y título
plt.xlabel('Machine ID')
plt.ylabel('Duración Promedio (horas)')
plt.title('Duración Promedio de Mantenimiento por Máquina')

# Añade una leyenda con los colores
sm = plt.cm.ScalarMappable(cmap='viridis', norm=plt.Normalize(vmin=grouped_sorted['Duration'].min(), vmax=grouped_sorted['Duration'].max()))
cbar = plt.colorbar(sm, orientation='vertical')
cbar.set_label('Duración Promedio (horas)')

plt.xticks(rotation=45)
plt.show()
