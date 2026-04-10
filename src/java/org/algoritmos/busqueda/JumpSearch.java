package org.algoritmos.busqueda;

/**
 * Busqueda por Saltos (Jump Search)
 *
 * Algoritmo de busqueda para arreglos ordenados que salta bloques
 * de tamano sqrt(n) hasta encontrar el rango del elemento.
 *
 * Fuente: GeeksforGeeks
 *
 * Requiere: Arreglo ORDENADO
 *
 * Complejidad: O(sqrt(n))
 */
public class JumpSearch {

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

        int n = array.length;
        int step = (int) Math.sqrt(n);

        int prev = 0;
        int curr = Math.min(step, n) - 1;

        while (curr < n && array[curr] < target) {
            prev = curr + 1;
            curr = Math.min(curr + step, n) - 1;

            if (prev >= n) {
                return -1;
            }
        }

        curr = Math.min(curr, n - 1);

        for (int i = prev; i <= curr; i++) {
            if (array[i] == target) {
                return i;
            }
            if (array[i] > target) {
                return -1;
            }
        }

        return -1;
    }
}
