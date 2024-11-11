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
df = df.sort_values(by=['Machine_ID', 'Start_Time'])

df['Duration'] = df['End_Time'] - df['Start_Time']
df['Duration'] = df['Duration'].dt.total_seconds() / 3600
df = df[df['Duration'] >= 0]

df_filtered_0 = df[df['Failure_Mode'] == 0]
df_filtered_1 = df[df['Failure_Mode'] == 1]
df_filtered_2 = df[df['Failure_Mode'] == 2]
df_filtered_3 = df[df['Failure_Mode'] == 3]
df_filtered_4 = df[df['Failure_Mode'] == 4]
df_filtered_5 = df[df['Failure_Mode'] == 5]




plt.figure(figsize=(10, 6))

#sns.kdeplot(df_filtered_0['Duration'], color='deepskyblue', fill=True, label='Manutención Programada')
#sns.kdeplot(df_filtered_1['Duration'], color='crimson', fill=True, label='Desgaste Menor')
#sns.kdeplot(df_filtered_2['Duration'], color='darkorange', fill=True, label='Fallo del Componente')
#sns.kdeplot(df_filtered_3['Duration'], color='limegreen', fill=True, label='Fuga en el Sistema')
#sns.kdeplot(df_filtered_4['Duration'], color='magenta', fill=True, label='Falla Operacional del Sistema')
#sns.kdeplot(df_filtered_5['Duration'], color='gold', fill=True, label='Falla Crítica')

# Configurar el gráfico
plt.xlabel('Tiempo entre fallas (horas)')
plt.ylabel('Densidad')
plt.title('Densidades de tiempo entre fallas')
plt.grid(True)
plt.legend(title='Failure Mode')
plt.show()

