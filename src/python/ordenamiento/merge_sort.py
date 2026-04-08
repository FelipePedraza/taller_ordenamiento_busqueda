"""
Merge Sort - Implementación en Python.

Algoritmo de ordenamiento basado en Divide y Vencerás.
Divide el arreglo en mitades, ordena recursivamente y combina.

Complejidad:
- Peor caso: O(n log n) - garantizado
- Mejor caso: O(n log n)
- Caso promedio: O(n log n)
- Espacio: O(n) - requiere arreglo auxiliar

Proceso:
1. Dividir: dividir el arreglo en dos mitades
2. Conquistar: ordenar recursivamente cada mitad
3. Combinar: fusionar las dos mitades ordenadas

Ventaja: Estabilidad (mantiene orden relativo de elementos iguales)
y complejidad garantizada O(n log n).
"""

from typing import List


def merge_sort(arr: List[int]) -> List[int]:
    """
    Ordena un arreglo usando el algoritmo Merge Sort.

    Args:
        arr: Lista de enteros a ordenar

    Returns:
        Nueva lista ordenada en orden ascendente
    """
    if not arr:
        return []

    result = arr.copy()

    if len(result) <= 1:
        return result

    _merge_sort_recursive(result, 0, len(result) - 1)
    return result


def _merge_sort_recursive(arr: List[int], left: int, right: int) -> None:
    """
    Función recursiva auxiliar para Merge Sort.

    Args:
        arr: Lista a ordenar (modificada in-place)
        left: Índice izquierdo del subarreglo
        right: Índice derecho del subarreglo
    """
    if left < right:
        # Encontrar el punto medio (evitar overflow)
        mid = left + (right - left) // 2

        # Ordenar la primera mitad
        _merge_sort_recursive(arr, left, mid)

        # Ordenar la segunda mitad
        _merge_sort_recursive(arr, mid + 1, right)

        # Fusionar las mitades ordenadas
        _merge(arr, left, mid, right)


def _merge(arr: List[int], left: int, mid: int, right: int) -> None:
    """
    Fusiona dos subarreglos ordenados.

    El primer subarreglo es arr[left:mid+1]
    El segundo subarreglo es arr[mid+1:right+1]

    Args:
        arr: Lista que contiene los subarreglos
        left: Índice inicial del primer subarreglo
        mid: Índice final del primer subarreglo
        right: Índice final del segundo subarreglo
    """
    # Tamaños de los subarreglos temporales
    n1 = mid - left + 1
    n2 = right - mid

    # Crear arreglos temporales
    left_arr = [0] * n1
    right_arr = [0] * n2

    # Copiar datos a los arreglos temporales
    for i in range(n1):
        left_arr[i] = arr[left + i]

    for j in range(n2):
        right_arr[j] = arr[mid + 1 + j]

    # Fusionar los arreglos temporales de vuelta a arr
    i = 0  # Índice para left_arr
    j = 0  # Índice para right_arr
    k = left  # Índice para arr

    while i < n1 and j < n2:
        if left_arr[i] <= right_arr[j]:
            arr[k] = left_arr[i]
            i += 1
        else:
            arr[k] = right_arr[j]
            j += 1
        k += 1

    # Copiar elementos restantes de left_arr (si hay)
    while i < n1:
        arr[k] = left_arr[i]
        i += 1
        k += 1

    # Copiar elementos restantes de right_arr (si hay)
    while j < n2:
        arr[k] = right_arr[j]
        j += 1
        k += 1


def merge_sort_bottom_up(arr: List[int]) -> List[int]:
    """
    Versión iterativa (bottom-up) de Merge Sort.

    Evita la recursión dividiendo el arreglo en subarreglos
    de tamaño 1, 2, 4, 8, ... y fusionándolos.

    Args:
        arr: Lista de enteros a ordenar

    Returns:
        Nueva lista ordenada
    """
    if not arr:
        return []

    result = arr.copy()
    n = len(result)

    if n <= 1:
        return result

    # Tamaño actual de los subarreglos (comienza en 1, duplica cada vez)
    current_size = 1

    while current_size < n:
        # Procesar pares de subarreglos del tamaño actual
        for left_start in range(0, n, 2 * current_size):
            mid = min(left_start + current_size - 1, n - 1)
            right_end = min(left_start + 2 * current_size - 1, n - 1)

            if mid < right_end:
                _merge(result, left_start, mid, right_end)

        current_size *= 2

    return result