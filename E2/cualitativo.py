from clases import Simulacion
import time
from datetime import datetime, timedelta
import pandas as pd

def simular(umbral, tiempo):


    print(f"Simulación umbral: {umbral}\n")

    simulacion = Simulacion(tiempo, umbral)
    simulacion.inicio_politica_umbral_Cox()
    fallas_r = simulacion.dias_fallas_r
    fallas_p = simulacion.dias_fallas_p
    
    fecha_inicio = datetime(2024, 1, 1)

    datos_combinados = [(r, "Reactiva") for r in fallas_r] + [(p, "Proactiva") for p in fallas_p]
    datos_combinados.sort(key=lambda x: x[0])
    fechas = []
    for horas, etiqueta in datos_combinados:
        fecha = fecha_inicio + timedelta(hours=horas)
        fecha_formateada = fecha.strftime("%Y-%m-%d %H:%M:%S")
        fechas.append((fecha_formateada, etiqueta))

    # Imprimir las fechas resultantes con su respectiva etiqueta
    for i, (fecha, etiqueta) in enumerate(fechas):
        print(f"Posición {i}: {fecha} - {etiqueta}")

    print(f"\nToneladas cargadas en promedio por dia: {simulacion.camion.CTT/365}")
    print(f"Kilometros cargados en promedio por dia: {simulacion.camion.CKT/365}")








"""
    fallas_totales = simulacion.camion.CFallas 
    fallas_programadas = simulacion.camion.CFallaP
    fallas_reactivas = fallas_totales - fallas_programadas
    Ftotales.append(fallas_totales)
    TReparación.append(simulacion.camion.TReparacion)
    Fprogramadas.append(fallas_programadas)
    Freactivas.append(fallas_reactivas)
    if len(simulacion.tiempos_entre_falla) != 0:
        mtbf.append(sum(simulacion.tiempos_entre_falla) / len(simulacion.tiempos_entre_falla))
    tiempo_op.append(simulacion.camion.TOperacion)
    tiempo_rep.append(simulacion.camion.TReparacion)
    tiempo_sin.append(tiempo - simulacion.camion.TOperacion - simulacion.camion.TReparacion)

    

        
    print(f"Fallas totales promedio: {sum(Ftotales)/len(Ftotales)}")
    print(f"Fallas programadas promedio: {sum(Fprogramadas)/len(Fprogramadas)}")
    print(f"Fallas reactivas promedio: {sum(Freactivas)/len(Freactivas)}")
    print(f"Tiempo promedio entre fallas: {sum(mtbf) / len(mtbf)}")
    print(f"Tiempo de operacion promedio: {sum(tiempo_op) / len(tiempo_op)}")
    print(f"Tiempo sin operar promedio: {sum(tiempo_sin) / len(tiempo_sin)}")
    print(f"Tiempo de Operacion/Tiempo de Reparacion: {sum(tiempo_op)/sum(tiempo_rep)}")  
    print(f"Tiempo de reparació total promedio: {sum(TReparación)/len(TReparación)}")
    print(f"\n\nTiempo total de ejecución para {cantidad_x_umbral} repeticiones de {tiempo/8640} año/s es: {time.time() - start} segundos")
"""
simular(0.3,8640)

