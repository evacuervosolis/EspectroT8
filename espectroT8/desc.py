import numpy as np
from struct import unpack
from base64 import b64decode
from zlib import decompress
from datetime import UTC, datetime



def decode_and_convert_to_float(raw_data: str) -> np.ndarray:
    """
    Esta función toma una cadena raw (codificada en base64), la descomprime y 
    convierte los datos a un arreglo de tipo float.

    :param raw_data: Cadena de texto codificada en base64
    :return: Un array de tipo float con los datos descomprimidos
    """
    # Descomprimir los datos
    decompressed_data = decompress(b64decode(raw_data.encode()))

    # Convertir los datos descomprimidos en valores flotantes
    float_array = np.array(
        [unpack("h", decompressed_data[i * 2 : (i + 1) * 2])[0] for i in range(int(len(decompressed_data) / 2))],
        dtype="f",
    )
    return float_array

def url_generator(type, machine, point, pmode, year, month, day, hour, min, seg):
    utc_time = datetime(year, month, day, hour, min, seg, tzinfo=UTC)
    timestamp = int(utc_time.timestamp())

    URL=f'https://lzfs45.mirror.twave.io/lzfs45/rest/{type}/{machine}/{point}/{pmode}/{timestamp}'

    return URL
