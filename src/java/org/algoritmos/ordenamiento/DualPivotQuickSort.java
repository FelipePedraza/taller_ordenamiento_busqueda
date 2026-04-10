package org.algoritmos.ordenamiento;

/**
 * Dual-Pivot QuickSort
 *
 * Variante de QuickSort que usa dos pivotes para dividir en tres partes.
 *
 * Fuente: GeeksforGeeks
 *
 * Complejidad: O(n log n) promedio
 */
public class DualPivotQuickSort {

    /**
     * Ordena el arreglo usando Dual-Pivot QuickSort.
     *
     * @param array Arreglo a ordenar (se modifica in-place)
     * @return El mismo arreglo ordenado
     */
    public static int[] sort(int[] array) {
        if (array == null || array.length < 2) {
            return array;
        }

        sort(array, 0, array.length - 1);
        return array;
    }

    private static void sort(int[] array, int left, int right) {
        if (left < right) {
            if (array[left] > array[right]) {
                swap(array, left, right);
            }

            int pivot1 = array[left];
            int pivot2 = array[right];

            int i = left + 1;
            int k = right - 1;
            int j = i;

            while (j <= k) {
                if (array[j] < pivot1) {
                    swap(array, j, i);
                    i++;
                } else if (array[j] >= pivot2) {
                    while (array[k] > pivot2 && j < k) {
                        k--;
                    }
                    swap(array, j, k);
                    k--;
                    if (array[j] < pivot1) {
                        swap(array, j, i);
                        i++;
                    }
                }
                j++;
            }

            i--;
            k++;
            swap(array, left, i);
            swap(array, right, k);

            sort(array, left, i - 1);
            sort(array, i + 1, k - 1);
            sort(array, k + 1, right);
        }
    }

    private static void swap(int[] array, int i, int j) {
        int temp = array[i];
        array[i] = array[j];
        array[j] = temp;
    }
}
