from carga_archivos import cargar_operaciones, cargar_operaciones_tiempo, cargar_ocios, cargar_fallas, cargar_mantenciones, cargar_probabilidades, cargar_mantenciones_2, cargar_probabilidades_2, cargar_hazzard
from dados_cargados import dado_cargado_2_1, dado_cargado_3_1, dado_cargado_4_1, dado_cargado_5_1
from typing import Generator
import random
import numpy as np

np.random.seed(42)

def rangos_1(g_operaciones: Generator):
    """
    Quiero ver cuantas veces el camión 1 está en los rangos 5-15 de carga y 20-45 de carga
    Este código calcula la probabilidad de estar en los 2 rangos planteados por la distribucion
    encontrada en la carpeta distribuciones para el primer camión
    """
    n_1 = 0
    n_2 = 0
    total = 0
    for operacion in g_operaciones:
        if 5 <= operacion.Toneladas < 15:
            n_1 += 1
            total += 1
        else: 
            n_2 += 1
            total += 1
    p_1 = n_1 / total
    p_2 = n_2 / total
    return [p_1, p_2]

#g_operaciones = cargar_operaciones("truck_operational_data", "AWOU5IMX")
#lista = rangos_1(g_operaciones)
#print(lista[0])
#print(lista[1])

def escribe_tiempos_ocio(g_operaciones_tiempo_1: Generator, g_operaciones_tiempo_2: Generator, nombre_archivo: str):
    with open(nombre_archivo +".txt", "w") as archivo:
        archivo.write("Machine_ID,TOcio" + "\n")
        next(g_operaciones_tiempo_2)
        for operacion in g_operaciones_tiempo_1:
            tiempo_final_actual = operacion.TFin
            for operacion_siguiente in g_operaciones_tiempo_2:
                tiempo_inicio_siguiente = operacion_siguiente.TInicio
                TOcio = tiempo_inicio_siguiente - tiempo_final_actual

                horas_decimal = TOcio.total_seconds() / 3600
                archivo.write("AWOU5IMX" + "," + str(horas_decimal) + "\n")
                break

#g_operaciones_tiempo_1 = cargar_operaciones_tiempo("truck_operational_data", "AWOU5IMX")
#g_operaciones_tiempo_2 = cargar_operaciones_tiempo("truck_operational_data", "AWOU5IMX")

#escribe_tiempos_ocio(g_operaciones_tiempo_1, g_operaciones_tiempo_2, "tiempos_ocio")

def rangos_2(g_ocios: Generator):
    n_1 = 0
    n_2 = 0
    total = 0
    for ocio in g_ocios:
        if 0 <= ocio < 1:
            n_1 += 1
            total += 1
        else: 
            n_2 += 1
            total += 1
    p_1 = n_1 / total
    p_2 = n_2 / total
    return [p_1, p_2]

#g_ocios = cargar_ocios("tiempos_ocio")
#lista = rangos_2(g_ocios)
#print("Probabilidad de ocio uniforme entre 0 y 1:", lista[0])
#print("Probabilidad de ocio uniforme entre 1 y 2:", lista[1])

def p_falla(g_fallas):
    contador_tipo_fallas = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0}
    contador_total = 0
    p_fallas = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0}
    for falla in g_fallas:
        i = falla.Tipo
        if i != 0:
            contador_tipo_fallas[str(i)] += 1
            contador_total += 1
    for falla in contador_tipo_fallas:
        p = contador_tipo_fallas[falla]/contador_total
        p_fallas[falla] = p
    return p_fallas

#diccionario = p_falla(cargar_fallas("maintenance_data", "AWOU5IMX"))
#for i in diccionario:
    #print(f"La probabilidad de falla tipo {i} es {diccionario[i]}")

def p_falla_1(g_mantenciones: Generator):
    conteo = {"1": 0, "2": 0, "3": 0}
    total = 0
    for mantencion in g_mantenciones:
        if mantencion.Failure_Mode == "1":
            duracion = mantencion.Duracion
            total += 1
            if 0 <= duracion < 0.5:
                conteo["1"] += 1
            elif 0.5 <= duracion < 1:
                conteo["2"] += 1
            else:
                conteo["3"] += 1
    probabilidades = {i: conteo[i]/total for i in conteo}
    return probabilidades

