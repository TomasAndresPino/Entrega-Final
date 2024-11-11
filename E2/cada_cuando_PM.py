import pandas as pd

# Cargar toda la base de datos desde un archivo CSV
df = pd.read_csv("maintenance_data.csv")

# Asegurarse de que las columnas de fecha estén en el formato correcto
df["Start_Time"] = pd.to_datetime(df["Start_Time"], format="%m/%d/%Y %H:%M")
df["End_Time"] = pd.to_datetime(df["End_Time"], format="%m/%d/%Y %H:%M")

# Filtrar para seleccionar solo los registros donde Machine_ID es "AWOU5IMX" y Failure_Mode es 0
df_filtrado = df[(df["Machine_ID"] == "AWOU5IMX") & (df["Failure_Mode"] == 0)]

# Ordenar el DataFrame filtrado por la columna de tiempo de inicio
df_filtrado = df_filtrado.sort_values(by="Start_Time")

# Calcular las diferencias de tiempo entre las mantenciones en horas
diferencias_tiempo = df_filtrado["Start_Time"].diff().dropna().dt.total_seconds() / 3600

# Calcular el promedio de las diferencias
promedio_diferencia = diferencias_tiempo.mean()

# Mostrar resultados
print("Diferencias entre mantenciones (en horas):", diferencias_tiempo.tolist())
print("Promedio de tiempo entre mantenciones (en horas):", promedio_diferencia)
