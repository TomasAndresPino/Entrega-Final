import pandas as pd
import matplotlib.pyplot as plt
datos = [2505.38, 2161.3599999999997, 3281.969999999998, 2323.4500000000003, 2598.119999999999, 1123.63, 271.49, 849.8100000000001, 396.48, 567.0999999999999, 1738.3399999999997, 1812.9299999999996, 1722.52, 1861.29, 2735.930000000001, 1923.1200000000001, 1866.450000000001, 482.23, 2047.9400000000007, 742.8499999999999, 732.07, 1353.23, 895.58, 2643.9400000000014, 2180.62, 1914.6300000000006, 2330.5, 913.1400000000002, 3850.1300000000006, 2118.7700000000004, 3345.17, 2533.310000000001, 2088.620000000001, 1078.3799999999999, 2377.290000000001, 2384.279999999998, 3060.6100000000015, 3185.189999999999, 2605.2700000000004, 2155.860000000001, 691.62, 4739.75, 2457.090000000001, 1630.94, 2768.7599999999998, 1673.58, 2564.37, 1531.0399999999995, 3440.7000000000007, 851.8399999999998, 1649.3100000000002, 3457.350000000001, 1154.2600000000004, 1542.67, 2258.6299999999997, 2162.7199999999993, 2900.85, 2446.8600000000006, 1990.3600000000004, 2636.0300000000007, 2600.79, 4035.679999999998, 2660.93, 3234.559999999999, 2968.0, 1825.51, 3181.3299999999995, 2404.079999999999, 2521.7899999999995, 3195.2500000000005, 1631.07, 3328.6899999999996, 1697.9800000000005, 1704.1499999999996, 1414.2299999999996, 3349.789999999998, 2675.690000000001, 4025.190000000001, 2638.85, 2410.18, 2355.9799999999987, 1424.2800000000004, 3875.2, 4282.240000000001, 2824.3899999999994, 4048.6100000000024, 1599.0, 1523.490000000001, 2932.9900000000002]
# Leer el archivo CSV
df = pd.read_csv('sensor_data.csv')

# Convertir la columna 'Date_Time' a tipo datetime
df['Date_Time'] = pd.to_datetime(df['Date_Time'], format='%m/%d/%Y %H:%M')
df = df.dropna(subset=['Engine_Temperature'])
df = df[(df['Date_Time'].dt.year == 2022)]
df = df[(df['Date_Time'].dt.month.isin([9]))]
df = df[(df['Engine_Temperature'] >= 60) & (df['Engine_Temperature'] <=90)]
df_filtered = df[df['Machine_ID'] == 'OKU9UWCY']
df_filtered = df_filtered.sort_values(by=['Date_Time'])
df = df_filtered

# Configurar el índice del DataFrame como la fecha y hora
df.set_index('Date_Time', inplace=True)


df_maint = pd.read_csv('maintenance_data.csv')
df_maint['Start_Time'] = pd.to_datetime(df_maint['Start_Time'], format='%m/%d/%Y %H:%M')
df_maint = df_maint[(df_maint['Start_Time'].dt.year == 2022)]
df_maint = df_maint[(df_maint['Start_Time'].dt.month.isin([9]))]
df_maint = df_maint[df_maint['Machine_ID'] == 'OKU9UWCY']
#df_maint = df_maint[(df_maint['Failure_Mode'] != 0)]

plt.figure(figsize=(12, 6))
plt.plot(df.index, df['Engine_Temperature'], marker='o', linestyle='-', color='b')
contador = 0
for maint_time in df_maint['Start_Time']:
    plt.axvline(x=maint_time, color='r', linestyle='-', linewidth=0.5, label='Mantenimiento')
    contador +=1
print(contador)

# Graficar la temperatura


plt.title('Temperatura Septiembre 2022: OKU9UWCY')
plt.xlabel('Fecha y Hora')
plt.ylabel('Temperatura: OKU9UWCY')
plt.xticks(rotation=45)
plt.tight_layout()

# Mostrar el gráfico
plt.show()
