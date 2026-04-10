"""
Busqueda Ternaria (Ternary Search) - Implementacion en Python.
Fuente: GeeksforGeeks

Algoritmo de busqueda para arreglos ordenados que divide
el espacio de busqueda en tres partes usando dos puntos medios.

Complejidad: O(log3 n)
Requisito: El arreglo debe estar ordenado.
"""

from typing import List, Optional


def busqueda_ternaria(arr: List[int], target: int) -> Optional[int]:
    """
    Realiza busqueda ternaria en un arreglo ordenado.

    Args:
        arr: Lista ordenada de enteros
        target: Valor a buscar

    Returns:
        Indice del elemento si se encuentra, None en caso contrario
    """
    if not arr:
        return None

    left = 0
    right = len(arr) - 1

    while left <= right:
        # Dividir el rango en tres partes
        third = (right - left) // 3
        mid1 = left + third
        mid2 = right - third

        # Verificar si el target esta en alguno de los puntos medios
        if arr[mid1] == target:
            return mid1

        if arr[mid2] == target:
            return mid2

        # Determinar en cual de las tres secciones continuar
        if target < arr[mid1]:
            right = mid1 - 1
        elif target > arr[mid2]:
            left = mid2 + 1
        else:
            left = mid1 + 1
            right = mid2 - 1

    return None