#diccionario = p_falla_1(cargar_mantenciones("maintenance_data"))
#for i in diccionario:
#    print(f"La probabilidad p_{i} es {diccionario[i]}")

def p_falla_0(g_mantenciones: Generator):
    conteo = {"1": 0, "2": 0}
    total = 0
    for mantencion in g_mantenciones:
        if mantencion.Failure_Mode == "0":
            duracion = mantencion.Duracion
            total += 1
            if 2 <= duracion < 3.325:
                conteo["1"] += 1
            elif 3.325 <= duracion <= 3.985:
                conteo["2"] += 1
    probabilidades = {i: conteo[i]/total for i in conteo}
    return probabilidades

#diccionario = p_falla_0(cargar_mantenciones("maintenance_data"))
#for i in diccionario:
#    print(f"La probabilidad p_{i} es {diccionario[i]}")

#def cantidades(g_fallas):
def cantidades(nombre: str, modelo: str):
    g_fallas = cargar_fallas(nombre, modelo)
    contador_tipo_fallas = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0}
    contador_total = 0
    for falla in g_fallas:
        i = falla.Tipo
        if i != 0:
            contador_tipo_fallas[str(i)] += 1
            contador_total += 1
    return contador_tipo_fallas

#diccionario = cantidades("maintenance_data", "AWOU5IMX")
#for i in diccionario:
    #print(f"La probabilidad de falla tipo {i} es {diccionario[i]}")

def p_segun_t_mas_cerca(generador: Generator, horas: int):
    """
    Calcula la probabilidad en base al tiempo más cercano en los csv de falla
    esto lo hace para cualquier csv, cualquier tiempo
    """
    resta_minima = 100000
    p = 0
    resta_2 = False
    for tiempo in generador:
        if resta_2 == True:
            p2 = tiempo.Survival
            resta_2 = False
        resta = abs(tiempo.Time - horas)
        if resta < resta_minima:
            resta_2 = True
            resta_minima = resta
            p = tiempo.Survival
        else:
            break
    #print("La probabilidad es", abs(p-p2))
    return p2/p

def p_segun_t_mas_cerca_antiguo(generador: Generator, horas: int):
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
    #print("La probabilidad es", abs(p-p2))
    return p

def probabilidades(horas: list):
    g_electrico = cargar_probabilidades("km.electrical")
    g_motor = cargar_probabilidades("km.engine")
    g_escape = cargar_probabilidades("km.exhaust")
    g_hidraulico = cargar_probabilidades("km.hydraulic")
    g_suspension = cargar_probabilidades("km.suspension")

    p_1 = p_segun_t_mas_cerca_antiguo(g_electrico, horas[0])
    p_2 = p_segun_t_mas_cerca_antiguo(g_motor, horas[1])
    p_3 = p_segun_t_mas_cerca_antiguo(g_escape, horas[2])
    p_4 = p_segun_t_mas_cerca_antiguo(g_hidraulico, horas[3])
    p_5 = p_segun_t_mas_cerca_antiguo(g_suspension, horas[4])

    proba = [p_1, p_2, p_3, p_4, p_5]
    #print(proba)
    return proba

#plist = probabilidades([0,5000,4000,0,0])
#print(plist)

