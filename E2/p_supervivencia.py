from carga_archivos import cargar_probabilidades
from consultas import cantidades
from carga_archivos import cargar_fallas
from typing import Generator
import random

g_electrico = cargar_probabilidades("km.electrical")
g_motor = cargar_probabilidades("km.engine")
g_escape = cargar_probabilidades("km.exhaust")
g_hidraulico = cargar_probabilidades("km.hydraulic")
g_suspension = cargar_probabilidades("km.suspension")

def p_segun_t_mas_cerca(generador: Generator, horas: int):
    """
    Calcula la probabilidad en base al tiempo más cercano en los csv de falla
    esto lo hace para cualquier csv, cualquier tiempo
    """
    resta_minima = 100000
    p = 0
    for tiempo in generador:
        resta = abs(tiempo.Time - horas)
        if resta < resta_minima:
            resta_minima = resta
            p = tiempo.Survival
    return p

def dado_cargado_5():
    u = random.uniform(0, 1)
    # p falla tipo 1 0.5285
    # p falla tipo 2 0.2062
    # p falla tipo 3 0.0274
    # p falla tipo 4 0.145
    # p falla tipo 5 0.0928
    if 0 <= u < 0.5285:
        i = 1
    elif 0.5285 <= u < 0.7347:
        i = 2
    elif 0.7347 <= u < 0.7621:
        i = 3
    elif 0.7621 <= u < 0.9071:
        i = 4
    else:
        i = 5
    return i

def dado_cargado_4(diccionario_cantidades: dict, eventos_posibles: list):
    n = 0

    for i in diccionario_cantidades.keys():
        if i in eventos_posibles:
            n += diccionario_cantidades[i]

    cantidades = {evento: diccionario_cantidades[evento] for evento in eventos_posibles}
    p = [cantidades[evento]/n for evento in eventos_posibles]
    u = random.uniform(0, 1)
    if 0 <= u < p[0]:
        i = eventos_posibles[0]
    elif p[0] <= u < p[0] + p[1]:
        i = eventos_posibles[1]
    elif p[0] + p[1] <= u < p[0] + p[1] + p[2]:
        i = eventos_posibles[2]
    elif p[0] + p[1] + p[2] <= u <= 1:
        i = eventos_posibles[3]
    return i

def dado_cargado_3(diccionario_cantidades: dict, eventos_posibles: list):
    n = 0

    for i in diccionario_cantidades.keys():
        if i in eventos_posibles:
            n += diccionario_cantidades[i]

    cantidades = {evento: diccionario_cantidades[evento] for evento in eventos_posibles}
    p = [cantidades[evento]/n for evento in eventos_posibles]
    u = random.uniform(0, 1)
    if 0 <= u < p[0]:
        i = eventos_posibles[0]
    elif p[0] <= u < p[0] + p[1]:
        i = eventos_posibles[1]
    elif p[0] + p[1] <= u <= 1:
        i = eventos_posibles[2]
    return i

def dado_cargado_2(diccionario_cantidades: dict, eventos_posibles: list):
    n = 0

    for i in diccionario_cantidades.keys():
        if i in eventos_posibles:
            n += diccionario_cantidades[i]

    cantidades = {evento: diccionario_cantidades[evento] for evento in eventos_posibles}
    p = [cantidades[evento]/n for evento in eventos_posibles]
    u = random.uniform(0, 1)
    if 0 <= u < p[0]:
        i = eventos_posibles[0]
    elif p[0] <= u <= 1:
        i = eventos_posibles[1]
    return i

def Tipo_Falla(horas: list):
    diccionario = cantidades(cargar_fallas("maintenance_data", "AWOU5IMX"))

    g_electrico = cargar_probabilidades("km.electrical")
    g_motor = cargar_probabilidades("km.engine")
    g_escape = cargar_probabilidades("km.exhaust")
    g_hidraulico = cargar_probabilidades("km.hydraulic")
    g_suspension = cargar_probabilidades("km.suspension")

    p_1 = p_segun_t_mas_cerca(g_electrico, horas[0])
    p_2 = p_segun_t_mas_cerca(g_motor, horas[1])
    p_3 = p_segun_t_mas_cerca(g_escape, horas[2])
    p_4 = p_segun_t_mas_cerca(g_hidraulico, horas[3])
    p_5 = p_segun_t_mas_cerca(g_suspension, horas[4])

    probabilidades = [p_1, p_2, p_3, p_4, p_5]
    eventos_posibles = []
    u = random.uniform(0, 1)
    for i in range(5):
        if u > probabilidades[i]:
            "La falla i puede ocurrir"
            evento = str(i+1)
            eventos_posibles.append(evento)
    
    if len(eventos_posibles) > 1:
        "puede ocurrir más de un evento"
        if len(eventos_posibles) == 5:
            "pueden ocurrir 5 eventos"
            print(eventos_posibles)
            i = dado_cargado_5()
        elif len(eventos_posibles) == 4:
            "pueden ocurrir 4 eventos"
            print(eventos_posibles)
            i = dado_cargado_4(diccionario, eventos_posibles)
        elif len(eventos_posibles) == 3:
            "pueden ocurrir 3 eventos"
            print(eventos_posibles)
            i = dado_cargado_3(diccionario, eventos_posibles)
        elif len(eventos_posibles) == 2:
            "pueden ocurrir 2 eventos"
            print(eventos_posibles)
            i = dado_cargado_2(diccionario, eventos_posibles)
    if len(eventos_posibles) == 1:
        "ocurre solo 1 evento"
        i = eventos_posibles[0]
    if len(eventos_posibles) == 0:
        "no ocurre ningun evento"
        i = str(0)
    return i 

#i = Tipo_Falla([0, 4000, 5000, 0, 0])
#print(i)
#print(type(i))

def probabilidades(horas: list):
    g_electrico = cargar_probabilidades("km.electrical")
    g_motor = cargar_probabilidades("km.engine")
    g_escape = cargar_probabilidades("km.exhaust")
    g_hidraulico = cargar_probabilidades("km.hydraulic")
    g_suspension = cargar_probabilidades("km.suspension")

    p_1 = p_segun_t_mas_cerca(g_electrico, horas[0])
    p_2 = p_segun_t_mas_cerca(g_motor, horas[1])
    p_3 = p_segun_t_mas_cerca(g_escape, horas[2])
    p_4 = p_segun_t_mas_cerca(g_hidraulico, horas[3])
    p_5 = p_segun_t_mas_cerca(g_suspension, horas[4])

    proba = [p_1, p_2, p_3, p_4, p_5]
    return proba