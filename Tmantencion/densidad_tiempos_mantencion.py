import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar los datos
maintenance_data = pd.read_csv("../maintenance_data.csv")

# Convertir las columnas de fecha a datetime
maintenance_data['Start_Time'] = pd.to_datetime(maintenance_data['Start_Time'])
maintenance_data['End_Time'] = pd.to_datetime(maintenance_data['End_Time'])

# Calcular la duración de cada mantenimiento en minutos
maintenance_data['Duration_Minutes'] = (maintenance_data['End_Time'] - maintenance_data['Start_Time']).dt.total_seconds() / 60

# Filtrar valores negativos
duration_data = maintenance_data['Duration_Minutes'][maintenance_data['Duration_Minutes'] >= 0]

# Opcional: Filtrar valores extremos
threshold = duration_data.quantile(0.99)  # Ajusta este valor si es necesario
filtered_data = duration_data[duration_data <= threshold]

# Crear el gráfico de densidad
plt.figure(figsize=(20, 15))
sns.kdeplot(filtered_data, fill=True, color='blue', alpha=0.6, bw_adjust=0.5)

# Calcular el valor de la mayor densidad
kde = sns.kdeplot(filtered_data, bw_adjust=0.5)
kde_values = kde.get_lines()[0].get_ydata()  # Obtener valores de densidad
x_values = kde.get_lines()[0].get_xdata()  # Obtener valores de x
max_density_index = kde_values.argmax()  # Índice del valor máximo de densidad
max_density_x = x_values[max_density_index]  # Valor de x correspondiente a la máxima densidad

# Agregar línea vertical
plt.axvline(x=max_density_x, color='red', linestyle='--', label=f'Máxima Densidad: {max_density_x:.2f} min')

# Configurar etiquetas y título
plt.xlabel('Duración del Mantenimiento (minutos)')
plt.ylabel('Densidad')
plt.title('Distribución de la Duración de Mantenimiento')
plt.xlim(left=0)  # Limitar el eje x a valores no negativos

# Ajustar los ticks del eje x
plt.xticks(ticks=range(0, int(filtered_data.max()) + 100, 100), rotation=90)  # Rotar labels del eje x

plt.grid()
plt.legend()  # Mostrar leyenda

# Mostrar el gráfico
plt.show()



