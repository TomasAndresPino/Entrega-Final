import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.stats import gaussian_kde


# Lee el archivo CSV
df = pd.read_csv('maintenance_data.csv')
df_1 = pd.read_csv('part_data.csv')

mantenciones = df.merge(df_1, on='Part_ID', how='left')
mantenciones['pieza_tipo'] = mantenciones['Part_ID'] +  '\n' + '(' + mantenciones['Part_Type'] + ')'

mantenciones = mantenciones.groupby(['pieza_tipo']).size().reset_index(name='Cantidad')
mantenciones = mantenciones.sort_values(ascending=False, by=['Cantidad'])
mantenciones_1 = mantenciones.head(7)
print(mantenciones_1)


colors_sorted = plt.cm.viridis(np.linspace(0, 1, len(mantenciones_1)))
plt.figure(figsize=(10, 8))
bars = plt.bar(mantenciones_1['pieza_tipo'], mantenciones_1['Cantidad'], color=colors_sorted)

plt.xlabel('Máquina - Pieza')
plt.ylabel('Cantidad')
plt.title('Histograma de ocurrencias por Máquina y Pieza')
plt.xticks(fontsize='small')
plt.xticks(rotation=12)
plt.show()