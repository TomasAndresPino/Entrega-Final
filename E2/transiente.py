
import matplotlib.pyplot as plt

# Supongamos que estas son tus listas de valores
x = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75]  # Valores para el eje x
y = [0.07833251012221415, 0.1082936787484539, 0.18214810302767132, 0.29102761349470624, 0.3208409865288095, 0.3517670096165842, 0.477128895196509, 0.449345795355638, 0.46123254821465365, 0.459345795355638, 0.462789432, 0.455678123, 0.461234567, 0.457890123, 0.460123456]

 # Valores para el eje y

# Crear el gráfico
plt.plot(x, y, marker='o')  # 'marker' es opcional, pero ayuda a visualizar los puntos
plt.xlabel('Dias')  # Etiqueta para el eje X
plt.ylabel('% tiempo de ocupación')  # Etiqueta para el eje Y
plt.title('Cálculo periodo transiente')  # Título del gráfico

# Mostrar el gráfico
plt.show()