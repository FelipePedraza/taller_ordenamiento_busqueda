"""
Búsqueda por Saltos (Jump Search) - Implementación en Python.

Algoritmo de búsqueda para arreglos ordenados que salta
bloques de tamaño √n y luego hace búsqueda lineal.

Complejidad:
- Peor caso: O(√n)
- Mejor caso: O(1) - elemento en el primer salto
- Caso promedio: O(√n)
- Espacio: O(1)

Requisito: El arreglo debe estar ordenado.

Principio:
1. Saltar bloques de tamaño √n hasta encontrar un bloque
   que podría contener el elemento
2. Hacer búsqueda lineal en ese bloque

Ventaja: Menor cantidad de comparaciones que búsqueda lineal,
más simple que búsqueda binaria.
"""

import math
from typing import List, Optional


def jump_search(arr: List[int], target: int) -> Optional[int]:
    """
    Realiza búsqueda por saltos en un arreglo ordenado.

    Args:
        arr: Lista ordenada de enteros
        target: Valor a buscar

    Returns:
        Índice del elemento si se encuentra, None en caso contrario
    """
    if not arr:
        return None

    n = len(arr)

    # Casos especiales
    if n == 0:
        return None

    if arr[0] == target:
        return 0

    if arr[-1] == target:
        return n - 1

    # Tamaño óptimo del salto: √n
    step = int(math.sqrt(n))

    # Encontrar el bloque donde podría estar el elemento
    prev = 0
    current = step

    # Saltar bloques mientras el elemento del final del bloque
    # sea menor que el target
    while current < n and arr[current] <= target:
        if arr[current] == target:
            return current
        prev = current
        current += step
        if current >= n:
            current = n - 1
            break

    # Si nos pasamos, ajustar el límite superior
    if current >= n:
        current = n - 1

    # Búsqueda lineal en el bloque identificado
    # El bloque es [prev+1, current]
    for i in range(prev + 1, min(current + 1, n)):
        if arr[i] == target:
            return i
        if arr[i] > target:
            # Como el arreglo está ordenado, si encontramos
            # un valor mayor, el target no está en el arreglo
            break

    return None


def jump_search_optimized(arr: List[int], target: int) -> Optional[int]:
    """
    Versión optimizada de jump search con manejo de casos especiales.

    Args:
        arr: Lista ordenada de enteros
        target: Valor a buscar

    Returns:
        Índice del elemento si se encuentra, None en caso contrario
    """
    if not arr:
        return None

    n = len(arr)

    # Casos especiales
    if n == 0:
        return None

    if arr[0] == target:
        return 0

    if arr[-1] == target:
        return n - 1

    if target < arr[0] or target > arr[-1]:
        return None

    # Tamaño del salto
    step = int(math.sqrt(n))

    # Encontrar el bloque
    prev = 0
    current = step

    while current < n and arr[current] <= target:
        if arr[current] == target:
            return current
        prev = current
        current += step
        if current > n - 1:
            current = n - 1

    # Si el bloque anterior tenía el elemento
    if arr[current] == target:
        return current

    # Búsqueda lineal en el bloque
    for i in range(prev + 1, min(current + 1, n)):
        if arr[i] == target:
            return i
        if arr[i] > target:
            break

    return None


def jump_search_con_pasos(arr: List[int], target: int) -> dict:
    """
    Versión que retorna información detallada del proceso.

    Args:
        arr: Lista ordenada de enteros
        target: Valor a buscar

    Returns:
        Diccionario con resultado y estadísticas
    """
    if not arr:
        return {
            'encontrado': False,
            'indice': None,
            'saltos_realizados': 0,
            'comparaciones': 0,
            'bloque_inicio': None,
            'bloque_fin': None
        }

    n = len(arr)
    step = int(math.sqrt(n))
    saltos = 0
    comparaciones = 0

    prev = 0
    current = 0

    # Fase de saltos
    while current < n:
        saltos += 1
        comparaciones += 1

        idx = min(current, n - 1)
        if arr[idx] >= target:
            break

        prev = current
        current += step

    bloque_inicio = prev
    bloque_fin = min(current, n - 1)

    # Fase de búsqueda lineal
    for i in range(prev, min(current + 1, n)):
        comparaciones += 1
        if arr[i] == target:
            return {
                'encontrado': True,
                'indice': i,
                'saltos_realizados': saltos,
                'comparaciones': comparaciones,
                'bloque_inicio': bloque_inicio,
                'bloque_fin': bloque_fin
            }
        if arr[i] > target:
            break

    return {
        'encontrado': False,
        'indice': None,
        'saltos_realizados': saltos,
        'comparaciones': comparaciones,
        'bloque_inicio': bloque_inicio,
        'bloque_fin': bloque_fin
    }


def jump_search_block_size(arr: List[int], target: int, block_size: int) -> Optional[int]:
    """
    Versión con tamaño de bloque personalizable.

    Permite especificar un tamaño de bloque diferente al √n.

    Args:
        arr: Lista ordenada de enteros
        target: Valor a buscar
        block_size: Tamaño del salto personalizado

    Returns:
        Índice del elemento si se encuentra, None en caso contrario
    """
    if not arr or block_size <= 0:
        return None

    n = len(arr)
    step = block_size

    prev = 0
    current = 0

    while current < n and arr[min(current, n - 1)] < target:
        prev = current
        current += step

    for i in range(prev, min(current + 1, n)):
        if arr[i] == target:
            return i
        if arr[i] > target:
            break

    return None


def calcular_mejor_block_size(n: int) -> int:
    """
    Calcula el tamaño óptimo de bloque para jump search.

    El tamaño óptimo teórico es √n, pero puede variar según
    las características de los datos.

    Args:
        n: Tamaño del arreglo

    Returns:
        Tamaño óptimo de bloque
    """
    if n <= 0:
        return 0
    return int(math.sqrt(n))