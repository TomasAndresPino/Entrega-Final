import pandas as pd
import matplotlib.pyplot as plt

# Leer el archivo CSV
df = pd.read_csv('sensor_data.csv')

# Convertir la columna 'Date_Time' a tipo datetime
df['Date_Time'] = pd.to_datetime(df['Date_Time'], format='%m/%d/%Y %H:%M')
df = df.dropna(subset=['Engine_Temperature'])
df = df[(df['Date_Time'].dt.year == 2021) & (df['Date_Time'].dt.month.isin([5, 6, 7, 8]))]
#df = df[(df['Engine_Temperature'] >= 20) & (df['Engine_Temperature'] <= 1000)]
df_filtered = df[df['Machine_ID'] == 'AWOU5IMX']
df_filtered = df_filtered.sort_values(by=['Date_Time'])
df = df_filtered

# Configurar el índice del DataFrame como la fecha y hora
df.set_index('Date_Time', inplace=True)


df_maint = pd.read_csv('maintenance_data.csv')
df_maint['Start_Time'] = pd.to_datetime(df_maint['Start_Time'], format='%m/%d/%Y %H:%M')
df_maint = df_maint[(df_maint['Start_Time'].dt.year == 2021) & (df_maint['Start_Time'].dt.month.isin([5, 6, 7, 8]))]
df_maint = df_maint[df_maint['Machine_ID'] == 'AWOU5IMX']
df_maint = df_maint[(df_maint['Failure_Mode'] == 5)]

plt.figure(figsize=(12, 6))
plt.plot(df.index, df['Engine_Temperature'], marker='o', linestyle='-', color='b')

for maint_time in df_maint['Start_Time']:
    plt.axvline(x=maint_time, color='r', linestyle='-', linewidth=0.5, label='Mantenimiento')

# Graficar la temperatura


plt.title('Temperatura a lo Largo del Tiempo')
plt.xlabel('Fecha y Hora')
plt.ylabel('Temperatura')
plt.xticks(rotation=45)
plt.tight_layout()

# Mostrar el gráfico
plt.show()
