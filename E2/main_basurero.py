from clases import Simulacion

contador = 0
porcentajes = []
if __name__ == "__main__":
    #while contador < 30:
        #simulacion = Simulacion()
        #simulacion.inicio_politica_2()
        ##simulacion.KPIs()
        #percentage = simulacion.KPI_porcentaje_ut()
        #porcentajes.append(percentage)
        #contador += 1
    #for p in porcentajes:
        #print(p)
    porcentaje_operacion = 0
    tons = 0
    kms = 0
    tiempo_reparacion = 0
    tiempo_operacion = 0
    tiempos = list()
    fallas = list()
    tiempo_op = list()
    tiempo_rep = list()
    tiempo_sin = list()
    for i in range (30):
        simulacion = Simulacion(3000, 0.7)
        simulacion.inicio_politica_3()
        #porcentaje_operacion += (simulacion.camion.TOperacion/1200)
        #tons += simulacion.camion.CTT
        #kms += simulacion.camion.CKT
        #tiempo_reparacion += simulacion.camion.TReparacion
        #tiempo_operacion += simulacion.camion.TOperacion
        if len(simulacion.tiempos) != 0:
            tiempos.append(sum(simulacion.tiempos) / len(simulacion.tiempos))
        if len(simulacion.fallas) != 0:
            fallas.append(sum(simulacion.fallas) / len(simulacion.fallas))
        tiempo_op.append(simulacion.camion.TOperacion)
        tiempo_rep.append(simulacion.camion.TReparacion)
        tiempo_sin.append(tiempo_sin)


        simulacion.KPIs()

    
    print("Caso 0.7!")
    print(f"Tiempo promedio entre fallas: {sum(tiempos) / len(tiempos)}")
    print(f"Tiempo sin operar: {sum(tiempo_sin) / len(tiempo_sin)}")
    print(f"Tiempo de operacion: {sum(tiempo_op) / len(tiempo_op)}")
    print(f"Tiempo en Reparacion: {sum(tiempo_rep) / len(tiempo_rep)}")
    print(f"Tiempo de operacion/Tiempo de Reparacion: {simulacion.camion.TOperacion/simulacion.camion.TReparacion}")
    print(f"Duracion promedio de las mantenciones: {sum(fallas) / len(fallas)}")

    # while contador < 20:
    #     simulacion = Simulacion()
    #     simulacion.inicio_politica_3()
    #     percentage = simulacion.KPI_porcentaje_ut()
    #     porcentajes.append(percentage)
    #     contador += 1
    # for p in porcentajes:
    #    print(p)