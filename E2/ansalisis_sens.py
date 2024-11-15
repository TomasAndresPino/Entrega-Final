from clases import Simulacion
import time
import datetime
import pandas as pd

def simular(umbrales, cantidad_x_umbral, tiempo):

    for umbral in umbrales:
        print(f"Simulación umbral: {umbral}\n")
        start = time.time()
        Ftotales = list()
        Fprogramadas = list()
        Freactivas = list()
        TReparación = list()
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
        
        var1 = sum(Ftotales)/len(Ftotales)
        var2 = sum(Fprogramadas)/len(Fprogramadas)
        var3 = sum(Freactivas)/len(Freactivas)
        var4 = sum(mtbf) / len(mtbf)
        var5 = sum(tiempo_op) / len(tiempo_op)
        var6 = sum(tiempo_sin) / len(tiempo_sin)
        var7 = sum(tiempo_op)/sum(tiempo_rep)
        var8 = sum(TReparación)/len(TReparación)

        data = {
            "Umbral": [umbral],
            "Fallas totales promedio": [var1],
            "Fallas programadas promedio": [var2],
            "Fallas reactivas promedio": [var3],
            "Tiempo promedio entre fallas": [var4],
            "Tiempo de operacion promedio": [var5],
            "Tiempo sin operar promedio": [var6],
            "Tiempo de Operacion/Tiempo de Reparacion": [var7],
            "Tiempo de reparació total promedio": [var8]
        }
                    
        df_new = pd.DataFrame(data)

        # Nombre del archivo CSV donde se guardarán los datos
        csv_file = "registro_variables.csv"

        try:
            # Intentar leer el archivo CSV existente
            df_existing = pd.read_csv(csv_file)

            # Concatenar el nuevo DataFrame con el existente
            df_final = pd.concat([df_existing, df_new], ignore_index=True)

        except FileNotFoundError:
            # Si el archivo no existe, usar solo el nuevo DataFrame
            df_final = df_new

        # Guardar el DataFrame en el archivo CSV
        df_final.to_csv(csv_file, index=False, encoding="utf-8")

        print("Valores guardados en 'registro_variables.csv'.")

simular([0.1, 0.12, 0.14, 0.16, 0.18], 2, 8640)


#[0.1, 0.12, 0.14, 0.16, 0.18] asi se deberia ver la lista

#mauro simula desde 0.1 0.18 de 0.02 en 0.02
#pino simula desde 0.2 hasta 0.28 de 0.02 en 0.02
#manuel simula desde 0.3 hasta 0.38 de 0.02 en 0.02
#mabbot simula desde 0.4 hasta 0.48 de 0.02 en 0.02





