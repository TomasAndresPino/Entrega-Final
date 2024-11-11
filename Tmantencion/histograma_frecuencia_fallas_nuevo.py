import pandas as pd
import matplotlib.pyplot as plt

# Leer el archivo CSV
df = pd.read_csv('maintenance_data.csv')

# Diccionario de modos de falla
modos_falla_dict = {
    0: 'Mantención programada (0)',
    1: 'Desgaste Menor (1)',
    2: 'Fallo de Componente (2)',
    3: 'Fuga en el Sistema (3)',
    4: 'Falla Operacional del Sistema (4)',
    5: 'Falla Crítica (5)'
}

# Reemplazar los códigos de falla con sus descripciones y mantener el orden
df['Failure_Mode'] = pd.Categorical(
    df['Failure_Mode'].replace(modos_falla_dict),
    categories=list(modos_falla_dict.values()), 
    ordered=True
)

# Contar la frecuencia de cada modo de falla
frecuencia_fallas = df['Failure_Mode'].value_counts().reindex(df['Failure_Mode'].cat.categories)

# Obtener los modos de falla y sus frecuencias
modos_falla = frecuencia_fallas.index
frecuencias = frecuencia_fallas.values

# Crear el gráfico de barras
plt.figure(figsize=(1920 / 100, 1080 / 100))  # Tamaño de la figura en pulgadas
plt.bar(modos_falla, frecuencias, color='blue')  # Usar los nombres de los modos de falla
plt.xlabel('Modo de Falla')
plt.ylabel('Frecuencia')
plt.title('Histograma de Frecuencia de Modos de Falla')
plt.xticks(rotation=45)  # Rotar las etiquetas del eje x si es necesario
plt.tight_layout()  # Ajustar el layout para que no se solapen las etiquetas

# Mostrar el gráfico
plt.savefig("AAAA.png", dpi=100)  # DPI puede ser ajustado para cambiar la calidad
print("Imagen guardada con éxito")
#plt.show()