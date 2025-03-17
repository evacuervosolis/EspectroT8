# Importamos los módulos necesarios
import os
import numpy as np
from dotenv import load_dotenv
from datetime import datetime
import requests
from espectroT8.desc import decode_and_convert_to_float
import matplotlib.pyplot as plt
from espectroT8.espectro import get_spectrum_from_api
from espectroT8.espectro import get_spectrum_from_waveform
from espectroT8.desc import url_generator
# -------------------------------------------------------------------------------------------------------------------------------------


# Cargar las variables de entorno
load_dotenv()
user = os.getenv("T8_USER")
password = os.getenv("T8_PASSWORD")

# Parámetros para la API
urlS = url_generator(
    "spectra", "LP_Turbine", "MAD31CY005", "AM1", 2019, 4, 11, 18, 25, 54
)
urlW = url_generator(
    "waves", "LP_Turbine", "MAD31CY005", "AM1", 2019, 4, 11, 18, 25, 54
)

# Obtener el espectro original de la API de T8
freq_original, espectro_original = get_spectrum_from_api(urlS, user, password)

# Obtener el espectro calculado (de la señal de onda)
freq_calculado, espectro_calculado = get_spectrum_from_waveform(urlW, user, password)

# -------------------------------------------------------------------------------------------------------------
# Crear la figura para la comparación
plt.figure(figsize=(10, 6))

# Espectro calculado (de la FFT)
plt.plot(
    freq_calculado, espectro_calculado, label="Espectro calculado (FFT)", color="blue"
)

# Espectro original (de la API)
plt.plot(
    freq_original,
    espectro_original,
    label="Espectro original",
    color="red",
    linestyle="--",
)


# Título y etiquetas
plt.title("Comparación de Espectros")
plt.xlabel("Frecuencia (Hz)")
plt.ylabel("Magnitud")
plt.legend()  # Mostrar la leyenda
plt.grid(True)
plt.show()
# --------------------------------------------------------------------------------------------------------------------------------
