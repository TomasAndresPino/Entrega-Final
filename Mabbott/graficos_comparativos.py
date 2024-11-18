import pandas as pd
import matplotlib.pyplot as plt
import os

# Cargar los datos de los archivos CSV
df_politica = pd.read_csv('Resultados/umbral_0.358/KPIs_finales.csv')
df_base = pd.read_csv('Resultados/casos_base/KPIs_finales_cbase.csv')
df_base_5d = pd.read_csv('Resultados/caso_base_5_dias/KPIs_finales_cbase5d.csv')

# Crear la carpeta de gráficos si no existe
output_dir = 'Resultados/Graficos'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Crear gráficos comparativos
def crear_graficos_comparativos():
    # Comparar Factor Toneladas
    plt.figure(figsize=(10, 6))
    plt.plot(df_politica['Dias'], df_politica['Factor Toneladas'], marker='o', label='Política Óptima Preventiva (Umbral 0.358)')
    plt.plot(df_base['Dias'], df_base['Factor Toneladas'], marker='o', label='Política Reactiva (Caso Base 1)')
    plt.plot(df_base_5d['Dias'], df_base_5d['Factor Toneladas'], marker='o', label='Política Actual (Caso Base 2)')
    plt.xlabel('Días')
    plt.ylabel('Factor Toneladas')
    plt.title('Comparación del Factor Toneladas a lo largo del tiempo')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(output_dir, 'Comparacion_Factor_Toneladas_2.png'))
    plt.show()

    # Comparar Factor Kilómetros
    plt.figure(figsize=(10, 6))
    plt.plot(df_politica['Dias'], df_politica['Factor Kilometros'], marker='o', label='Política Óptima Preventiva (Umbral 0.358)')
    plt.plot(df_base['Dias'], df_base['Factor Kilometros'], marker='o', label='Política Reactiva (Caso Base 1)')
    plt.plot(df_base_5d['Dias'], df_base_5d['Factor Kilometros'], marker='o', label='Política Actual (Caso Base 2)')
    plt.xlabel('Días')
    plt.ylabel('Factor Kilómetros')
    plt.title('Comparación del Factor Kilómetros a lo largo del tiempo')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(output_dir, 'Comparacion_Factor_Kilometros_2.png'))
    plt.show()

    # Comparar ambos factores en un solo gráfico
    plt.figure(figsize=(10, 6))
    plt.plot(df_politica['Dias'], df_politica['Factor Toneladas'], marker='o', label='Factor Toneladas - Política Óptima Preventiva (Umbral 0.358)')
    plt.plot(df_base['Dias'], df_base['Factor Toneladas'], marker='o', label='Factor Toneladas - Política Reactiva (Caso Base 1)')
    plt.plot(df_base_5d['Dias'], df_base_5d['Factor Toneladas'], marker='o', label='Factor Toneladas - Política Actual (Caso Base 2)')
    plt.plot(df_politica['Dias'], df_politica['Factor Kilometros'], marker='o', linestyle='--', label='Factor Kilómetros - Política Óptima Preventiva (Umbral 0.358)')
    plt.plot(df_base['Dias'], df_base['Factor Kilometros'], marker='o', linestyle='--', label='Factor Kilómetros - Política Reactiva (Caso Base 1)')
    plt.plot(df_base_5d['Dias'], df_base_5d['Factor Kilometros'], marker='o', linestyle='--', label='Factor Kilómetros - Política Actual (Caso Base 2)')
    plt.xlabel('Días')
    plt.ylabel('Factor')
    plt.title('Comparación de Factores a lo largo del tiempo')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(output_dir, 'Comparacion_Factores_2.png'))
    plt.show()

if __name__ == "__main__":
    crear_graficos_comparativos()