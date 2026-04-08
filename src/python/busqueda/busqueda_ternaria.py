"""
Búsqueda Ternaria (Ternary Search) - Implementación en Python.

Algoritmo de búsqueda similar a búsqueda binaria pero divide
el espacio de búsqueda en tres partes en lugar de dos.

Complejidad:
- Peor caso: O(log₃ n) ≈ O(log n) con base diferente
- Mejor caso: O(1) - elemento en mid1 o mid2
- Caso promedio: O(log₃ n)
- Espacio: O(1) - iterativo, O(log n) - recursivo

Requisito: El arreglo debe estar ordenado.

Principio: Dividir en tres partes iguales usando dos puntos medios.
Comparar target con ambos puntos medios para determinar
en cuál de las tres secciones continuar la búsqueda.

Nota: En la práctica, búsqueda binaria es generalmente más eficiente
debido a menor cantidad de comparaciones por iteración.
"""

from typing import List, Optional


def busqueda_ternaria(arr: List[int], target: int) -> Optional[int]:
    """
    Realiza búsqueda ternaria en un arreglo ordenado.

    Divide el arreglo en tres partes y determina en cuál
    de ellas puede estar el elemento buscado.

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
        # Calcular los dos puntos medios
        # Dividir el rango en tres partes aproximadamente iguales
        third = (right - left) // 3
        mid1 = left + third
        mid2 = right - third

        # Verificar si el target está en alguno de los puntos medios
        if arr[mid1] == target:
            return mid1

        if arr[mid2] == target:
            return mid2

        # Determinar en cuál de las tres secciones continuar
        if target < arr[mid1]:
            # El target está en la primera tercera parte
            right = mid1 - 1
        elif target > arr[mid2]:
            # El target está en la última tercera parte
            left = mid2 + 1
        else:
            # El target está en la parte del medio
            left = mid1 + 1
            right = mid2 - 1

    return None


def busqueda_ternaria_recursiva(arr: List[int], target: int) -> Optional[int]:
    """
    Versión recursiva de búsqueda ternaria.

    Args:
        arr: Lista ordenada de enteros
        target: Valor a buscar

    Returns:
        Índice del elemento si se encuentra, None en caso contrario
    """
    return _busqueda_ternaria_helper(arr, target, 0, len(arr) - 1)


def _busqueda_ternaria_helper(
    arr: List[int], target: int, left: int, right: int
) -> Optional[int]:
    """
    Función auxiliar recursiva para búsqueda ternaria.

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

    # Calcular puntos medios
    third = (right - left) // 3
    mid1 = left + third
    mid2 = right - third

    # Verificar puntos medios
    if arr[mid1] == target:
        return mid1

    if arr[mid2] == target:
        return mid2

    # Determinar sección y recursión
    if target < arr[mid1]:
        return _busqueda_ternaria_helper(arr, target, left, mid1 - 1)
    elif target > arr[mid2]:
        return _busqueda_ternaria_helper(arr, target, mid2 + 1, right)
    else:
        return _busqueda_ternaria_helper(arr, target, mid1 + 1, mid2 - 1)


def busqueda_ternaria_con_pasos(arr: List[int], target: int) -> dict:
    """
    Versión que retorna información detallada del proceso.

    Args:
        arr: Lista ordenada de enteros
        target: Valor a buscar

    Returns:
        Diccionario con resultado y estadísticas del proceso
    """
    if not arr:
        return {
            'encontrado': False,
            'indice': None,
            'pasos': 0,
            'rangos_visitados': []
        }

    left = 0
    right = len(arr) - 1
    pasos = 0
    rangos_visitados = []

    while left <= right:
        pasos += 1
        rangos_visitados.append((left, right))

        third = (right - left) // 3
        mid1 = left + third
        mid2 = right - third

        if arr[mid1] == target:
            return {
                'encontrado': True,
                'indice': mid1,
                'pasos': pasos,
                'rangos_visitados': rangos_visitados
            }

        if arr[mid2] == target:
            return {
                'encontrado': True,
                'indice': mid2,
                'pasos': pasos,
                'rangos_visitados': rangos_visitados
            }

        if target < arr[mid1]:
            right = mid1 - 1
        elif target > arr[mid2]:
            left = mid2 + 1
        else:
            left = mid1 + 1
            right = mid2 - 1

    return {
        'encontrado': False,
        'indice': None,
        'pasos': pasos,
        'rangos_visitados': rangos_visitados
    }


def busqueda_ternaria_float(
    func, left: float, right: float, epsilon: float = 1e-9
) -> float:
    """
    Búsqueda ternaria para encontrar el máximo de una función unimodal.

    Útil en optimización cuando se busca el punto máximo/mínimo
    de una función continua unimodal.

    Args:
        func: Función unimodal a maximizar
        left: Límite izquierdo
        right: Límite derecho
        epsilon: Precisión deseada

    Returns:
        Valor x donde func(x) es máximo (aproximadamente)
    """
    while abs(right - left) > epsilon:
        m1 = left + (right - left) / 3
        m2 = right - (right - left) / 3

        f1 = func(m1)
        f2 = func(m2)

        if f1 < f2:
            left = m1
        else:
            right = m2

    return (left + right) / 2