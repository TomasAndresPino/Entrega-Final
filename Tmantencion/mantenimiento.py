# abrir archivo
# manejar las fechas de inicio y termino
# con funcion generadora ir escribiendo nuevo texto
from typing import Generator
from generadores_data import generador_mantenimiento, generador_tiempos_mantencion, generador_frecuencias_relativas, generador_part_data, generador_tractores, generador_t_mantencion, generador_operaciones, generador_t_operaciones, generador_mantenimiento2, generador_sensor
from clases import Meses
import datetime
import os

def cargar_datos(nombre_archivo: str) -> Generator:
    # Carga los datos de mantención
    nombre = nombre_archivo + ".csv"
    ruta = os.path.join(nombre)
    with open(ruta, "r", encoding= "latin-1") as archivo:
        if nombre == "maintenance_data.csv":
            yield from generador_mantenimiento(archivo)

def cargar_datos2(nombre_archivo: str) -> Generator:
    # Carga los datos de mantención
    nombre = nombre_archivo + ".csv"
    ruta = os.path.join("Tmantencion", nombre)
    with open(ruta, "r", encoding= "latin-1") as archivo:
        if nombre == "maintenance_data.csv":
            yield from generador_mantenimiento2(archivo)

def cargar_sensores(nombre_archivo: str) -> Generator:
    # Carga los datos de mantención
    nombre = nombre_archivo + ".csv"
    with open(nombre, "r", encoding= "latin-1") as archivo:
        if nombre == "sensor_data.csv":
            yield from generador_sensor(archivo)

def cargar_tiempos(nombre_archivo: str) -> Generator:
    nombre = nombre_archivo + ".txt"
    #ruta = os.path.join("Tmantencion", nombre)
    with open(nombre, "r", encoding= "latin_1") as archivo:
        if nombre == "tiempos_mantencion.txt":
            #yield from generador_tiempos_mantencion(archivo)
            yield from generador_t_mantencion(archivo)

def cargar_datos_2(nombre_archivo: str) -> Generator:
    nombre = nombre_archivo + ".csv"
    with open(nombre, "r", encoding= "latin_1") as archivo:
        if nombre == "conteo_por_rango.csv":
            yield from generador_frecuencias_relativas(archivo)
        elif nombre == "part_data.csv":
            yield from generador_part_data(archivo)

def cargar_partes(nombre_archivo: str) -> Generator:
    nombre = nombre_archivo + ".csv"
    with open(nombre, "r", encoding= "latin-1") as archivo:
        if nombre == "part_data.csv":
            yield from generador_part_data(archivo)

def cargar_tractores(nombre_archivo: str) -> Generator:
    nombre = nombre_archivo + ".csv"
    with open(nombre, "r", encoding= "latin-1") as archivo:
        if nombre == "truck_data.csv":
            yield from generador_tractores(archivo)

def cargar_operaciones(nombre_archivo: str) -> Generator:
    # Carga los datos de operacion
    nombre = nombre_archivo + ".csv"
    with open(nombre, "r", encoding= "latin-1") as archivo:
        if nombre == "truck_operational_data.csv":
            yield from generador_operaciones(archivo)

def cargar_tiempos_operacion(nombre_archivo: str) -> Generator:
    nombre = nombre_archivo + ".txt"
    with open(nombre, "r", encoding= "latin_1") as archivo:
        if nombre == "tiempos_operaciones.txt":
            #yield from generador_tiempos_mantencion(archivo)
            yield from generador_t_operaciones(archivo)

def mantenciones_mas_un_dia(generador_mantenimiento: Generator) -> int:
    # Calcula la cantidad de mantenciones que duran más de 1 día
    filtro = filter(lambda mantencion: mantencion.Start_Time[0] - mantencion.End_Time[0] != 0 or 
                    mantencion.Start_Time[1] - mantencion.End_Time[1] != 0 or
                    mantencion.Start_Time[2] - mantencion.End_Time[2] != 0, generador_mantenimiento)
    cantidad = sum(map(lambda mantencion: 1, filtro))
    return cantidad

