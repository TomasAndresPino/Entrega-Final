from typing import Generator
from datetime import datetime
from NamedTuples import Operacion_Toneladas, Operacion_Tiempo, Operacion_Kms, Falla, Hazzard, Mantencion, Probabilidad, Mantencion_2
import pandas as pd

def generador_operaciones(archivo, modelo) -> Generator:
    next(archivo)
    for linea in archivo:
        if modelo == "AWOU5IMX":
            elementos = linea.strip().split(",")
            toneladas = float(elementos[4])
            operacion = Operacion_Toneladas(Toneladas= toneladas)
            yield operacion

def generador_operaciones_tiempo(archivo, modelo) -> Generator:
    next(archivo)
    for linea in archivo:
        if modelo == "AWOU5IMX":
            elementos = linea.strip().split(",")
            tinicio = datetime.strptime(elementos[1], "%m/%d/%Y %H:%M")
            tfin = datetime.strptime(elementos[2], "%m/%d/%Y %H:%M")
            operacion = Operacion_Tiempo(TInicio= tinicio, TFin= tfin)
            yield operacion
 
def generador_ocios(archivo) -> Generator:
    next(archivo)
    for linea in archivo:
        elementos = linea.strip().split(",")
        tocio = float(elementos[1])
        yield tocio

def generador_kilometros(archivo, modelo) -> Generator:
    next(archivo)
    for linea in archivo:
        if modelo == "AWOU5IMX":
            elementos = linea.strip().split(",")
            kilometros = float(elementos[3])
            operacion = Operacion_Kms(Kms= kilometros)
            yield operacion

def generador_fallas(archivo, modelo) -> Generator:
    next(archivo)
    for linea in archivo:
        if modelo == "AWOU5IMX":
            elementos = linea.strip().split(",")
            falla = int(elementos[4])
            fail = Falla(Tipo= falla)
            yield fail

def generador_hazard(archivo) -> Generator:
    next(archivo)
    for linea in archivo:
        elementos = linea.strip().split(",")
        tiempo = float(elementos[1])
        hazzard = float(elementos[0])
        instancia = Hazzard(Haz= hazzard, Tiempo= tiempo)
        yield instancia

def generador_mantenciones(archivo) -> Generator:
    next(archivo)
    for linea in archivo:
        elementos = linea.strip().split(",")
        id = elementos[0]
        falla = elementos[4]
        inicio = pd.to_datetime(elementos[2], format='%m/%d/%Y %H:%M')
        final = pd.to_datetime(elementos[3], format='%m/%d/%Y %H:%M')
        duracion = final - inicio  
        d = duracion.total_seconds()/3600 
        mantencion = Mantencion(Machine_ID= id, Failure_Mode= falla, Duracion= d)
        yield mantencion

def generador_probabilidad(archivo) -> Generator:
    next(archivo)
    for linea in archivo:
        elementos = linea.strip().split(",")
        t = elementos[0]
        survival = elementos[1]
        probabilidad = Probabilidad(Time= float(t), Survival= float(survival))
        yield probabilidad

def generador_mantenciones_año(archivo) -> Generator:
    next(archivo)
    for linea in archivo:
        elementos = linea.strip().split(",")
        id = elementos[0]
        failure = elementos[4]
        fecha = elementos[2].split("/")
        año_hora = fecha[2].split()
        año = int(año_hora[0])
        mantencion = Mantencion_2(Machine_ID= id, Año= año, Failure_Mode= failure)
        yield mantencion
