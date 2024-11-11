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

# Definir los intervalos de 150 minutos
bins = range(0, int(maintenance_data['Duration_Minutes'].max()) + 150, 150)

# Crear el gráfico de distribución (histograma)
plt.figure(figsize=(10, 6))
counts, bins, patches = plt.hist(maintenance_data['Duration_Minutes'], bins=bins, alpha=0.7, color='blue', edgecolor='black')

# Añadir etiquetas con el intervalo en cada barra
for count, x in zip(counts, bins):
    plt.text(x + 75, count, f'{count:.0f}', ha='center', va='bottom')  # Etiqueta en el centro del intervalo

# Configurar etiquetas y título
plt.xlabel('Duración del Mantenimiento (minutos)')
plt.ylabel('Frecuencia')
plt.title('Distribución de la Duración de Mantenimiento')
plt.grid(axis='y')

# Personalizar los ticks del eje X para mostrar los intervalos
plt.xticks(bins, rotation=45)

# Mostrar el gráfico
plt.show()

