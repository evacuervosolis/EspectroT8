
#Creamos un código para pasar de el formato UTC a timestamp
#Importamos el módulo necesario
from datetime import datetime

# Definir la fecha en formato UTC 
utc_date_str = "2019-04-11 18:25:54"

# Convertir la cadena de texto a un objeto datetime en UTC
utc_date = datetime.strptime(utc_date_str, "%Y-%m-%d %H:%M:%S")

# Convertir a timestamp
timestamp = utc_date.timestamp()
#De esta forma me imprime por pantalla el tiempo en formato timestamp
print("La fecha UTC:", utc_date)
print("El timestamp correspondiente:", timestamp)
