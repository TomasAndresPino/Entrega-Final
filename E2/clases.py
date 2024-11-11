from distribuciones import Ocio, Carga, Operacion, Cox, Kilometros, Nivel_Falla, TFalla1, TFalla2, TFalla3, TFalla4, TFalla5, TMantencionP
from collections import namedtuple
import random
import pandas as pd
from lifelines import KaplanMeierFitter
from consultas import Tipo_Falla, probabilidades, cantidades

#Operacion_Toneladas = namedtuple('Operacion_Toneladas', ['Toneladas'])
#Operacion_Tiempo = namedtuple('Operacion_Tiempo', ['TInicio', 'TFin'])
#Operacion_Kms = namedtuple('Operacion_Kms', ['Kms'])
#Falla = namedtuple('Falla', ['Tipo'])
#Hazzard = namedtuple('Hazzard', ['Haz', 'Tiempo'])
#Mantencion = namedtuple('Mantencion', ['Machine_ID', 'Failure_Mode', 'Duracion'])
#Probabilidad = namedtuple('Probabilidad', ['Time', 'Survival'])

class Camion:
    def __init__(self, tipo, id):
        self.tipo = tipo
        self.id = id
        self.TOcio = 0 # Tiempo de ocio

        self.CTT = 0 # carga total transportada
        self.CKT = 0 # cantidad de kilometros totales
        self.CFallas = 0 # cantidad de fallas
        self.CFallaP = 0
        self.TOperacion = 0 # tiempo en operacion
        self.TReparacion = 0 # tiempo en reparacion

        "Variables que hay que ir reiniciando para calcular cox"
        self.kms_acumulados = 0
        self.ton_acumuladas = 0
        self.fallas_acumuladas = 0
        self.tiempo_en_funcionamiento = 0
        self.tiempo_desde_la_última_falla = {"1:": 0, "2": 0, "3": 0, "4": 0, "5": 0}

        "Próximos eventos del camión"
        self.TPE = 0

    def cargar(self):
        """
        Ocupar función generadora de cargas
        """
        self.CTT += Carga()

    def opera(self):
        """
        Ocupar función generadora de tiempo de operación y generadora de tiempo de ocio, es el evento TPE
        """
        self.TOcio = Ocio()
        self.TPE = Operacion() + self.TOcio
        self.CKT += Kilometros()

