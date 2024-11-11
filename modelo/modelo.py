import gurobipy as gp
from gurobipy import GRB
import numpy as np
import random


###############################################################################################################################################
# Conjuntos, función h() y parametros #
###############################################################################################################################################

# Información de los camiones (Machine_ID)
camiones = [
    'AWOU5IMX', '6VABNMFW', '7PML7DX0', 'WVSI44XE', '12ZHA8WI', 'H4R6Y02Y',
    '3A6STZAR', 'TS5TPP35', 'HLU6OU9B', 'OKU9UWCY', 'LYRHF3HX', 'JIRK0F5R'
]

# Tipos de falla para las mantenciones no programadas
tipos_falla = [1, 2, 3, 4, 5]

# Parámetros
meses = 12  # Para cubrir un año completo
horas_por_mes = 720
horas_total = meses * horas_por_mes

# Capacidades máximas de carga por hora (en toneladas)
carga_maxima = {
    'AWOU5IMX': 420,
    '6VABNMFW': 450,
    '7PML7DX0': 400,
    'WVSI44XE': 405,
    '12ZHA8WI': 380,
    'H4R6Y02Y': 370,
    '3A6STZAR': 400,
    'TS5TPP35': 330,
    'HLU6OU9B': 360,
    'OKU9UWCY': 390,
    'LYRHF3HX': 320,
    'JIRK0F5R': 340
}

# kilometros maximos recorridos por hora (en km)
kilometros_maximos = {
    'AWOU5IMX': 30,
    '6VABNMFW': 35,
    '7PML7DX0': 15,
    'WVSI44XE': 22,
    '12ZHA8WI': 27,
    'H4R6Y02Y': 29,
    '3A6STZAR': 34,
    'TS5TPP35': 40,
    'HLU6OU9B': 18,
    'OKU9UWCY': 19,
    'LYRHF3HX': 22,
    'JIRK0F5R': 37
}

#M
M = 1000000000000000000000000000000000000000000000000000

# Demandas anuales de carga (en toneladas)
demanda_carga = {
    'AWOU5IMX': 1500000,
    '6VABNMFW': 1700000,
    '7PML7DX0': 1600000,
    'WVSI44XE': 1800000,
    '12ZHA8WI': 1400000,
    'H4R6Y02Y': 1650000,
    '3A6STZAR': 1750000,
    'TS5TPP35': 1580000,
    'HLU6OU9B': 1620000,
    'OKU9UWCY': 1700000,
    'LYRHF3HX': 1600000,
    'JIRK0F5R': 1540000
}

# Demandas anuales de kilómetros (en km)
demanda_km = {
    'AWOU5IMX': 60000,
    '6VABNMFW': 70000,
    '7PML7DX0': 65000,
    'WVSI44XE': 75000,
    '12ZHA8WI': 58000,
    'H4R6Y02Y': 68000,
    '3A6STZAR': 72000,
    'TS5TPP35': 64000,
    'HLU6OU9B': 66000,
    'OKU9UWCY': 70000,
    'LYRHF3HX': 65000,
    'JIRK0F5R': 62000
}


# Función h(KA_it, CA_it): Crece con los kilómetros y la carga acumulada
def h(KA_it, CA_it, t, i):
    """Función que representa la probabilidad de falla basada en los kilómetros y carga acumulada"""
    return (KA_it + CA_it) / (t * (kilometros_maximos[i] + carga_maxima[i]))

# Umbral para entrar a 


###############################################################################################################################################
# VARIABLES #
###############################################################################################################################################

# Crear el modelo de Gurobi
model = gp.Model("Minimizar_mantenimiento_camiones")


# Variables binarias para el mantenimiento no programado por tipo de falla
TMNP = model.addVars(tipos_falla, camiones, horas_total, vtype=GRB.BINARY, name="TMNP")  # Mantenimiento no programado

# Variables binarias para el mantenimiento programado (sin tipos de falla)
TMP = model.addVars(camiones, horas_total, vtype=GRB.BINARY, name="TMP")  # Mantenimiento programado

# Variables continuas para kilómetros acumulados y carga acumulada
KA = model.addVars(camiones, horas_total, vtype=GRB.CONTINUOUS, name="KA")  # Kilómetros acumulados
CA = model.addVars(camiones, horas_total, vtype=GRB.CONTINUOUS, name="CA")  # Carga acumulada

