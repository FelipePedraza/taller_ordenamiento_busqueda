"""
Shaker Sort (Cocktail Sort) - Implementación en Python.

Variante del Bubble Sort que ordena en ambas direcciones:
- De izquierda a derecha (mueve el elemento más grande al final)
- De derecha a izquierda (mueve el elemento más pequeño al inicio)

Complejidad:
- Peor caso: O(n²)
- Mejor caso: O(n) - cuando el arreglo ya está ordenado
- Caso promedio: O(n²)
- Espacio: O(1)

Ventaja: reduce el número de iteraciones comparado con Bubble Sort estándar.
"""

from typing import List


def shaker_sort(arr: List[int]) -> List[int]:
    """
    Ordena un arreglo usando el algoritmo Shaker Sort (Cocktail Sort).

    Args:
        arr: Lista de enteros a ordenar

    Returns:
        Nueva lista ordenada en orden ascendente
    """
    if not arr:
        return []

    # Crear copia para no modificar el original
    result = arr.copy()
    n = len(result)

    if n <= 1:
        return result

    # Límites del subarreglo no ordenado
    left = 0
    right = n - 1

    while left < right:
        # Flag para detectar si hubo intercambios
        swapped = False

        # Pasada de izquierda a derecha (burbuja hacia arriba)
        # El elemento más grande "burbujea" hacia el final
        for i in range(left, right):
            if result[i] > result[i + 1]:
                result[i], result[i + 1] = result[i + 1], result[i]
                swapped = True

        if not swapped:
            break  # Arreglo ordenado

        # Reducir el límite derecho (el elemento más grande ya está en su lugar)
        right -= 1

        # Pasada de derecha a izquierda (burbuja hacia abajo)
        # El elemento más pequeño "burbujea" hacia el inicio
        for i in range(right - 1, left - 1, -1):
            if result[i] > result[i + 1]:
                result[i], result[i + 1] = result[i + 1], result[i]
                swapped = True

        if not swapped:
            break  # Arreglo ordenado

        # Reducir el límite izquierdo (el elemento más pequeño ya está en su lugar)
        left += 1

    return result


def shaker_sort_in_place(arr: List[int]) -> None:
    """
    Versión in-place del Shaker Sort (modifica el arreglo original).

    Args:
        arr: Lista de enteros a ordenar (modificada in-place)
    """
    n = len(arr)

    if n <= 1:
        return

    left = 0
    right = n - 1

    while left < right:
        swapped = False

        # Izquierda a derecha
        for i in range(left, right):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True

        if not swapped:
            break

        right -= 1

        # Derecha a izquierda
        for i in range(right - 1, left - 1, -1):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True

        if not swapped:
            break

        left += 1