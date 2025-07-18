import pandas as pd
import matplotlib.pyplot as plt

# Leer el archivo CSV
df = pd.read_csv("ping_log.csv")

# Convertir la columna timestamp a datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Convertir ping_ms a numérico, reemplazando N/A con NaN
df['ping_ms'] = pd.to_numeric(df['ping_ms'], errors='coerce')

# Calcular estadísticas
total = len(df)
na_count = df['ping_ms'].isna().sum()
na_pct = (na_count / total) * 100

avg_ping = df['ping_ms'].mean()
max_ping = df['ping_ms'].max()
min_ping = df['ping_ms'].min()

# Eliminar filas con NaN para graficar
df_clean = df.dropna(subset=['ping_ms'])

# Crear gráfico
plt.figure(figsize=(12, 6))
plt.plot(df_clean['timestamp'], df_clean['ping_ms'], marker='o', linestyle='-', markersize=3, label='Ping (ms)')

# Añadir líneas de promedio, máximo y mínimo
plt.axhline(avg_ping, color='orange', linestyle='--', label=f'Promedio: {avg_ping:.2f} ms')
plt.axhline(max_ping, color='red', linestyle='--', label=f'Máximo: {max_ping:.2f} ms')
plt.axhline(min_ping, color='green', linestyle='--', label=f'Mínimo: {min_ping:.2f} ms')

# Títulos y etiquetas
plt.title("Histórico de Ping (ms)")
plt.xlabel("Fecha y hora")
plt.ylabel("Tiempo de respuesta (ms)")
plt.grid(True)
plt.xticks(rotation=45)
plt.legend()

# Texto adicional con porcentaje de N/A
plt.figtext(0.99, 0.01, f"% de fallos (N/A): {na_pct:.2f}%", horizontalalignment='right')

# Guardar como PDF
plt.tight_layout()
plt.savefig("grafico_ping.pdf")

# También puedes mostrarlo si quieres
plt.show()
