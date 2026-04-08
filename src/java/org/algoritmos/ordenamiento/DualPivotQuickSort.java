package org.algoritmos.ordenamiento;

/**
 * Dual-Pivot QuickSort
 *
 * Variante del QuickSort desarrollada por Vladimir Yaroslavskiy,
 * usada por defecto en Arrays.sort() de Java 7+ para tipos primitivos.
 *
 * Usa dos pivotes (p1 < p2) para particionar el arreglo en tres partes:
 * - Elementos menores que p1
 * - Elementos entre p1 y p2
 * - Elementos mayores que p2
 *
 * Complejidad:
 * - Peor caso: O(n log n) - con particionamiento balanceado
 * - Mejor caso: O(n log n)
 * - Caso promedio: O(n log n)
 * - Espacio auxiliar: O(log n) por la recursión
 *
 * Ventajas:
 * - ~10% más rápido que QuickSort tradicional en promedio
 * - Menos comparaciones que el QuickSort de un pivote
 * - Cache-friendly por sus patrones de acceso
 */
public class DualPivotQuickSort {

    /**
     * Umbral para usar Insertion Sort en subarreglos pequeños
     */
    private static final int INSERTION_SORT_THRESHOLD = 27;

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
        // Usar Insertion Sort para subarreglos pequeños
        if (right - left < INSERTION_SORT_THRESHOLD) {
            insertionSort(array, left, right);
            return;
        }

        // Elegir pivotes y asegurar que array[left] <= array[right]
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

        // Colocar pivotes en su posición final
        i--;
        k++;
        swap(array, left, i);
        swap(array, right, k);

        // Recursión en las tres particiones
        sort(array, left, i - 1);
        sort(array, i + 1, k - 1);
        sort(array, k + 1, right);
    }

    /**
     * Insertion Sort para subarreglos pequeños.
     * Más eficiente que QuickSort para n pequeño.
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

    private static void swap(int[] array, int i, int j) {
        int temp = array[i];
        array[i] = array[j];
        array[j] = temp;
    }
}