def mantenciones_año_diferente(generador_mantenimiento: Generator) -> int:
    # Calcula las mantenciones en años diferentes
    filtro = filter(lambda mantencion: mantencion.Start_Time[2] - mantencion.End_Time[2] != 0, generador_mantenimiento)
    cantidad = sum(map(lambda mantencion: 1, filtro))
    return cantidad

def escribe_tiempos_mantencion(generador_mantenimiento: Generator, tiempos_mantencion):
    # Escribe los tiempos de mantencion en formato hora y los minutos los pasa como fracción de hora
    """"
    OJO que cambie como funciona esta función que se ocupaba el archivo que tenía escrito paras otras cosas...
    """
    with open(tiempos_mantencion, 'w') as archivo:
        for mantencion in generador_mantenimiento:
            horas = [mantencion.Start_Time[3], mantencion.End_Time[3]]
            dias = mantencion.Start_Time[0] - mantencion.End_Time[0]
            meses = mantencion.Start_Time[1] - mantencion.End_Time[1]
            años =  mantencion.Start_Time[2] - mantencion.End_Time[2]
            if años != 0:
                dia_inicio = datetime.datetime(mantencion.Start_Time[2], mantencion.Start_Time[1], mantencion.Start_Time[0])
                dia_i = dia_inicio.timetuple().tm_yday
                dia_final = datetime.datetime(mantencion.End_Time[2], mantencion.End_Time[1], mantencion.End_Time[0])
                dia_f = dia_final.timetuple().tm_yday

                resto_1 = (365 - dia_i - 1)*24
                resto_2 = (dia_f)*24
                delta_d = resto_1 + resto_2

                t_inicio = horas[0].split(':')
                h_min_inicio = [int(t_inicio[0]),int(t_inicio[1])]
                t_usado_inicio = 24 - h_min_inicio[0] + (h_min_inicio[1]/60)
                t_fin = horas[1].split(':')
                h_min_fin = [int(t_fin[0]),int(t_fin[1])]
                t_usado_fin = h_min_fin[0] + (h_min_fin[1]/60)
                delta_t = t_usado_inicio + t_usado_fin

                suma = delta_d + delta_t
                archivo.write(str(mantencion.Machine_ID) + "," + str(suma) + "," + str(mantencion.Failure_Mode) + '\n')

            elif meses != 0 or dias != 0:
                dia_inicio = datetime.datetime(mantencion.Start_Time[2], mantencion.Start_Time[1], mantencion.Start_Time[0])
                dia_i = dia_inicio.timetuple().tm_yday
                dia_final = datetime.datetime(mantencion.End_Time[2], mantencion.End_Time[1], mantencion.End_Time[0])
                dia_f = dia_final.timetuple().tm_yday
                dias = dia_f - dia_i - 1
                delta_d = dias*24
                
                t_inicio = horas[0].split(':')
                h_min_inicio = [int(t_inicio[0]),int(t_inicio[1])]
                t_usado_inicio = 24 - h_min_inicio[0] - (h_min_inicio[1]/60)

                t_fin = horas[1].split(':')
                h_min_fin = [int(t_fin[0]),int(t_fin[1])]
                t_usado_fin = h_min_fin[0] + (h_min_fin[1]/60)

                delta_t = t_usado_inicio + t_usado_fin

                suma = delta_t + delta_d
                archivo.write(str(mantencion.Machine_ID) + "," + str(suma) + "," + str(mantencion.Failure_Mode) + '\n')
            
            else:
                t_inicio = horas[0].split(':')
                h_min_inicio = [int(t_inicio[0]),int(t_inicio[1])]

                t_fin = horas[1].split(':')
                h_min_fin = [int(t_fin[0]),int(t_fin[1])]

                delta_t = (h_min_fin[0] - h_min_inicio[0]) + ((h_min_fin[1]/60) - (h_min_inicio[1]/60))
                archivo.write(str(mantencion.Machine_ID) + "," + str(delta_t) + "," + str(mantencion.Failure_Mode) + '\n')

def cuantos_hay_cada_horas(generador_t_mantenimiento: Generator, *args):
    # Función no terminada
    conteo = {rango: 0 for rango in args}
    for tiempo in generador_t_mantenimiento:
        if 0 <= tiempo <= 1:
            conteo["una_hora"] += 1
        elif 1 < tiempo <= 2:
            conteo["dos_horas"] += 1
        elif 2 < tiempo <= 3:
            conteo["tres_horas"] += 1
    pass

