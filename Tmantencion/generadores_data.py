from typing import Generator
from clases import Mantencion, Rango, Parte, Tractor, Operacion, Mantencion2, Medicion

def generador_mantenimiento(archivo) -> Generator:
    next(archivo)
    for linea in archivo:
        elementos = linea.strip().split(",")
        # inicio es elementos[2], es un string "4/6/2020 20:07"
        inicio = elementos[2].split()
        # inicio es una lista ["4/6/2020", "20:07"]
        fecha_inicio = inicio[0].split("/")
        dia_inicio = fecha_inicio[1]
        mes_inicio = fecha_inicio[0]
        año_inicio = fecha_inicio[2]
        hora_inicio = inicio[1]

        Start = [int(dia_inicio), int(mes_inicio), int(año_inicio), hora_inicio]

        fin = elementos[3].split()
        fecha_fin = fin[0].split("/")
        dia_fin = fecha_fin[1]
        mes_fin = fecha_fin[0]
        año_fin = fecha_fin[2]
        hora_fin = fin[1]

        End = [int(dia_fin), int(mes_fin), int(año_fin), hora_fin]

        mantencion = Mantencion(Machine_ID= str(elementos[0]), Part_ID= str(elementos[1]), Start_Time= Start, End_Time= End, Failure_Mode= int(elementos[4]))
        yield mantencion

def generador_operaciones(archivo) -> Generator:
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

        Inicio = [int(dia_inicio), int(mes_inicio), int(año_inicio), hora_inicio]

        fin = elementos[2].split()
        fecha_fin = fin[0].split("/")
        dia_fin = fecha_fin[1]
        mes_fin = fecha_fin[0]
        año_fin = fecha_fin[2]
        hora_fin = fin[1]

        Final = [int(dia_fin), int(mes_fin), int(año_fin), hora_fin]

        operacion = Operacion(Machine_ID= str(elementos[0]), Start= Inicio, End= Final, Km_recorridos= float(elementos[3]), Toneladas= float(elementos[4]))
        yield operacion

def generador_tiempos_mantencion(archivo) -> Generator:
    for linea in archivo:
        tiempo = float(linea)
        yield tiempo

def generador_frecuencias_relativas(archivo) -> Generator:
    next(archivo)
    for linea in archivo:
        elementos = linea.split(",")
        entero = int(elementos[1])
        rango = Rango(Inicio_Final= elementos[0], Frecuencia_Relativa= float(entero/1575))
        yield rango

def generador_part_data(archivo) -> Generator:
    next(archivo)
    for linea in archivo:
        elementos = linea.split(",")
        parte = Parte(Machine_ID= elementos[0], Part_ID= elementos[1], Tipo= elementos[2], Adquisicion= elementos[3])
        yield parte

def generador_tractores(archivo) -> Generator:
    next(archivo)
    for linea in archivo:
        elementos = linea.split(",")
        if elementos[1] == "Model_A":
            modelo = "A"
            tractor = Tractor(Machine_ID= elementos[0], Modelo= modelo, Adquisicion= elementos[2]) 
        elif elementos[1] == "Model_B":
            modelo = "B"
            tractor = Tractor(Machine_ID= elementos[0], Modelo= modelo, Adquisicion= elementos[2])
        yield tractor

def generador_t_mantencion(archivo) -> Generator:
    for linea in archivo:
        elementos = linea.strip('\n').split(",")
        yield [elementos[0], float(elementos[1])]

def generador_t_operaciones(archivo) -> Generator:
    for linea in archivo:
        elementos = linea.strip('\n').split(',')
        yield [elementos[0], float(elementos[1])]

def generador_sensor(archivo) -> Generator:
    next(archivo)
    for linea in archivo:
        elementos = linea.strip('\n').split(',')
        tiempo = elementos[1].split()
        fecha = tiempo[0].split('/') 
        medicion = Medicion(Machine_ID= elementos[0], hora= tiempo[1], dia= fecha[1], mes= fecha[0], year= fecha[2], Engine_Temperature= elementos[2], Hydraulic_Pressure= elementos[3])
        yield medicion

def generador_mantenimiento2(archivo) -> Generator:
    next(archivo)
    for linea in archivo:
        elementos = linea.strip().split(",")
        # inicio es elementos[2], es un string "4/6/2020 20:07"
        inicio = elementos[2].split()
        # inicio es una lista ["4/6/2020", "20:07"]
        fecha_inicio = inicio[0].split("/")
        dia_inicio = fecha_inicio[1]
        mes_inicio = fecha_inicio[0]
        año_inicio = fecha_inicio[2]
        hora_inicio = inicio[1]

        Start = [int(dia_inicio), int(mes_inicio), int(año_inicio), hora_inicio]
        a_inicio = Start[2]

        fin = elementos[3].split()
        fecha_fin = fin[0].split("/")
        dia_fin = fecha_fin[1]
        mes_fin = fecha_fin[0]
        año_fin = fecha_fin[2]
        hora_fin = fin[1]

        End = [int(dia_fin), int(mes_fin), int(año_fin), hora_fin]


        mantencion2 = Mantencion2(Machine_ID= str(elementos[0]), Part_ID= str(elementos[1]), Start_Time= Start, End_Time= End, Failure_Mode= int(elementos[4]), year= a_inicio)
        yield mantencion2


