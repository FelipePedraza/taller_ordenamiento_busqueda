package org.algoritmos.busqueda;

/**
 * Busqueda Binaria (Binary Search)
 *
 * Algoritmo de busqueda en arreglos ordenados.
 * Divide repetidamente el espacio de busqueda a la mitad.
 *
 * Fuente: GeeksforGeeks
 *
 * Requiere: Arreglo ORDENADO
 *
 * Complejidad: O(log n)
 */
public class BinarySearch {

    /**
     * Busca un elemento en un arreglo ordenado.
     *
     * @param array Arreglo ORDENADO donde buscar
     * @param target Elemento a buscar
     * @return Indice del elemento encontrado, o -1 si no existe
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
}
