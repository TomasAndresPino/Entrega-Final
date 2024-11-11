import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# Cargar los datos
truck_operational_data = pd.read_csv("truck_operational_data.csv")
maintenance_data = pd.read_csv("maintenance_data.csv")

truck_operational_data['Start'] = pd.to_datetime(truck_operational_data['Start'])
truck_operational_data['End'] = pd.to_datetime(truck_operational_data['End'])
maintenance_data['Start_Time'] = pd.to_datetime(maintenance_data['Start_Time'])
maintenance_data['End_Time'] = pd.to_datetime(maintenance_data['End_Time'])

maintenance_data = maintenance_data[maintenance_data["Machine_ID"]=="AWOU5IMX"]
truck_operational_data = truck_operational_data[truck_operational_data["Machine_ID"]=="AWOU5IMX"]

df_combined = pd.merge_asof(truck_operational_data.sort_values('End'), 
                            maintenance_data[['Machine_ID', 'Start_Time', 'Failure_Mode']].sort_values('Start_Time'),
                            left_on='End', 
                            right_on='Start_Time', 
                            by='Machine_ID',
                            direction='forward')

df_combined = df_combined[df_combined['Start_Time'].dt.year < 2023]
df_combined = df_combined[df_combined['Start_Time'].dt.year >= 2020]


fechas = pd.date_range(start='2020-01-01', end='2022-12-31', periods=3542)
cont=0
tons = []
tons2 = []
falla = []
programada = []
for machine in df_combined.itertuples(index=True):
    if cont == 0:
        machine_start = machine.Start_Time
    cont += float(machine.Distance_Traveled_km)
    tons.append(cont)
    if machine.Start > machine_start:
        tons2.append(cont)
        cont = 0
        
        print(machine.Failure_Mode)
        if machine.Failure_Mode == 0.0:
            programada.append(machine_start)
            continue
        falla.append(machine_start)

print(tons2)
falla = pd.Series(falla)
programada = pd.Series(programada)

if falla.isnull().any() or programada.isnull().any():
    print("Algunos eventos contienen valores no válidos (NaT).")
    programada = programada.dropna()
    falla = falla.dropna()

fig, ax = plt.subplots(figsize=(12, 8))

# Plotear la línea de tiempo
ax.plot(fechas, tons, label='Valores', color='darkgreen', linestyle='-', linewidth=2)

"""
# Agregar líneas rojas para la primera lista de datetimes
for fecha in falla:
    ax.axvline(x=fecha, color='red', linestyle='--', label='Evento Rojo')
"""
# Agregar líneas azules para la segunda lista de datetimes
for fecha in programada:
    ax.axvline(x=fecha, color='blue', linestyle='--', label='Manutención Programada')


# Mejorar la visualización del eje x
ax.xaxis.set_major_locator(mdates.MonthLocator())  # Colocar un tick por año
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.xticks(rotation=45)

# Evitar duplicados en la leyenda
handles, labels = ax.get_legend_handles_labels()
by_label = dict(zip(labels, handles))
ax.legend(by_label.values(), by_label.keys())

# Título y etiquetas
plt.title('AWOU5IMX')
plt.xlabel('Fecha')
plt.ylabel('Toneladas Acumuladas hasta Falla')

# Mostrar el gráfico
plt.tight_layout()
plt.show()