def Tipo_Falla(horas: list, diccionario_cantidades):
    #diccionario_cantidades = cantidades(cargar_fallas("maintenance_data", "AWOU5IMX"))

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
    # print("Prob", probabilidades)
    eventos_posibles = []
    ###########################################################u = random.uniform(0, 1)
    u = random.randint(0, 10000)/10000
    # print("U no puedes ser tan grande", u)
    for i in range(5):
        if u > probabilidades[i]:
            "La falla i puede ocurrir"
            evento = str(i+1)
            eventos_posibles.append(evento)
            ####print("u", u)
            ####print("evento", evento)
            ####print("p", probabilidades[i])
    
    probabilidades_filtradas = []
    for e in eventos_posibles:
        i = int(e) - 1
        probabilidades_filtradas.append(probabilidades[i])
    #print("Eventos posibles", eventos_posibles)
    if len(eventos_posibles) > 1:
        "puede ocurrir más de un evento"
        if len(eventos_posibles) == 5:
            "pueden ocurrir 5 eventos"
            #print(eventos_posibles)
            i = dado_cargado_5_1(probabilidades_filtradas, eventos_posibles)
            ####print("Falla", i)
            ####print(probabilidades[int(i)-1])
        elif len(eventos_posibles) == 4:
            "pueden ocurrir 4 eventos"
            #print(eventos_posibles)
            i = dado_cargado_4_1(probabilidades_filtradas, eventos_posibles)
            ####print("Falla", i)
            ####print(probabilidades[int(i)-1])
        elif len(eventos_posibles) == 3:
            "pueden ocurrir 3 eventos"
            #print(eventos_posibles)
            i = dado_cargado_3_1(probabilidades_filtradas, eventos_posibles)
            ####print("Falla", i)
            ####print(probabilidades[int(i)-1])
        elif len(eventos_posibles) == 2:
            "pueden ocurrir 2 eventos"
            #print(eventos_posibles)
            i = dado_cargado_2_1(probabilidades_filtradas, eventos_posibles)
            ####print("Falla", i)
            ####print(probabilidades[int(i)-1])
    if len(eventos_posibles) == 1:
        "ocurre solo 1 evento"
        i = eventos_posibles[0]
        ####print("Falla", i)
        ####print(probabilidades[int(i)-1])
    if len(eventos_posibles) == 0:
        "no ocurre ningun evento"
        i = str(0)
    
    # if int(i) != 0:
    #     print("----------------------")
    #     print("Falla Reactiva del sistema", i)
    #     "Quiero entregar la probabilidad de sobrevivir el evento, dado que falló"
    #     print("La probabilidad de sobrevivir la operación era de", probabilidades[int(i)-1])
    return i 

#i = Tipo_Falla([0, 4000, 5000, 0, 0], cantidades("maintenance_data", "AWOU5IMX"))
#print(i)
#print(type(i))

def mantenciones_por_año(g_mantenciones_2: Generator):
    contador_PM = 0
    contador_RM = 0
    for mantencion in g_mantenciones_2:
        if mantencion.Año == 2018:
            if mantencion.Machine_ID == "AWOU5IMX" and mantencion.Failure_Mode == str(0):
                contador_PM += 1
            elif mantencion.Machine_ID == "AWOU5IMX" and mantencion.Failure_Mode != str(0):
                contador_RM += 1
    total = contador_PM + contador_RM
    return contador_PM, contador_RM, total

# programadas, reactivas, total = mantenciones_por_año(cargar_mantenciones_2("maintenance_data"))
# print("El total de mantenciones programadas para AWOU5IMX el 2018 fueron", programadas)
# print("El total de mantenciones reactivas para AWOU5IMX el 2018 fueron", reactivas)
# print("El total de mantenciones para AWOU5IMX el 2018 fueron", total)

def encontrar_hazzard_og(generador: Generator, horas: int):
    """
    Busca Hazzard en Base a tiempo actual
    """
    resta_minima = 100000
    for hazz in generador:
        resta = abs(hazz.Tiempo - horas)
        if resta < resta_minima:
            resta_minima = resta
            haz_1 = hazz.Haz
            t1 = hazz.Tiempo
            continue
        if resta >= resta_minima:
            haz_2 = hazz.Haz
            t2 = hazz.Tiempo
            break
    haz_2 = haz_1 + ((horas - t1)/(t2 - t1))*(haz_2 - haz_1)
    return haz_1, haz_2

def encontrar_hazzard(generador, t):
    t = abs(t)
    anterior = None
    for hazz in generador:
        # Si encontramos el primer tiempo mayor que t
        if hazz.Tiempo > t:

            t1, haz_1 = anterior.Tiempo, anterior.Haz
            t2, haz_2 = hazz.Tiempo, hazz.Haz
            interpolado = haz_1 + ((t - t1) / (t2 - t1)) * (haz_2 - haz_1)
            return haz_1, interpolado
        anterior = hazz

