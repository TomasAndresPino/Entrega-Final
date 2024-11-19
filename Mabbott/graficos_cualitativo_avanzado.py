import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Cargar los datos del archivo CSV
df_comportamiento = pd.read_csv('Resultados/cualitativo/datos_comportamiento_camion_optimo.csv')
df_fallas_programadas = pd.read_csv('Resultados/cualitativo/mantenciones_programadas.csv')
df_fallas_reactivas = pd.read_csv('Resultados/cualitativo/mantenciones_reactivas.csv')

# Crear la carpeta de gráficos si no existe
output_dir = 'Resultados/Graficos/Develop'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Configuración de estilo
sns.set(style="whitegrid")

# Información del camión y política
camion_info = "Camión Model_A (ID: AWOU5IMX)"
politica_info = "Política Óptima Preventiva (Umbral 0.358)"
anio_simulacion = "Simulación Año 2024"

# Seleccionar un rango de filas para mostrar en detalle
fila_inicio = 2600
fila_fin = 3360
df_comportamiento_zoom = df_comportamiento.iloc[fila_inicio:fila_fin]

# Filtrar puntos para evitar contaminación visual
df_comportamiento_zoom_filtrado = df_comportamiento_zoom.iloc[::20, :]  # Tomar cada 20 puntos

# Gráfico de Kms por Operación a lo largo del tiempo con fallas (Zoom)
plt.figure(figsize=(14, 8))
ax = sns.lineplot(x='Hora_termino_operacion', y='Kms_por_operacion', data=df_comportamiento_zoom_filtrado, marker='o', label='Kms por Operación')
plt.ylabel('Kilómetros')
plt.title('Kms por Operación a lo largo del tiempo (Filas 2600 a 3360)')
plt.legend()

# Añadir líneas verticales para las fallas programadas (verdes) y reactivas (rojas)
for xc in df_fallas_programadas['Horas_mantenciones_programadas']:
    if df_comportamiento_zoom['Hora_termino_operacion'].min() <= xc <= df_comportamiento_zoom['Hora_termino_operacion'].max():
        plt.axvline(x=xc, color='green', linestyle='--', label='Falla Programada' if xc == df_fallas_programadas['Horas_mantenciones_programadas'].iloc[0] else "")
for xc in df_fallas_reactivas['Horas_mantenciones_reactivas']:
    if df_comportamiento_zoom['Hora_termino_operacion'].min() <= xc <= df_comportamiento_zoom['Hora_termino_operacion'].max():
        plt.axvline(x=xc, color='red', linestyle='--', label='Falla Reactiva' if xc == df_fallas_reactivas['Horas_mantenciones_reactivas'].iloc[0] else "")

# Añadir leyenda para los tipos de fallas
handles, labels = ax.get_legend_handles_labels()
handles.append(plt.Line2D([0], [0], color='green', linestyle='--'))
labels.append('Falla Programada')
handles.append(plt.Line2D([0], [0], color='red', linestyle='--'))
labels.append('Falla Reactiva')
ax.legend(handles=handles, labels=labels)

# Añadir cuadro con información del camión y política
plt.text(1.02, 0.5, f'{camion_info}\n{politica_info}\n{anio_simulacion}', transform=ax.transAxes, fontsize=12, verticalalignment='center', bbox=dict(facecolor='white', alpha=0.5))

plt.savefig(os.path.join(output_dir, 'Kms_por_Operacion_Tiempo_Zoom.png'), bbox_inches='tight')
plt.show()

# Gráfico de Toneladas por Operación a lo largo del tiempo con fallas (Zoom)
plt.figure(figsize=(14, 8))
ax = sns.lineplot(x='Hora_termino_operacion', y='Tons_por_operacion', data=df_comportamiento_zoom_filtrado, marker='o', label='Toneladas por Operación')
plt.ylabel('Toneladas')
plt.title('Toneladas por Operación a lo largo del tiempo (Filas 2600 a 3360)')
plt.legend()

# Añadir líneas verticales para las fallas programadas (verdes) y reactivas (rojas)
for xc in df_fallas_programadas['Horas_mantenciones_programadas']:
    if df_comportamiento_zoom['Hora_termino_operacion'].min() <= xc <= df_comportamiento_zoom['Hora_termino_operacion'].max():
        plt.axvline(x=xc, color='green', linestyle='--', label='Falla Programada' if xc == df_fallas_programadas['Horas_mantenciones_programadas'].iloc[0] else "")
