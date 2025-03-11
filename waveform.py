import os
import numpy as np
from dotenv import load_dotenv
from datetime import datetime
import requests
from espectroT8.desc import zint_to_float
import matplotlib.pyplot as plt
from requests.auth import HTTPBasicAuth

# Parámetros para la API
url = "http://lzfs45.mirror.twave.io/lzfs45/rest/waves/LP_Turbine/MAD31CY005/AM1/1555007154"
user = 'practicas'
password = 'Practicas2025'

factor = 0.034013085
sample_rate = 5120  # Frecuencia de muestreo

# Pedir los datos
response = requests.get(url, auth=HTTPBasicAuth(user, password))
waveform = zint_to_float(response.json()["data"])  # Esto debería ser una lista de valores numéricos

# vamos a imprimir por pantalla los primeros valores de la señal para asegurarse de que es correcta
print(waveform[:10]) 

#multiplicamos por el factor dado en la API T8
adjusted_waveform = waveform * factor

# Aplicar la ventana Hanning antes de hacer la FFT
window = np.hanning(len(adjusted_waveform))
windowed_waveform = adjusted_waveform * window

# Aplicar zero-padding antes de hacer la FFT
n = len(windowed_waveform)
n_zero_padded = n * 4 
zero_padded_waveform = np.pad(windowed_waveform, (0, n_zero_padded - n), 'constant')

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

#Graficar las longitudes de onda
t=np.linspace(0,len(adjusted_waveform)/sample_rate,len(adjusted_waveform))
#Vamos a graficar ahora las longitudes de onda
plt.plot(t, adjusted_waveform)
plt.title('Longitudes de onda frente a t')
plt.xlabel('tiempo (s)')
plt.ylabel('Longitud de onda')
plt.grid(True)
plt.show()

# Graficar el espectro
plt.figure(figsize=(10, 6))
plt.plot(positive_freqs, normalized_magnitude)
plt.title('Espectro de la señal')
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Magnitud')
plt.grid(True)
plt.show()
