import pandas as pd

# Cargar el archivo CSV
data = pd.read_csv('C:/Users/tpin0/Desktop/Entrega-Final/E2/BasesCox/baseline_haz_suspension.csv')

# Eliminar duplicados consecutivos en la columna 'hazard'
data_unique = data.drop_duplicates(subset='hazard', keep='first')

# Guardar el DataFrame resultante en un nuevo archivo CSV
data_unique.to_csv('baseline_haz_suspension_filtrado.csv', index=False)
