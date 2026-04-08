package org.algoritmos.ordenamiento;

/**
 * Merge Sort
 *
 * Algoritmo de ordenamiento por división y conquista (divide and conquer).
 * Divide el arreglo en mitades, ordena recursivamente cada mitad,
 * y luego mezcla (merge) las mitades ordenadas.
 *
 * Complejidad:
 * - Peor caso: O(n log n) - garantizado
 * - Mejor caso: O(n log n)
 * - Caso promedio: O(n log n)
 * - Espacio auxiliar: O(n) - requiere arreglo temporal
 *
 * Ventajas:
 * - Complejidad O(n log n) garantizada
 * - Estable (mantiene orden relativo de elementos iguales)
 * - Excelente para listas enlazadas y ordenamiento externo
 *
 * Desventajas:
 * - Requiere O(n) espacio extra
 * - Más lento en la práctica que QuickSort para arreglos pequeños
 * - Menos cache-friendly por el arreglo auxiliar
 */
public class MergeSort {

    /**
     * Umbral para usar Insertion Sort en subarreglos pequeños
     */
    private static final int INSERTION_SORT_THRESHOLD = 20;

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
        // Optimización: usar Insertion Sort para subarreglos pequeños
        if (right - left < INSERTION_SORT_THRESHOLD) {
            insertionSort(array, left, right);
            return;
        }

        if (left < right) {
            int mid = left + (right - left) / 2;

            // Ordenar recursivamente las dos mitades
            sort(array, temp, left, mid);
            sort(array, temp, mid + 1, right);

            // Mezclar las mitades ordenadas
            merge(array, temp, left, mid, right);
        }
    }

    /**
     * Mezcla dos subarreglos ordenados:
     * - array[left..mid]
     * - array[mid+1..right]
     */
    private static void merge(int[] array, int[] temp, int left, int mid, int right) {
        // Copiar datos al arreglo temporal
        for (int i = left; i <= right; i++) {
            temp[i] = array[i];
        }

        int i = left;      // Índice para la primera mitad
        int j = mid + 1;   // Índice para la segunda mitad
        int k = left;      // Índice para el arreglo resultante

        // Mezclar mientras haya elementos en ambas mitades
        while (i <= mid && j <= right) {
            if (temp[i] <= temp[j]) {
                array[k++] = temp[i++];
            } else {
                array[k++] = temp[j++];
            }
        }

        // Copiar elementos restantes de la primera mitad (si hay)
        while (i <= mid) {
            array[k++] = temp[i++];
        }

        // Copiar elementos restantes de la segunda mitad (si hay)
        // Nota: los elementos restantes de la segunda mitad ya están en su lugar
        while (j <= right) {
            array[k++] = temp[j++];
        }
    }

    /**
     * Insertion Sort para subarreglos pequeños.
     */
    private static void insertionSort(int[] array, int left, int right) {
        for (int i = left + 1; i <= right; i++) {
            int key = array[i];
            int j = i - 1;
            while (j >= left && array[j] > key) {
                array[j + 1] = array[j];
                j--;
            }
            array[j + 1] = key;
        }
    }
}
