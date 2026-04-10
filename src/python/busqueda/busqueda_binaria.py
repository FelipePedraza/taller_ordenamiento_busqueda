"""
Busqueda Binaria (Binary Search) - Implementacion en Python.
Fuente: GeeksforGeeks

Algoritmo de busqueda eficiente para arreglos ordenados.
Divide repetidamente el espacio de busqueda a la mitad.

Complejidad: O(log n)
Requisito: El arreglo debe estar ordenado.
"""

from typing import List, Optional


def busqueda_binaria(arr: List[int], target: int) -> Optional[int]:
    """
    Realiza busqueda binaria en un arreglo ordenado.

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
        # Calcular punto medio (evita overflow)
        mid = left + (right - left) // 2

        # Elemento encontrado
        if arr[mid] == target:
            return mid

        # Si el target es menor, ignorar mitad derecha
        if arr[mid] > target:
            right = mid - 1
        # Si el target es mayor, ignorar mitad izquierda
        else:
            left = mid + 1

    # Elemento no encontrado
    return None
