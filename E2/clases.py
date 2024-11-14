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

        "Parámetros necesarios para CB2"
        self.contador_dias = 0 
        self.contador_5_dias = 0

        self.umbral = umbral
        self.tiempos_fallas = list() # almacena el tiempo de las fallas (Reactivas y Programadas)
        self.tiempos_entre_falla = list() # almacena el tiempo hasta la falla reactiva, sirve para calcular MTBF

        "Puestos para debuggear"
        self.TFP = list() # lista que contendrá los tiempos de falla programadas
        self.TFR = list() # lista que contendrá los tiempos de falla reactiva
 
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
                    for i in range(5):
                        self.TLast[i] = 0
                    tfalla = TMantencionP()
                    self.TFP.append(tfalla)
                    self.tiempos_fallas.append(tfalla)
                    self.T += tfalla
                    self.camion.TReparacion += tfalla
                    self.camion.CFallaP += 1
                    self.camion.CFallas += 1
                    self.Tdia5 = self.T - 24*(self.contador_dias)
                    self.contador_5_dias += 1

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
                
                self.tiempos_entre_falla.append(self.TLast[nivel-1])
                self.T += tfalla
                self.TFR.append(tfalla)
                self.tiempos_fallas.append(tfalla)
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
                self.tiempos_entre_falla.append(self.TLast[nivel-1])
                self.T += tfalla
                self.tiempos_fallas.append(tfalla)
                self.camion.TReparacion += tfalla
                self.TLast[int(i)-1] = 0
                self.camion.CFallas += 1
    
    def inicio_politica_umbral(self):
        self.camion.cargar()
        self.camion.opera()
        while self.T < self.TFin:
            toperacion = self.camion.TPE - self.camion.TOcio
            self.T += self.camion.TPE
            for i in range(5):
                self.TLast[i] += self.camion.TPE
            
            self.camion.TOperacion += toperacion
            self.camion.cargar()
            self.camion.opera()

            i = Tipo_Falla(self.TLast, cantidades("maintenance_data", "AWOU5IMX"))
            if i != str(0):
                print("Mantención reactiva del sistema", i)
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
                self.tiempos_entre_falla.append(self.TLast[nivel-1])
                self.T += tfalla
                self.tiempos_fallas.append(tfalla)
                self.camion.TReparacion += tfalla
                self.TLast[int(i)-1] = 0
                self.camion.CFallas += 1
            else:
                "El equipo no falla"
                p_list = probabilidades(self.TLast)
                hubo_mantencion = False
                if p_list[0] < self.umbral:
                    "Mantencion Programada de Sistema Electrico"
                    hubo_mantencion = True
                if p_list[1] < self.umbral:
                    "Mantencion Programada de Motor"
                    hubo_mantencion = True
                if p_list[2] < self.umbral:
                    "Mantencion Programada de Escape"
                    hubo_mantencion = True
                if p_list[3] < self.umbral:
                    "Mantencion Programada de Hidraulico"
                    hubo_mantencion = True
                if p_list[4] < self.umbral:
                    "Mantencion Programada de Suspension"
                    hubo_mantencion = True
                
                if hubo_mantencion == True:
                    print("Mantención programada")
                    for i in range(5):
                        self.TLast[i] = 0
                    tfalla = TMantencionP()
                    self.tiempos_fallas.append(tfalla)
                    self.T += tfalla
                    self.camion.TReparacion += tfalla
                    self.camion.CFallaP += 1
                    hubo_mantencion = False

    def inicio_politica_umbral_Cox(self):
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

            self.camion.cargar()
            self.camion.opera()

            """Operación Teórica"""
            ton = self.camion.carga_teorico()
            kms, t_operacion= self.camion.opera_teorico()
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
                self.tiempos_entre_falla.append(self.TLast[nivel-1])
                self.T += tfalla
                self.tiempos_fallas.append(tfalla)
                self.camion.TReparacion += tfalla

                self.TLast[int(i)-1] = 0
                self.camion.ton_per_time[int(i)-1] = 0
                self.camion.kms_per_time[int(i)-1] = 0

                self.camion.CFallas += 1
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

                    end = time.time()
                    tiempo_usado = end - start
                    #print("Tiempo 3", tiempo_usado)

    def inicio_politica_Cox_diario(self):
        while self.T < self.TFin:
            if self.TdiaVirtual < 24:
                "Dia virtual"
                ton = self.camion.carga_teorico()
                kms, t_operacion= self.camion.opera_teorico()
                o = self.camion.t_ocio_teorico()
                ton_per_time = ton/t_operacion
                kms_per_time = kms/t_operacion
                self.TdiaVirtual += (t_operacion + o)
                self.camion.kms_per_time_virtual += kms_per_time
                self.camion.ton_per_time_virtual += ton_per_time
            else:
                "Termina el día virtual"
                self.TdiaVirtual = 0
                "Tengo que ver si lo sobrevivo o no"
                i, probabilidades = Tipo_Falla_Cox(self.TLast, self.camion.kms_per_time, self.camion.ton_per_time, self.camion.ton_per_time_virtual, self.camion.kms_per_time_virtual, 1)
                self.camion.kms_per_time_virtual = 0
                self.camion.ton_per_time_virtual = 0
                if i != str(0):
                    # print(f"El equipo falla reactivamente en el tiempo {self.T}")
                    print("------Mantención Reactiva------")
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
                    self.tiempos_entre_falla.append(self.TLast[nivel-1])
                    self.T += tfalla
                    self.tiempos_fallas.append(tfalla)
                    self.camion.TReparacion += tfalla

                    self.TLast[int(i)-1] = 0
                    self.camion.ton_per_time[int(i)-1] = 0
                    self.camion.kms_per_time[int(i)-1] = 0

                    self.camion.CFallas += 1
                else:
                    print("Sobreviviste un día más!")
                    while self.Tdia < 24:
                        self.camion.cargar()
                        self.camion.opera()
                        toperacion = self.camion.TPE - self.camion.TOcio
                        self.camion.TOperacion += toperacion
                        self.T += self.camion.TPE
                        self.Tdia += self.camion.TPE
                        for i in range(5):
                            self.TLast[i] += self.camion.TPE
                            self.camion.ton_per_time[i] += self.camion.carga/toperacion
                            self.camion.kms_per_time[i] += self.camion.carga/toperacion
                        
                        "Ver si alguna baja del umbral"
                        mantencion_programada = False
                        p = Probabilidades_Cox(self.TLast, self.camion.kms_per_time, self.camion.ton_per_time, 1)
                        # mantener = []
                        for i in range(5):
                            if p[i] < self.umbral:
                                mantencion_programada = True
                                # mantener.append(i)
                        
                        if mantencion_programada == True:
                            # "Mantener el que lleva más tiempo sin mantener"
                            # posibles_PM = [self.TLast[i] for i in mantener]
                            # indice = posibles_PM.index(max(posibles_PM))
                            # indice_real = mantener[indice]
                            print("------Mantención Programada------")
                            for i in range(5):
                                self.TLast[i] = 0
                                self.camion.ton_per_time[i] = 0
                                self.camion.kms_per_time[i] = 0
                            # self.TLast[indice_real] = 0
                            # self.camion.ton_per_time[i] = 0
                            # self.camion.kms_per_time[i] = 0
                                        
                            tfalla = TMantencionP()
                            self.tiempos_fallas.append(tfalla)
                            self.T += tfalla
                            self.camion.TReparacion += tfalla
                            self.camion.CFallaP += 1
                            self.camion.CFallas += 1
                            mantencion_programada = False
                    self.Tdia = 0

    def inicio_politica_Cox_diario_simplificado(self):
            while self.T < self.TFin:
                "Creación dia virtual"
                "Dia virtual"
                self.camion.kms_per_time_virtual = 126.4
                self.camion.ton_per_time_virtual = 161.1

                "Tengo que ver si lo sobrevivo o no"
                i, probabilidades = Tipo_Falla_Cox(self.TLast, self.camion.kms_per_time, self.camion.ton_per_time, self.camion.ton_per_time_virtual, self.camion.kms_per_time_virtual, 1)
                if i != str(0):
                    # print(f"El equipo falla reactivamente en el tiempo {self.T}")
                    print("------Mantención Reactiva------")
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
                    self.tiempos_entre_falla.append(self.TLast[nivel-1])
                    self.T += tfalla
                    self.tiempos_fallas.append(tfalla)
                    self.camion.TReparacion += tfalla

                    self.TLast[int(i)-1] = 0
                    self.camion.ton_per_time[int(i)-1] = 0
                    self.camion.kms_per_time[int(i)-1] = 0

                    self.camion.CFallas += 1
                else:
                    print("Sobreviviste un día más!")
                    while self.Tdia < 24:
                        self.camion.cargar()
                        self.camion.opera()
                        toperacion = self.camion.TPE - self.camion.TOcio
                        self.camion.TOperacion += toperacion
                        self.T += self.camion.TPE
                        self.Tdia += self.camion.TPE
                        for i in range(5):
                            self.TLast[i] += self.camion.TPE
                            self.camion.ton_per_time[i] += self.camion.carga/toperacion
                            self.camion.kms_per_time[i] += self.camion.carga/toperacion
                        
                        "Ver si alguna baja del umbral"
                        mantencion_programada = False
                        p = Probabilidades_Cox(self.TLast, self.camion.kms_per_time, self.camion.ton_per_time, 1)
                        # mantener = []
                        for i in range(5):
                            if p[i] < self.umbral:
                                mantencion_programada = True
                                # mantener.append(i)
                        
                        if mantencion_programada == True:
                            # "Mantener el que lleva más tiempo sin mantener"
                            # posibles_PM = [self.TLast[i] for i in mantener]
                            # indice = posibles_PM.index(max(posibles_PM))
                            # indice_real = mantener[indice]
                            print("------Mantención Programada------")
                            for i in range(5):
                                self.TLast[i] = 0
                                self.camion.ton_per_time[i] = 0
                                self.camion.kms_per_time[i] = 0
                            # self.TLast[indice_real] = 0
                            # self.camion.ton_per_time[i] = 0
                            # self.camion.kms_per_time[i] = 0
                                        
                            tfalla = TMantencionP()
                            self.tiempos_fallas.append(tfalla)
                            self.T += tfalla
                            self.camion.TReparacion += tfalla
                            self.camion.CFallaP += 1
                            self.camion.CFallas += 1
                            mantencion_programada = False
                    self.Tdia = 0


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