class Simulacion:
    def __init__(self, tfin, umbral):
        self.camion = Camion("Model_A", "AWOU5IMX")
        self.T = 0
        self.Tdia = 0
        self.Tdia20 = 0
        self.Tdia5 = 0
        self.TLast = [0, 0, 0, 0, 0] 
        #self.TLast2 = [0, 0, 0, 0, 0]# tiempo desde la última mantención de cada parte
        self.TFin = tfin # inicialmente con 30 días y 1 camión

        "Sacar"
        self.contador_dias = 0 
        self.contador_20_dias = 0
        self.contador_5_dias = 0
        self.KM_model = None

        self.umbral = umbral
        self.fallas = list()
        self.tiempos = list()

        "Puestos para debuggear"
        self.TFP = list() # lista que contendrá los tiempos de falla programadas
        self.TFR = list() # lista que contendrá los tiempos de falla reactiva
    
    def KM_set(self):
        "no necesaria, borrar después"
        # Cargar los datos desde un archivo CSV
        df = pd.read_csv('../base_de_datos')
        # Crear el modelo Kaplan-Meier
        self.KM_model = KaplanMeierFitter()
        # Ajustar el modelo Kaplan-Meier con los datos de "Edad" y "Falla"
        self.KM_model.fit(df['Edad'], event_observed=df['Falla'])
    
    def inicio_politica_1(self):
        """
        Lo que hace esta primera política es simular el caso base de mantener cada 20 días
        Pasa que en medio año, como nuestra política cae en hacer mantenciones reactivas más veces
        pierde porque esta cae menos veces.
        Ojo que esta esta programada para, cuando se hace una PM, se mantiene todo el sistema.
        """
        self.camion.cargar()
        self.camion.opera()
        while self.T < self.TFin:
            toperacion = self.camion.TPE - self.camion.TOcio
            self.T += self.camion.TPE
            self.Tdia += self.camion.TPE
            self.Tdia20 += self.camion.TPE
            for i in range(5):
                self.TLast[i] += self.camion.TPE
                #self.TLast2[i] += self.camion.TPE
            self.camion.TOperacion += toperacion
            self.camion.cargar()
            self.camion.opera()
            if self.Tdia > 24:
                # Pasó 1 día
                self.contador_dias += 1
                self.Tdia = self.T - 24*(self.contador_dias)
                if self.Tdia20 > 24*20:
                    # Pasaron 20 días
                    # Hacer mantención programada
                    # Se mantendrá la que lleva más tiempo sin mantener
                    for i in range(5):
                        self.TLast[i] = 0
                    tfalla = TMantencionP()
                    print("Tiempo de Falla Programada", tfalla)
                    self.TFP.append(tfalla)
                    self.fallas.append(tfalla)
                    self.T += tfalla
                    self.camion.TReparacion += tfalla
                    self.camion.CFallaP += 1
                    self.camion.CFallas += 1
                    self.Tdia20 = self.T - 24*(self.contador_dias)
                    #print(self.contador_dias)
                    self.contador_20_dias += 1
                    #print(self.T)

            i = Tipo_Falla(self.TLast, cantidades("maintenance_data", "AWOU5IMX"))
            if i != str(0):
                print(f"Falla de sistema {i}")
                "El equipo Falla"
                nivel = Nivel_Falla()
                if nivel == 1:
                    "Falla tipo 1"
                    tfalla = TFalla1()
                    print(f"Falla tipo 1, duración {tfalla}")
                    print("El tiempo desde la última reparación es", self.TLast[0])
                elif nivel == 2:
                    "Falla tipo 2"
                    tfalla = TFalla2()
                    print(f"Falla tipo 1, duración {tfalla}")
                    print("El tiempo actual es", self.T)
                    print("El tiempo desde la última reparación es", self.TLast[1])
                elif nivel == 3:
                    "Falla tipo 3"
                    tfalla = TFalla3()
                    print(f"Falla tipo 1, duración {tfalla}")
                    print("El tiempo desde la última reparación es", self.TLast[2])
                elif nivel == 4:
                    "Falla tipo 4"
                    tfalla = TFalla4()
                    print(f"Falla tipo 1, duración {tfalla}")
                    print("El tiempo desde la última reparación es", self.TLast[3])
                elif nivel == 5:
                    "Falla tipo 5"
                    tfalla = TFalla5()
                    print(f"Falla tipo 1, duración {tfalla}")
                    print("El tiempo desde la última reparación es", self.TLast[4])
                
                self.tiempos.append(self.TLast[nivel-1])
                self.T += tfalla
                self.TFR.append(tfalla)
                self.fallas.append(tfalla)
                self.camion.TReparacion += tfalla
                self.TLast[int(i)-1] = 0
                self.camion.CFallas += 1
 
    def inicio_CASO_BASE_2(self):
        """
        Esta gran política 2 trata de simular el caso base más puro, cómo este camión se mantiene PM
        cada 5 días sólo el primer año de funcionamiento, busqué simular esa mantención y genera muchas más fallas
        reactivas, en dónde nuestra política debe ganarle.

        No he comparado con nuestra política.

        Política 2 está programado para que la PM se le haga a el componente que lleva más tiempo sin mantenerse.

        Hay un máximo de 9 mantenciones PM, que es lo que vendría siendo el CB.
        """
        self.camion.cargar()
        self.camion.opera()
        while self.T < self.TFin:
            toperacion = self.camion.TPE - self.camion.TOcio
            self.T += self.camion.TPE
            self.Tdia += self.camion.TPE
            self.Tdia5 += self.camion.TPE

            for i in range(5):
                self.TLast[i] += self.camion.TPE

            self.camion.TOperacion += toperacion
            self.camion.cargar()
            self.camion.opera()
            if self.Tdia > 24:
                # Pasó 1 día
                self.contador_dias += 1
                self.Tdia = self.T - 24*(self.contador_dias)
                if self.Tdia5 > 24*5 and self.contador_5_dias < 10:
                    # Pasaron 5 días
                    # Hacer mantención programada
                    # Se mantendrá la que lleva más tiempo sin mantener
                    # Alfinal se mantendrá todo
                    # indice = self.TLast.index(max(self.TLast))
                    # self.TLast[indice] = 0
                    for i in range(5):
                        self.TLast[i] = 0
                    tfalla = TMantencionP()
                    #print("Tiempo de Falla Programada", tfalla)
                    self.TFP.append(tfalla)
                    self.fallas.append(tfalla)
                    self.T += tfalla
                    self.camion.TReparacion += tfalla
                    self.camion.CFallaP += 1
                    self.camion.CFallas += 1
                    self.Tdia5 = self.T - 24*(self.contador_dias)
                    #print(self.contador_dias)
                    self.contador_5_dias += 1
                    #print(self.T)

            i = Tipo_Falla(self.TLast, cantidades("maintenance_data", "AWOU5IMX"))
            if i != str(0):
                # print(f"Falla de sistema {i}")
                "El equipo Falla"
                nivel = Nivel_Falla()
                if nivel == 1:
                    "Falla tipo 1"
                    tfalla = TFalla1()
                    # print(f"Falla tipo 1, duración {tfalla}")
                    # print("El tiempo desde la última reparación es", self.TLast[0])
                elif nivel == 2:
                    "Falla tipo 2"
                    tfalla = TFalla2()
                    # print(f"Falla tipo 1, duración {tfalla}")
                    # print("El tiempo actual es", self.T)
                    # print("El tiempo desde la última reparación es", self.TLast[1])
                elif nivel == 3:
                    "Falla tipo 3"
                    tfalla = TFalla3()
                    # print(f"Falla tipo 1, duración {tfalla}")
                    # print("El tiempo desde la última reparación es", self.TLast[2])
                elif nivel == 4:
                    "Falla tipo 4"
                    tfalla = TFalla4()
                    # print(f"Falla tipo 1, duración {tfalla}")
                    # print("El tiempo desde la última reparación es", self.TLast[3])
                elif nivel == 5:
                    "Falla tipo 5"
                    tfalla = TFalla5()
                    # print(f"Falla tipo 1, duración {tfalla}")
                    # print("El tiempo desde la última reparación es", self.TLast[4])
                
                self.tiempos.append(self.TLast[nivel-1])
                self.T += tfalla
                self.TFR.append(tfalla)
                self.fallas.append(tfalla)
                self.camion.TReparacion += tfalla
                self.TLast[int(i)-1] = 0
                self.camion.CFallas += 1
    
    def inicio_politica_reactiva(self):
        self.camion.cargar()
        self.camion.opera()
        while self.T < self.TFin:
            toperacion = self.camion.TPE - self.camion.TOcio
            self.T += self.camion.TPE
            for i in range(5):
                self.TLast[i] += self.camion.TPE
                #self.TLast2[i] += self.camion.TPE
            
            self.camion.TOperacion += toperacion
            self.camion.cargar()
            self.camion.opera()

            i = Tipo_Falla(self.TLast, cantidades("maintenance_data", "AWOU5IMX"))
            if i != str(0):
                "El equipo Falla"
                nivel = Nivel_Falla()
                if nivel == 1:
                    "Falla tipo 1"
                    tfalla = TFalla1()
                elif nivel == 2:
                    "Falla tipo 2"
                    tfalla = TFalla2()
                elif nivel == 3:
                    "Falla tipo 3"
                    tfalla = TFalla3()
                elif nivel == 4:
                    "Falla tipo 4"
                    tfalla = TFalla4()
                elif nivel == 5:
                    "Falla tipo 5"
                    tfalla = TFalla5()
                self.tiempos.append(self.TLast[nivel-1])
                self.T += tfalla
                self.fallas.append(tfalla)
                self.camion.TReparacion += tfalla
                self.TLast[int(i)-1] = 0
                self.camion.CFallas += 1
    
    def inicio_politica_4(self):
        self.camion.cargar()
        self.camion.opera()
        while self.T < self.TFin:
            toperacion = self.camion.TPE - self.camion.TOcio
            self.T += self.camion.TPE
            for i in range(5):
                self.TLast[i] += self.camion.TPE
                #self.TLast2[i] += self.camion.TPE
            
            self.camion.TOperacion += toperacion
            self.camion.cargar()
            self.camion.opera()

            i = Tipo_Falla(self.TLast, cantidades("maintenance_data", "AWOU5IMX"))
            if i != str(0):
                #print(f"Falla de sistema {i}")
                "El equipo Falla"
                nivel = Nivel_Falla()
                #print("Nivel", nivel)
                #print(type(nivel))
                if nivel == 1:
                    "Falla tipo 1"
                    tfalla = TFalla1()
                    print(f"Falla Reactiva tipo 1, duración {tfalla}")
                    print("----------------------")
                elif nivel == 2:
                    "Falla tipo 2"
                    tfalla = TFalla2()
                    print(f"Falla tipo 2, duración {tfalla}")
                    print("----------------------")
                elif nivel == 3:
                    "Falla tipo 3"
                    tfalla = TFalla3()
                    print(f"Falla tipo 3, duración {tfalla}")
                    print("----------------------")
                elif nivel == 4:
                    "Falla tipo 4"
                    tfalla = TFalla4()
                    print(f"Falla tipo 4, duración {tfalla}")
                    print("----------------------")
                elif nivel == 5:
                    "Falla tipo 5"
                    tfalla = TFalla5()
                    print(f"Falla tipo 5, duración {tfalla}")
                    print("----------------------")
                
                #self.tiempos.append(self.TLast2[nivel-1])
                #print(self.TLast2[nivel-1])
                #self.TLast2 = [0,0,0,0,0]
                self.tiempos.append(self.TLast[nivel-1])
                self.T += tfalla
                self.fallas.append(tfalla)
                #print(tfalla)
                self.camion.TReparacion += tfalla
                self.TLast[int(i)-1] = 0
                self.camion.CFallas += 1
            else:
                "El equipo no falla"
                p_list = probabilidades(self.TLast)
                hubo_mantencion = False
                if p_list[0] < self.umbral:
                    "Mantencion Programada de Sistema Electrico"
                    #self.TLast[0] = 0
                    print("----------------------")
                    print("Mantención Programada")
                    print(f"La probabilidad de sobrevivir es {p_list[0]}")
                    print(f"El tiempo actual es {self.T}")
                    hubo_mantencion = True
                if p_list[1] < self.umbral:
                    "Mantencion Programada de Motor"
                    #self.TLast[1] = 0
                    # print("----------------------")
                    print("Mantención Programada")
                    print(f"La probabilidad de sobrevivir es {p_list[1]}")
                    print(f"El tiempo actual es {self.T}")
                    hubo_mantencion = True
                if p_list[2] < self.umbral:
                    "Mantencion Programada de Escape"
                    #self.TLast[2] = 0
                    print("----------------------")
                    print("Mantención Programada")
                    print(f"La probabilidad de sobrevivir es {p_list[2]}")
                    print(f"El tiempo actual es {self.T}")
                    hubo_mantencion = True
                if p_list[3] < self.umbral:
                    "Mantencion Programada de Hidraulico"
                    #self.TLast[3] = 0
                    print("----------------------")
                    print("Mantención Programada")
                    print(f"La probabilidad de sobrevivir es {p_list[3]}")
                    print(f"El tiempo actual es {self.T}")
                    hubo_mantencion = True
                if p_list[4] < self.umbral:
                    "Mantencion Programada de Suspension"
                    #self.TLast[4] = 0
                    print("----------------------")
                    print("Mantención Programada")
                    print(f"La probabilidad de sobrevivir es {p_list[3]}")
                    print(f"El tiempo actual es {self.T}")
                    hubo_mantencion = True
                
                if hubo_mantencion == True:
                    """
                    A diferencia de la política 3, esta PM mantiente sólo a quien lleva más tiempo sin mantenerse.
                    """
                    # indice = self.TLast.index(max(self.TLast))
                    # self.TLast[indice] = 0
                    for i in range(5):
                        self.TLast[i] = 0
                    tfalla = TMantencionP()
                    print(f"Tiempo de Falla Programada de duración {tfalla}")
                    print("----------------------")
                    self.fallas.append(tfalla)
                    self.T += tfalla
                    self.camion.TReparacion += tfalla
                    self.camion.CFallaP += 1
                    self.camion.CFallas += 1
                    hubo_mantencion = False
    
    def inicio_politica_5(self):
        self.camion.cargar()
        self.camion.opera()
        while self.T < self.TFin:
            toperacion = self.camion.TPE - self.camion.TOcio
            self.T += self.camion.TPE
            for i in range(5):
                self.TLast[i] += self.camion.TPE
                #self.TLast2[i] += self.camion.TPE
            
            self.camion.TOperacion += toperacion
            self.camion.cargar()
            self.camion.opera()

            i = Tipo_Falla(self.TLast, cantidades("maintenance_data", "AWOU5IMX"))
            if i != str(0):
                "El equipo Falla"
                nivel = Nivel_Falla()
                if nivel == 1:
                    "Falla tipo 1"
                    tfalla = TFalla1()
                elif nivel == 2:
                    "Falla tipo 2"
                    tfalla = TFalla2()
                elif nivel == 3:
                    "Falla tipo 3"
                    tfalla = TFalla3()
                elif nivel == 4:
                    "Falla tipo 4"
                    tfalla = TFalla4()
                elif nivel == 5:
                    "Falla tipo 5"
                    tfalla = TFalla5()
                self.tiempos.append(self.TLast[nivel-1])
                self.T += tfalla
                self.fallas.append(tfalla)
                self.camion.TReparacion += tfalla
                self.TLast[int(i)-1] = 0
                self.camion.CFallas += 1
            else:
                "El equipo no falla"
                p_list = probabilidades(self.TLast)
                hubo_mantencion = False
                if p_list[0] < self.umbral:
                    "Mantencion Programada de Sistema Electrico"
                    #self.TLast[0] = 0
                    hubo_mantencion = True
                if p_list[1] < self.umbral:
                    "Mantencion Programada de Motor"
                    #self.TLast[1] = 0
                    # print("----------------------")
                    hubo_mantencion = True
                if p_list[2] < self.umbral:
                    "Mantencion Programada de Escape"
                    #self.TLast[2] = 0
                    hubo_mantencion = True
                if p_list[3] < self.umbral:
                    "Mantencion Programada de Hidraulico"
                    #self.TLast[3] = 0
                    hubo_mantencion = True
                if p_list[4] < self.umbral:
                    "Mantencion Programada de Suspension"
                    #self.TLast[4] = 0
                    hubo_mantencion = True
                
                if hubo_mantencion == True:
                    for i in range(5):
                        self.TLast[i] = 0
                    tfalla = TMantencionP()
                    self.fallas.append(tfalla)
                    self.T += tfalla
                    self.camion.TReparacion += tfalla
                    self.camion.CFallaP += 1
                    self.camion.CFallas += 1
                    hubo_mantencion = False

    def KPIs(self):
        "Tiempo Operando"
        print("El tiempo de operacion del camion fue", self.camion.TOperacion)

        "Tiempo Reparacion"
        print("El tiempo de reparacion del camion fue", self.camion.TReparacion)

        "Cantidad de Fallas"
        print("La cantidad de fallas fueron", self.camion.CFallas)

        "Cantidad de Mantenciones Programadas"
        print("La cantidad de mantenciones programadas fue de", self.camion.CFallaP)

        "Cantidad Carga Transportada"
        print("La cantidad de carga transportada fue", self.camion.CTT)

        "Cantidad kms Recorridos"
        print("La cantidad de Kms Recorridos fue", self.camion.CKT)

        "Factor Ton/Kms"
        print("La cantidad de Toneladas cargadas por Kilómetros fue", (self.camion.CTT/self.camion.CKT))

        #"Debug"
        #print("Los dias simulados fueron", (self.contador_dias))

        "Horas mantenciones programadas"
        print(f"La duración de las {self.camion.CFallaP} mantenciones programadas fue {self.TFP}")

        "Horas mantenciones reactivas"
        print(f"La duración de las {self.camion.CFallas - self.camion.CFallaP} mantenciones reactivas fue {self.TFR}")

        "Total de horas simuladas"
        print(f"El total de horas de simulación fue {self.T} lo cual corresponde a {self.T/24} dias")

        "Factor TOpera/TRepara"
        if self.camion.TReparacion != 0:
            print(f"El factor TOpera/TRepara es ({self.camion.TOperacion/self.camion.TReparacion})")
        else:
            print("No hubo manutenciones")

    def KPI_porcentaje_ut(self):
        "Porcentaje de ocupación"
        #print("El porcentaje de ocupación de la máquina fue", (self.camion.TOperacion*100)/self.T)
        return (self.camion.TOperacion*100)/self.T