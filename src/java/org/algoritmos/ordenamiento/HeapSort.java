package org.algoritmos.ordenamiento;

/**
 * Heap Sort
 *
 * Algoritmo de ordenamiento por comparación basado en la estructura
 * de datos "Heap" (montículo binario).
 *
 * Funcionamiento:
 * 1. Construir un max-heap a partir del arreglo
 * 2. Extraer el máximo (raíz) y colocarlo al final
 * 3. Reconstruir el heap con los elementos restantes
 * 4. Repetir hasta ordenar todo el arreglo
 *
 * Complejidad:
 * - Peor caso: O(n log n) - garantizado
 * - Mejor caso: O(n log n)
 * - Caso promedio: O(n log n)
 * - Espacio auxiliar: O(1) - in-place
 *
 * Ventajas:
 * - Complejidad O(n log n) garantizada (sin casos patológicos)
 * - In-place (solo requiere O(1) espacio extra)
 * - No recursivo (evita stack overflow)
 *
 * Desventajas:
 * - No estable (puede cambiar orden de elementos iguales)
 * - Acceso a memoria no secuencial (pobre cache locality)
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

        // Construir max-heap (bottom-up)
        // Empezar desde el último padre (n/2 - 1) hasta la raíz
        for (int i = n / 2 - 1; i >= 0; i--) {
            heapify(array, n, i);
        }

        // Extraer elementos del heap uno por uno
        for (int i = n - 1; i > 0; i--) {
            // Mover la raíz (máximo) al final
            swap(array, 0, i);

            // Reconstruir el heap con los elementos restantes
            heapify(array, i, 0);
        }

        return array;
    }

    /**
     * Mantiene la propiedad de max-heap para el subárbol con raíz en index.
     * Asume que los subárboles izquierdo y derecho ya son heaps.
     *
     * @param array El arreglo
     * @param heapSize Tamaño actual del heap
     * @param index Índice de la raíz del subárbol a heapificar
     */
    private static void heapify(int[] array, int heapSize, int index) {
        int largest = index;
        int left = 2 * index + 1;
        int right = 2 * index + 2;

        // Encontrar el mayor entre raíz, izquierdo y derecho
        if (left < heapSize && array[left] > array[largest]) {
            largest = left;
        }
        if (right < heapSize && array[right] > array[largest]) {
            largest = right;
        }

        // Si el mayor no es la raíz, intercambiar y continuar heapificando
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
