import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.stats import gaussian_kde


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
df_filtered['Time_Between_Failures'] = df_filtered['Time_Between_Failures'].dt.total_seconds() / 86400
df_filtered_0 = df_filtered[df_filtered['Failure_Mode'] == 0]
df_filtered_1 = df_filtered[df_filtered['Failure_Mode'] == 1]
df_filtered_2 = df_filtered[df_filtered['Failure_Mode'] == 2]
df_filtered_3 = df_filtered[df_filtered['Failure_Mode'] == 3]
df_filtered_4 = df_filtered[df_filtered['Failure_Mode'] == 4]
df_filtered_5 = df_filtered[df_filtered['Failure_Mode'] == 5]



plt.figure(figsize=(10, 6))

#sns.kdeplot(df_filtered_0['Time_Between_Failures'], bw_adjust=0.5, color='deepskyblue', fill=True, label='Manutención Programada')
#sns.kdeplot(df_filtered_1['Time_Between_Failures'], bw_adjust=0.5, color='crimson', fill=True, label='Desgaste Menor')
#sns.kdeplot(df_filtered_2['Time_Between_Failures'], bw_adjust=0.5, color='darkorange', fill=True, label='Fallo del Componente')
#sns.kdeplot(df_filtered_3['Time_Between_Failures'], bw_adjust=0.5, color='limegreen', fill=True, label='Fuga en el Sistema')
#sns.kdeplot(df_filtered_4['Time_Between_Failures'], bw_adjust=0.5, color='magenta', fill=True, label='Falla Operacional del Sistema')
#sns.kdeplot(df_filtered_5['Time_Between_Failures'], bw_adjust=0.5, color='gold', fill=True, label='Falla Crítica')


# Configurar el gráfico
plt.xlabel('Tiempo entre fallas/manutención (días)')
plt.ylabel('Densidad')
plt.title('Densidades de tiempo entre fallas/manutención')
plt.grid(True)
plt.legend(title='Failure Mode')
plt.show()