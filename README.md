# EspectroT8

Este proyecto permite obtener y analizar espectros de señales de la máquina **LP_Turbine** de T8. Los datos se extraen a través de la API T8 y se procesan para generar los espectros, tanto originales como calculados mediante la Transformada de Fourier (FFT).

Calcularemso el espectro para el caso concreto de:
- **Nombre de la máquina**: `LP_Turbine`.
- **Punto de medida**: `MAD31CY005`.
- **Modo de procesamiento**: `AM1`.
- **Fecha de captura (UTC)**: `11-04-2019 18:25:54`.


## Comparar los resultados

Se presenta una gráfica con los dos espectros superpuestos, el calculado a partir de la señal de onda y el obtenido directamente desde la API de T8. Esta comparación nos permite comprobar que los resultados sean similares y verificar la exactitud del cálculo realizado.


## Requisitos

Este proyecto requiere que tengas las siguientes bibliotecas instaladas:

- **`requests`**: Para hacer peticiones HTTP a la API.
- **`matplotlib`**: Para graficar los espectros.
- **`numpy`**: Para el manejo de arrays y el cálculo de la FFT.
- **`python-dotenv`**: Para cargar variables de entorno de forma segura.
- **`espectroT8.desc`**: Para descomprimir los datos obtenidos de la API.