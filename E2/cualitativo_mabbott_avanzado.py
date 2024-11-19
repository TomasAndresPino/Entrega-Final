import time
from datetime import datetime, timedelta
import pandas as pd
import os
# Importar la clase Simulacion desde el archivo correcto
from clases_mabbott import Simulacion

def simular(umbral, tiempo):
    print(f"Simulación umbral: {umbral}\n")

    simulacion = Simulacion(tiempo, umbral)
    simulacion.inicio_politica_umbral_Cox()

    # Guardar datos cualitativos en un archivo CSV
    output_dir = '../Mabbott/Resultados/cualitativo'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    datos_comportamiento = {
        'Hora_termino_operacion': simulacion.horas_termino_operacion,
        'Kms_por_operacion': simulacion.kms_por_operacion,
        'Tons_por_operacion': simulacion.tons_por_operacion,
        'Kms_acumulados_por_operacion': simulacion.kms_acumulados_por_operacion,
        'Tons_acumulados_por_operacion': simulacion.tons_acumulados_por_operacion
    }

    df_comportamiento = pd.DataFrame(datos_comportamiento)
    df_comportamiento.to_csv(os.path.join(output_dir, 'datos_comportamiento_camion_optimo.csv'), index=False)

    # Guardar horas de mantenciones reactivas en un archivo CSV
    df_mantenciones_reactivas = pd.DataFrame({'Horas_mantenciones_reactivas': simulacion.horas_mantenciones_reactivas})
    df_mantenciones_reactivas.to_csv(os.path.join(output_dir, 'mantenciones_reactivas.csv'), index=False)

    # Guardar horas de mantenciones programadas en un archivo CSV
    df_mantenciones_programadas = pd.DataFrame({'Horas_mantenciones_programadas': simulacion.horas_mantenciones_programadas})
    df_mantenciones_programadas.to_csv(os.path.join(output_dir, 'mantenciones_programadas.csv'), index=False)

    print("Datos de comportamiento del camión extraídos y guardados.")

# Ejecutar la simulación para el año 2024
simular(0.358, 8760)