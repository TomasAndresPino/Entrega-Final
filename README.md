# Proyecto-Capstone
Proyecto de Taller de Investigación Operativa: Planificación de mantención de Camiones

## Notas TAPR
Se creó una nueva carpeta para la siguiente entrega, se llama E2. En esta se trabajará al menos la **simulación** la cual se está trabajando inicialmente con 4 archivos, **clases**, **distribuciones**, **main** y **parametros**. Cada uno de estos archivos será explicado a continuación:

### Archivos
1) clases: Este archivo contendrá las clases, se creó la clase __Camion__ y se piensa quizás crear una clase para la Simulación o para las Políticas.
2) distribuciones: serán funciones las cuales serán útiles para generar las cargas, los tiempos de viajes y los tiempos de fallas.
3) main: se tiene la idea de armar la simulación en este código.
4) parametros: poner parámetros utilizados en el proyecto.

#### Otras consideraciones
- La simulación está pensada como eventos. 
- Se asume que después de cada falla se opera de inmediato.
- Se simulará 1 año 1 camión en primera instancia.

##### Variables de Estado
- T: Reloj Simulación
- Tfin: tiempo que demora la simulación (8760hrs)
- TPE: tiempo próxima operación. Lo que se modela es un tiempo de viaje y un tiempo de ocio, ya que cuando termina eso, podría empezar una nueva operación.
- TPE0: tiempo próxima mantención programada.
- TPEi: tiempo próxima falla i.
- Tmin: minimo tiempo entre TPE, TPE0, TPEi.
- Carga: carga de operación.

###### Medidas de desempeño iniciale
- TOperacion: tiempo en operación.
- CTT: carga total transportada.
- CFallas: cantidad de fallas.
- TReparacion: tiempo en reparación.