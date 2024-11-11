from clases import Simulacion
import time

"""
Este código estará construido para correr los 2 casos base y el caso política.
Caso base 1 (Mantenciones Reactivas): estará en inicio_politica_3()
Caso base 2 (Mantenciones programadas año 2020 para camión AWOU5IMX): estará en inicio_politica_2()
Politica (Umbral Óptimo): estará en inicio_politica_4()
"""
contador = 0
porcentajes = []
if __name__ == "__main__":
    start = time.time()

    mtbf = list() # Esta lista guarda los tiempos promedio entre fallas para cada simulación
    fallas = list() # Esta lista guarda los tiempos de las fallas, para cada simulación
    tiempo_op = list() # Esta lista guarda los tiempos de operación, para cada simulación
    tiempo_rep = list() # Esta lista guarda los tiempos de reparación, para cada simulación
    tiempo_sin = list() # Esta lista guarda los tiempos de ocio (yo la sacaría), para cada simulación

    Ftotales = list() # Esta lista guarda las fallas totales, para cada simulación
    Fprogramadas = list() # Esta lista guarda las fallas programadas, para cada simulación
    Freactivas = list() # Esta lista guarda las fallas reactivas, para cada simulación

    for i in range (50):
        contador += 1
        """
        Se crean simulaciones de 1 año, el segundo parámetro es el umbral.
        Si se corre politica_3 para evitar errores, poner umbral = 0.
        Cambiar la política según lo que se quiera analizar
        """
        simulacion = Simulacion(8640, 0.6)
        simulacion.inicio_politica_4()
        if len(simulacion.tiempos) != 0:
            mtbf.append(sum(simulacion.tiempos) / len(simulacion.tiempos))
        if len(simulacion.fallas) != 0:
            fallas.append(sum(simulacion.fallas) / len(simulacion.fallas)) 
        tiempo_op.append(simulacion.camion.TOperacion)
        tiempo_rep.append(simulacion.camion.TReparacion)
        fallas_totales = simulacion.camion.CFallas 
        fallas_programadas = simulacion.camion.CFallaP
        fallas_reactivas = fallas_totales - fallas_programadas
        Ftotales.append(fallas_totales)
        Fprogramadas.append(fallas_programadas)
        Freactivas.append(fallas_reactivas)

        tiempo_sin.append(8640 - simulacion.camion.TOperacion - simulacion.camion.TReparacion)

        print(f"Simulación n°{contador} de {simulacion.T} horas.")
    
    end = time.time()
    tiempo_usado = end - start

    """
    Ahora en distintos archivos se guardan los resultados respectivos 
    (Esto se recomienda para guardar los resultados y graficar lo que queramos con ellos).

    Se recomienda llevar todo a un excel para hacer los cálculos.

    Se recomienda cambiar los nombres de los archivos según la política que se corra.

    Nombres recomendados:
    - tiempos_reparacion_CASOBASE1
    - tiempos_reparacion_CASOBASE2
    - tiempos_reparacion_POLITICA
    (Se sigue la idea para los otros archivos)
    """
    with open("tiempos_reparacion_NOMBRE.txt", "w") as archivo_1:
        for tiempo in tiempo_rep:
            archivo_1.write(str(tiempo) + "\n")
    with open("tiempos_operacion_NOMBRE.txt", "w") as archivo_2:
        for tiempo in tiempo_op:
            archivo_2.write(str(tiempo) + "\n")
    with open("tiempos_sin_operar_NOMBRE.txt", "w") as archivo_3:
        for tiempo in tiempo_sin:
            archivo_3.write(str(tiempo) + "\n")
    with open("tiempo_promedio_entre_fallas_NOMBRE.txt", "w") as archivo_4:
        for tiempo in mtbf:
            archivo_4.write(str(tiempo) + "\n")

    """
    Estos resultados también se recomienda guardarlos.
    """
    print("Otros Indicadores Útiles")
    print()
    print(f"Fallas totales promedio {sum(Ftotales)/len(Ftotales)}")
    print(f"Fallas programadas promedio {sum(Fprogramadas)/len(Fprogramadas)}")
    print(f"Fallas reactivas promedio {sum(Freactivas)/len(Freactivas)}")
    print(f"Tiempo total de ejecución para 100 simulaciones: {tiempo_usado:.2f} segundos")   