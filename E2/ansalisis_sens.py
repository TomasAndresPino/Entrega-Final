from clases import Simulacion
import time
import datetime
import pandas as pd

# Definir la función frange
def frange(start, stop, step):
    while start <= stop:
        yield start
        start += step

secuencia = [round(x, 3) for x in frange(0.282, 0.29, 0.001)]


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
        lista_n_simulaciones = list()
        lista_umbrales = list()
        lista_kms = list()
        lista_tons = list()
        for i in range (cantidad_x_umbral):
            print(f"Simulación número {i}")
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
            lista_n_simulaciones.append(i+1)
            lista_umbrales.append(umbral)
            lista_kms.append(simulacion.camion.CKT)
            lista_tons.append(simulacion.camion.CTT)
            
        print(f"Fallas totales promedio: {sum(Ftotales)/len(Ftotales)}")
        print(f"Fallas programadas promedio: {sum(Fprogramadas)/len(Fprogramadas)}")
        print(f"Fallas reactivas promedio: {sum(Freactivas)/len(Freactivas)}")
        print(f"Tiempo promedio entre fallas: {sum(mtbf) / len(mtbf)}")
        print(f"Tiempo de operacion promedio: {sum(tiempo_op) / len(tiempo_op)}")
        print(f"Tiempo sin operar promedio: {sum(tiempo_sin) / len(tiempo_sin)}")
        print(f"Tiempo de Operacion/Tiempo de Reparacion: {sum(tiempo_op)/sum(tiempo_rep)}")  
        print(f"\n\nTiempo total de ejecución para {cantidad_x_umbral} repeticiones de {tiempo/8640} año/s es: {time.time() - start} segundos")
        var0 = lista_n_simulaciones
        var1 = (Ftotales)
        var2 = (Fprogramadas)
        var3 = (Freactivas)
        var4 = (mtbf)
        var5 = (tiempo_op)
        var6 = (tiempo_sin)
        var7 = [op / rep if rep != 0 else None for op, rep in zip(tiempo_op, tiempo_rep)]
        var8 = tiempo_rep
        var9 = lista_kms
        var10 = lista_tons

        data = {
            "Umbral": lista_umbrales,
            "N_simulacion": var0,
            "Fallas totales promedio": var1,
            "Fallas programadas promedio": var2,
            "Fallas reactivas promedio": var3,
            "Tiempo promedio entre fallas": var4,
            "Tiempo de operacion promedio": var5,
            "Tiempo sin operar promedio": var6,
            "Tiempo de Operacion/Tiempo de Reparacion": var7,
            "Tiempo_Reparacion": var8,
            "Kilometros totales": var9,
            "Toneladas totales": var10
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

valores_simulados = [
    0.358
]

simular(valores_simulados, 10, 8760)