import pandas as pd
import matplotlib.pyplot as plt

# Leer el archivo CSV
df = pd.read_csv('maintenance_data.csv')

labels = [
    'Manutención Programada',
    'Desgaste Menor',
    'Fallo del Componente',
    'Fuga en el Sistema',
    'Falla Operacional del Sistema',
    'Falla Crítica'
]

# Contar la frecuencia de cada Failure_Mode
frecuencias = df['Failure_Mode'].value_counts(sort=False)
lista=[0,0,0,0,0,0]
for machine in df.itertuples():
    lista[machine.Failure_Mode] += 1

print(lista)

plt.figure(figsize=(10, 6))

# Crear el histograma
plt.bar(labels, lista, color=plt.cm.viridis(frecuencias.values / max(frecuencias.values)))

# Etiquetas y título

plt.ylabel('Frecuencia')
plt.title('Frecuencia de Failure Modes')
plt.xticks(rotation=25, ha='right')
plt.tight_layout()

# Mostrar el gráfico
plt.show()
