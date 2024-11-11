import pandas as pd
import matplotlib.pyplot as plt

# Cargar los datos
maintenance_data = pd.read_csv('../maintenance_data.csv')
truck_data = pd.read_csv('../truck_data.csv')

# Filtrar las mantenciones de tipo 0
maintenance_type_0 = maintenance_data[maintenance_data['Failure_Mode'] == 0]

# Unir los datos de mantenimiento con los datos de los camiones
merged_data = pd.merge(maintenance_type_0, truck_data, on='Machine_ID')

# Contar las mantenciones de tipo 0 por modelo de camión
counts = merged_data['Model'].value_counts()

# Crear el gráfico
plt.figure(figsize=(9.6, 5.4), dpi=200)  # Tamaño interno del gráfico ajustado
counts.plot(kind='bar', color=['blue', 'green'])  # Modelo A: azul, Modelo B: verde
plt.title('Cantidad de Mantenciones de Tipo 0 por Modelo de Camión', fontsize=16)  # Título más grande
plt.xlabel('Modelo de Camión', fontsize=14)  # Eje X más grande
plt.ylabel('Cantidad de Mantenciones', fontsize=14)  # Eje Y más grande
plt.xticks(rotation=0, fontsize=12)  # Etiquetas del eje X más grandes
plt.grid(axis='y')

# Guardar el gráfico
plt.tight_layout()
plt.savefig('AAAA.png', dpi=100)  # dpi = 100 para obtener 1920 x 1080 px


