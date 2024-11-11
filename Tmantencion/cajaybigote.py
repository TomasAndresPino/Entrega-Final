import matplotlib.pyplot as plt
import pandas as pd

# Cargar los datos
df = pd.read_csv('tiempos_mantencion.txt', header=None, names=['numero'])

# Crear el diagrama de caja y bigote
plt.figure(figsize=(8, 6))
plt.boxplot(df['numero'], vert=False)

# Etiquetas y título
plt.xlabel('Tiempos de Mantenimiento')
plt.title('Diagrama de Caja y Bigote')

# Mostrar el gráfico
plt.show()
