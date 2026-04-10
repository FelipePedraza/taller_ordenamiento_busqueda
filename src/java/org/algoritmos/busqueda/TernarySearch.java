package org.algoritmos.busqueda;

/**
 * Busqueda Ternaria (Ternary Search)
 *
 * Variante de la busqueda binaria que divide el espacio de busqueda
 * en tres partes iguales usando dos puntos medios.
 *
 * Fuente: GeeksforGeeks
 *
 * Requiere: Arreglo ORDENADO
 *
 * Complejidad:
 * - Peor caso: O(log3 n)
 * - Mejor caso: O(1)
 * - Caso promedio: O(log3 n)
 */
public class TernarySearch {

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
            int third = (right - left) / 3;
            int mid1 = left + third;
            int mid2 = right - third;

            if (array[mid1] == target) {
                return mid1;
            }

            if (array[mid2] == target) {
                return mid2;
            }

            if (target < array[mid1]) {
                right = mid1 - 1;
            } else if (target > array[mid2]) {
                left = mid2 + 1;
            } else {
                left = mid1 + 1;
                right = mid2 - 1;
            }
        }

        return -1;
    }
}
