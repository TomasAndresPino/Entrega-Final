# Proyecto-Capstone
Proyecto de Taller de Investigación Operativa: Planificación de mantención de Camiones

## Consideraciones importantes
La carpeta que se tiene que ejecutar para el proyecto es la carpeta E2. En esta se encuentran los archivos que permiten realizar simulaciones y el ejemplo de aplicación.
Uno de los archivos está hardcodeado, es decir, tiene rutas absolutas que pertenecen a mi computador. En el archivo cargar_archivos, cargar_probabilidades y cargar_hazzard tienen las rutas de las carpetas KMs y BasesCox. No pudimos arreglar este problema.

### Archivos Importantes
1) clases: Este archivo contendrá las clases, se creó la clase __Camion__, con sus variantes __CamionSensible__ y __CamionReal__. Además existe la clase __Simulacion__ con diferentes métodos que son las políticas.
2) distribuciones: funciones las cuales son útiles para generar las cargas, los tiempos de viajes y los tiempos de fallas, entre otros.
3) main: si se ejecuta, comienza el ejemplo de aplicación.
4) analisis_sens: En realidad, no hace un análisis sensible, sino que permite generar muchas simulaciones.

#### Ejemplo Implementación
Hay que ejecutar el archivo main.py desde la terminal. Te pide cuanto tiempo quieres planificar (poner en días, por ejemplo 365 días).
Luego te pregunta cuanta carga, cuanta tonelada y cuanto tiempo vas a transportar. Lo pregunta constantemente avisando si es que se sobrevive la operación, si es que se recomienda hacer una mantención preventiva o si hay una mantención reactiva, siempre indicando la fecha del suceso y el tipo de falla, siendo Desgaste Menor, Fallo de Componente, Fuga en el Sistema, Falla Operacional del Sistema o Falla Crítica.

OJO: si se ponen ceros o si se ponen números muy grandes el programa se cae. No es apto para errores aún. 

##### Variables de Estado
1. T: Reloj Simulación
2. TFin: Horizonte de simulación
3. TPE: Próximo evento de operación (carga y ocio)
4. TLast: Última reparación de Sistema (Vector)
5. TON_PER_TIME & KMS_PER_TIME (Vectores)

###### KPIs primarios
1. FACTOR KMS
2. FACTOR TON

###### KPIs secundarios
1. MTBM
2. DOWNTIME
