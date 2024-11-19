import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

# Cargar los datos del archivo CSV
df = pd.read_csv('Resultados/cualitativo/datos_cualitativos_20_años.csv')

# Crear la carpeta de gráficos si no existe
output_dir = 'Resultados/Graficos'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Configuración de estilo
sns.set(style="whitegrid")

# Información del camión y política
camion_info = "Camión Model_A (ID: AWOU5IMX)"
politica_info = "Política Óptima Preventiva (Umbral 0.358)"
anio_simulacion = "Simulación Años 2024-2043"

# Función para agregar información del camión y política
def agregar_info(ax):
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    textstr = f'{camion_info}\n{politica_info}\n{anio_simulacion}'
    ax.text(1.02, 0.5, textstr, transform=ax.transAxes, fontsize=10,
            verticalalignment='center', bbox=props)

# Gráficos para los 20 años

# Gráfico de Fallas Totales por Año
plt.figure(figsize=(10, 6))
ax = sns.lineplot(x='Año', y='Fallas_totales', data=df, marker='o', palette='Blues_d')
plt.ylabel('Cantidad')
plt.title('Fallas Totales por Año')
agregar_info(ax)
plt.savefig(os.path.join(output_dir, 'Fallas_Totales_por_Año.png'), bbox_inches='tight')
plt.show()

# Gráfico de Fallas Programadas vs Reactivas por Año
plt.figure(figsize=(10, 6))
ax = sns.lineplot(x='Año', y='Fallas_programadas', data=df, marker='o', label='Fallas Programadas', palette='Set2')
sns.lineplot(x='Año', y='Fallas_reactivas', data=df, marker='o', label='Fallas Reactivas', palette='Set2')
plt.ylabel('Cantidad')
plt.title('Fallas Programadas vs Reactivas por Año')
agregar_info(ax)
plt.legend()
plt.savefig(os.path.join(output_dir, 'Fallas_Programadas_vs_Reactivas_por_Año.png'), bbox_inches='tight')
plt.show()

# Gráfico de Tiempo de Operación por Año
plt.figure(figsize=(10, 6))
ax = sns.lineplot(x='Año', y='Tiempo_operacion', data=df, marker='o', palette='Greens_d')
plt.ylabel('Horas')
plt.title('Tiempo de Operación por Año')
agregar_info(ax)
plt.savefig(os.path.join(output_dir, 'Tiempo_Operacion_por_Año.png'), bbox_inches='tight')
plt.show()

# Gráfico de Tiempo de Reparación por Año
plt.figure(figsize=(10, 6))
ax = sns.lineplot(x='Año', y='Tiempo_reparacion', data=df, marker='o', palette='Reds_d')
plt.ylabel('Horas')
plt.title('Tiempo de Reparación por Año')
agregar_info(ax)
plt.savefig(os.path.join(output_dir, 'Tiempo_Reparacion_por_Año.png'), bbox_inches='tight')
plt.show()

# Gráfico de Tiempo sin Operar por Año
plt.figure(figsize=(10, 6))
ax = sns.lineplot(x='Año', y='Tiempo_sin_operar', data=df, marker='o', palette='Oranges_d')
plt.ylabel('Horas')
plt.title('Tiempo sin Operar por Año')
agregar_info(ax)
plt.savefig(os.path.join(output_dir, 'Tiempo_sin_Operar_por_Año.png'), bbox_inches='tight')
plt.show()

# Gráfico de Factor Toneladas por Año
plt.figure(figsize=(10, 6))
ax = sns.lineplot(x='Año', y='Factor_toneladas', data=df, marker='o', palette='Blues_d')
plt.ylabel('Factor')
plt.title('Factor Toneladas por Año')
agregar_info(ax)
plt.savefig(os.path.join(output_dir, 'Factor_Toneladas_por_Año.png'), bbox_inches='tight')
plt.show()

# Gráfico de Factor Kilómetros por Año
plt.figure(figsize=(10, 6))
ax = sns.lineplot(x='Año', y='Factor_kilometros', data=df, marker='o', palette='Purples_d')
plt.ylabel('Factor')
plt.title('Factor Kilómetros por Año')
agregar_info(ax)
plt.savefig(os.path.join(output_dir, 'Factor_Kilometros_por_Año.png'), bbox_inches='tight')
plt.show()

# Gráficos específicos para el año 2024
df_2024 = df[df['Año'] == 2024]

# Gráfico de Fallas Totales en 2024
plt.figure(figsize=(8, 6))
ax = sns.barplot(x=['Fallas Totales'], y=df_2024['Fallas_totales'], palette='Blues_d', width=0.3)
plt.ylabel('Cantidad')
plt.title('Fallas Totales en 2024')
plt.savefig(os.path.join(output_dir, 'Fallas_Totales_2024.png'), bbox_inches='tight')
plt.show()

