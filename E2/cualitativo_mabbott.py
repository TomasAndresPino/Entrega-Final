import time
from datetime import datetime, timedelta
import pandas as pd
import os
# Importar la clase Simulacion desde el archivo correcto
from clases import Simulacion

def simular(umbral, tiempo, años):
    print(f"Simulación umbral: {umbral}\n")

    datos_cualitativos = {
        'Año': [],
        'Fallas_totales': [],
        'Fallas_programadas': [],
        'Fallas_reactivas': [],
        'Tiempo_operacion': [],
        'Tiempo_reparacion': [],
        'Tiempo_sin_operar': [],
        'Factor_toneladas': [],
        'Factor_kilometros': []
    }

    for año in range(años):
        simulacion = Simulacion(tiempo, umbral)
        simulacion.inicio_politica_umbral_Cox()

        fallas_totales = simulacion.camion.CFallas 
        fallas_programadas = simulacion.camion.CFallaP
        fallas_reactivas = fallas_totales - fallas_programadas
        tiempo_operacion = simulacion.camion.TOperacion
        tiempo_reparacion = simulacion.camion.TReparacion
        tiempo_sin_operar = tiempo - tiempo_operacion - tiempo_reparacion
        factor_toneladas = (simulacion.camion.CTT / tiempo_operacion) / tiempo_reparacion if tiempo_reparacion != 0 else 0
        factor_kilometros = (simulacion.camion.CKT / tiempo_operacion) / tiempo_reparacion if tiempo_reparacion != 0 else 0

        datos_cualitativos['Año'].append(2024 + año)
        datos_cualitativos['Fallas_totales'].append(fallas_totales)
        datos_cualitativos['Fallas_programadas'].append(fallas_programadas)
        datos_cualitativos['Fallas_reactivas'].append(fallas_reactivas)
        datos_cualitativos['Tiempo_operacion'].append(tiempo_operacion)
        datos_cualitativos['Tiempo_reparacion'].append(tiempo_reparacion)
        datos_cualitativos['Tiempo_sin_operar'].append(tiempo_sin_operar)
        datos_cualitativos['Factor_toneladas'].append(factor_toneladas)
        datos_cualitativos['Factor_kilometros'].append(factor_kilometros)

    # Guardar datos cualitativos en un archivo CSV
    output_dir = '../Mabbott/Resultados/cualitativo'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    df_cualitativos = pd.DataFrame(datos_cualitativos)
    df_cualitativos.to_csv(os.path.join(output_dir, 'datos_cualitativos_20_años.csv'), index=False)

    print("Datos cualitativos extraídos y guardados.")

# Ejecutar la simulación para 20 años
simular(0.358, 8760, 20)