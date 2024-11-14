from clases import Simulacion
import time
import datetime

def simular(umbrales, cantidad_x_umbral, tiempo):

    for umbral in umbrales:
        print(f"Simulación umbral: {umbral}\n")
        start = time.time()
        Ftotales = list()
        Fprogramadas = list()
        Freactivas = list()
        mtbf = list()
        tiempo_op = list()
        tiempo_rep = list()
        tiempo_sin = list()
        
        for i in range (cantidad_x_umbral):
            

            simulacion = Simulacion(tiempo, umbral)
            simulacion.inicio_politica_umbral_Cox()

            fallas_totales = simulacion.camion.CFallas 
            fallas_programadas = simulacion.camion.CFallaP
            fallas_reactivas = fallas_totales - fallas_programadas
            Ftotales.append(fallas_totales)
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
        print(f"\n\nTiempo total de ejecución para {cantidad_x_umbral} repeticiones de {tiempo/8640} año/s es: {time.time() - start} segundos")

        var1 = sum(Ftotales)/len(Ftotales)
        var2 = sum(Fprogramadas)/len(Fprogramadas)
        var3 = sum(Freactivas)/len(Freactivas)
        var4 = sum(mtbf) / len(mtbf)
        var5 = sum(tiempo_op) / len(tiempo_op)
        var6 = sum(tiempo_sin) / len(tiempo_sin)
        var7 = sum(tiempo_op)/sum(tiempo_rep)

        # Nombre del archivo de texto donde se guardarán los resultados
        log_file = "resultados_simulacion.txt"

        # Obtener la fecha y hora actuales para registrar cuándo se ejecutó
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Crear el formato de texto que deseas guardar
        log_text = f"""
        === Ejecución: {timestamp} umbral {umbral} ===
        Fallas totales promedio: {var1}
        Fallas programadas promedio: {var2}
        Fallas reactivas promedio: {var3}
        Tiempo promedio entre fallas: {var4}
        Tiempo de operacion promedio: {var5}
        Tiempo sin operar promedio: {var6}
        Tiempo de Operacion/Tiempo de Reparacion: {var7}
        Tiempo total de ejecución para {cantidad_x_umbral} repeticiones de {tiempo/8640} año/s es: {time.time() - start} segundos
        =============================
        """

        # Escribir en el archivo en modo 'append' (agregar al final)
        with open(log_file, "a", encoding="utf-8") as file:
            file.write(log_text)

        print("Valores guardados en 'resultados_simulacion.txt'")   
                    

simular([0.6, 0.4], 1, 8640)


