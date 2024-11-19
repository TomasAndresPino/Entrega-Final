from distribuciones import Ocio, Carga, Operacion, Cox, Kilometros, Nivel_Falla, TFalla1, TFalla2, TFalla3, TFalla4, TFalla5, TMantencionP
from collections import namedtuple
import random
import pandas as pd
from lifelines import KaplanMeierFitter
from consultas import Tipo_Falla, probabilidades, cantidades, Tipo_Falla_Cox, Probabilidades_Cox
import time

class Camion:
    def __init__(self, tipo, id):
        self.tipo = tipo
        self.id = id
        self.TOcio = 0 # Tiempo de ocio

        self.CTT = 0 # carga total transportada
        self.carga = 0 # carga de la operación actual
        self.CKT = 0 # cantidad de kilometros totales
        self.kilometros = 0 #kilometros de la operación actual
        self.CFallas = 0 # cantidad de fallas
        self.CFallaP = 0
        self.CFallaF = 0
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

        "Vectores por sistema"
        self.ton_per_time = [0, 0, 0, 0, 0] # lista que cuenta toneladas/t para la operación, sirve para cox
        self.kms_per_time = [0, 0, 0, 0, 0] # lista que cuenta kilómetros/t para la operación, sirve para cox
        self.ton_per_time_virtual = 0 # lista que cuenta toneladas/t para la operación, sirve para cox
        self.kms_per_time_virtual = 0 # lista que cuenta kilómetros/t para la operación, sirve para cox

    def cargar(self):
        """
        Ocupar función generadora de cargas
        """
        c = Carga()
        self.CTT += c
        self.carga = c

    def opera(self):
        """
        Ocupar función generadora de tiempo de operación y generadora de tiempo de ocio, es el evento TPE
        """
        self.TOcio = Ocio()
        self.TPE = Operacion() + self.TOcio
        k = Kilometros()
        self.CKT += k
        self.kilometros = k
    
    def carga_teorico(self):
        c = Carga()
        return c

    def opera_teorico(self):
        k = Kilometros()
        topera = Operacion()
        return k, topera
    
    def t_ocio_teorico(self):
        o = Ocio()
        return o

