import pandas as pd
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter

# Crear un DataFrame con los datos que has proporcionado
df = pd.read_csv('base_de_datos')

# Crear el modelo Kaplan-Meier
kmf = KaplanMeierFitter()

# Ajustar el modelo Kaplan-Meier con los datos de "Edad" (tiempo hasta la falla) y "Falla"
kmf.fit(df['Edad'], event_observed=df['Falla'])

# Graficar la curva de supervivencia
kmf.plot_survival_function()
plt.title('Curva de Supervivencia de Kaplan-Meier (Tiempo hasta la Falla)')
plt.xlabel('Tiempo (Edad)')
plt.ylabel('Probabilidad de Supervivencia')
plt.show()