# Gráfico de Fallas Programadas vs Reactivas en 2024
plt.figure(figsize=(8, 6))
ax = sns.barplot(x=['Fallas Programadas', 'Fallas Reactivas'], y=[df_2024['Fallas_programadas'].values[0], df_2024['Fallas_reactivas'].values[0]], palette='Set2', width=0.3)
plt.ylabel('Cantidad')
plt.title('Fallas Programadas vs Reactivas en 2024')
plt.savefig(os.path.join(output_dir, 'Fallas_Programadas_vs_Reactivas_2024.png'), bbox_inches='tight')
plt.show()

# Gráfico de Tiempo de Operación en 2024
plt.figure(figsize=(8, 6))
ax = sns.barplot(x=['Tiempo de Operación'], y=df_2024['Tiempo_operacion'], palette='Greens_d', width=0.3)
plt.ylabel('Horas')
plt.title('Tiempo de Operación en 2024')
plt.savefig(os.path.join(output_dir, 'Tiempo_Operacion_2024.png'), bbox_inches='tight')
plt.show()

# Gráfico de Tiempo de Reparación en 2024
plt.figure(figsize=(8, 6))
ax = sns.barplot(x=['Tiempo de Reparación'], y=df_2024['Tiempo_reparacion'], palette='Reds_d', width=0.3)
plt.ylabel('Horas')
plt.title('Tiempo de Reparación en 2024')
plt.savefig(os.path.join(output_dir, 'Tiempo_Reparacion_2024.png'), bbox_inches='tight')
plt.show()

# Gráfico de Tiempo sin Operar en 2024
plt.figure(figsize=(8, 6))
ax = sns.barplot(x=['Tiempo sin Operar'], y=df_2024['Tiempo_sin_operar'], palette='Oranges_d', width=0.3)
plt.ylabel('Horas')
plt.title('Tiempo sin Operar en 2024')
plt.savefig(os.path.join(output_dir, 'Tiempo_sin_Operar_2024.png'), bbox_inches='tight')
plt.show()

# Gráfico de Factor Toneladas en 2024
plt.figure(figsize=(8, 6))
ax = sns.barplot(x=['Factor Toneladas'], y=df_2024['Factor_toneladas'], palette='Blues_d', width=0.3)
plt.ylabel('Factor')
plt.title('Factor Toneladas en 2024')
plt.savefig(os.path.join(output_dir, 'Factor_Toneladas_2024.png'), bbox_inches='tight')
plt.show()

# Gráfico de Factor Kilómetros en 2024
plt.figure(figsize=(8, 6))
ax = sns.barplot(x=['Factor Kilómetros'], y=df_2024['Factor_kilometros'], palette='Purples_d', width=0.3)
plt.ylabel('Factor')
plt.title('Factor Kilómetros en 2024')
plt.savefig(os.path.join(output_dir, 'Factor_Kilometros_2024.png'), bbox_inches='tight')
plt.show()

# Tabla de valores para el año 2024
fig, ax = plt.subplots(figsize=(10, 2)) 
ax.axis('tight')
ax.axis('off')

# Aproximar los valores a tres decimales
table_data = [
    ['Fallas Totales', round(df_2024['Fallas_totales'].values[0], 3)],
    ['Fallas Programadas', round(df_2024['Fallas_programadas'].values[0], 3)],
    ['Fallas Reactivas', round(df_2024['Fallas_reactivas'].values[0], 3)],
    ['Tiempo de Operación (Horas)', round(df_2024['Tiempo_operacion'].values[0], 3)],
    ['Tiempo de Reparación (Horas)', round(df_2024['Tiempo_reparacion'].values[0], 3)],
    ['Tiempo sin Operar (Horas)', round(df_2024['Tiempo_sin_operar'].values[0], 3)],
    ['Factor Toneladas', round(df_2024['Factor_toneladas'].values[0], 3)],
    ['Factor Kilómetros', round(df_2024['Factor_kilometros'].values[0], 3)]
]

# Crear la tabla
table = ax.table(cellText=table_data, colLabels=['Métrica', 'Valor'], cellLoc='center', loc='center')
table.auto_set_font_size(False)
table.set_fontsize(12)
table.scale(1.2, 1.2)

# Aplicar colores a las filas
colors = plt.cm.BuPu(np.linspace(0, 0.5, len(table_data)))
for i, (cell, color) in enumerate(zip(table.get_celld().values(), colors)):
    if i == 0:
        cell.set_fontsize(14)
        cell.set_text_props(weight='bold')
    cell.set_facecolor(color)

# Título de la tabla
plt.title('Valores para el Año 2024', fontsize=16, pad=20)

# Guardar la tabla como imagen
plt.savefig(os.path.join(output_dir, 'Tabla_Valores_2024.png'), bbox_inches='tight')
plt.show()

print("Gráficos generados y guardados.")