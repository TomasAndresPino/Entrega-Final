from collections import namedtuple

Operacion_Toneladas = namedtuple('Operacion_Toneladas', ['Toneladas'])
Operacion_Tiempo = namedtuple('Operacion_Tiempo', ['TInicio', 'TFin'])
Operacion_Kms = namedtuple('Operacion_Kms', ['Kms'])
Falla = namedtuple('Falla', ['Tipo'])
#Falla_2 = namedtuple('Falla_2', [])
Hazzard = namedtuple('Hazzard', ['Haz', 'Tiempo'])
Mantencion = namedtuple('Mantencion', ['Machine_ID', 'Failure_Mode', 'Duracion'])
Mantencion_2 = namedtuple('Mantencion_2', ['Machine_ID', 'Año', 'Failure_Mode'])
Probabilidad = namedtuple('Probabilidad', ['Time', 'Survival'])