# Variables continuas para kilómetros y carga en cada hora
K = model.addVars(camiones, horas_total, vtype=GRB.CONTINUOUS, name="K")  # Kilómetros andados por el camion i en la hora t
C = model.addVars(camiones, horas_total, vtype=GRB.CONTINUOUS, name="C")  # Carga llevada por el camion i en la hora t


###############################################################################################################################################
# Funcion Objetivo #
###############################################################################################################################################

# **Función objetivo: minimizar la suma de TMNP y TMP**
model.setObjective(gp.quicksum(TMNP[f, i, t] for f in tipos_falla for i in camiones for t in range(horas_total)) + 
                   gp.quicksum(TMP[i, t] for i in camiones for t in range(horas_total)), GRB.MINIMIZE)


###############################################################################################################################################
# Restricciones #
###############################################################################################################################################

# **Restricción 1**: Solo un tipo de mantenimiento a la vez
for i in camiones:
    for t in range(horas_total):
        model.addConstr(gp.quicksum(TMNP[f, i, t] for f in tipos_falla) + TMP[i, t] <= 1, f"R1_{i}_{t}")

# **Restricción 2**: Los camiones no pueden cargar si estan en mantenimientos no porgramados
for i in camiones:
    for t in range(1, horas_total):
        model.addConstr(C[i, t] <= (1 - gp.quicksum(TMNP[f, i, t] for f in tipos_falla)) * M, f"R2_{i}_{t}")

# **Restricción 3**: Los camiones no pueden cargar si estan en mantenimientos programados
for i in camiones:
    for t in range(1, horas_total):
        model.addConstr(C[i, t] <= (1 - TMP[i, t]) * M, f"R3_{i}_{t}")

# **Restricción 4**: Los camiones no pueden andar si estan en mantenimientos no porgramados
for i in camiones:
    for t in range(1, horas_total):
        model.addConstr(K[i, t] <= (1 - gp.quicksum(TMNP[f, i, t] for f in tipos_falla)) * M, f"R4_{i}_{t}")

# **Restricción 5**: Los camiones no pueden andar si estan en mantenimientos programados
for i in camiones:
    for t in range(1, horas_total):
        model.addConstr(K[i, t] <= (1 - TMP[i, t]) * M, f"R5_{i}_{t}")

# **Restricción 6**: Cumplir demanda anual de toneladas cargadas
for i in camiones:
    model.addConstr(gp.quicksum(C[i, t] for t in range (horas_total)) >= demanda_carga[i], f"R6_{i}")

# **Restricción 7**: Cumplir demanda anual de kilometros recorridos
for i in camiones:
    model.addConstr(gp.quicksum(K[i, t] for t in range (horas_total)) >= demanda_km[i], f"R6_{i}")

# **Restricción 8**: Maximo de carga por hora
for i in camiones:
    for t in range(horas_total):
        model.addConstr(C[i, t] <= carga_maxima[i], f"R8_{i}_{t}")

# **Restricción 9**: Maximos kilometros recorridos por hora
for i in camiones:
    for t in range(horas_total):
        model.addConstr(K[i, t] <= kilometros_maximos[i], f"R9_{i}_{t}")

# **Restricción 10**: def Km acumulado y reinicio de este post mantenimiento
for i in camiones:
    for t in range (horas_total):
        if t == 0:
            model.addConstr(KA[i, t] == 0, f"R10_KA_inicio_{i}_{t}")  # Inicializa KA en 0 para t = 0
        else:
            model.addConstr(KA[i, t] == (KA[i, t-1] + K[i, t]) * (1 - (gp.quicksum(TMNP[f, i, t] for f in tipos_falla) + TMP[i, t])), f"R10_{i}_{t}")

# **Restricción 11**: def carga acumulada y reinicio de este post mantenimiento
for i in camiones:
    for t in range (horas_total):
        if t == 0:
            model.addConstr(CA[i, t] == 0, f"R10_CA_inicio_{i}_{t}")  # Inicializa CA en 0 para t = 0
        else:
            model.addConstr(CA[i, t] == (CA[i, t-1] + C[i, t]) * (1 - (gp.quicksum(TMNP[f, i, t] for f in tipos_falla) + TMP[i, t])), f"R10_{i}_{t}")

