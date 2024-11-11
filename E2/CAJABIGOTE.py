import matplotlib.pyplot as plt

# Leer los datos del archivo
with open('tiempos_reparacion_CASOBASE2.txt', 'r') as file:
    data = [float(line.strip()) for line in file]

# Crear el diagrama de caja y bigote
plt.boxplot(data)

# Configurar etiquetas
plt.title('Diagrama de Caja y Bigote TReparación Caso Año 2020 AWOU5IMX')
plt.ylabel('Horas')

# Mostrar el gráfico
plt.show()
