package org.algoritmos.ordenamiento;

/**
 * Heap Sort
 *
 * Algoritmo de ordenamiento basado en la estructura de datos Heap.
 *
 * Fuente: GeeksforGeeks
 *
 * Complejidad: O(n log n)
 */
public class HeapSort {

    /**
     * Ordena el arreglo usando Heap Sort.
     *
     * @param array Arreglo a ordenar (se modifica in-place)
     * @return El mismo arreglo ordenado
     */
    public static int[] sort(int[] array) {
        if (array == null || array.length < 2) {
            return array;
        }

        int n = array.length;

        for (int i = n / 2 - 1; i >= 0; i--) {
            heapify(array, n, i);
        }

        for (int i = n - 1; i > 0; i--) {
            swap(array, 0, i);
            heapify(array, i, 0);
        }

        return array;
    }

    private static void heapify(int[] array, int heapSize, int index) {
        int largest = index;
        int left = 2 * index + 1;
        int right = 2 * index + 2;

        if (left < heapSize && array[left] > array[largest]) {
            largest = left;
        }
        if (right < heapSize && array[right] > array[largest]) {
            largest = right;
        }

        if (largest != index) {
            swap(array, index, largest);
            heapify(array, heapSize, largest);
        }
    }

    private static void swap(int[] array, int i, int j) {
        int temp = array[i];
        array[i] = array[j];
        array[j] = temp;
    }
}
