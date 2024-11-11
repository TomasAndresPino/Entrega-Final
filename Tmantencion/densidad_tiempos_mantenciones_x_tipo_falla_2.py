import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Lee el archivo CSV
df = pd.read_csv('maintenance_data.csv')

# Convierte las columnas de tiempo a tipo datetime
df['Start_Time'] = pd.to_datetime(df['Start_Time'], format='%m/%d/%Y %H:%M')
df['End_Time'] = pd.to_datetime(df['End_Time'], format='%m/%d/%Y %H:%M')

# Calcula el tiempo de mantención en horas
df['Maintenance_Duration'] = (df['End_Time'] - df['Start_Time']).dt.total_seconds() / 3600  # Convertir a horas

# Filtra las filas donde la duración de la mantención es mayor a 0 y menor o igual a 20 horas
df_filtered = df[(df['Maintenance_Duration'] > 0) & (df['Maintenance_Duration'] <= 20)]

# Definir colores y etiquetas para cada modo de falla
failure_labels = {
    0: ('deepskyblue', 'Manutención Programada'),
    1: ('crimson', 'Desgaste Menor'),
    2: ('darkorange', 'Fallo del Componente'),
    3: ('limegreen', 'Fuga en el Sistema'),
    4: ('magenta', 'Falla Operacional del Sistema'),
    5: ('gold', 'Falla Crítica')
}

plt.figure(figsize=(1920 / 100, 1080 / 100))

# Graficar densidades para cada modo de falla
for mode, (color, label) in failure_labels.items():
    if mode in df_filtered['Failure_Mode'].values:
        # Graficar KDE sin alterar las densidades
        sns.kdeplot(df_filtered[df_filtered['Failure_Mode'] == mode]['Maintenance_Duration'], 
                    bw_adjust=1,  # Ajustar esto según sea necesario
                    fill=False,   # No llenar la curva
                    color=color, 
                    label=label)

# Configurar el gráfico
plt.xlabel('Duración de la mantención (horas)')
plt.ylabel('Densidad')
plt.title('Densidades de duración de mantenciones por tipo de falla')

# Establecer límites del eje x entre 0 y 20 horas
plt.xlim(0, 20)

# Establecer marcas del eje x de 0.5 en 0.5
plt.xticks(np.arange(0, 21, 0.5))

plt.grid(True)
plt.legend(title='Modo de Falla')

# Guardar la figura con la resolución deseada
plt.savefig("AAAA.png", dpi=100)  # DPI puede ser ajustado para cambiar la calidad
print("Imagen guardada con éxito")




