import random
import math
from scipy.stats import gamma
import numpy as np

def Ocio():
    """
    Función para asignar tiempos de ocio a camión AWOU5IMX
    """
    u = random.random()
    if u <= 0.169:
        tiempo = random.random()
    else:
        tiempo = random.uniform(1, 2)
    return tiempo

def Carga():
    u = random.random()
    if u <= 0.5:
        carga = random.uniform(5, 11)
    else:
        carga = random.uniform(20, 42)
    return carga

def Kilometros():
    kms = random.uniform(8, 22)
    return kms

def Operacion():
    toperacion = random.normalvariate(1.15, 0.39)
    return toperacion

def Cox():
    "Entrega probabilidad Cox de no falla en un tiempo T"
    lam = 1
    U = random.uniform(0.9, 1)
    
    x = -math.log(1 - U) / lam
    
    P = 1 - math.exp(-lam * x)
    
    return P

def TMantencionP():
    u = random.uniform(0, 1)
    if 0 <= u < 0.7:
        tiempo = random.uniform(2, 3.325)
    else:
        tiempo = random.uniform(3.325, 3.985)
    return tiempo

def Nivel_Falla():
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

def TFalla1():
    u = random.uniform(0, 1)
    if 0 <= u < 0.4785:
        tiempo = random.uniform(0, 0.5)
    elif 0.4785 <= u < 0.4967:
        tiempo = random.uniform(0.5, 1)
    else:
        tiempo = random.uniform(1, 1.5)
    return tiempo

def TFalla2():
    loc = 0.0
    scale = 1.2450555555555556
    tiempo = np.random.exponential(scale=scale)
    return tiempo

def TFalla3():
    c = 9.874230185804198 
    loc = -17.830724838101602 
    scale = 23.663424877179796  
    tiempo = loc + scale * np.random.weibull(c)
    return tiempo

def TFalla4():
    c = 2.491204492107027
    loc = -2.681229748047439
    scale = 12.702245598440982
    tiempo = loc + scale*np.random.weibull(c)
    return tiempo

def TFalla5():
    c = 1.7691695777559389
    loc = -3.037916292442177
    scale = 40.860870050932625
    tiempo = loc + scale*np.random.weibull(c)
    return tiempo

tiempo = TFalla5()
print(tiempo)