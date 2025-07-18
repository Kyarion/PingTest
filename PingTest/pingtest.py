import subprocess
import datetime
import platform
import re
import time
import csv
import os

# Dirección del host
host = "8.8.8.8"
# Ruta del archivo CSV
csv_file = "ping_log.csv"

# Detectar sistema operativo
system = platform.system().lower()
param = "-n" if system == "windows" else "-c"
command = ["ping", param, "1", host]

# Escribir encabezado del CSV si no existe
if not os.path.isfile(csv_file):
    with open(csv_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "host", "status", "ping_ms"])

for i in range(720):  # Repetir 1000 veces
    try:
        # Ejecutar ping
        output = subprocess.run(command, capture_output=True, text=True)
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        success = output.returncode == 0
        result = "OK" if success else "FAIL"
        ping_time = "N/A"
        
        if success:
            match = re.search(r"time[=<]?\s*=?\s*(\d+(?:\.\d+)?)\s*ms", output.stdout, re.IGNORECASE)
            if match:
                ping_time = match.group(1)


        # Escribir fila en el CSV
        with open(csv_file, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([now, host, result, ping_time])

        # Mostrar en consola
        print(f"[{now}] Ping {host} - {result} - {ping_time} ms")

    except Exception as e:
        print(f"Error: {e}")

    # Esperar 60 segundos antes de repetir
    time.sleep(5)
