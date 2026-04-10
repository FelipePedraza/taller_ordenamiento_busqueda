"""
Busqueda por Saltos (Jump Search) - Implementacion en Python.
Fuente: GeeksforGeeks

Algoritmo de busqueda para arreglos ordenados que salta
bloques de tamano sqrt(n) y luego hace busqueda lineal.

Complejidad: O(sqrt(n))
Requisito: El arreglo debe estar ordenado.
"""

import math
from typing import List, Optional


def jump_search(arr: List[int], target: int) -> Optional[int]:
    """
    Realiza busqueda por saltos en un arreglo ordenado.

    Args:
        arr: Lista ordenada de enteros
        target: Valor a buscar

    Returns:
        Indice del elemento si se encuentra, None en caso contrario
    """
    if not arr:
        return None

    n = len(arr)

    # Casos especiales
    if arr[0] == target:
        return 0

    if arr[-1] == target:
        return n - 1

    # Tamano optimo del salto: sqrt(n)
    step = int(math.sqrt(n))

    # Encontrar el bloque donde podria estar el elemento
    prev = 0
    current = step

    # Saltar bloques mientras el elemento del final del bloque
    # sea menor que el target
    while current < n and arr[current] <= target:
        if arr[current] == target:
            return current
        prev = current
        current += step
        if current >= n:
            current = n - 1
            break

    # Si nos pasamos, ajustar el limite superior
    if current >= n:
        current = n - 1

    # Busqueda lineal en el bloque identificado
    for i in range(prev + 1, min(current + 1, n)):
        if arr[i] == target:
            return i
        if arr[i] > target:
            break

    return None
