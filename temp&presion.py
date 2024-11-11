from typing import Generator
from generadores_data_2 import generador_sensor

def cargar_sensor_data(nombre_archivo: str) -> Generator:
    nombre = nombre_archivo + ".csv"
    with open(nombre, "r", encoding= "latin-1") as archivo:
        if nombre == "sensor_data.csv":
            yield from generador_sensor(archivo)

def filtro_por_maquina(generador_sensores: Generator, id_maquina: str) -> Generator:
    filtro = filter(lambda medicion: medicion.Machine_ID == id_maquina, generador_sensores)
    for medicion in filtro:
        yield medicion

def puntos_tiempo_temperatura(filtro_por_maquina: Generator, necesidad, nombre_archivo):
    # escribir un archivo que tenga el filtro aplicado y ponga el tiempo (en continuo) vs la T o P 
    # segun lo indicado en necesidad
    if necesidad == "T":
        with open(nombre_archivo, "w") as archivo:
            # poner el tiempo en continuo
            pass
    elif necesidad == "P":
        with open(nombre_archivo, "w") as archivo:
            # poner el tiempo en continuo
            pass

