import pandas as pd

def mauro_qlo(machine_id, sistem):
    truck_operational_data = pd.read_csv("truck_operational_data.csv")
    maintenance_data = pd.read_csv("maintenance_data.csv")
    part_data = pd.read_csv("part_data.csv")

    truck_operational_data['Start'] = pd.to_datetime(truck_operational_data['Start'])
    truck_operational_data['End'] = pd.to_datetime(truck_operational_data['End'])
    maintenance_data['Start_Time'] = pd.to_datetime(maintenance_data['Start_Time'])
    maintenance_data['End_Time'] = pd.to_datetime(maintenance_data['End_Time'])


    maintenance_data = maintenance_data[maintenance_data["Machine_ID"]==machine_id]
    truck_operational_data = truck_operational_data[truck_operational_data["Machine_ID"]==machine_id]

    df_combined = pd.merge_asof(truck_operational_data.sort_values('End'), 
                                maintenance_data[['Machine_ID', 'Part_ID', 'Start_Time','End_Time', 'Failure_Mode']].sort_values('Start_Time'),
                                left_on='End', 
                                right_on='Start_Time', 
                                by='Machine_ID',
                                direction='forward')

    cont_tons = 0
    cont_kms = 0
    tons = []
    edad_camion = []
    tipo_de_falla = []
    kms = []
    inicio = True

    for machine in df_combined.itertuples(index=True):
        
        if inicio:
            inicio = False
            start = machine.Start
            end = machine.Start_Time

        if machine.Start < end:     
            cont_tons += float(machine.Tons_Loaded)
            cont_kms += float(machine.Distance_Traveled_km)

        elif not pd.isna(machine.Start_Time):

            pieza = part_data[(part_data['Machine_ID'] == machine.Machine_ID) & (part_data['Part_ID'] == machine.Part_ID)]
            if pieza.iloc[0]['Part_Type'] == sistem:
                edad_camion.append((end - start).total_seconds() / 3600)
                tons.append(cont_tons)
                kms.append(cont_kms)
                cont_kms = 0
                cont_kms += float(machine.Distance_Traveled_km)
                cont_tons = 0
                cont_tons += float(machine.Tons_Loaded)
                start = machine.Start
                end = machine.Start_Time
                if machine.Failure_Mode == 0.0:
                    tipo_de_falla.append(0)
                    continue
                tipo_de_falla.append(1)
            else:
                cont_tons += float(machine.Tons_Loaded)
                cont_kms += float(machine.Distance_Traveled_km)
                end = machine.Start_Time
        else:
            break

    df = pd.DataFrame({
        'Tons': tons,
        'Kms': kms,
        'Edad': edad_camion,
        'Sesgo': tipo_de_falla
    })

    return df

dfs = list()
machines = ["AWOU5IMX","6VABNMFW","7PML7DX0","WVSI44XE","12ZHA8WI","H4R6Y02Y","3A6STZAR","TS5TPP35","HLU6OU9B","OKU9UWCY","LYRHF3HX","JIRK0F5R"]
for machine in machines:
    df = mauro_qlo(machine,'Suspension System')
    if machine in ["AWOU5IMX","WVSI44XE","12ZHA8WI","H4R6Y02Y","3A6STZAR","HLU6OU9B","LYRHF3HX"]:
        df['Model'] = "A"
    else:
        df['Model'] = "B"
    df['ID'] = machine
    dfs.append(df)
    
df_final = pd.concat(dfs, ignore_index=True)
print(df_final)
input()

df_final.to_csv('Suspension System.csv', index=False)


