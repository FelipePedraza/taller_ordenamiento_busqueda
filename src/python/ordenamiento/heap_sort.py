"""
Heap Sort - Implementación en Python.

Algoritmo de ordenamiento basado en la estructura de datos Heap (montículo).
Primero construye un Max-Heap y luego extrae el máximo repetidamente.

Complejidad:
- Peor caso: O(n log n) - garantizado
- Mejor caso: O(n log n)
- Caso promedio: O(n log n)
- Espacio: O(1) - ordenamiento in-place

Estructura del Heap:
- Para un nodo en índice i:
  - Hijo izquierdo: 2i + 1
  - Hijo derecho: 2i + 2
  - Padre: (i - 1) // 2

Ventaja: Complejidad garantizada O(n log n) sin casos patológicos.
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

    # Crear copia para no modificar el original
    result = arr.copy()
    n = len(result)

    if n <= 1:
        return result

    # Fase 1: Construir Max-Heap (heapify)
    # Comenzar desde el último nodo no hoja (índice n//2 - 1)
    # y aplicar heapify hacia arriba
    for i in range(n // 2 - 1, -1, -1):
        _heapify(result, n, i)

    # Fase 2: Extraer elementos del heap uno por uno
    for i in range(n - 1, 0, -1):
        # Mover la raíz actual (máximo) al final del arreglo
        result[0], result[i] = result[i], result[0]

        # Aplicar heapify en el heap reducido (sin el último elemento)
        _heapify(result, i, 0)

    return result


def _heapify(arr: List[int], heap_size: int, root_idx: int) -> None:
    """
    Mantiene la propiedad del Max-Heap (heapify).

    Asegura que el subárbol con raíz en root_idx satisfaga
    la propiedad del heap: padre >= hijos.

    Args:
        arr: Lista que representa el heap
        heap_size: Tamaño actual del heap
        root_idx: Índice de la raíz del subárbol a heapificar
    """
    largest = root_idx
    left_child = 2 * root_idx + 1
    right_child = 2 * root_idx + 2

    # Comparar con hijo izquierdo
    if left_child < heap_size and arr[left_child] > arr[largest]:
        largest = left_child

    # Comparar con hijo derecho
    if right_child < heap_size and arr[right_child] > arr[largest]:
        largest = right_child

    # Si el máximo no es la raíz, intercambiar y continuar heapificando
    if largest != root_idx:
        arr[root_idx], arr[largest] = arr[largest], arr[root_idx]
        # Recursivamente heapificar el subárbol afectado
        _heapify(arr, heap_size, largest)


def heap_sort_in_place(arr: List[int]) -> None:
    """
    Versión in-place del Heap Sort (modifica el arreglo original).

    Args:
        arr: Lista de enteros a ordenar (modificada in-place)
    """
    n = len(arr)

    if n <= 1:
        return

    # Construir Max-Heap
    for i in range(n // 2 - 1, -1, -1):
        _heapify_in_place(arr, n, i)

    # Extraer elementos
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        _heapify_in_place(arr, i, 0)


def _heapify_in_place(arr: List[int], heap_size: int, root_idx: int) -> None:
    """
    Heapify iterativo (evita recursión profunda).

    Args:
        arr: Lista que representa el heap
        heap_size: Tamaño actual del heap
        root_idx: Índice de la raíz del subárbol
    """
    while True:
        largest = root_idx
        left_child = 2 * root_idx + 1
        right_child = 2 * root_idx + 2

        if left_child < heap_size and arr[left_child] > arr[largest]:
            largest = left_child

        if right_child < heap_size and arr[right_child] > arr[largest]:
            largest = right_child

        if largest == root_idx:
            break

        arr[root_idx], arr[largest] = arr[largest], arr[root_idx]
        root_idx = largest