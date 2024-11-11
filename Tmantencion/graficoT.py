import pandas as pd
import matplotlib.pyplot as plt

# Cargar los datos desde los archivos CSV
archivo_temperatura = 'sensor_data.csv'
archivo_mantenciones = 'maintenance_data.csv'

datos_temperatura = pd.read_csv(archivo_temperatura)
datos_mantenciones = pd.read_csv(archivo_mantenciones)

# Asegurarse de que las columnas Date_Time y Start_Time estén en formato de fecha y hora
datos_temperatura['Date_Time'] = pd.to_datetime(datos_temperatura['Date_Time'], format='%m/%d/%Y %H:%M')
datos_mantenciones['Start_Time'] = pd.to_datetime(datos_mantenciones['Start_Time'], format='%m/%d/%Y %H:%M')

# Filtrar los datos por Machine_ID específico y año 2019
machine_id = 'AWOU5IMX'  # Cambia esto por el Machine_ID que desees analizar
datos_temperatura_filtrados = datos_temperatura[(datos_temperatura['Machine_ID'] == machine_id) & (datos_temperatura['Date_Time'].dt.year == 2023)]
datos_mantenciones_filtrados = datos_mantenciones[(datos_mantenciones['Machine_ID'] == machine_id) & (datos_mantenciones['Start_Time'].dt.year == 2023)]

# Definir colores para cada Failure_Mode
colores = {0: 'red', 1: 'blue', 2: 'green', 3: 'orange', 4: 'black', 5: 'yellow'}  # Añade más modos de fallo y colores según sea necesario

# Graficar la temperatura del motor a lo largo del tiempo
plt.figure(figsize=(10, 6))
plt.plot(datos_temperatura_filtrados['Date_Time'], datos_temperatura_filtrados['Engine_Temperature'], marker='o', linestyle='-')

# Añadir líneas verticales con diferentes colores según el Failure_Mode
for index, row in datos_mantenciones_filtrados.iterrows():
    color = colores.get(row['Failure_Mode'], 'black')  # Usa 'black' si el modo de fallo no está en la lista
    plt.axvline(x=row['Start_Time'], color=color, linestyle='--', label=f'Failure Mode {row["Failure_Mode"]}')

plt.title(f'Temperatura del Motor para Machine_ID {machine_id} en 2023')
plt.xlabel('Fecha y Hora')
plt.ylabel('Temperatura del Motor (°C)')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

