from clases import Simulacion

tiempos = list()
fallas = list()
for i in range (100):
    simulacion = Simulacion(8760, 0.575)
    simulacion.inicio_politica_3()
    #porcentaje_operacion += (simulacion.camion.TOperacion/1200)
    #tons += simulacion.camion.CTT
    #kms += simulacion.camion.CKT
    #tiempo_reparacion += simulacion.camion.TReparacion
    #tiempo_operacion += simulacion.camion.TOperacion
    if len(simulacion.tiempos) != 0:
        tiempos.append(sum(simulacion.tiempos) / len(simulacion.tiempos))
    if len(simulacion.fallas) != 0:
        fallas.append(sum(simulacion.fallas) / len(simulacion.fallas))



print(tiempos[4])
print(tiempos[95])



print(fallas[4])
print(fallas[95])

print(tiempos)
print(fallas)

