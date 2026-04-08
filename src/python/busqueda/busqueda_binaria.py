"""
Búsqueda Binaria (Binary Search) - Implementación en Python.

Algoritmo de búsqueda eficiente para arreglos ordenados.
Divide repetidamente el espacio de búsqueda a la mitad.

Complejidad:
- Peor caso: O(log n)
- Mejor caso: O(1) - elemento en el centro
- Caso promedio: O(log n)
- Espacio: O(1) - iterativo, O(log n) - recursivo

Requisito: El arreglo debe estar ordenado.

Principio: Comparar con el elemento del medio,
si es menor, buscar en la mitad izquierda,
si es mayor, buscar en la mitad derecha.
"""

from typing import List, Optional


def busqueda_binaria(arr: List[int], target: int) -> Optional[int]:
    """
    Realiza búsqueda binaria en un arreglo ordenado.

    Args:
        arr: Lista ordenada de enteros
        target: Valor a buscar

    Returns:
        Índice del elemento si se encuentra, None en caso contrario
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


def busqueda_binaria_recursiva(arr: List[int], target: int) -> Optional[int]:
    """
    Versión recursiva de búsqueda binaria.

    Args:
        arr: Lista ordenada de enteros
        target: Valor a buscar

    Returns:
        Índice del elemento si se encuentra, None en caso contrario
    """
    return _busqueda_binaria_recursiva_helper(arr, target, 0, len(arr) - 1)


def _busqueda_binaria_recursiva_helper(
    arr: List[int], target: int, left: int, right: int
) -> Optional[int]:
    """
    Función auxiliar recursiva.

    Args:
        arr: Lista ordenada
        target: Valor a buscar
        left: Índice izquierdo del rango
        right: Índice derecho del rango

    Returns:
        Índice del elemento si se encuentra, None en caso contrario
    """
    if left > right:
        return None

    mid = left + (right - left) // 2

    if arr[mid] == target:
        return mid

    if arr[mid] > target:
        return _busqueda_binaria_recursiva_helper(arr, target, left, mid - 1)
    else:
        return _busqueda_binaria_recursiva_helper(arr, target, mid + 1, right)


def busqueda_binaria_lower_bound(arr: List[int], target: int) -> int:
    """
    Encuentra el índice del primer elemento >= target.

    Útil para encontrar el punto de inserción o el
    primer elemento que cumple una condición.

    Args:
        arr: Lista ordenada
        target: Valor de referencia

    Returns:
        Índice del lower bound (puede ser len(arr) si todos son menores)
    """
    left = 0
    right = len(arr)

    while left < right:
        mid = left + (right - left) // 2
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid

    return left


def busqueda_binaria_upper_bound(arr: List[int], target: int) -> int:
    """
    Encuentra el índice del primer elemento > target.

    Args:
        arr: Lista ordenada
        target: Valor de referencia

    Returns:
        Índice del upper bound
    """
    left = 0
    right = len(arr)

    while left < right:
        mid = left + (right - left) // 2
        if arr[mid] <= target:
            left = mid + 1
        else:
            right = mid

    return left


def busqueda_binaria_con_comparaciones(arr: List[int], target: int) -> tuple:
    """
    Versión que cuenta el número de comparaciones realizadas.

    Args:
        arr: Lista ordenada de enteros
        target: Valor a buscar

    Returns:
        Tupla (índice, número_de_comparaciones)
    """
    if not arr:
        return None, 0

    left = 0
    right = len(arr) - 1
    comparaciones = 0

    while left <= right:
        mid = left + (right - left) // 2
        comparaciones += 1

        if arr[mid] == target:
            return mid, comparaciones

        comparaciones += 1
        if arr[mid] > target:
            right = mid - 1
        else:
            left = mid + 1

    return None, comparaciones