# h_1, h_2 = encontrar_hazzard(cargar_hazzard("baseline_haz_electrical_filtrado"), 4.45)
# print("H1", h_1)
# print("H2", h_2)

def Cox_Electrico(hazzard: float, kms_per_time: list):
    beta = 4.644819e-05 
    score = beta * kms_per_time
    
    # Calcular la probabilidad de supervivencia
    probabilidad = np.exp(-hazzard * np.exp(score))
    return probabilidad

# p = Cox_Electrico(0, 0)
# print("Probabilidad", p)

def Cox_Motor(hazzard: float, ton_per_time: list, modelo: int):
    beta_1 = 2.843042e-05  
    beta_2 = 5.489886e-01 
    score = beta_1 * ton_per_time + beta_2 * modelo
    
    # Calcular la probabilidad de supervivencia
    probabilidad = np.exp(-hazzard * np.exp(score))
    return probabilidad

def Cox_Escape(hazzard: float, ton_per_time: list):
    beta = 2.312856e-05 
    score = beta * ton_per_time
    
    # Calcular la probabilidad de supervivencia
    probabilidad = np.exp(-hazzard * np.exp(score))
    return probabilidad

def Cox_Hidraulico(hazzard: float, kms_per_time: list):
    beta = 3.683101e-05  
    score = beta * kms_per_time
    
    # Calcular la probabilidad de supervivencia
    probabilidad = np.exp(-hazzard * np.exp(score))
    return probabilidad

def Cox_Suspension(hazzard: float, kms_per_time: list):
    beta = 6.439217e-05   
    score = beta * kms_per_time
    
    # Calcular la probabilidad de supervivencia
    probabilidad = np.exp(-hazzard * np.exp(score))
    return probabilidad

# g_suspension = cargar_hazzard("baseline_haz_suspension")
# haz_suspension = encontrar_hazzard(g_suspension, 10)
# p = Cox_Suspension(haz_suspension, 10)
# print("Probabilidad", p)

#################### PASAR EL TLAST A CADA COX!!!!!!!!!!!!!!!!!!!


