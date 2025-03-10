
#Importo los módulos que voy a utilizar
import os #leer variables entorno
import numpy as np
from dotenv import load_dotenv #credenciales de la API
#from datetime import datetime
#import requests #peticiones HTP a la api
from espectroT8.desc import zint_to_float
import requests
from requests.auth import HTTPBasicAuth
import matplotlib.pyplot as plt
import json

# Parámetros para la API
url = "http://lzfs45.mirror.twave.io/lzfs45/rest/spectra/LP_Turbine/MAD31CY005/AM1/1555007154"
user = 'practicas'  # Usuario de autenticación
password = 'Practicas2025'  # Contraseña de autenticación

# Pedimos los datos
response = requests.get(url, auth=HTTPBasicAuth(user, password))
espectro = zint_to_float(response.json()["data"])# Esto debería ser una lista de valores numéricos


# Cargar variables de entorno
load_dotenv()
T8_USER = os.getenv("T8_USER")
T8_PASSWORD = os.getenv("T8_PASSWORD")


#Gráfica del espectro
min_freq=2.5 #valores concreto de la maquina
max_freq=2000
freq = np.linspace(min_freq, max_freq, len(espectro))
plt.plot(freq, espectro)
plt.title('Espectro de la señal')
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Espectro')
plt.grid(True)
plt.show()