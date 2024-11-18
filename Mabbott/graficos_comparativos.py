import pandas as pd
import matplotlib.pyplot as plt

# Cargar los datos de los archivos CSV
df_politica = pd.read_csv('Resultados/umbral_0.358/KPIs_finales.csv')
df_base = pd.read_csv('Resultados/casos_base/KPIs_finales_cbase.csv')

# Crear gráficos comparativos
def crear_graficos_comparativos():
    # Comparar Factor Toneladas
    plt.figure(figsize=(10, 6))
    plt.plot(df_politica['Dias'], df_politica['Factor Toneladas'], marker='o', label='Política Reactiva (Umbral 0.358)')
    plt.plot(df_base['Dias'], df_base['Factor Toneladas'], marker='o', label='Caso Base (Umbral 0)')
    plt.xlabel('Días')
    plt.ylabel('Factor Toneladas')
    plt.title('Comparación del Factor Toneladas a lo largo del tiempo')
    plt.legend()
    plt.grid(True)
    plt.savefig('Resultados/Graficos/Comparacion_Factor_Toneladas.png')
    plt.show()

    # Comparar Factor Kilómetros
    plt.figure(figsize=(10, 6))
    plt.plot(df_politica['Dias'], df_politica['Factor Kilometros'], marker='o', label='Política Reactiva (Umbral 0.358)')
    plt.plot(df_base['Dias'], df_base['Factor Kilometros'], marker='o', label='Caso Base (Umbral 0)')
    plt.xlabel('Días')
    plt.ylabel('Factor Kilómetros')
    plt.title('Comparación del Factor Kilómetros a lo largo del tiempo')
    plt.legend()
    plt.grid(True)
    plt.savefig('Resultados/Graficos/Comparacion_Factor_Kilometros.png')
    plt.show()

    # Comparar ambos factores en un solo gráfico
    plt.figure(figsize=(10, 6))
    plt.plot(df_politica['Dias'], df_politica['Factor Toneladas'], marker='o', label='Factor Toneladas - Política Reactiva (Umbral 0.358)')
    plt.plot(df_base['Dias'], df_base['Factor Toneladas'], marker='o', label='Factor Toneladas - Caso Base (Umbral 0)')
    plt.plot(df_politica['Dias'], df_politica['Factor Kilometros'], marker='o', linestyle='--', label='Factor Kilómetros - Política Reactiva (Umbral 0.358)')
    plt.plot(df_base['Dias'], df_base['Factor Kilometros'], marker='o', linestyle='--', label='Factor Kilómetros - Caso Base (Umbral 0)')
    plt.xlabel('Días')
    plt.ylabel('Factor')
    plt.title('Comparación de Factores a lo largo del tiempo')
    plt.legend()
    plt.grid(True)
    plt.savefig('Resultados/Graficos/Comparacion_Factores.png')
    plt.show()

if __name__ == "__main__":
    crear_graficos_comparativos()