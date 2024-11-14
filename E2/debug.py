import numpy as np

def tiempo_hasta_falla_cox(hazard_base, kms_per_time, beta):
    """
    Simula el tiempo hasta la falla basado en un modelo de Cox.
    
    Parámetros:
    - hazard_base: Tasa base de riesgo (hazard)
    - kms_per_time: Lista de kilómetros acumulados por unidad de tiempo.
    - beta: Coeficiente de riesgo asociado con kilómetros.
    
    Retorna:
    - Tiempo hasta la falla basado en la simulación.
    """
    # Calcula el score basado en los kilómetros y el coeficiente beta
    score = beta * np.sum(kms_per_time)
    hazard = hazard_base * np.exp(score)
    
    # Genera un valor aleatorio exponencial con la tasa de riesgo calculada
    tiempo_falla = np.random.exponential(1 / hazard)
    
    return tiempo_falla

# Ejemplo de uso:
hazard_base = 0.01       # Tasa base de riesgo
kms_per_time = [100, 120, 150]  # Kilómetros por cada unidad de tiempo
beta = 4.644819e-05      # Coeficiente beta

# Calcula el tiempo hasta la falla
tiempo_falla = tiempo_hasta_falla_cox(hazard_base, kms_per_time, beta)
print("Tiempo estimado hasta la falla:", tiempo_falla)
