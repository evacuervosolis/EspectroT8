import numpy as np
import requests

from espectroT8.desc import (
    decode_and_convert_to_float,
)


def get_spectrum_from_api(url, user, password):
    """Obtiene el espectro original de la API de T8 y lo normaliza.

    Args:
        url (str): URL para obtener los datos del espectro.
        user (str): Usuario para autenticación.
        password (str): Contraseña para autenticación.

    Returns:
        tuple: Contiene las frecuencias y la magnitud del espectro original normalizada.
    """
    response = requests.get(url, auth=(user, password), timeout=30)
    espectro = decode_and_convert_to_float(response.json()["data"])

    # Frecuencias obtenidas de la API
    min_freq = 2.5
    max_freq = 2000
    freq = np.linspace(min_freq, max_freq, len(espectro))

    return freq, espectro


def get_spectrum_from_waveform(
    url, user, password, factor=0.034013085, sample_rate=5120
):
    """Obtiene la señal de la API, aplica la ventana Hanning, hace zero-padding
    y calcula el espectro usando la FFT.

    Args:
        url (str): URL para obtener los datos de la forma de onda.
        user (str): Usuario para autenticación.
        password (str): Contraseña para autenticación.
        factor (float, optional): Factor de escala para la señal.
        sample_rate (int, optional): Frecuencia de muestreo. Default es 5120.

    Returns:
        tuple: Contiene las frecuencias y la magnitud del espectro calculado.
    """

    response = requests.get(url, auth=(user, password), timeout=30)
    waveform = decode_and_convert_to_float(response.json()["data"])
    adjusted_waveform = waveform * factor

    # Aplicar la ventana Hanning
    window = np.hanning(len(adjusted_waveform))
    windowed_waveform = adjusted_waveform * window

    # Zero-padding
    n = len(windowed_waveform)
    n_zero_padded = n * 4
    zero_padded_waveform = np.pad(windowed_waveform, (0, n_zero_padded - n), "constant")

    # Calcular la FFT
    fft_signal = np.fft.fft(zero_padded_waveform)
    fft_signal = np.fft.fftshift(fft_signal)
    magnitude = np.abs(fft_signal)

    # Generar las frecuencias correspondientes
    freqs = np.fft.fftfreq(n_zero_padded, 1 / sample_rate)
    freqs = np.fft.fftshift(freqs)

    positive_freqs = freqs[(freqs > 2.5) & (freqs < 2000)]
    positive_magnitude = magnitude[(freqs > 2.5) & (freqs < 2000)]

    return positive_freqs, positive_magnitude
