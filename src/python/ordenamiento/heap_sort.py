"""
Heap Sort - Implementacion en Python.
Fuente: GeeksforGeeks

Algoritmo de ordenamiento basado en la estructura de datos Heap (monticulo).

Complejidad: O(n log n) garantizado
Espacio: O(1) - ordenamiento in-place
"""

from typing import List


def heap_sort(arr: List[int]) -> List[int]:
    """
    Ordena un arreglo usando el algoritmo Heap Sort.

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

    # Construir Max-Heap
    for i in range(n // 2 - 1, -1, -1):
        _heapify(result, n, i)

    # Extraer elementos del heap uno por uno
    for i in range(n - 1, 0, -1):
        result[0], result[i] = result[i], result[0]
        _heapify(result, i, 0)

    return result


def _heapify(arr: List[int], heap_size: int, root_idx: int) -> None:
    """Mantiene la propiedad del Max-Heap."""
    largest = root_idx
    left_child = 2 * root_idx + 1
    right_child = 2 * root_idx + 2

    if left_child < heap_size and arr[left_child] > arr[largest]:
        largest = left_child

    if right_child < heap_size and arr[right_child] > arr[largest]:
        largest = right_child

    if largest != root_idx:
        arr[root_idx], arr[largest] = arr[largest], arr[root_idx]
        _heapify(arr, heap_size, largest)
