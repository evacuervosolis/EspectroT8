from datetime import datetime
import pytz

def tiempo(utc_time_str):
    # Convertimos el string UTC a un objeto datetime
    utc_time = datetime.strptime(utc_time_str, "%Y-%m-%d %H:%M:%S")
    
    # Asignamos la zona horaria UTC
    utc_time = pytz.utc.localize(utc_time)
    
    # Convertimos a segundos desde la época (sin afectar la zona horaria)
    epoch_time = int(utc_time.timestamp())
    
    return epoch_time

utc_time_str = "2019-04-11 18:25:54"  
epoch_seconds = tiempo(utc_time_str)
print(epoch_seconds)