def tiempo_maximo(generador_t_mantenimiento: Generator, maximo: 0):
    # Calcula el tiempo más largo
    for tiempo in generador_t_mantenimiento:
        if float(tiempo) > maximo:
            maximo = float(tiempo)
    return maximo

def eliminar_outlayers(generador_t_mantenimiento: Generator, tiempos_sin_outlayers):
    # Esta función quizás no es necesaria
    with open(tiempos_sin_outlayers, "w") as archivo:
        for tiempo in generador_t_mantenimiento:
            if float(tiempo) <= 6.4:
                archivo.write(str(tiempo) + '\n')

def frecuencia_relativa(generador_rangos: Generator, nombre_archivo):
    with open(nombre_archivo, 'w') as archivo:
        archivo.write("Rangos, Frecuencias_Relativas" + '\n')
        for rango in generador_rangos:
            archivo.write(str(rango.Inicio_Final) + ", " + str(rango.Frecuencia_Relativa) + '\n')

def que_tipo_falla_mas(generador_mantencion: Generator, generador_tractores: Generator):
    conteo_fallas = {'Tipo_A': 0, 'Tipo_B': 0}
    tractores = {'Tipo_A': [], 'Tipo_B': []}
    for tractor in generador_tractores:
        if tractor.Modelo == "A":
            tractores['Tipo_A'].append(tractor.Machine_ID)
        elif tractor.Modelo == "B":
            tractores['Tipo_B'].append(tractor.Machine_ID)
    for mantencion in generador_mantencion:
        if mantencion.Machine_ID in tractores['Tipo_A'] and mantencion.Failure_Mode != 0:
            conteo_fallas["Tipo_A"] += 1
        elif mantencion.Machine_ID in tractores["Tipo_B"] and mantencion.Failure_Mode != 0:
            conteo_fallas["Tipo_B"] += 1
    return conteo_fallas

def ordenar_por_fecha(fecha: str) -> int:
    fecha_separada = fecha.split("/")
    dia = datetime.datetime(int(fecha_separada[2]), int(fecha_separada[0]), int(fecha_separada[1]))
    n_dia = dia.timetuple().tm_yday
    años = int(fecha_separada[2]) - 2000
    fraccion_de_años = (int(n_dia) - 1)/365
    return años + fraccion_de_años

def conteo_fallas_por_parte(generador_mantencion: Generator, generador_partes: Generator):
    conteo_por_partes = {parte.Part_ID: [0, parte.Adquisicion] for parte in generador_partes}
    tuplas = []
    for mantencion in generador_mantencion:
        if mantencion.Failure_Mode != 0:
            conteo_por_partes[mantencion.Part_ID][0] += 1
    for parte in conteo_por_partes:
        tuplas.append((parte, conteo_por_partes[parte][0], conteo_por_partes[parte][1]))
    return tuplas

def ordenar_tuplas_por_fecha(tuplas):
    # Ordenar tuplas usando la función ordenar_por_fecha
    return sorted(tuplas, key=lambda x: ordenar_por_fecha(x[2]))

def escribe_partes_frecuencia_fecha(nombre_archivo, tuplas):
    with open(nombre_archivo, "w") as archivo:
        archivo.write("Frecuencia,Fecha" + '\n')
        for tupla in tuplas:
            archivo.write(str(tupla[1]) + "," + str(tupla[2]))

def reparaciones_segun_año_adquisicion(tuplas_ordenadas):
    conteo_por_año = {"2016": 0, "2017": 0, "2019": 0, "2020": 0, "2021": 0}
    for tupla in tuplas_ordenadas:
        elementos = tupla[2].strip('\n').split("/")
        año = str(elementos[2])
        conteo_por_año[año] += int(tupla[1])
    return conteo_por_año

def escribe_frecuencias_por_año(nombre_archivo, conteo_por_año):
    with open(nombre_archivo, "w") as archivo:
        archivo.write("Frecuencia,Year" + '\n')
        for año in conteo_por_año:
            archivo.write(str(conteo_por_año[año]) + "," + año + '\n')

