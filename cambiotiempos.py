from datetime import datetime

# Función para convertir UTC a segundos desde la época
def tiempo(utc_time_str):
    # Convertimos el string UTC a un objeto datetime
    utc_time = datetime.strptime(utc_time_str, "%Y-%m-%d %H:%M:%S")

    # Convertimos el objeto datetime en segundos desde la época
    epoch_time = int(utc_time.timestamp())

    return epoch_time

utc_time_str = "2019-04-11 18:25:54"  
epoch_seconds = tiempo(utc_time_str)

print(f"El tiempo UTC '{utc_time_str}' es {epoch_seconds} segundos desde la época (epoch).")
