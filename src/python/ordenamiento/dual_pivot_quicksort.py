"""
Dual-Pivot QuickSort - Implementacion en Python.
Fuente: GeeksforGeeks

Algoritmo QuickSort optimizado que utiliza dos pivotes.
Usado en Java 7+ Arrays.sort() para objetos.

Complejidad: O(n log n) promedio, O(n^2) peor caso
"""

from typing import List


def dual_pivot_quicksort(arr: List[int]) -> List[int]:
    """
    Ordena un arreglo usando el algoritmo Dual-Pivot QuickSort.

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

    _dual_pivot_quicksort_recursive(result, 0, len(result) - 1)
    return result


def _dual_pivot_quicksort_recursive(arr: List[int], left: int, right: int) -> None:
    """Funcion recursiva auxiliar."""
    if left < right:
        pivot1, pivot2 = _partition(arr, left, right)

        _dual_pivot_quicksort_recursive(arr, left, pivot1 - 1)
        _dual_pivot_quicksort_recursive(arr, pivot1 + 1, pivot2 - 1)
        _dual_pivot_quicksort_recursive(arr, pivot2 + 1, right)


def _partition(arr: List[int], left: int, right: int) -> tuple:
    """Realiza la particion con dos pivotes."""
    if arr[left] > arr[right]:
        arr[left], arr[right] = arr[right], arr[left]

    pivot1 = arr[left]
    pivot2 = arr[right]

    i = left + 1
    lt = left + 1
    gt = right - 1

    while i <= gt:
        if arr[i] < pivot1:
            arr[i], arr[lt] = arr[lt], arr[i]
            lt += 1
            i += 1
        elif arr[i] > pivot2:
            arr[i], arr[gt] = arr[gt], arr[i]
            gt -= 1
        else:
            i += 1

    lt -= 1
    gt += 1
    arr[left], arr[lt] = arr[lt], arr[left]
    arr[right], arr[gt] = arr[gt], arr[right]

    return lt, gt