for xc in df_fallas_reactivas['Horas_mantenciones_reactivas']:
    if df_comportamiento_zoom['Hora_termino_operacion'].min() <= xc <= df_comportamiento_zoom['Hora_termino_operacion'].max():
        plt.axvline(x=xc, color='red', linestyle='--', label='Falla Reactiva' if xc == df_fallas_reactivas['Horas_mantenciones_reactivas'].iloc[0] else "")

# Añadir leyenda para los tipos de fallas
handles, labels = ax.get_legend_handles_labels()
handles.append(plt.Line2D([0], [0], color='green', linestyle='--'))
labels.append('Falla Programada')
handles.append(plt.Line2D([0], [0], color='red', linestyle='--'))
labels.append('Falla Reactiva')
ax.legend(handles=handles, labels=labels)

# Añadir cuadro con información del camión y política
plt.text(1.02, 0.5, f'{camion_info}\n{politica_info}\n{anio_simulacion}', transform=ax.transAxes, fontsize=12, verticalalignment='center', bbox=dict(facecolor='white', alpha=0.5))

plt.savefig(os.path.join(output_dir, 'Toneladas_por_Operacion_Tiempo_Zoom.png'), bbox_inches='tight')
plt.show()

# Gráfico de Kms Acumulados por Operación con fallas
plt.figure(figsize=(14, 8))
ax = sns.lineplot(x='Hora_termino_operacion', y='Kms_acumulados_por_operacion', data=df_comportamiento, marker='', label='Kms Acumulados por Operación')
plt.plot(df_comportamiento['Hora_termino_operacion'], df_comportamiento['Kms_acumulados_por_operacion'], marker='o', markersize=10, linestyle='-', color='blue')
plt.ylabel('Kilómetros')
plt.title('Kms Acumulados por Operación')
plt.legend()

# Añadir líneas verticales para las fallas programadas (verdes) y reactivas (rojas)
for xc in df_fallas_programadas['Horas_mantenciones_programadas']:
    plt.axvline(x=xc, color='green', linestyle='--')
for xc in df_fallas_reactivas['Horas_mantenciones_reactivas']:
    plt.axvline(x=xc, color='red', linestyle='--')

# Añadir leyenda para los tipos de fallas
handles, labels = ax.get_legend_handles_labels()
if 'Falla Programada' not in labels:
    handles.append(plt.Line2D([0], [0], color='green', linestyle='--'))
    labels.append('Falla Programada')
if 'Falla Reactiva' not in labels:
    handles.append(plt.Line2D([0], [0], color='red', linestyle='--'))
    labels.append('Falla Reactiva')
ax.legend(handles=handles, labels=labels)

# Añadir cuadro con información del camión y política
plt.text(1.02, 0.5, f'{camion_info}\n{politica_info}\n{anio_simulacion}', transform=ax.transAxes, fontsize=12, verticalalignment='center', bbox=dict(facecolor='white', alpha=0.5))

plt.savefig(os.path.join(output_dir, 'Kms_Acumulados_por_Operacion.png'), bbox_inches='tight')
plt.show()

# Gráfico de Toneladas Acumuladas por Operación con fallas
plt.figure(figsize=(14, 8))
ax = sns.lineplot(x='Hora_termino_operacion', y='Tons_acumulados_por_operacion', data=df_comportamiento, marker='', label='Toneladas Acumuladas por Operación')
plt.plot(df_comportamiento['Hora_termino_operacion'], df_comportamiento['Tons_acumulados_por_operacion'], marker='o', markersize=10, linestyle='-', color='blue')
plt.ylabel('Toneladas')
plt.title('Toneladas Acumuladas por Operación')
plt.legend()

# Añadir líneas verticales para las fallas programadas (verdes) y reactivas (rojas)
for xc in df_fallas_programadas['Horas_mantenciones_programadas']:
    plt.axvline(x=xc, color='green', linestyle='--')
for xc in df_fallas_reactivas['Horas_mantenciones_reactivas']:
    plt.axvline(x=xc, color='red', linestyle='--')

# Añadir leyenda para los tipos de fallas
handles, labels = ax.get_legend_handles_labels()
if 'Falla Programada' not in labels:
    handles.append(plt.Line2D([0], [0], color='green', linestyle='--'))
    labels.append('Falla Programada')
