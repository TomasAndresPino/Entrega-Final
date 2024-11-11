import pandas as pd
import matplotlib.pyplot as plt

# Leer el archivo CSV
df = pd.read_csv('maintenance_data.csv')

# Convertir las columnas de tiempo a formato datetime con el formato M/D/A
df['Start_Time'] = pd.to_datetime(df['Start_Time'], format='%m/%d/%Y %H:%M')
df['End_Time'] = pd.to_datetime(df['End_Time'], format='%m/%d/%Y %H:%M')

# Filtrar los datos solo para el camión AWOU5IMX y Failure_Mode 5
df_filtered = df[(df['Failure_Mode'] == 5) & (df['Machine_ID'] == 'AWOU5IMX')]

# Calcular la duración de las mantenciones en horas
df_filtered['Duration'] = (df_filtered['End_Time'] - df_filtered['Start_Time']).dt.total_seconds() / 3600

# Crear el histograma relativo (normalizado) con bins de 0.5
plt.hist(df_filtered['Duration'], bins=int((df_filtered['Duration'].max() - df_filtered['Duration'].min()) / 0.5), 
         edgecolor='black', density=True)

# Configurar etiquetas y título del gráfico
plt.xlabel('Duración de las Mantenciones (horas)')
plt.ylabel('Proporción')
plt.title('Histograma Relativo de Duración de Mantenciones para Failure Mode 5')

# Mostrar el gráfico
plt.show()