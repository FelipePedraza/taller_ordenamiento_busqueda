import time
from typing import Callable, Any


def medir_ordenamiento(
    algoritmo: Callable[[list], list],
    datos: list,
    repeticiones: int = 1
) -> float:
    """
    Mide el tiempo de ejecucion de un algoritmo de ordenamiento.

    Args:
        algoritmo: Funcion de ordenamiento
        datos: Lista de entrada
        repeticiones: Numero de ejecuciones para promediar

    Returns:
        Tiempo promedio en milisegundos
    """
    tiempos = []

    for _ in range(repeticiones):
        datos_copia = datos.copy()
        inicio = time.perf_counter()
        algoritmo(datos_copia)
        fin = time.perf_counter()
        tiempos.append((fin - inicio) * 1000)

    return sum(tiempos) / len(tiempos)


def medir_busqueda(
    algoritmo: Callable,
    datos: list,
    valor: Any,
    repeticiones: int = 10
) -> float:
    """
    Mide el tiempo de ejecucion de un algoritmo de busqueda.

    Args:
        algoritmo: Funcion de busqueda
        datos: Lista donde buscar
        valor: Valor a buscar
        repeticiones: Numero de ejecuciones para promediar

    Returns:
        Tiempo promedio en nanosegundos
    """
    tiempos = []

    for _ in range(repeticiones):
        inicio = time.perf_counter()
        algoritmo(datos, valor)
        fin = time.perf_counter()
        tiempos.append((fin - inicio) * 1_000_000_000)

    return sum(tiempos) / len(tiempos)