def Tipo_Falla_Cox(T_last: list, lista_kms: list, lista_ton: list, ton_teorico_per_time: float, kms_teorico_per_time: float, modelo: int):

    g_electrico = cargar_hazzard("baseline_haz_electrical_filtrado")
    g_motor = cargar_hazzard("baseline_haz_engine_filtrado")
    g_escape = cargar_hazzard("baseline_haz_exhaust_filtrado")
    g_hidraulico = cargar_hazzard("baseline_haz_hydraulic_filtrado")
    g_suspension = cargar_hazzard("baseline_haz_suspension_filtrado")

    haz_e_1, haz_e_2 = encontrar_hazzard(g_electrico, T_last[0])
    haz_m_1, haz_m_2 = encontrar_hazzard(g_motor, T_last[1])
    haz_ex_1, haz_ex_2 = encontrar_hazzard(g_escape, T_last[2])
    haz_h_1, haz_h_2 = encontrar_hazzard(g_hidraulico, T_last[3])
    haz_s_1, haz_s_2 = encontrar_hazzard(g_suspension, T_last[4])

    p_1_el = Cox_Electrico(haz_e_1, lista_kms[0])
    p_2_el = Cox_Electrico(haz_e_2, lista_kms[0] + kms_teorico_per_time)

    p_1_m = Cox_Motor(haz_m_1, lista_ton[1], modelo)
    p_2_m = Cox_Motor(haz_m_2, lista_ton[1] + ton_teorico_per_time, modelo)

    p_1_es = Cox_Escape(haz_ex_1, lista_ton[2])
    p_2_es = Cox_Escape(haz_ex_2, lista_ton[2] + ton_teorico_per_time)

    p_1_h = Cox_Hidraulico(haz_h_1, lista_kms[3])
    p_2_h = Cox_Hidraulico(haz_h_2, lista_kms[3] + kms_teorico_per_time)

    p_1_s = Cox_Suspension(haz_s_1, lista_kms[4])
    p_2_s = Cox_Suspension(haz_s_2, lista_kms[4] + kms_teorico_per_time)

    p_condicionales = [
    p_2_el / p_1_el if p_1_el != 0 else 0,
    p_2_m / p_1_m if p_1_m != 0 else 0,
    p_2_es / p_1_es if p_1_es != 0 else 0,
    p_2_h / p_1_h if p_1_h != 0 else 0,
    p_2_s / p_1_s if p_1_s != 0 else 0
]

    p = [p_2_el, p_2_m, p_2_es, p_2_h, p_2_s]
    # print("PROBABILIDADES", p_condicionales)
    eventos_posibles = []
    u = random.randint(0, 10000)/10000
    # print("UUUUuuuuuuu", u)
    for i in range(5):
        if u > p_condicionales[i]:
            "La falla i puede ocurrir"
            evento = str(i+1)
            eventos_posibles.append(evento)
            # print("UUUUUUUUUUUUUUUUUUUu", u)
            # print("evento", evento)
            # print("PROBABILIDAD", p_condicionales[i])
            
    probabilidades_filtradas = []
    for e in eventos_posibles:
        i = int(e) - 1
        probabilidades_filtradas.append(p_condicionales[i])

    if len(eventos_posibles) > 1:
        "puede ocurrir más de un evento"
        if len(eventos_posibles) == 5:
            "pueden ocurrir 5 eventos"
            i = dado_cargado_5_1(probabilidades_filtradas, eventos_posibles)
            # print("Probabilidades filtradas", probabilidades_filtradas)
            # print("El dado cargado 5 arrojó", i)

        elif len(eventos_posibles) == 4:
            "pueden ocurrir 4 eventos"
            i = dado_cargado_4_1(probabilidades_filtradas, eventos_posibles)
            # print("Probabilidades filtradas", probabilidades_filtradas)
            # print("El dado cargado 4 arrojó", i)

        elif len(eventos_posibles) == 3:
            "pueden ocurrir 3 eventos"
            i = dado_cargado_3_1(probabilidades_filtradas, eventos_posibles)
            # print("Probabilidades filtradas", probabilidades_filtradas)
            # print("El dado cargado 3 arrojó", i)

        elif len(eventos_posibles) == 2:
            "pueden ocurrir 2 eventos"
            i = dado_cargado_2_1(probabilidades_filtradas, eventos_posibles)
            # print("Probabilidades filtradas", probabilidades_filtradas)
            # print("El dado cargado 2 arrojó", i)

    if len(eventos_posibles) == 1:
        "ocurre solo 1 evento"
        i = eventos_posibles[0]
        # print("Probabilidades filtradas", probabilidades_filtradas)
        # print("El dado cargado 1 arrojó", i)

    if len(eventos_posibles) == 0:
        "no ocurre ningun evento"
        i = str(0)

    probabilidades_cox = [p_1_el, p_1_m, p_1_es, p_1_h, p_1_s]
    return i, probabilidades_cox

def Probabilidades_Cox(T_last: list, lista_kms: list, lista_ton: list, modelo: int):

    g_electrico = cargar_hazzard("baseline_haz_electrical")
    g_motor = cargar_hazzard("baseline_haz_engine")
    g_escape = cargar_hazzard("baseline_haz_exhaust")
    g_hidraulico = cargar_hazzard("baseline_haz_hydraulic")
    g_suspension = cargar_hazzard("baseline_haz_suspension")

    haz_electrico = encontrar_hazzard(g_electrico, T_last[0])
    haz_motor = encontrar_hazzard(g_motor, T_last[1])
    haz_escape = encontrar_hazzard(g_escape, T_last[2])
    haz_hidraulico = encontrar_hazzard(g_hidraulico, T_last[3])
    haz_suspension = encontrar_hazzard(g_suspension, T_last[4])

    p_1 = Cox_Electrico(haz_electrico[0], lista_kms[0])

    p_2 = Cox_Motor(haz_motor[0], lista_ton[1], modelo)

    p_3 = Cox_Escape(haz_escape[0], lista_ton[2])

    p_4 = Cox_Hidraulico(haz_hidraulico[0], lista_kms[3])

    p_5 = Cox_Suspension(haz_suspension[0], lista_kms[4])

    probabilidades = [p_1, p_2, p_3, p_4, p_5]
    return probabilidades