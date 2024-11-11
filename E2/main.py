from clases import Simulacion
import time

contador = 0
porcentajes = []
if __name__ == "__main__":
    start = time.time()

    # mtbf = list()
    # fallas = list()
    # tiempo_op = list()
    # tiempo_rep = list()
    Ftotales = list()
    Fprogramadas = list()
    Freactivas = list()
    # tiempo_sin = list()
    # veces_20_dias = list()


    # simulacion = Simulacion(34560, 0.55)
    # simulacion.inicio_politica_4()
    # simulacion.KPIs()


    for i in range (50):
        contador += 1
        simulacion = Simulacion(8640, 0.6)
        simulacion.inicio_politica_5()
    # #   simulacion.inicio_politica_3()
    #     simulacion.inicio_politica_1()
        # if len(simulacion.tiempos) != 0:
        #     mtbf.append(sum(simulacion.tiempos) / len(simulacion.tiempos))
        # if len(simulacion.fallas) != 0:
        #     fallas.append(sum(simulacion.fallas) / len(simulacion.fallas)) #tiempo promedio de falla
        # tiempo_op.append(simulacion.camion.TOperacion)
        # tiempo_rep.append(simulacion.camion.TReparacion)
        fallas_totales = simulacion.camion.CFallas 
        fallas_programadas = simulacion.camion.CFallaP
        fallas_reactivas = fallas_totales - fallas_programadas
        Ftotales.append(fallas_totales)
        Fprogramadas.append(fallas_programadas)
        Freactivas.append(fallas_reactivas)

    #     tiempo_sin.append(3000 - simulacion.camion.TOperacion - simulacion.camion.TReparacion)
    #     veces_20_dias.append(simulacion.contador_20_dias) 

        print(f"Simulación n°{contador} de {simulacion.T} horas.")
    #     ######################3#simulacion.KPIs()
    
    end = time.time()
    tiempo_usado = end - start

    # with open("umbral_03_operacion.txt", "w") as archivo_1:
    #     for tiempo in tiempo_op:
    #         archivo_1.write(str(tiempo) + "\n")
    # with open("umbral_03_reparacion.txt", "w") as archivo_2:
    #     for tiempo in tiempo_rep:
    #         archivo_2.write(str(tiempo) + "\n")
    
    # with open("tiempos_reparacion_CASOBASE2.txt", "w") as archivo_1:
    #     for tiempo in tiempo_rep:
    #         archivo_1.write(str(tiempo) + "\n")
    # with open("tiempos_operacion_CASOBASE2.txt", "w") as archivo_2:
    #     for tiempo in tiempo_op:
    #         archivo_2.write(str(tiempo) + "\n")
    # with open("tiempos_sin_operar_20dias.txt", "w") as archivo_3:
    #     for tiempo in tiempo_sin:
    #         archivo_3.write(str(tiempo) + "\n")
    # with open("tiempo_promedio_entre_fallas_CASOBASE2.txt", "w") as archivo_4:
    #     for tiempo in mtbf:
    #         archivo_4.write(str(tiempo) + "\n")


    print("Umbral 06")
    print()


    # print("Caso cada 20 dias mantener!")
    # print(f"Tiempo promedio entre fallas: {sum(mtbf) / len(mtbf)}")
    # print(f"Tiempo sin operar: {sum(tiempo_sin) / len(tiempo_sin)}")




    # # # # print(f"Tiempo de operacion: {sum(tiempo_op) / len(tiempo_op)}")
    # # # # print(f"Tiempo en Reparacion: {sum(tiempo_rep) / len(tiempo_rep)}")
    print(f"Fallas totales promedio {sum(Ftotales)/len(Ftotales)}")
    print(f"Fallas programadas promedio {sum(Fprogramadas)/len(Fprogramadas)}")
    print(f"Fallas reactivas promedio {sum(Freactivas)/len(Freactivas)}")





    #print(f"Tiempo de operacion/Tiempo de Reparacion: {sum(tiempo_op)/sum(tiempo_rep)}")
    # print(f"Duracion promedio de las mantenciones: {sum(fallas) / len(fallas)}")  
    # print(f"La cantidad de veces que pasaron 20 días fue: {sum(veces_20_dias) / len(veces_20_dias)}")

    print(f"Tiempo total de ejecución para 50 rep, 1 año es: {tiempo_usado:.2f} segundos")      