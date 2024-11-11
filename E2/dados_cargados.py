import random

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
    #print("prob cargadas", p)
    u = random.uniform(0, 1)
    if 0 <= u < p[0]:
        i = eventos_posibles[0]
    elif p[0] <= u <= 1:
        i = eventos_posibles[1]
    return i

#i = dado_cargado_2({"1": 769, "2": 300, "3": 40, "4": 211, "5": 135}, ["2", "3"])
#print(i)

def dado_cargado_5_1(probabilidades_filtradas: list, eventos_posibles: list):
    ###############################u = random.uniform(0, 1)
    u = random.randint(0, 10000)/10000
    total = 0
    for p in probabilidades_filtradas:
        total += p
    p_1 = probabilidades_filtradas[0]/total
    p_2 = probabilidades_filtradas[1]/total
    p_3 = probabilidades_filtradas[2]/total
    p_4 = probabilidades_filtradas[3]/total
    p_5 = probabilidades_filtradas[4]/total
    if 0 <= u < p_1:
        i = 1
    elif p_1 <= u < p_1 + p_2:
        i = 2
    elif p_1 + p_2 <= u < p_1 + p_2 + p_3:
        i = 3
    elif p_1 + p_2 + p_3 <= u < p_1 + p_2 + p_3 + p_4:
        i = 4
    else:
        i = 5
    return str(i)

def dado_cargado_4_1(probabilidades_filtradas: list, eventos_posibles: list):
    #################################u = random.uniform(0, 1)
    u = random.randint(0, 10000)/10000
    total = 0
    for p in probabilidades_filtradas:
        total += p
    p_1 = probabilidades_filtradas[0]/total
    p_2 = probabilidades_filtradas[1]/total
    p_3 = probabilidades_filtradas[2]/total
    p_4 = probabilidades_filtradas[3]/total
    if 0 <= u < p_1:
        i = 1
    elif p_1 <= u < p_1 + p_2:
        i = 2
    elif p_1 + p_2 <= u < p_1 + p_2 + p_3:
        i = 3
    else:
        i = 4
    evento = eventos_posibles[i-1]
    return evento

def dado_cargado_3_1(probabilidades_filtradas: list, eventos_posibles: list):
    #################################u = random.uniform(0, 1)
    u = random.randint(0, 10000)/10000
    total = 0
    for p in probabilidades_filtradas:
        total += p
    p_1 = probabilidades_filtradas[0]/total
    p_2 = probabilidades_filtradas[1]/total
    p_3 = probabilidades_filtradas[2]/total
    if 0 <= u < p_1:
        i = 1
    elif p_1 <= u < p_1 + p_2:
        i = 2
    else:
        i = 3
    evento = eventos_posibles[i-1]
    return evento

def dado_cargado_2_1(probabilidades_filtradas: list, eventos_posibles: list):
    ####################################3u = random.uniform(0, 1)
    u = random.randint(0, 10000)/10000
    total = 0
    for p in probabilidades_filtradas:
        total += p
    p_1 = probabilidades_filtradas[0]/total
    p_2 = probabilidades_filtradas[1]/total
    if 0 <= u < p_1:
        i = 1
    else:
        i = 2
    evento = eventos_posibles[i-1]
    return evento
