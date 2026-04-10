package org.algoritmos.ordenamiento;

/**
 * Merge Sort
 *
 * Algoritmo de ordenamiento por division y conquista.
 *
 * Fuente: GeeksforGeeks
 *
 * Complejidad: O(n log n)
 */
public class MergeSort {

    /**
     * Ordena el arreglo usando Merge Sort.
     *
     * @param array Arreglo a ordenar (se modifica in-place)
     * @return El mismo arreglo ordenado
     */
    public static int[] sort(int[] array) {
        if (array == null || array.length < 2) {
            return array;
        }

        int[] temp = new int[array.length];
        sort(array, temp, 0, array.length - 1);
        return array;
    }

    private static void sort(int[] array, int[] temp, int left, int right) {
        if (left < right) {
            int mid = left + (right - left) / 2;

            sort(array, temp, left, mid);
            sort(array, temp, mid + 1, right);
            merge(array, temp, left, mid, right);
        }
    }

    private static void merge(int[] array, int[] temp, int left, int mid, int right) {
        for (int i = left; i <= right; i++) {
            temp[i] = array[i];
        }

        int i = left;
        int j = mid + 1;
        int k = left;

        while (i <= mid && j <= right) {
            if (temp[i] <= temp[j]) {
                array[k++] = temp[i++];
            } else {
                array[k++] = temp[j++];
            }
        }

        while (i <= mid) {
            array[k++] = temp[i++];
        }

        while (j <= right) {
            array[k++] = temp[j++];
        }
    }
}
