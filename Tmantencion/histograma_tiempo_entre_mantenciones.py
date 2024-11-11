import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar los datos
maintenance_data = pd.read_csv("../maintenance_data.csv")

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

# Definir los límites de los intervalos de 2 en 2 hasta el 44
bins = range(0, 46, 2)  # Esto crea los intervalos [0, 2, 4, ..., 44]

# Crear el histograma
plt.figure(figsize=(20, 15))
ax = sns.histplot(maintenance_data['Time_Between_Maintenances'], bins=bins, kde=False, color='blue', alpha=0.7)

# Configurar etiquetas y título
plt.xlabel('Tiempo Entre Mantenciones (días)')
plt.ylabel('Frecuencia')
plt.title('Histograma del Tiempo Entre Mantenciones por Camión')

# Añadir frecuencia sobre cada barra
for p in ax.patches:
    ax.annotate(f'{int(p.get_height())}', 
                (p.get_x() + p.get_width() / 2, p.get_height()), 
                ha='center', va='bottom', fontsize=10)

# Ajustar los ticks del eje x
plt.xticks(bins, rotation=45)

# Mostrar el gráfico
plt.show()



