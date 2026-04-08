"""
Dual-Pivot QuickSort - Implementación en Python.

Algoritmo de ordenamiento QuickSort optimizado que utiliza dos pivotes
en lugar de uno solo, similar a la implementación usada en Java 7+.

Complejidad:
- Peor caso: O(n²) - raro con buena elección de pivotes
- Mejor caso: O(n log n)
- Caso promedio: O(n log n)
- Espacio: O(log n) - recursión

Divide el arreglo en 3 particiones:
1. Elementos menores que pivot1
2. Elementos entre pivot1 y pivot2 (inclusive)
3. Elementos mayores que pivot2

Ventaja: Menos comparaciones y swaps que QuickSort tradicional.
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
    """
    Función recursiva auxiliar para Dual-Pivot QuickSort.

    Args:
        arr: Lista a ordenar (modificada in-place)
        left: Índice izquierdo del subarreglo
        right: Índice derecho del subarreglo
    """
    if left < right:
        # Casos base para pequeños subarreglos (optimización)
        if right - left <= 17:
            _insertion_sort(arr, left, right)
            return

        # Partición con dos pivotes
        pivot1, pivot2 = _partition(arr, left, right)

        # Recursión en las tres particiones
        _dual_pivot_quicksort_recursive(arr, left, pivot1 - 1)
        _dual_pivot_quicksort_recursive(arr, pivot1 + 1, pivot2 - 1)
        _dual_pivot_quicksort_recursive(arr, pivot2 + 1, right)


def _partition(arr: List[int], left: int, right: int) -> tuple:
    """
    Realiza la partición con dos pivotes.

    Selecciona dos pivotes y organiza el arreglo en tres particiones:
    - [left...pivot1]: elementos < pivot1
    - [pivot1...pivot2]: elementos entre pivot1 y pivot2
    - [pivot2...right]: elementos > pivot2

    Args:
        arr: Lista a particionar
        left: Índice izquierdo
        right: Índice derecho

    Returns:
        Tupla con las posiciones finales de los dos pivotes
    """
    # Asegurar que arr[left] <= arr[right]
    if arr[left] > arr[right]:
        arr[left], arr[right] = arr[right], arr[left]

    # Pivotes
    pivot1 = arr[left]   # Pivote izquierdo (menor)
    pivot2 = arr[right]  # Pivote derecho (mayor)

    # Pointers para las particiones
    # [left] es pivot1, [right] es pivot2
    # i recorre los elementos no procesados
    # lt marca el fin de la partición < pivot1
    # gt marca el inicio de la partición > pivot2
    i = left + 1
    lt = left + 1   # Menores que pivot1
    gt = right - 1  # Mayores que pivot2

    while i <= gt:
        if arr[i] < pivot1:
            # Elemento menor que pivot1: intercambiar con lt
            arr[i], arr[lt] = arr[lt], arr[i]
            lt += 1
            i += 1
        elif arr[i] > pivot2:
            # Elemento mayor que pivot2: intercambiar con gt
            arr[i], arr[gt] = arr[gt], arr[i]
            gt -= 1
            # No incrementar i porque el elemento intercambiado
            # desde gt aún no ha sido procesado
        else:
            # Elemento entre pivot1 y pivot2: dejar en la partición del medio
            i += 1

    # Colocar los pivotes en sus posiciones finales
    lt -= 1
    gt += 1
    arr[left], arr[lt] = arr[lt], arr[left]
    arr[right], arr[gt] = arr[gt], arr[right]

    return lt, gt


def _insertion_sort(arr: List[int], left: int, right: int) -> None:
    """
    Insertion Sort para subarreglos pequeños (optimización).

    Args:
        arr: Lista a ordenar
        left: Índice izquierdo
        right: Índice derecho
    """
    for i in range(left + 1, right + 1):
        key = arr[i]
        j = i - 1
        while j >= left and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key