from mantenimiento import horas_mantencion_maquinas, cargar_tiempos, cargar_tractores, cuantas_veces_me_mantuve, cargar_datos2
from typing import Generator
from clases import Meses
import datetime
import os

def tiempo_en_uso_por_maquina(generador_tractores: Generator, generador_t_operaciones):
    # esta funcion te da los tiempos de operacion por maquina
    # POR AHORA NO FUNCIONA
    conteo = {tractor.Machine_ID: 0 for tractor in generador_tractores}
    for operacion in generador_t_operaciones:
        tractor = operacion[0]
        t = operacion[1]
        conteo[tractor] += t
    return conteo

tiempos_mantenciones = cargar_tiempos("tiempos_mantencion")
g_tractores_1 = cargar_tractores("truck_data")
g_tractores_2 = cargar_tractores("truck_data")
conteo_horas_mantencion = horas_mantencion_maquinas(tiempos_mantenciones, g_tractores_1)
conteo_veces_mantencion = cuantas_veces_me_mantuve()
g_mantencion2 = cargar_datos2("maintenance_data")
numero_1 = cuantas_veces_me_mantuve(g_mantencion2, "AWOU5IMX", 2019)