"""

import pandas as pd

#AWO
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
                            maintenance_data[['Machine_ID', 'Start_Time','End_Time', 'Failure_Mode']].sort_values('Start_Time'),
                            left_on='End', 
                            right_on='Start_Time', 
                            by='Machine_ID',
                            direction='forward')

cont_tons = 0
cont_kms = 0
tons = []
edad_camion = []
tipo_de_falla = []
kms = []
falla = []
programada = []
inicio = 0

previous_tuple = False
for machine in df_combined.itertuples(index=True):
    if cont_tons == 0:
        machine_start = machine.Start_Time
    cont_tons += float(machine.Tons_Loaded)
    cont_kms += float(machine.Distance_Traveled_km)
    if machine.Start > machine_start:
        tons.append(cont_tons)
        cont_tons = 0
        kms.append(cont_kms)
        cont_kms = 0
        if machine.Failure_Mode == 0.0:
            tipo_de_falla.append(0)
            continue
        tipo_de_falla.append(1)
    
import pandas as pd

import pandas as pd

# Asegurarte de que las columnas 'End_Time' y 'Start_Time' están en formato datetime
import pandas as pd

# Asegurarte de que las columnas 'End_Time' y 'Start_Time' están en formato datetime
df_combined['End_Time'] = pd.to_datetime(df_combined['End_Time'])
df_combined['Start_Time'] = pd.to_datetime(df_combined['Start_Time'])

# Crear una columna para marcar dónde cambia el valor de 'End_Time'
df_combined['End_Time_Change'] = df_combined['End_Time'].ne(df_combined['End_Time'].shift())

# Inicializar la columna 'Time_Diff'
df_combined['Time_Diff'] = pd.NaT

# Asignar la diferencia de tiempo en la primera fila entre 'End_Time' y 'Start_Time'
df_combined.loc[0, 'Time_Diff'] = df_combined.loc[0, 'Start_Time'] - df_combined.loc[0, 'Start']

# Calcular la diferencia de tiempo para las filas restantes donde cambia 'End_Time'
df_combined.loc[1:, 'Time_Diff'] = df_combined['End_Time'].diff().where(df_combined['End_Time_Change'])

# Llenar los valores faltantes hacia abajo para mantener el tiempo transcurrido hasta el siguiente cambio
df_combined['Time_Diff'] = df_combined['Time_Diff'].ffill()


end_time_unique_list = df_combined['Time_Diff'].unique().tolist()

df_AWOU5IMX = pd.DataFrame({
    'Tons': tons,
    'Kms': kms,
    'Falla': tipo_de_falla,
    'Edad': end_time_unique_list
})

df_AWOU5IMX['Edad'] = df_AWOU5IMX['Edad'].dt.total_seconds() / 3600
df_AWOU5IMX['Modelo'] = 0
df_AWOU5IMX['ID'] = 'AWOU5IMX'

    
    
############################## 2

#WVS
# Cargar los datos
truck_operational_data = pd.read_csv("truck_operational_data.csv")
maintenance_data = pd.read_csv("maintenance_data.csv")

truck_operational_data['Start'] = pd.to_datetime(truck_operational_data['Start'])
truck_operational_data['End'] = pd.to_datetime(truck_operational_data['End'])
maintenance_data['Start_Time'] = pd.to_datetime(maintenance_data['Start_Time'])
maintenance_data['End_Time'] = pd.to_datetime(maintenance_data['End_Time'])

maintenance_data = maintenance_data[maintenance_data["Machine_ID"]=="WVSI44XE"]
truck_operational_data = truck_operational_data[truck_operational_data["Machine_ID"]=="WVSI44XE"]

df_combined = pd.merge_asof(truck_operational_data.sort_values('End'), 
                            maintenance_data[['Machine_ID', 'Start_Time','End_Time', 'Failure_Mode']].sort_values('Start_Time'),
                            left_on='End', 
                            right_on='Start_Time', 
                            by='Machine_ID',
                            direction='forward')

cont_tons = 0
cont_kms = 0
tons = []
edad_camion = []
tipo_de_falla = []
kms = []
falla = []
programada = []
inicio = 0

previous_tuple = False
for machine in df_combined.itertuples(index=True):
    if cont_tons == 0:
        machine_start = machine.Start_Time
    cont_tons += float(machine.Tons_Loaded)
    cont_kms += float(machine.Distance_Traveled_km)
    if machine.Start > machine_start:
        tons.append(cont_tons)
        cont_tons = 0
        kms.append(cont_kms)
        cont_kms = 0
        if machine.Failure_Mode == 0.0:
            tipo_de_falla.append(0)
            continue
        tipo_de_falla.append(1)

    
import pandas as pd

import pandas as pd

# Asegurarte de que las columnas 'End_Time' y 'Start_Time' están en formato datetime
import pandas as pd

# Asegurarte de que las columnas 'End_Time' y 'Start_Time' están en formato datetime
df_combined['End_Time'] = pd.to_datetime(df_combined['End_Time'])
df_combined['Start_Time'] = pd.to_datetime(df_combined['Start_Time'])

# Crear una columna para marcar dónde cambia el valor de 'End_Time'
df_combined['End_Time_Change'] = df_combined['End_Time'].ne(df_combined['End_Time'].shift())

# Inicializar la columna 'Time_Diff'
df_combined['Time_Diff'] = pd.NaT

# Asignar la diferencia de tiempo en la primera fila entre 'End_Time' y 'Start_Time'
df_combined.loc[0, 'Time_Diff'] = df_combined.loc[0, 'Start_Time'] - df_combined.loc[0, 'Start']

# Calcular la diferencia de tiempo para las filas restantes donde cambia 'End_Time'
df_combined.loc[1:, 'Time_Diff'] = df_combined['End_Time'].diff().where(df_combined['End_Time_Change'])

# Llenar los valores faltantes hacia abajo para mantener el tiempo transcurrido hasta el siguiente cambio
df_combined['Time_Diff'] = df_combined['Time_Diff'].ffill()

end_time_unique_list = df_combined['Time_Diff'].unique().tolist()

df_WVSI44XE = pd.DataFrame({
    'Tons': tons,
    'Kms': kms,
    'Falla': tipo_de_falla,
    'Edad': end_time_unique_list
})

df_WVSI44XE['Edad'] = df_WVSI44XE['Edad'].dt.total_seconds() / 3600
df_WVSI44XE['Modelo'] = 0
df_WVSI44XE['ID'] = 'WVSI44XE'


############################## 3

#12Z
# Cargar los datos
truck_operational_data = pd.read_csv("truck_operational_data.csv")
maintenance_data = pd.read_csv("maintenance_data.csv")

truck_operational_data['Start'] = pd.to_datetime(truck_operational_data['Start'])
truck_operational_data['End'] = pd.to_datetime(truck_operational_data['End'])
maintenance_data['Start_Time'] = pd.to_datetime(maintenance_data['Start_Time'])
maintenance_data['End_Time'] = pd.to_datetime(maintenance_data['End_Time'])

maintenance_data = maintenance_data[maintenance_data["Machine_ID"]=="12ZHA8WI"]
truck_operational_data = truck_operational_data[truck_operational_data["Machine_ID"]=="12ZHA8WI"]

df_combined = pd.merge_asof(truck_operational_data.sort_values('End'), 
                            maintenance_data[['Machine_ID', 'Start_Time','End_Time', 'Failure_Mode']].sort_values('Start_Time'),
                            left_on='End', 
                            right_on='Start_Time', 
                            by='Machine_ID',
                            direction='forward')

cont_tons = 0
cont_kms = 0
tons = []
edad_camion = []
tipo_de_falla = []
kms = []
falla = []
programada = []
inicio = 0

previous_tuple = False
for machine in df_combined.itertuples(index=True):
    if cont_tons == 0:
        machine_start = machine.Start_Time
    cont_tons += float(machine.Tons_Loaded)
    cont_kms += float(machine.Distance_Traveled_km)
    if machine.Start > machine_start:
        tons.append(cont_tons)
        cont_tons = 0
        kms.append(cont_kms)
        cont_kms = 0
        if machine.Failure_Mode == 0.0:
            tipo_de_falla.append(0)
            continue
        tipo_de_falla.append(1)


    
import pandas as pd

import pandas as pd

# Asegurarte de que las columnas 'End_Time' y 'Start_Time' están en formato datetime
import pandas as pd

# Asegurarte de que las columnas 'End_Time' y 'Start_Time' están en formato datetime
df_combined['End_Time'] = pd.to_datetime(df_combined['End_Time'])
df_combined['Start_Time'] = pd.to_datetime(df_combined['Start_Time'])

# Crear una columna para marcar dónde cambia el valor de 'End_Time'
df_combined['End_Time_Change'] = df_combined['End_Time'].ne(df_combined['End_Time'].shift())

# Inicializar la columna 'Time_Diff'
df_combined['Time_Diff'] = pd.NaT

# Asignar la diferencia de tiempo en la primera fila entre 'End_Time' y 'Start_Time'
df_combined.loc[0, 'Time_Diff'] = df_combined.loc[0, 'Start_Time'] - df_combined.loc[0, 'Start']

# Calcular la diferencia de tiempo para las filas restantes donde cambia 'End_Time'
df_combined.loc[1:, 'Time_Diff'] = df_combined['End_Time'].diff().where(df_combined['End_Time_Change'])

# Llenar los valores faltantes hacia abajo para mantener el tiempo transcurrido hasta el siguiente cambio
df_combined['Time_Diff'] = df_combined['Time_Diff'].ffill()

end_time_unique_list = df_combined['Time_Diff'].unique().tolist()[0:-1]



df_12ZHA8WI = pd.DataFrame({
    'Tons': tons,
    'Kms': kms,
    'Falla': tipo_de_falla,
    'Edad': end_time_unique_list
})

df_12ZHA8WI['Edad'] = df_12ZHA8WI['Edad'].dt.total_seconds() / 3600
df_12ZHA8WI['Modelo'] = 0
df_12ZHA8WI['ID'] = '12ZHA8WI'

############################## 4

#H4R
# Cargar los datos
truck_operational_data = pd.read_csv("truck_operational_data.csv")
maintenance_data = pd.read_csv("maintenance_data.csv")

truck_operational_data['Start'] = pd.to_datetime(truck_operational_data['Start'])
truck_operational_data['End'] = pd.to_datetime(truck_operational_data['End'])
maintenance_data['Start_Time'] = pd.to_datetime(maintenance_data['Start_Time'])
maintenance_data['End_Time'] = pd.to_datetime(maintenance_data['End_Time'])

maintenance_data = maintenance_data[maintenance_data["Machine_ID"]=="H4R6Y02Y"]
truck_operational_data = truck_operational_data[truck_operational_data["Machine_ID"]=="H4R6Y02Y"]

df_combined = pd.merge_asof(truck_operational_data.sort_values('End'), 
                            maintenance_data[['Machine_ID', 'Start_Time','End_Time', 'Failure_Mode']].sort_values('Start_Time'),
                            left_on='End', 
                            right_on='Start_Time', 
                            by='Machine_ID',
                            direction='forward')

cont_tons = 0
cont_kms = 0
tons = []
edad_camion = []
tipo_de_falla = []
kms = []
falla = []
programada = []
inicio = 0

previous_tuple = False
for machine in df_combined.itertuples(index=True):
    if cont_tons == 0:
        machine_start = machine.Start_Time
    cont_tons += float(machine.Tons_Loaded)
    cont_kms += float(machine.Distance_Traveled_km)
    if machine.Start > machine_start:
        tons.append(cont_tons)
        cont_tons = 0
        kms.append(cont_kms)
        cont_kms = 0
        if machine.Failure_Mode == 0.0:
            tipo_de_falla.append(0)
            continue
        tipo_de_falla.append(1)


    
import pandas as pd

import pandas as pd

# Asegurarte de que las columnas 'End_Time' y 'Start_Time' están en formato datetime
import pandas as pd

# Asegurarte de que las columnas 'End_Time' y 'Start_Time' están en formato datetime
df_combined['End_Time'] = pd.to_datetime(df_combined['End_Time'])
df_combined['Start_Time'] = pd.to_datetime(df_combined['Start_Time'])

# Crear una columna para marcar dónde cambia el valor de 'End_Time'
df_combined['End_Time_Change'] = df_combined['End_Time'].ne(df_combined['End_Time'].shift())

# Inicializar la columna 'Time_Diff'
df_combined['Time_Diff'] = pd.NaT

# Asignar la diferencia de tiempo en la primera fila entre 'End_Time' y 'Start_Time'
df_combined.loc[0, 'Time_Diff'] = df_combined.loc[0, 'Start_Time'] - df_combined.loc[0, 'Start']

# Calcular la diferencia de tiempo para las filas restantes donde cambia 'End_Time'
df_combined.loc[1:, 'Time_Diff'] = df_combined['End_Time'].diff().where(df_combined['End_Time_Change'])

# Llenar los valores faltantes hacia abajo para mantener el tiempo transcurrido hasta el siguiente cambio
df_combined['Time_Diff'] = df_combined['Time_Diff'].ffill()

end_time_unique_list = df_combined['Time_Diff'].unique().tolist()



df_H4R6Y02Y = pd.DataFrame({
    'Tons': tons,
    'Kms': kms,
    'Falla': tipo_de_falla,
    'Edad': end_time_unique_list
})

df_H4R6Y02Y['Edad'] = df_H4R6Y02Y['Edad'].dt.total_seconds() / 3600
df_H4R6Y02Y['Modelo'] = 0
df_H4R6Y02Y['ID'] = 'H4R6Y02Y'
    
    
############################## 5

#3A6
# Cargar los datos
truck_operational_data = pd.read_csv("truck_operational_data.csv")
maintenance_data = pd.read_csv("maintenance_data.csv")

truck_operational_data['Start'] = pd.to_datetime(truck_operational_data['Start'])
truck_operational_data['End'] = pd.to_datetime(truck_operational_data['End'])
maintenance_data['Start_Time'] = pd.to_datetime(maintenance_data['Start_Time'])
maintenance_data['End_Time'] = pd.to_datetime(maintenance_data['End_Time'])

maintenance_data = maintenance_data[maintenance_data["Machine_ID"]=="3A6STZAR"]
truck_operational_data = truck_operational_data[truck_operational_data["Machine_ID"]=="3A6STZAR"]

df_combined = pd.merge_asof(truck_operational_data.sort_values('End'), 
                            maintenance_data[['Machine_ID', 'Start_Time','End_Time', 'Failure_Mode']].sort_values('Start_Time'),
                            left_on='End', 
                            right_on='Start_Time', 
                            by='Machine_ID',
                            direction='forward')

cont_tons = 0
cont_kms = 0
tons = []
edad_camion = []
tipo_de_falla = []
kms = []
falla = []
programada = []
inicio = 0

previous_tuple = False
for machine in df_combined.itertuples(index=True):
    if cont_tons == 0:
        machine_start = machine.Start_Time
    cont_tons += float(machine.Tons_Loaded)
    cont_kms += float(machine.Distance_Traveled_km)
    if machine.Start > machine_start:
        tons.append(cont_tons)
        cont_tons = 0
        kms.append(cont_kms)
        cont_kms = 0
        if machine.Failure_Mode == 0.0:
            tipo_de_falla.append(0)
            continue
        tipo_de_falla.append(1)


import pandas as pd

import pandas as pd

# Asegurarte de que las columnas 'End_Time' y 'Start_Time' están en formato datetime
import pandas as pd

# Asegurarte de que las columnas 'End_Time' y 'Start_Time' están en formato datetime
df_combined['End_Time'] = pd.to_datetime(df_combined['End_Time'])
df_combined['Start_Time'] = pd.to_datetime(df_combined['Start_Time'])

# Crear una columna para marcar dónde cambia el valor de 'End_Time'
df_combined['End_Time_Change'] = df_combined['End_Time'].ne(df_combined['End_Time'].shift())

# Inicializar la columna 'Time_Diff'
df_combined['Time_Diff'] = pd.NaT

# Asignar la diferencia de tiempo en la primera fila entre 'End_Time' y 'Start_Time'
df_combined.loc[0, 'Time_Diff'] = df_combined.loc[0, 'Start_Time'] - df_combined.loc[0, 'Start']

# Calcular la diferencia de tiempo para las filas restantes donde cambia 'End_Time'
df_combined.loc[1:, 'Time_Diff'] = df_combined['End_Time'].diff().where(df_combined['End_Time_Change'])

# Llenar los valores faltantes hacia abajo para mantener el tiempo transcurrido hasta el siguiente cambio
df_combined['Time_Diff'] = df_combined['Time_Diff'].ffill()

end_time_unique_list = df_combined['Time_Diff'].unique().tolist()

df_3A6STZAR = pd.DataFrame({
    'Tons': tons[0:-1],
    'Kms': kms[0:-1],
    'Falla': tipo_de_falla[0:-1],
    'Edad': end_time_unique_list
})

df_3A6STZAR['Edad'] = df_3A6STZAR['Edad'].dt.total_seconds() / 3600
df_3A6STZAR['Modelo'] = 0
df_3A6STZAR['ID'] = '3A6STZAR'


############################## 6

#HLU
# Cargar los datos
truck_operational_data = pd.read_csv("truck_operational_data.csv")
maintenance_data = pd.read_csv("maintenance_data.csv")

truck_operational_data['Start'] = pd.to_datetime(truck_operational_data['Start'])
truck_operational_data['End'] = pd.to_datetime(truck_operational_data['End'])
maintenance_data['Start_Time'] = pd.to_datetime(maintenance_data['Start_Time'])
maintenance_data['End_Time'] = pd.to_datetime(maintenance_data['End_Time'])

maintenance_data = maintenance_data[maintenance_data["Machine_ID"]=="HLU6OU9B"]
truck_operational_data = truck_operational_data[truck_operational_data["Machine_ID"]=="HLU6OU9B"]

df_combined = pd.merge_asof(truck_operational_data.sort_values('End'), 
                            maintenance_data[['Machine_ID', 'Start_Time','End_Time', 'Failure_Mode']].sort_values('Start_Time'),
                            left_on='End', 
                            right_on='Start_Time', 
                            by='Machine_ID',
                            direction='forward')

cont_tons = 0
cont_kms = 0
tons = []
edad_camion = []
tipo_de_falla = []
kms = []
falla = []
programada = []
inicio = 0

previous_tuple = False
for machine in df_combined.itertuples(index=True):
    if cont_tons == 0:
        machine_start = machine.Start_Time
    cont_tons += float(machine.Tons_Loaded)
    cont_kms += float(machine.Distance_Traveled_km)
    if machine.Start > machine_start:
        tons.append(cont_tons)
        cont_tons = 0
        kms.append(cont_kms)
        cont_kms = 0
        if machine.Failure_Mode == 0.0:
            tipo_de_falla.append(0)
            continue
        tipo_de_falla.append(1)


import pandas as pd

import pandas as pd

# Asegurarte de que las columnas 'End_Time' y 'Start_Time' están en formato datetime
import pandas as pd

# Asegurarte de que las columnas 'End_Time' y 'Start_Time' están en formato datetime
df_combined['End_Time'] = pd.to_datetime(df_combined['End_Time'])
df_combined['Start_Time'] = pd.to_datetime(df_combined['Start_Time'])

# Crear una columna para marcar dónde cambia el valor de 'End_Time'
df_combined['End_Time_Change'] = df_combined['End_Time'].ne(df_combined['End_Time'].shift())

# Inicializar la columna 'Time_Diff'
df_combined['Time_Diff'] = pd.NaT

# Asignar la diferencia de tiempo en la primera fila entre 'End_Time' y 'Start_Time'
df_combined.loc[0, 'Time_Diff'] = df_combined.loc[0, 'Start_Time'] - df_combined.loc[0, 'Start']

# Calcular la diferencia de tiempo para las filas restantes donde cambia 'End_Time'
df_combined.loc[1:, 'Time_Diff'] = df_combined['End_Time'].diff().where(df_combined['End_Time_Change'])

# Llenar los valores faltantes hacia abajo para mantener el tiempo transcurrido hasta el siguiente cambio
df_combined['Time_Diff'] = df_combined['Time_Diff'].ffill()

end_time_unique_list = df_combined['Time_Diff'].unique().tolist()[0:-1]


df_HLU6OU9B = pd.DataFrame({
    'Tons': tons,
    'Kms': kms,
    'Falla': tipo_de_falla,
    'Edad': end_time_unique_list
})

df_HLU6OU9B['Edad'] = df_HLU6OU9B['Edad'].dt.total_seconds() / 3600
df_HLU6OU9B['Modelo'] = 0
df_HLU6OU9B['ID'] = 'HLU6OU9B'
    
############################## 7

#LYR
# Cargar los datos
truck_operational_data = pd.read_csv("truck_operational_data.csv")
maintenance_data = pd.read_csv("maintenance_data.csv")

truck_operational_data['Start'] = pd.to_datetime(truck_operational_data['Start'])
truck_operational_data['End'] = pd.to_datetime(truck_operational_data['End'])
maintenance_data['Start_Time'] = pd.to_datetime(maintenance_data['Start_Time'])
maintenance_data['End_Time'] = pd.to_datetime(maintenance_data['End_Time'])

maintenance_data = maintenance_data[maintenance_data["Machine_ID"]=="LYRHF3HX"]
truck_operational_data = truck_operational_data[truck_operational_data["Machine_ID"]=="LYRHF3HX"]

df_combined = pd.merge_asof(truck_operational_data.sort_values('End'), 
                            maintenance_data[['Machine_ID', 'Start_Time','End_Time', 'Failure_Mode']].sort_values('Start_Time'),
                            left_on='End', 
                            right_on='Start_Time', 
                            by='Machine_ID',
                            direction='forward')

cont_tons = 0
cont_kms = 0
tons = []
edad_camion = []
tipo_de_falla = []
kms = []
falla = []
programada = []
inicio = 0

previous_tuple = False
for machine in df_combined.itertuples(index=True):
    if cont_tons == 0:
        machine_start = machine.Start_Time
    cont_tons += float(machine.Tons_Loaded)
    cont_kms += float(machine.Distance_Traveled_km)
    if machine.Start > machine_start:
        tons.append(cont_tons)
        cont_tons = 0
        kms.append(cont_kms)
        cont_kms = 0
        if machine.Failure_Mode == 0.0:
            tipo_de_falla.append(0)
            continue
        tipo_de_falla.append(1)


import pandas as pd

import pandas as pd

# Asegurarte de que las columnas 'End_Time' y 'Start_Time' están en formato datetime
import pandas as pd

# Asegurarte de que las columnas 'End_Time' y 'Start_Time' están en formato datetime
df_combined['End_Time'] = pd.to_datetime(df_combined['End_Time'])
df_combined['Start_Time'] = pd.to_datetime(df_combined['Start_Time'])

# Crear una columna para marcar dónde cambia el valor de 'End_Time'
df_combined['End_Time_Change'] = df_combined['End_Time'].ne(df_combined['End_Time'].shift())

# Inicializar la columna 'Time_Diff'
df_combined['Time_Diff'] = pd.NaT

# Asignar la diferencia de tiempo en la primera fila entre 'End_Time' y 'Start_Time'
df_combined.loc[0, 'Time_Diff'] = df_combined.loc[0, 'Start_Time'] - df_combined.loc[0, 'Start']

# Calcular la diferencia de tiempo para las filas restantes donde cambia 'End_Time'
df_combined.loc[1:, 'Time_Diff'] = df_combined['End_Time'].diff().where(df_combined['End_Time_Change'])

# Llenar los valores faltantes hacia abajo para mantener el tiempo transcurrido hasta el siguiente cambio
df_combined['Time_Diff'] = df_combined['Time_Diff'].ffill()

end_time_unique_list = df_combined['Time_Diff'].unique().tolist()


df_LYRHF3HX = pd.DataFrame({
    'Tons': tons,
    'Kms': kms,
    'Falla': tipo_de_falla,
    'Edad': end_time_unique_list
})

df_LYRHF3HX['Edad'] = df_LYRHF3HX['Edad'].dt.total_seconds() / 3600
df_LYRHF3HX['Modelo'] = 0
df_LYRHF3HX['ID'] = 'LYRHF3HX'

df_mauro = pd.concat([df_AWOU5IMX, df_WVSI44XE, df_12ZHA8WI, df_H4R6Y02Y, df_3A6STZAR, df_HLU6OU9B, df_LYRHF3HX], ignore_index=True)

df_mauro.to_csv('df_modelo_A_csv.csv', index=False)
    
"""
    
    
    
    
    
    
    
    
    
    
    
    
    
    