if 'Falla Reactiva' not in labels:
    handles.append(plt.Line2D([0], [0], color='red', linestyle='--'))
    labels.append('Falla Reactiva')
ax.legend(handles=handles, labels=labels)

# Añadir cuadro con información del camión y política
plt.text(1.02, 0.5, f'{camion_info}\n{politica_info}\n{anio_simulacion}', transform=ax.transAxes, fontsize=12, verticalalignment='center', bbox=dict(facecolor='white', alpha=0.5))

plt.savefig(os.path.join(output_dir, 'Toneladas_Acumuladas_por_Operacion.png'), bbox_inches='tight')
plt.show()

# Gráfico de Kms por Operación a lo largo del tiempo con fallas (Todas las horas)
plt.figure(figsize=(14, 8))
ax = sns.lineplot(x='Hora_termino_operacion', y='Kms_por_operacion', data=df_comportamiento, marker='o', label='Kms por Operación')
plt.ylabel('Kilómetros')
plt.title('Kms por Operación a lo largo del tiempo (Todas las horas)')
plt.legend()

# Añadir líneas verticales para las fallas programadas (verdes) y reactivas (rojas)
for xc in df_fallas_programadas['Horas_mantenciones_programadas']:
    plt.axvline(x=xc, color='green', linestyle='--', label='Falla Programada' if xc == df_fallas_programadas['Horas_mantenciones_programadas'].iloc[0] else "")
for xc in df_fallas_reactivas['Horas_mantenciones_reactivas']:
    plt.axvline(x=xc, color='red', linestyle='--', label='Falla Reactiva' if xc == df_fallas_reactivas['Horas_mantenciones_reactivas'].iloc[0] else "")

# Añadir leyenda para los tipos de fallas
handles, labels = ax.get_legend_handles_labels()
handles.append(plt.Line2D([0], [0], color='green', linestyle='--'))
labels.append('Falla Programada')
handles.append(plt.Line2D([0], [0], color='red', linestyle='--'))
labels.append('Falla Reactiva')
ax.legend(handles=handles, labels=labels)

# Añadir cuadro con información del camión y política
plt.text(1.02, 0.5, f'{camion_info}\n{politica_info}\n{anio_simulacion}', transform=ax.transAxes, fontsize=12, verticalalignment='center', bbox=dict(facecolor='white', alpha=0.5))

plt.savefig(os.path.join(output_dir, 'Kms_por_Operacion_Tiempo_Todas_Horas.png'), bbox_inches='tight')
plt.show()

# Gráfico de Toneladas por Operación a lo largo del tiempo con fallas (Todas las horas)
plt.figure(figsize=(14, 8))
ax = sns.lineplot(x='Hora_termino_operacion', y='Tons_por_operacion', data=df_comportamiento, marker='o', label='Toneladas por Operación')
plt.ylabel('Toneladas')
plt.title('Toneladas por Operación a lo largo del tiempo (Todas las horas)')
plt.legend()

# Añadir líneas verticales para las fallas programadas (verdes) y reactivas (rojas)
for xc in df_fallas_programadas['Horas_mantenciones_programadas']:
    plt.axvline(x=xc, color='green', linestyle='--', label='Falla Programada' if xc == df_fallas_programadas['Horas_mantenciones_programadas'].iloc[0] else "")
for xc in df_fallas_reactivas['Horas_mantenciones_reactivas']:
    plt.axvline(x=xc, color='red', linestyle='--', label='Falla Reactiva' if xc == df_fallas_reactivas['Horas_mantenciones_reactivas'].iloc[0] else "")

# Añadir leyenda para los tipos de fallas
handles, labels = ax.get_legend_handles_labels()
handles.append(plt.Line2D([0], [0], color='green', linestyle='--'))
labels.append('Falla Programada')
handles.append(plt.Line2D([0], [0], color='red', linestyle='--'))
labels.append('Falla Reactiva')
ax.legend(handles=handles, labels=labels)

# Añadir cuadro con información del camión y política
plt.text(1.02, 0.5, f'{camion_info}\n{politica_info}\n{anio_simulacion}', transform=ax.transAxes, fontsize=12, verticalalignment='center', bbox=dict(facecolor='white', alpha=0.5))

plt.savefig(os.path.join(output_dir, 'Toneladas_por_Operacion_Tiempo_Todas_Horas.png'), bbox_inches='tight')
plt.show()