class Simulacion:
    def __init__(self, tfin, umbral):
        self.camion = Camion("Model_A", "AWOU5IMX")
        self.T = 0
        self.Tdia = 0
        self.TdiaVirtual = 0
        self.Tdia5 = 0
        self.TLast = [0, 0, 0, 0, 0] 
        self.TFin = tfin # inicialmente con 30 días y 1 camión
        self.dias_fallas_r = []
        self.dias_fallas_p = []

        "Parámetros necesarios para CB2"
        self.contador_dias = 0 
        self.contador_5_dias = 0

        self.umbral = umbral
        self.tiempos_fallas = list() # almacena el tiempo de las fallas (Reactivas y Programadas)
        self.tiempos_entre_falla = list() # almacena el tiempo hasta la falla reactiva, sirve para calcular MTBF

        "Puestos para debuggear"
        self.TFP = list() # lista que contendrá los tiempos de falla programadas
        self.TFR = list() # lista que contendrá los tiempos de falla reactiva

        # Listas para almacenar los valores por operación
        self.horas_termino_operacion = []
        self.kms_por_operacion = []
        self.tons_por_operacion = []
        self.kms_acumulados_por_operacion = []
        self.tons_acumulados_por_operacion = []

        # Listas para almacenar las horas de las mantenciones
        self.horas_mantenciones_reactivas = []
        self.horas_mantenciones_programadas = []

    def inicio_politica_umbral_Cox(self):
        kms_acumulados = 0
        tons_acumulados = 0

        self.camion.cargar()
        self.camion.opera()
        while self.T < self.TFin:
            start = time.time()
            toperacion = self.camion.TPE - self.camion.TOcio
            self.T += self.camion.TPE
            for i in range(5):
                self.TLast[i] += self.camion.TPE
                self.camion.ton_per_time[i] += self.camion.carga/toperacion
                self.camion.kms_per_time[i] += self.camion.carga/toperacion
            
            self.camion.TOperacion += toperacion

            # Registrar los valores por operación
            self.horas_termino_operacion.append(self.T)
            self.kms_por_operacion.append(self.camion.kilometros)
            self.tons_por_operacion.append(self.camion.carga)
            kms_acumulados += self.camion.kilometros
            tons_acumulados += self.camion.carga
            self.kms_acumulados_por_operacion.append(kms_acumulados)
            self.tons_acumulados_por_operacion.append(tons_acumulados)

            self.camion.cargar()
            self.camion.opera()

            """Operación Teórica"""
            ton = self.camion.carga_teorico()
            kms, t_operacion = self.camion.opera_teorico()
            ton_per_time = ton/t_operacion
            kms_per_time = kms/t_operacion

            end = time.time()
            tiempo_usado = end - start
            #print("Tiempo 1", tiempo_usado)

            # print(f"Revisión Cox en tiempo {self.T}")
            i, probabilidades = Tipo_Falla_Cox(self.TLast, self.camion.kms_per_time, self.camion.ton_per_time, ton_per_time, kms_per_time, 1)
            # print(f"Fin Revisión Cox en tiempo {self.T}")
            # print(i)
            if i != str(0):
                #print(f"El equipo falla reactivamente en el tiempo {self.T}")
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
                self.dias_fallas_r.append(self.T)
                self.tiempos_entre_falla.append(self.TLast[nivel-1])
                self.T += tfalla
                self.tiempos_fallas.append(tfalla)
                self.camion.TReparacion += tfalla

                self.TLast[int(i)-1] = 0
                self.camion.ton_per_time[int(i)-1] = 0
                self.camion.kms_per_time[int(i)-1] = 0

                self.camion.CFallas += 1

                # Registrar las horas de las mantenciones reactivas
                self.horas_mantenciones_reactivas.append(self.T)

                # Reiniciar los valores acumulados
                kms_acumulados = 0
                tons_acumulados = 0
            else:
                start = time.time()
                "El equipo no falla"
                p_list = probabilidades
                hubo_mantencion = False
                bajo_umbral = []
                if p_list[0] < self.umbral:
                    "Mantencion Programada de Sistema Electrico"
                    hubo_mantencion = True
                    bajo_umbral.append(0)
                if p_list[1] < self.umbral:
                    "Mantencion Programada de Motor"
                    hubo_mantencion = True
                    bajo_umbral.append(1)
                if p_list[2] < self.umbral:
                    "Mantencion Programada de Escape"
                    hubo_mantencion = True
                    bajo_umbral.append(2)
                if p_list[3] < self.umbral:
                    "Mantencion Programada de Hidraulico"
                    hubo_mantencion = True
                    bajo_umbral.append(3)
                if p_list[4] < self.umbral:
                    "Mantencion Programada de Suspension"
                    hubo_mantencion = True
                    bajo_umbral.append(4)

                end = time.time()
                tiempo_usado = end - start
                #print("Tiempo 2", tiempo_usado)

                if hubo_mantencion == True:
                    start = time.time()

                    #print(f"El equipo falla proactivamente en el tiempo {self.T}")
                    self.dias_fallas_p.append(self.T)
                    "Se mantendrá quien haya bajado del umbral cox y lleve menos tiempo sin mantener"
                    # tlast_filtrado = []
                    # for indice in bajo_umbral:
                    #     tlast_filtrado.append(self.TLast[indice])
                    # indice = tlast_filtrado.index(max(tlast_filtrado))
                    # indice_max = bajo_umbral[indice]

                    # self.TLast[indice_max] = 0
                    # self.camion.ton_per_time[indice_max] = 0
                    # self.camion.kms_per_time[indice_max] = 0
                    for i in range(5):
                        self.TLast[i] = 0
                        self.camion.ton_per_time[i] = 0
                        self.camion.kms_per_time[i] = 0
                        
                    tfalla = TMantencionP()
                    self.tiempos_fallas.append(tfalla)
                    self.T += tfalla
                    self.camion.TReparacion += tfalla
                    self.camion.CFallaP += 1
                    self.camion.CFallas += 1
                    hubo_mantencion = False

                    # Registrar las horas de las mantenciones programadas
                    self.horas_mantenciones_programadas.append(self.T)

                    end = time.time()
                    tiempo_usado = end - start
                    #print("Tiempo 3", tiempo_usado)