import pandas as pd
import numpy as np



truck_operational_data = pd.read_csv("truck_operational_data.csv")
maintenance_data = pd.read_csv("maintenance_data.csv")
part_data = pd.read_csv("part_data.csv")


truck_operational_data['Start'] = pd.to_datetime(truck_operational_data['Start'])
truck_operational_data['End'] = pd.to_datetime(truck_operational_data['End'])
maintenance_data['Start_Time'] = pd.to_datetime(maintenance_data['Start_Time'])
maintenance_data['End_Time'] = pd.to_datetime(maintenance_data['End_Time'])


maintenance_data = maintenance_data[maintenance_data["Machine_ID"]=="AWOU5IMX"]
truck_operational_data = truck_operational_data[truck_operational_data["Machine_ID"]=="AWOU5IMX"]

df_combined = pd.merge_asof(truck_operational_data.sort_values('End'), 
                            maintenance_data[['Machine_ID', 'Part_ID', 'Start_Time','End_Time', 'Failure_Mode']].sort_values('Start_Time'),
                            left_on='End', 
                            right_on='Start_Time', 
                            by='Machine_ID',
                            direction='forward')

cont_tons = 0
cont_kms = 0
cont_horas = 0 
tons = []
edad_camion = []
tipo_de_falla = []
kms = []
inicio = True
falla = list()
horas_inicio = list()
horas_termino = list()

for machine in df_combined.itertuples(index=True):

    
    if inicio:
        inicio = False
        start = machine.Start
        end = machine.Start_Time

    if machine.Start < end:    
        horas_inicio.append(cont_horas)
        cont_horas += (machine.End - machine.Start).total_seconds() / 3600
        horas_termino.append(cont_horas)
        cont_tons += float(machine.Tons_Loaded)
        cont_kms += float(machine.Distance_Traveled_km)  
        tons.append(cont_tons)
        kms.append(cont_kms)  
        edad_camion.append((machine.Start - start).total_seconds() / 3600)
        falla.append(0)
        tipo_de_falla.append(np.nan)

        


    elif not pd.isna(machine.Start_Time):


        pieza = part_data[(part_data['Machine_ID'] == machine.Machine_ID) & (part_data['Part_ID'] == machine.Part_ID)]
        
        if pieza.iloc[0]['Part_Type'] == 'Engine':
            cont_kms += float(machine.Distance_Traveled_km)
            cont_tons += float(machine.Tons_Loaded)
            print("a")
            edad_camion.append((end - start).total_seconds() / 3600)
            tons.append(cont_tons)
            kms.append(cont_kms)
            horas_inicio.append(cont_horas)
            cont_horas += (machine.End - machine.Start).total_seconds() / 3600
            horas_termino.append(cont_horas)
            cont_horas = 0
            cont_kms = 0
            cont_tons = 0
            start = machine.Start
            end = machine.Start_Time
            
            if machine.Failure_Mode == 0.0:
                falla.append(0)
                tipo_de_falla.append(0)
                continue
            tipo_de_falla.append(machine.Failure_Mode)
            falla.append(1)
        else:
            cont_tons += float(machine.Tons_Loaded)
            cont_kms += float(machine.Distance_Traveled_km)
            end = machine.Start_Time
    else:
        break

df1 = pd.DataFrame({
    'Tons': tons,
    'Kms': kms,
    'Edad': edad_camion,
    'Inicio': horas_inicio,
    'Termino': horas_termino,
    'Falla': falla,
    'Sesgo': tipo_de_falla
})



import pandas as pd
import numpy as np



truck_operational_data = pd.read_csv("truck_operational_data.csv")
maintenance_data = pd.read_csv("maintenance_data.csv")
part_data = pd.read_csv("part_data.csv")

truck_operational_data['Start'] = pd.to_datetime(truck_operational_data['Start'])
truck_operational_data['End'] = pd.to_datetime(truck_operational_data['End'])
maintenance_data['Start_Time'] = pd.to_datetime(maintenance_data['Start_Time'])
maintenance_data['End_Time'] = pd.to_datetime(maintenance_data['End_Time'])


maintenance_data = maintenance_data[maintenance_data["Machine_ID"]=="WVSI44XE"]
truck_operational_data = truck_operational_data[truck_operational_data["Machine_ID"]=="WVSI44XE"]

df_combined = pd.merge_asof(truck_operational_data.sort_values('End'), 
                            maintenance_data[['Machine_ID', 'Part_ID', 'Start_Time','End_Time', 'Failure_Mode']].sort_values('Start_Time'),
                            left_on='End', 
                            right_on='Start_Time', 
                            by='Machine_ID',
                            direction='forward')

cont_tons = 0
cont_kms = 0
cont_horas = 0 
tons = []
edad_camion = []
tipo_de_falla = []
kms = []
inicio = True
falla = list()
horas_inicio = list()
horas_termino = list()

for machine in df_combined.itertuples(index=True):
    
    if inicio:
        inicio = False
        start = machine.Start
        end = machine.Start_Time

    if machine.Start < end:    
        horas_inicio.append(cont_horas)
        cont_horas += (machine.End - machine.Start).total_seconds() / 3600
        horas_termino.append(cont_horas)
        cont_tons += float(machine.Tons_Loaded)
        cont_kms += float(machine.Distance_Traveled_km)  
        tons.append(cont_tons)
        kms.append(cont_kms)  
        edad_camion.append((machine.Start - start).total_seconds() / 3600)
        falla.append(0)
        tipo_de_falla.append(np.nan)

    elif not pd.isna(machine.Start_Time):


        pieza = part_data[(part_data['Machine_ID'] == machine.Machine_ID) & (part_data['Part_ID'] == machine.Part_ID)]
        
        if pieza.iloc[0]['Part_Type'] == 'Engine':
            cont_kms += float(machine.Distance_Traveled_km)
            cont_tons += float(machine.Tons_Loaded)
            print("a")
            edad_camion.append((end - start).total_seconds() / 3600)
            tons.append(cont_tons)
            kms.append(cont_kms)
            horas_inicio.append(cont_horas)
            cont_horas += (machine.End - machine.Start).total_seconds() / 3600
            horas_termino.append(cont_horas)
            cont_horas = 0
            cont_kms = 0
            cont_tons = 0
            start = machine.Start
            end = machine.Start_Time
            
            if machine.Failure_Mode == 0.0:
                falla.append(0)
                tipo_de_falla.append(0)
                continue
            tipo_de_falla.append(machine.Failure_Mode)
            falla.append(1)
        else:
            cont_tons += float(machine.Tons_Loaded)
            cont_kms += float(machine.Distance_Traveled_km)
            end = machine.Start_Time
    else:
        break

df2 = pd.DataFrame({
    'Tons': tons,
    'Kms': kms,
    'Edad': edad_camion,
    'Inicio': horas_inicio,
    'Termino': horas_termino,
    'Falla': falla,
    'Sesgo': tipo_de_falla
})

df1['ID'] = "AWOU5IMX"
df2['ID'] = "WVSI44XE"

dfs = [df1,df2]

df = pd.concat(dfs, ignore_index=True)
print(df)

df.to_csv('Engine AWOU y WVSI.csv', index=False)