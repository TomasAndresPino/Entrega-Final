from typing import Generator
from funciones_generadoras import generador_operaciones, generador_operaciones_tiempo, generador_ocios, generador_kilometros, generador_fallas, generador_hazard, generador_mantenciones, generador_probabilidad, generador_mantenciones_año
import os

def cargar_operaciones(nombre_archivo: str, modelo: str) -> Generator:
    # Carga los datos de operacion
    nombre = nombre_archivo + ".csv"
    with open(nombre, "r", encoding= "latin-1") as archivo:
        if nombre == "truck_operational_data.csv":
            yield from generador_operaciones(archivo, modelo)

def cargar_operaciones_tiempo(nombre_archivo: str, modelo: str) -> Generator:
    # Carga los datos de operacion
    nombre = nombre_archivo + ".csv"
    with open(nombre, "r", encoding= "latin-1") as archivo:
        if nombre == "truck_operational_data.csv":
            yield from generador_operaciones_tiempo(archivo, modelo)

def cargar_ocios(nombre_archivo: str) -> Generator:
    # Carga los datos de ocio
    nombre = nombre_archivo + ".txt"
    with open(nombre, "r", encoding= "latin-1") as archivo:
        if nombre == "tiempos_ocio.txt":
            yield from generador_ocios(archivo)

def cargar_kilometros(nombre_archivo: str, modelo) -> Generator:
    # Carga los datos de operacion
    nombre = nombre_archivo + ".csv"
    with open(nombre, "r", encoding= "latin-1") as archivo:
        if nombre == "truck_operational_data.csv":
            yield from generador_kilometros(archivo, modelo)

def cargar_fallas(nombre_archivo: str, modelo) -> Generator:
    nombre = nombre_archivo + ".csv"
    with open(nombre, "r", encoding= "latin-1") as archivo:
        if nombre == "maintenance_data.csv":
            yield from generador_fallas(archivo, modelo)

def cargar_hazzard(nombre_archivo: str) -> Generator:
    nombre = nombre_archivo + ".csv"
    with open(nombre, "r", encoding= "latin-1") as archivo:
        if nombre == "basline_haz.csv":
            yield from generador_hazard(archivo)

def cargar_mantenciones(nombre_archivo: str) -> Generator:
    nombre = nombre_archivo + ".csv"
    with open(nombre, "r", encoding= "latin-1") as archivo:
        if nombre == "maintenance_data.csv":
            yield from generador_mantenciones(archivo)

def cargar_mantenciones_2(nombre_archivo: str) -> Generator:
    nombre = nombre_archivo + ".csv"
    with open(nombre, "r", encoding= "latin-1") as archivo:
        if nombre == "maintenance_data.csv":
            yield from generador_mantenciones_año(archivo)

def cargar_probabilidades(nombre_archivo: str) -> Generator:
    nombre = nombre_archivo + ".csv"
   
    with open(f"C:/Users/tpin0/Desktop/Proyecto-Capstone/E2/KMs/{nombre}", "r", encoding= "latin-1") as archivo:
        yield from generador_probabilidad(archivo)
