package org.algoritmos.ordenamiento;

/**
 * Shaker Sort (Cocktail Sort)
 *
 * Variante del Bubble Sort que ordena en ambas direcciones.
 *
 * Fuente: GeeksforGeeks
 *
 * Complejidad: O(n^2)
 */
public class ShakerSort {

    /**
     * Ordena el arreglo usando Shaker Sort.
     *
     * @param array Arreglo a ordenar (se modifica in-place)
     * @return El mismo arreglo ordenado
     */
    public static int[] sort(int[] array) {
        if (array == null || array.length < 2) {
            return array;
        }

        int left = 0;
        int right = array.length - 1;

        while (left < right) {
            for (int i = left; i < right; i++) {
                if (array[i] > array[i + 1]) {
                    swap(array, i, i + 1);
                }
            }
            right--;

            for (int i = right; i > left; i--) {
                if (array[i] < array[i - 1]) {
                    swap(array, i, i - 1);
                }
            }
            left++;
        }

        return array;
    }

    private static void swap(int[] array, int i, int j) {
        int temp = array[i];
        array[i] = array[j];
        array[j] = temp;
    }
}