def horas_mantencion_maquinas(generador_t_mantencion: Generator, generador_tractores: Generator):
    # horas en mantencion por maquina
    conteo = {tractor.Machine_ID: 0 for tractor in generador_tractores}
    for mantencion in generador_t_mantencion:
        conteo[mantencion[0]] += mantencion[1]
    return conteo

def porcentaje_ocupacion_maquinas(dic_horas_por_maquina: dict):
    for id_tractor in dic_horas_por_maquina:
        horas = dic_horas_por_maquina[id_tractor]
        porcentaje = (horas*100)/32496
        dic_horas_por_maquina[id_tractor] = porcentaje
    return dic_horas_por_maquina

def escribe_tiempos_operaciones(generador_operaciones: Generator, tiempos_operaciones):
    """
    No necesaria
    """
    with open(tiempos_operaciones, 'w') as archivo:
        for operacion in generador_operaciones:
            horas = [operacion.Start[3], operacion.End[3]]
            dias = operacion.Start[0] - operacion.End[0]
            meses = operacion.Start[1] - operacion.End[1]
            años =  operacion.Start[2] - operacion.End[2]
            if años != 0:
                dia_inicio = datetime.datetime(operacion.Start[2], operacion.Start[1], operacion.Start[0])
                dia_i = dia_inicio.timetuple().tm_yday
                dia_final = datetime.datetime(operacion.End[2], operacion.End[1], operacion.End[0])
                dia_f = dia_final.timetuple().tm_yday

                resto_1 = (365 - dia_i - 1)*24
                resto_2 = (dia_f)*24
                delta_d = resto_1 + resto_2

                t_inicio = horas[0].split(':')
                h_min_inicio = [int(t_inicio[0]),int(t_inicio[1])]
                t_usado_inicio = 24 - h_min_inicio[0] + (h_min_inicio[1]/60)
                t_fin = horas[1].split(':')
                h_min_fin = [int(t_fin[0]),int(t_fin[1])]
                t_usado_fin = h_min_fin[0] + (h_min_fin[1]/60)
                delta_t = t_usado_inicio + t_usado_fin

                suma = delta_d + delta_t
                archivo.write(str(operacion.Machine_ID) + "," + str(suma) + '\n')

            elif meses != 0 or dias != 0:
                dia_inicio = datetime.datetime(operacion.Start[2], operacion.Start[1], operacion.Start[0])
                dia_i = dia_inicio.timetuple().tm_yday
                dia_final = datetime.datetime(operacion.End[2], operacion.End[1], operacion.End[0])
                dia_f = dia_final.timetuple().tm_yday
                dias = dia_f - dia_i - 1
                delta_d = dias*24
                
                t_inicio = horas[0].split(':')
                h_min_inicio = [int(t_inicio[0]),int(t_inicio[1])]
                t_usado_inicio = 24 - h_min_inicio[0] - (h_min_inicio[1]/60)

                t_fin = horas[1].split(':')
                h_min_fin = [int(t_fin[0]),int(t_fin[1])]
                t_usado_fin = h_min_fin[0] + (h_min_fin[1]/60)

                delta_t = t_usado_inicio + t_usado_fin

                suma = delta_t + delta_d
                archivo.write(str(operacion.Machine_ID) + "," + str(suma) + '\n')
            
            else:
                t_inicio = horas[0].split(':')
                h_min_inicio = [int(t_inicio[0]),int(t_inicio[1])]

                t_fin = horas[1].split(':')
                h_min_fin = [int(t_fin[0]),int(t_fin[1])]

                delta_t = (h_min_fin[0] - h_min_inicio[0]) + ((h_min_fin[1]/60) - (h_min_inicio[1]/60))
                archivo.write(str(operacion.Machine_ID) + "," + str(delta_t) + '\n')

def horas_operando_maquinas(generador_tiempos_operaciones: Generator, generador_tractores: Generator):
    """
    No necesaria
    """
    conteo = {tractor.Machine_ID: 0 for tractor in generador_tractores}
    for operacion in generador_tiempos_operaciones:
        conteo[operacion[0]] += operacion[1]
    return conteo

def conteo_fallas_por_camion2(generador_tractores: Generator, generador_mantenciones: Generator):
    conteo = {tractor.Machine_ID: 0 for tractor in generador_tractores}
    for mantencion in generador_mantenciones:
        if mantencion.Failure_Mode != 0 and mantencion.year == 2023:
            conteo[mantencion.Machine_ID] += 1
    return conteo

