from typing import Generator
from clases import Meses
import datetime
import os

from mantenimiento import cargar_operaciones, cargar_datos, cargar_tractores
# Operacion = namedtuple('Operacion', ['Machine_ID', 'Start', 'End', 'Km_recorridos', 'Toneladas'])

def fallas_por_camion(generador_tractores: Generator, generador_mantenciones: Generator):
    " retorna diccionario con cantidad de fallas por camiones "
    conteo = {tractor.Machine_ID: 0 for tractor in generador_tractores}
    for mantencion in generador_mantenciones:
        conteo[mantencion.Machine_ID] += 1
    return conteo

def kms_ton_por_camion(generador_tractores: Generator, generador_operaciones: Generator):
    # cuenta kms y ton por camion ( en ese orden )
    conteo = {tractor.Machine_ID: [0, 0] for tractor in generador_tractores}
    for operacion in generador_operaciones:
        conteo[operacion.Machine_ID][0] += int(operacion.Km_recorridos)
        conteo[operacion.Machine_ID][1] += int(operacion.Toneladas)
    return conteo

def escribir_tractor_factor_fallas(generador_tractores: Generator, conteo_fallas: dict, conteo_kms_ton: dict, factoresyfallas):
    factores = {tractor.Machine_ID: [0, tractor.Modelo] for tractor in generador_tractores}
    with open(factoresyfallas, 'w') as archivo:
        archivo.write("Machine_ID,Factor,Fallas,Modelo" + '\n')
        for tractor in conteo_kms_ton:
            factor = float(conteo_kms_ton[tractor][1])/float(conteo_kms_ton[tractor][0])
            factores[tractor][0] = factor
        for tractor in conteo_fallas:
            archivo.write(tractor + "," + str(factores[tractor][0]) + "," + str(conteo_fallas[tractor]) + "," + factores[tractor][1] + '\n')

g_operaciones = cargar_operaciones("truck_operational_data")
g_mantenciones = cargar_datos("maintenance_data")
g_tractores_1 = cargar_tractores("truck_data")
g_tractores_2 = cargar_tractores("truck_data")
g_tractores_3 = cargar_tractores("truck_data")


conteo_fallas = fallas_por_camion(g_tractores_1, g_mantenciones)
conteo_kms_ton = kms_ton_por_camion(g_tractores_2, g_operaciones)
escribir_tractor_factor_fallas(g_tractores_3, conteo_fallas, conteo_kms_ton, "factoresyfallas.txt")



