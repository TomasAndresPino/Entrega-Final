import pandas as pd

# Cargar el CSV
df = pd.read_csv('maintenance_data.csv')

# Convertir Start_Time y End_Time a formato datetime
df['Start_Time'] = pd.to_datetime(df['Start_Time'])
df['End_Time'] = pd.to_datetime(df['End_Time'])

# Calcular la duración en minutos
df['Duration'] = (df['End_Time'] - df['Start_Time']).dt.total_seconds() / 60

# Agrupar por Failure_Mode y calcular el promedio
promedios = df.groupby('Failure_Mode')['Duration'].mean().reset_index()

# Renombrar la columna de duración para mayor claridad
promedios.columns = ['Failure_Mode', 'Average_Duration']

print(promedios)
