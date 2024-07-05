# AcuiferoEC

Este paquete calcula el volumen de agua almacenada en un sistema de acuíferos dado por una matriz 3×3 que representa las longitudes, anchos y profundidades en diferentes puntos del acuífero.

## Contenido del módulo `acuifero.py`

```python
import numpy as np

def calcular_volumen_agua(D):
    """
    Calcula el volumen de agua basado en las dimensiones proporcionadas.
    
    Parámetros:
    D (numpy.ndarray): Un array 2D donde cada fila representa una dimensión:
        - La primera fila contiene las longitudes.
        - La segunda fila contiene los anchos.
        - La tercera fila contiene los promedios.

    Devuelve:
    float: El volumen calculado como el producto de las medias de las longitudes, los anchos y los promedios.
    """
    # Calcular las medias de cada fila
    L, A, P = np.mean(D, axis=1)  # L: longitudes, A: anchos, P: promedios
    
    # Calcular el volumen
    V = L * A * P
    
    return V

