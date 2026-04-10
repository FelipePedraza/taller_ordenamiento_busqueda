package org.algoritmos.ordenamiento;

/**
 * Radix Sort (Base 10)
 *
 * Algoritmo de ordenamiento no comparativo que ordena digito por digito.
 *
 * Fuente: GeeksforGeeks
 *
 * Complejidad: O(d * (n + k))
 */
public class RadixSort {

    private static final int BASE = 10;

    /**
     * Ordena el arreglo usando Radix Sort.
     *
     * @param array Arreglo de enteros positivos a ordenar
     * @return El mismo arreglo ordenado
     */
    public static int[] sort(int[] array) {
        if (array == null || array.length < 2) {
            return array;
        }

        int max = findMax(array);

        for (int exp = 1; max / exp > 0; exp *= BASE) {
            countingSortByDigit(array, exp);
        }

        return array;
    }

    private static int findMax(int[] array) {
        int max = array[0];
        for (int value : array) {
            if (value > max) {
                max = value;
            }
        }
        return max;
    }

    private static void countingSortByDigit(int[] array, int exp) {
        int n = array.length;
        int[] output = new int[n];
        int[] count = new int[BASE];

        for (int value : array) {
            int digit = (value / exp) % BASE;
            count[digit]++;
        }

        for (int i = 1; i < BASE; i++) {
            count[i] += count[i - 1];
        }

        for (int i = n - 1; i >= 0; i--) {
            int digit = (array[i] / exp) % BASE;
            output[count[digit] - 1] = array[i];
            count[digit]--;
        }

        System.arraycopy(output, 0, array, 0, n);
    }
}
