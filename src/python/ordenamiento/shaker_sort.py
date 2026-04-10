"""
Shaker Sort (Cocktail Sort) - Implementacion en Python.
Fuente: GeeksforGeeks

Variante del Bubble Sort que ordena en ambas direcciones.

Complejidad: O(n^2)
Ventaja: reduce iteraciones comparado con Bubble Sort.
"""

from typing import List


def shaker_sort(arr: List[int]) -> List[int]:
    """
    Ordena un arreglo usando el algoritmo Shaker Sort.

    Args:
        arr: Lista de enteros a ordenar

    Returns:
        Nueva lista ordenada en orden ascendente
    """
    if not arr:
        return []

    result = arr.copy()
    n = len(result)

    if n <= 1:
        return result

    left = 0
    right = n - 1

    while left < right:
        swapped = False

        # Pasada de izquierda a derecha
        for i in range(left, right):
            if result[i] > result[i + 1]:
                result[i], result[i + 1] = result[i + 1], result[i]
                swapped = True

        if not swapped:
            break

        right -= 1

        # Pasada de derecha a izquierda
        for i in range(right - 1, left - 1, -1):
            if result[i] > result[i + 1]:
                result[i], result[i + 1] = result[i + 1], result[i]
                swapped = True

        if not swapped:
            break

        left += 1

    return result