def cuantas_veces_sobre_90(generador_medicion: Generator, id_tractor: str, año: int):
    conteo = 0
    for medicion in generador_medicion:
        if int(medicion.year) == año and medicion.Machine_ID == id_tractor:
            if medicion.Engine_Temperature != '':
                if float(medicion.Engine_Temperature) > 94:
                    conteo += 1
    return conteo

def cuantas_veces_me_mantuve(generador_mantencion2: Generator, id_tractor: str, año: int):
    contador = 0
    for mantencion in generador_mantencion2:
        if mantencion.Machine_ID == id_tractor and int(mantencion.year) == año:
            contador += 1
    return contador

def cuantas_veces_me_mantuve_todos_los_años(generador_mantencion2: Generator, id_tractor: str, año: int):
    contador = 0
    for mantencion in generador_mantencion2:
        if mantencion.Machine_ID == id_tractor and int(mantencion.year) == año:
            contador += 1
    return contador

"""Busca calcular cuantas veces cierto camion esta sobre ciertos grados"""
#g_sensor = cargar_sensores("sensor_data")
#g_mantencion2 = cargar_datos2("maintenance_data")
#numero_1 = cuantas_veces_sobre_90(g_sensor, "AWOU5IMX", 2019)
#numero_2 = cuantas_veces_me_mantuve(g_mantencion2, "AWOU5IMX", 2019)
#print(f"El tractor AWOU5IMX el 2019 estuvo sobre 95°C {numero_1} veces y se fue a mantención {numero_2}")






"""
Imprime cuantas veces cada tractor estuvo en mantención
"""
#g_mantencion = cargar_datos2("maintenance_data")
#g_tractores = cargar_tractores("truck_data")
#conteo = conteo_fallas_por_camion2(g_tractores, g_mantencion)
#for tractor in conteo:
    #sprint(f"El tractor {tractor} el año 2023 estuvo en mantención {conteo[tractor]} veces")


       
#generador = cargar_datos("maintenance_data")
#escribe_tiempos_mantencion(generador, "tiempos_mantencion.txt")
#generador = cargar_tiempos("tiempos_mantencion")
#max = tiempo_maximo(generador, maximo= 0)
#print("El tiempo máximo es", max)
#numero_1 = mantenciones_mas_un_dia(generador)
#print("La cantidad de mantenciones que duran más de un día son", numero_1)
#numero_2 = mantenciones_año_diferente(generador)
#print("La cantidad de mantenciones que duran mas de un año (hipoteticamente) son", numero_2)
#generador = cargar_datos_2('conteo_por_rango')
#frecuencia_relativa(generador, "frecuencias_relativas.txt")
#g_mantenciones = cargar_datos('maintenance_data')
#g_tractores = cargar_tractores("truck_data")
#conteo = que_tipo_falla_mas(g_mantenciones, g_tractores)
#print("La cantidad de mantenciones no programadas para Tipo A fue", conteo['Tipo_A'])
#print("La cantidad de mantenciones no programadas para Tipo B fue", conteo['Tipo_B'])
#g_m = cargar_datos('maintenance_data')
#g_p = cargar_partes('part_data')
#tuplas = conteo_fallas_por_parte(g_m, g_p)
#tuplas_ordenadas = ordenar_tuplas_por_fecha(tuplas)
# Imprimir la información ordenada
#for parte, conteo, fecha in tuplas_ordenadas:
    #print(f"La parte {parte} se reparó {conteo} veces y se compró el {fecha}")
#escribe_partes_frecuencia_fecha("frecuencia_reparacion_partes.txt", tuplas_ordenadas)
#conteo_por_año = reparaciones_segun_año_adquisicion(tuplas_ordenadas)
#escribe_frecuencias_por_año("frecuencias_por_year.txt", conteo_por_año)

#for parte in conteo:
    #print(f"La parte {parte} se reparó {conteo[parte][0]} veces y se compró el {conteo[parte][1]}")

generador = cargar_datos("maintenance_data")
escribe_tiempos_mantencion(generador, "tiempos_mantencion_2")