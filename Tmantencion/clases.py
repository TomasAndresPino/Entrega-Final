from collections import namedtuple

Meses = {'1': 31, '2': 28, '3': 31, '4': 30, '5': 31, '6': 30, '7': 31, '8': 31, '9': 30, '10': 31, '11': 30, '12': 31}
Mantencion = namedtuple('Mantencion',['Machine_ID','Part_ID','Start_Time', 'End_Time', 'Failure_Mode'])
Rango = namedtuple('Rango', ['Inicio_Final', 'Frecuencia_Relativa'])
Parte = namedtuple('Parte', ['Machine_ID', 'Part_ID', 'Tipo', 'Adquisicion'])
Tractor = namedtuple('Tractor', ['Machine_ID', 'Modelo', 'Adquisicion'])
Operacion = namedtuple('Operacion', ['Machine_ID', 'Start', 'End', 'Km_recorridos', 'Toneladas'])
Mantencion2 = namedtuple('Mantencion',['Machine_ID','Part_ID','Start_Time', 'End_Time', 'Failure_Mode', 'year'])
Medicion = namedtuple('Medicion', ['Machine_ID', 'hora', 'dia', 'mes', 'year', 'Engine_Temperature', 'Hydraulic_Pressure'])