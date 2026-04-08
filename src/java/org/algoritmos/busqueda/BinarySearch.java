package org.algoritmos.busqueda;

/**
 * Búsqueda Binaria (Binary Search)
 *
 * Algoritmo de búsqueda en arreglos ordenados.
 * Divide repetidamente el espacio de búsqueda a la mitad.
 *
 * Requiere: Arreglo ORDENADO
 *
 * Complejidad:
 * - Peor caso: O(log n)
 * - Mejor caso: O(1) - elemento en el medio
 * - Caso promedio: O(log n)
 * - Espacio auxiliar: O(1) iterativo, O(log n) recursivo
 *
 * Ventajas:
 * - Muy eficiente O(log n) para arreglos ordenados
 * - Simple de implementar
 * - Excelente para grandes datasets
 *
 * Desventajas:
 * - Requiere arreglo ordenado
 * - Solo funciona con estructuras de acceso aleatorio
 */
public class BinarySearch {

    /**
     * Busca un elemento en un arreglo ordenado.
     *
     * @param array Arreglo ORDENADO donde buscar
     * @param target Elemento a buscar
     * @return Índice del elemento encontrado, o -1 si no existe
     */
    public static int search(int[] array, int target) {
        if (array == null || array.length == 0) {
            return -1;
        }

        int left = 0;
        int right = array.length - 1;

        while (left <= right) {
            int mid = left + (right - left) / 2;

            if (array[mid] == target) {
                return mid;
            }

            if (array[mid] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }

        return -1;
    }

    /**
     * Busca el elemento más cercano menor o igual al target.
     * Útil para encontrar el "floor" de un valor.
     *
     * @param array Arreglo ORDENADO
     * @param target Valor de referencia
     * @return Índice del floor, o -1 si no existe
     */
    public static int findFloor(int[] array, int target) {
        if (array == null || array.length == 0) {
            return -1;
        }

        int left = 0;
        int right = array.length - 1;
        int result = -1;

        while (left <= right) {
            int mid = left + (right - left) / 2;

            if (array[mid] <= target) {
                result = mid;
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }

        return result;
    }

    /**
     * Busca el elemento más cercano mayor o igual al target.
     * Útil para encontrar el "ceiling" de un valor.
     *
     * @param array Arreglo ORDENADO
     * @param target Valor de referencia
     * @return Índice del ceiling, o -1 si no existe
     */
    public static int findCeiling(int[] array, int target) {
        if (array == null || array.length == 0) {
            return -1;
        }

        int left = 0;
        int right = array.length - 1;
        int result = -1;

        while (left <= right) {
            int mid = left + (right - left) / 2;

            if (array[mid] >= target) {
                result = mid;
                right = mid - 1;
            } else {
                left = mid + 1;
            }
        }

        return result;
    }
}