# **Restricción 13**: Prob{TMNP = 1} = h()
for i in camiones:
    for t in range(horas_total):
        h_value = h(KA[i, t], CA[i, t], t, i)
        valor_aleatorio = random.uniform(0, 1)

         # Restringir TMNP a ser 1 si valor_aleatorio > h_value
        model.addConstr(TMNP[1, i, t] >= (valor_aleatorio - h_value) / M, f"TMNP_must_be_1_{i}_{t}")

        # Restringir TMNP a ser 0 si valor_aleatorio <= h_value
        model.addConstr(TMNP[1, i, t] <= (h_value - valor_aleatorio + M) / M, f"TMNP_must_be_0_{i}_{t}")

















# **Restricción 3**: No se puede acumular kilómetros si está en mantenimiento programado
for i in camiones:
    for t in range(1, horas_total):
        model.addConstr(KA[i, t] == (KA[i, t-1] + 1) * (1 - TMP[i, t]), f"R3_KA_{i}_{t}")

# **Restricción 4**: El camión no puede andar si está en mantenimiento
for i in camiones:
    for t in range(horas_total):
        if t == 0:
            model.addConstr(KA[i, t] == 0, f"R4_KA_inicio_{i}_{t}")  # Inicializa KA en 0 para t = 0
            model.addConstr(CA[i, t] == 0, f"R4_CA_inicio_{i}_{t}")  # Inicializa CA en 0 para t = 0
        else:
            model.addConstr(KA[i, t] == (1 - TMP[i, t]) * KA[i, t-1], f"R4_KA_no_andar_{i}_{t}")
            model.addConstr(CA[i, t] == (1 - TMP[i, t]) * CA[i, t-1], f"R4_CA_no_andar_{i}_{t}")

# **Restricción 5**: Cumplimiento de demandas de carga y kilometraje
for i in camiones:
    demanda_km = 50000  # Ajustable según el caso
    demanda_carga = 20000  # Ajustable según el caso
    model.addConstr(gp.quicksum(KA[i, t] for t in range(horas_total)) >= demanda_km, f"R5_demanda_km_{i}")
    model.addConstr(gp.quicksum(CA[i, t] for t in range(horas_total)) >= demanda_carga, f"R5_demanda_carga_{i}")

# **Restricción 10**: Acumulación de kilómetros y carga
for i in camiones:
    for t in range(1, horas_total):
        # Kilómetros acumulados
        model.addConstr(KA[i, t] == KA[i, t-1] + (1 - gp.quicksum(TMNP[f, i, t] for f in tipos_falla) - TMP[i, t]), f"R10_KA_{i}_{t}")
        # Carga acumulada
        model.addConstr(CA[i, t] == CA[i, t-1] + (1 - gp.quicksum(TMNP[f, i, t] for f in tipos_falla) - TMP[i, t]), f"R10_CA_{i}_{t}")

# **Restricción 12**: Tiempo mínimo de mantenimiento (distribuciones normales)
# Para TMNP (mantenimiento no programado)
mu_TMNP = 1000  # Media de horas de fallo no programado
sigma_TMNP = 200  # Desviación estándar
for i in camiones:
    for f in tipos_falla:
        for t in range(horas_total):
            prob_falla = h(KA[i, t], CA[i, t])  # Probabilidad de fallo en función de KA y CA
            model.addConstr(TMNP[f, i, t] <= prob_falla, f"R12_TMNP_{f}_{i}_{t}")

# Para TMP (mantenimiento programado)
mu_TMP = 1000  # Media para mantenimiento programado
sigma_TMP = 200  # Desviación estándar
for i in camiones:
    for t in range(horas_total):
        prob_mantenimiento = h(KA[i, t], CA[i, t])
        model.addConstr(TMP[i, t] <= prob_mantenimiento, f"R12_TMP_{i}_{t}")

# Optimizar el modelo
model.optimize()

# Verificar los resultados
if model.status == GRB.OPTIMAL:
    print("Tiempo mínimo fuera de servicio:", model.objVal)
    for i in camiones:
        for t in range(horas_total):
            for f in tipos_falla:
                if TMNP[f, i, t].x > 0.5:
                    print(f"Camión {i} en mantenimiento no programado por falla {f} en la hora {t}")
            if TMP[i, t].x > 0.5:
                print(f"Camión {i} en mantenimiento programado en la hora {t}")

