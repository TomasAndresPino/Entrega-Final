from clases import Simulacion
import time
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

if __name__ == "__main__":
    print("Mantención de Camiones según Regresión Cox")
    tiempo = int(input("Para qué horizonte de tiempo quieres planificar las mantenciones (Días): "))

    # Fecha de inicio de la simulación (hoy)
    fecha_inicio = datetime.now()

    simulacion = Simulacion(tiempo * 24, 0.358)
    simulacion.ejemplo_implementacion(fecha_inicio)