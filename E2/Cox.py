from typing import Generator
import math
from carga_archivos import cargar_hazzard

def hazzard(g_hazzard: Generator, horas: int):
    resta_minima = 100000
    hazz_0 = 0
    for hazzard in g_hazzard:
        resta = abs(hazzard.Tiempo - horas)
        if resta < resta_minima:
            resta_minima = resta
            hazz_0 = hazzard.Haz
    return hazz_0

#def hazzard_1(g_hazzard: Generator, hazzard_0: float):
    #hazz_1 = 0
    #for hazzard in g_hazzard:
        #if hazzard.Haz == hazzard_0:
            #proximo = next(g_hazzard)
            #hazz_1 = proximo.Haz
            #break
    #return hazz_1

#h_0 = hazzard(cargar_hazzard("basline_haz"), 240)
#print("El h encontrado para 10 dias fue", h_0)
#h_1 = hazzard_1(cargar_hazzard("basline_haz"), h_0)
#print("El h_0 encontrado para 11 dias fue", h_1)

def Cox(dia: int, kms: float, ton: float):
    horas = dia * 24
    generador_1 = cargar_hazzard("basline_haz")
    generador_2 = cargar_hazzard("basline_haz")
    h_0 = hazzard(generador_1, horas)
    h_1 = hazzard(generador_2, horas + 24)

    beta_1 = -0.0005496639
    beta_2 = -0.0003898039

    "calcular score"
    score = beta_1*kms + beta_2*ton

    p = math.exp(-h_1*math.exp(score)) / math.exp(-h_0*math.exp(score))
    """
    Por ahora como la cox no esta funcionando bien, se dividirá por 2 la probabilidad 
    (ya que da numeros cerca de 1 casi siempre),
    luego se le sumará 0.2 para que las probabilidades estén en torno a 0.7 constantemente
    """
    #probabilidad_auxiliar = (p/2) + 0.2
    #return probabilidad_auxiliar
    return p

probabilidad = Cox(0, 0, 0)
print("La probabilidad de sobrevivir del día 0 al 1 con 0kms y 0ton acumuladas es", probabilidad)