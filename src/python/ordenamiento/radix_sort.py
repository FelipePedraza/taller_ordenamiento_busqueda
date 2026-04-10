"""
Radix Sort - Implementacion en Python (base 10).
Fuente: GeeksforGeeks

Algoritmo de ordenamiento no comparativo que ordena enteros
procesando digito por digito.

Complejidad: O(d * (n + k)) donde d = digitos, n = elementos, k = base
"""

from typing import List


def radix_sort(arr: List[int]) -> List[int]:
    """
    Ordena un arreglo de enteros no negativos usando Radix Sort.

    Args:
        arr: Lista de enteros no negativos a ordenar

    Returns:
        Nueva lista ordenada en orden ascendente

    Raises:
        ValueError: Si hay numeros negativos en el arreglo
    """
    if not arr:
        return []

    result = arr.copy()
    n = len(result)

    if n <= 1:
        return result

    # Verificar que no haya numeros negativos
    if any(x < 0 for x in result):
        raise ValueError("Radix Sort no soporta numeros negativos.")

    max_num = max(result)

    if max_num == 0:
        return result

    exp = 1
    while max_num // exp > 0:
        _counting_sort_by_digit(result, exp)
        exp *= 10

    return result


def _counting_sort_by_digit(arr: List[int], exp: int) -> None:
    """Counting Sort para ordenar por un digito especifico."""
    n = len(arr)
    output = [0] * n
    count = [0] * 10

    for i in range(n):
        digit = (arr[i] // exp) % 10
        count[digit] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    for i in range(n - 1, -1, -1):
        digit = (arr[i] // exp) % 10
        output[count[digit] - 1] = arr[i]
        count[digit] -= 1

    for i in range(n):
        arr[i] = output[i]
