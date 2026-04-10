"""
Merge Sort - Implementacion en Python.
Fuente: GeeksforGeeks

Algoritmo de ordenamiento basado en Divide y Venceras.

Complejidad: O(n log n) garantizado
Espacio: O(n)
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
    """Funcion recursiva auxiliar."""
    if left < right:
        mid = left + (right - left) // 2

        _merge_sort_recursive(arr, left, mid)
        _merge_sort_recursive(arr, mid + 1, right)
        _merge(arr, left, mid, right)


def _merge(arr: List[int], left: int, mid: int, right: int) -> None:
    """Fusiona dos subarreglos ordenados."""
    n1 = mid - left + 1
    n2 = right - mid

    left_arr = [0] * n1
    right_arr = [0] * n2

    for i in range(n1):
        left_arr[i] = arr[left + i]

    for j in range(n2):
        right_arr[j] = arr[mid + 1 + j]

    i = j = 0
    k = left

    while i < n1 and j < n2:
        if left_arr[i] <= right_arr[j]:
            arr[k] = left_arr[i]
            i += 1
        else:
            arr[k] = right_arr[j]
            j += 1
        k += 1

    while i < n1:
        arr[k] = left_arr[i]
        i += 1
        k += 1

    while j < n2:
        arr[k] = right_arr[j]
        j += 1
        k += 1
