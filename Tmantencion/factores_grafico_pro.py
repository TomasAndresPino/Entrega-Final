import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Cargar los datos desde un archivo CSV
archivo = 'factoresyfallas.txt'  # Cambia esto por el nombre de tu archivo
df = pd.read_csv(archivo)

# Filtrar los datos por modelo
modelo_a = df[df['Modelo'] == 'A']
modelo_b = df[df['Modelo'] == 'B']

# Graficar los puntos para el modelo A
plt.scatter(modelo_a['Fallas'], modelo_a['Factor'], color='blue', label='Modelo A')

# Graficar los puntos para el modelo B
plt.scatter(modelo_b['Fallas'], modelo_b['Factor'], color='green', label='Modelo B')

# Añadir líneas de tendencia para el modelo A
z_a = np.polyfit(modelo_a['Fallas'], modelo_a['Factor'], 1)
p_a = np.poly1d(z_a)
plt.plot(modelo_a['Fallas'], p_a(modelo_a['Fallas']), color='blue', linestyle='--')

# Añadir líneas de tendencia para el modelo B
z_b = np.polyfit(modelo_b['Fallas'], modelo_b['Factor'], 1)
p_b = np.poly1d(z_b)
plt.plot(modelo_b['Fallas'], p_b(modelo_b['Fallas']), color='green', linestyle='--')

# Configurar el gráfico
plt.title('Relación entre Fallas y Factor por Modelo')
plt.xlabel('Número de Fallas')
plt.ylabel('Factor Ton/Kms')
plt.legend()
plt.grid(True)
plt.show()
