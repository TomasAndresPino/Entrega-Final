from typing import Generator
from clases2 import Medicion

def generador_sensor(archivo) -> Generator:
    next(archivo)
    for linea in archivo:
        elementos = linea.strip().split(",")
        # inicio es elementos[1], es un string "4/6/2020 20:07"
        inicio = elementos[1].split()
        # inicio es una lista ["4/6/2020", "20:07"]
        fecha_inicio = inicio[0].split("/")
        dia_inicio = fecha_inicio[1]
        mes_inicio = fecha_inicio[0]
        año_inicio = fecha_inicio[2]
        hora_inicio = inicio[1]

        Start = [int(dia_inicio), int(mes_inicio), int(año_inicio), hora_inicio]

        medicion = Medicion(Machine_ID= str(elementos[0]), Tiempo= Start, Temperatura= int(elementos[2]), Presion= int(elementos[3]))
        yield medicion