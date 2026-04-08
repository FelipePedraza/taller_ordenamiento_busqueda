"""
Radix Sort - Implementación en Python (base 10).

Algoritmo de ordenamiento no comparativo que ordena enteros
procesando dígito por dígito, desde el menos significativo
hasta el más significativo (LSD - Least Significant Digit).

Complejidad:
- Peor caso: O(d × (n + k)) donde d = dígitos, n = elementos, k = base
- Mejor caso: O(d × (n + k))
- Caso promedio: O(d × (n + k))
- Espacio: O(n + k)

Para base 10: O(d × n) donde d es el número de dígitos del número máximo.

Ventaja: Complejidad lineal cuando d es constante (números de tamaño fijo).
No hace comparaciones entre elementos.

Requiere: Counting Sort como subrutina para ordenar por cada dígito.
"""

from typing import List


def radix_sort(arr: List[int]) -> List[int]:
    """
    Ordena un arreglo de enteros no negativos usando Radix Sort (base 10).

    Args:
        arr: Lista de enteros no negativos a ordenar

    Returns:
        Nueva lista ordenada en orden ascendente

    Raises:
        ValueError: Si hay números negativos en el arreglo
    """
    if not arr:
        return []

    result = arr.copy()
    n = len(result)

    if n <= 1:
        return result

    # Verificar que no haya números negativos
    if any(x < 0 for x in result):
        raise ValueError("Radix Sort no soporta números negativos. "
                        "Use otro algoritmo o implemente versión con separación.")

    # Encontrar el número máximo para determinar la cantidad de dígitos
    max_num = max(result)

    # Si todos son 0, ya está ordenado
    if max_num == 0:
        return result

    # Aplicar counting sort para cada dígito
    # exp representa la posición del dígito actual (1, 10, 100, ...)
    exp = 1
    while max_num // exp > 0:
        _counting_sort_by_digit(result, exp)
        exp *= 10

    return result


def _counting_sort_by_digit(arr: List[int], exp: int) -> None:
    """
    Counting Sort para ordenar por un dígito específico.

    Ordena el arreglo según el dígito en la posición 'exp'
    (1 = unidades, 10 = decenas, 100 = centenas, ...)

    Args:
        arr: Lista a ordenar (modificada in-place)
        exp: Posición del dígito actual (1, 10, 100, ...)
    """
    n = len(arr)

    # Arreglo de salida
    output = [0] * n

    # Count array para base 10 (dígitos 0-9)
    count = [0] * 10

    # Almacenar el conteo de ocurrencias del dígito actual
    for i in range(n):
        digit = (arr[i] // exp) % 10
        count[digit] += 1

    # Modificar count[i] para que contenga la posición real
    # del dígito en el output array
    for i in range(1, 10):
        count[i] += count[i - 1]

    # Construir el arreglo de salida (recorrer de atrás hacia adelante
    # para mantener estabilidad)
    for i in range(n - 1, -1, -1):
        digit = (arr[i] // exp) % 10
        output[count[digit] - 1] = arr[i]
        count[digit] -= 1

    # Copiar el arreglo de salida al arreglo original
    for i in range(n):
        arr[i] = output[i]


def radix_sort_with_negatives(arr: List[int]) -> List[int]:
    """
    Versión de Radix Sort que soporta números negativos.

    Separa números positivos y negativos, ordena por separado
    y combina al final.

    Args:
        arr: Lista de enteros (puede incluir negativos)

    Returns:
        Nueva lista ordenada
    """
    if not arr:
        return []

    if len(arr) <= 1:
        return arr.copy()

    # Separar negativos y positivos
    negatives = [-x for x in arr if x < 0]  # Convertir a positivos
    positives = [x for x in arr if x >= 0]

    result = []

    # Ordenar negativos (invertidos) y volver a invertir
    if negatives:
        sorted_negatives = radix_sort(negatives)
        # Invertir y cambiar signo
        result.extend([-x for x in reversed(sorted_negatives)])

    # Ordenar positivos
    if positives:
        result.extend(radix_sort(positives))

    return result


def get_max_digits(arr: List[int]) -> int:
    """
    Calcula la cantidad máxima de dígitos en el arreglo.

    Args:
        arr: Lista de enteros

    Returns:
        Número máximo de dígitos
    """
    if not arr:
        return 0
    max_num = max(abs(x) for x in arr)
    if max_num == 0:
        return 1
    digits = 0
    while max_num > 0:
        max_num //= 10
        digits += 1
    return digits