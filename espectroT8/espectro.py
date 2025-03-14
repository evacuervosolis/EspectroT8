# Importo los módulos que voy a utilizar
import os #leer variables entorno
import numpy as np
from dotenv import load_dotenv #credenciales de la API
from espectroT8.desc import decode_and_convert_to_float #Para poder descomprimir los datos
from espectroT8.desc import url_generator
import requests
from requests.auth import HTTPBasicAuth
import matplotlib.pyplot as plt
import json
#-------------------------------------------------------------------------------------------------------------------------

def get_spectrum_from_api(url, user, password):
    """
    Función que obtiene el espectro original de la API de T8 y lo normaliza.
    
    Parámetros:
    - url: URL para obtener los datos del espectro.
    - user: Usuario para autenticación.
    - password: Contraseña para autenticación.
    
    Retorna:
    - freqs: Las frecuencias del espectro original.
    - normalized_espectro: La magnitud del espectro original normalizada.
    """
    
    # Pedir los datos del espectro
    response = requests.get(url, auth=(user, password))
    espectro = decode_and_convert_to_float(response.json()["data"])       # Decodificar los datos
    
    # Generar las frecuencias correspondientes
    min_freq = 2.5  # Frecuencia mínima según la API
    max_freq = 2000  # Frecuencia máxima según la API
    freq = np.linspace(min_freq, max_freq, len(espectro))
    
    return freq, espectro
#-----------------------------------------------------------------------------------------------------------------------
def get_spectrum_from_waveform(url, user, password, factor=0.034013085, sample_rate=5120):
    """
    Función que obtiene la señal de la API, aplica la ventana Hanning, hace zero-padding
    y calcula el espectro usando la FFT.
    
    Parámetros:
    - url: URL para obtener los datos de la forma de onda.
    - user: Usuario para autenticación.
    - password: Contraseña para autenticación.
    - factor: Factor de escala para la señal.
    - sample_rate: Frecuencia de muestreo.
    
    Retorna:
    - freqs: Las frecuencias correspondientes al espectro calculado.
    - normalized_magnitude: La magnitud del espectro normalizado.
    """
    
    # Pedir los datos de la forma de onda
    response = requests.get(url, auth=(user, password))
    waveform = decode_and_convert_to_float(response.json()["data"])  # Decodificar los datos
    
    # Multiplicar la señal por el factor
    adjusted_waveform = waveform * factor
    
    # Aplicar la ventana Hanning
    window = np.hanning(len(adjusted_waveform))
    windowed_waveform = adjusted_waveform * window
    
    # Zero-padding
    n = len(windowed_waveform)
    n_zero_padded = n * 4  # Zero-padding con factor 4
    zero_padded_waveform = np.pad(windowed_waveform, (0, n_zero_padded - n), 'constant')
    
    # Calcular la FFT
    fft_signal = np.fft.fft(zero_padded_waveform)
    fft_signal = np.fft.fftshift(fft_signal)  # Desplazar para centrar en 0 Hz
    
    # Obtener la magnitud del espectro
    magnitude = np.abs(fft_signal)
    
    # Generar las frecuencias correspondientes
    freqs = np.fft.fftfreq(n_zero_padded, 1/sample_rate)
    freqs = np.fft.fftshift(freqs)  # Desplazar las frecuencias para que 0 Hz esté en el centro
    
    # Filtrar las frecuencias entre 2.5 y 2000 Hz
    positive_freqs = freqs[(freqs > 2.5) & (freqs < 2000)]
    positive_magnitude = magnitude[(freqs > 2.5) & (freqs < 2000)]
    
    return positive_freqs, positive_magnitude

#-----------------------------------------------------------------------------------------------------------------------------------
