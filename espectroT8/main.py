#Importamos los módulos necesarios
import os
import numpy as np
from dotenv import load_dotenv
from datetime import datetime
import requests
from espectroT8.desc import decode_and_convert_to_float
import matplotlib.pyplot as plt
from requests.auth import HTTPBasicAuth
#€-------------------------------------------------------------------------------------------------------------------------------------

###CARGAMOS LOS DATOS DE LA API DEL T8
# Parámetros para la API
urlS = "http://lzfs45.mirror.twave.io/lzfs45/rest/spectra/LP_Turbine/MAD31CY005/AM1/1555007154"
urlW = "http://lzfs45.mirror.twave.io/lzfs45/rest/waves/LP_Turbine/MAD31CY005/AM1/1555007154"
#Cargar variables de entorno
load_dotenv()
user = os.getenv("T8_USER")
password = os.getenv("T8_PASSWORD")
# Pedir los datos
responseW = requests.get(urlW, auth=HTTPBasicAuth(user, password))
waveform = decode_and_convert_to_float(responseW.json()["data"])  # Esto debería ser una lista de valores numéricos
responseS = requests.get(urlS, auth=HTTPBasicAuth(user, password))
espectro = decode_and_convert_to_float(responseS.json()["data"]) 
#------------------------------------------------------------------------------------------------------------------

#multiplicamos por el factor dado en la API T8
factor = 0.034013085
sample_rate = 5120  # Frecuencia de muestreo
adjusted_waveform = waveform * factor

# Aplicar la ventana Hanning antes de hacer la FFT
window = np.hanning(len(adjusted_waveform))
windowed_waveform = adjusted_waveform * window

# Aplicar zero-padding antes de hacer la FFT
n = len(windowed_waveform)
n_zero_padded = n * 4 
zero_padded_waveform = np.pad(windowed_waveform, (0, n_zero_padded - n), 'constant')
#---------------------------------------------------------------------------------------------------------------------------------
# Calculo explícito de la FFT
fft_signal = np.fft.fft(zero_padded_waveform)
fft_signal = np.fft.fftshift(fft_signal)  

# Obtener la magnitud del espectro
magnitude = np.abs(fft_signal)

# Generar las frecuencias correspondientes
freqs = np.fft.fftfreq(n_zero_padded, 1/sample_rate)
freqs = np.fft.fftshift(freqs)  # Desplazar las frecuencias para 0 Hz en el centro

# Filtrar solo las frecuencias entre 2.5 y 2000 Hz (ya que son los límites que nos daba la interfaz T8 para el espectro)
positive_freqs = freqs[(freqs > 2.5) & (freqs < 2000)]  
positive_magnitude = magnitude[(freqs > 2.5) & (freqs < 2000)]  

# Normalizamos el espectro para qeu sea más visual
normalized_magnitude = positive_magnitude / np.max(positive_magnitude)
#--------------------------------------------------------------------------------------------------------------------------


#Gráfica del espectro
min_freq=2.5 #valores concreto de la maquina
max_freq=2000
freq = np.linspace(min_freq, max_freq, len(espectro))
normalized_espectro = espectro / np.max(espectro)
#-------------------------------------------------------------------------------------------------------------------------------
#Gráfico comparando ambos espectros
plt.figure(figsize=(10, 6))
# Espectro calculado
plt.plot(positive_freqs, normalized_magnitude, label='Espectro calculado (FFT)', color='blue')
# Espectro original
plt.plot(freq, normalized_espectro, label='Espectro original', color='red', linestyle='--')
# Título y etiquetas
plt.title('Comparación de Espectros')
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Magnitud')
plt.legend()  # Para mostrar la leyenda
plt.grid(True)
plt.show()
#--------------------------------------------------------------------------------------------------------------------------------