package org.algoritmos.ordenamiento;

/**
 * Shaker Sort (Cocktail Sort / Cocktail Shaker Sort)
 *
 * Variante del Bubble Sort que ordena en ambas direcciones alternadamente.
 * En cada pasada, las burbujas más "ligeras" suben y las más "pesadas" bajan.
 *
 * Complejidad:
 * - Peor caso: O(n²)
 * - Mejor caso: O(n) - cuando el arreglo ya está ordenado
 * - Caso promedio: O(n²)
 *
 * Ventajas:
 * - Mejor que Bubble Sort para datos casi ordenados
 * - Reduce el "tortuga" problem de Bubble Sort (elementos pequeños al final)
 *
 * Desventajas:
 * - O(n²) en general, no es eficiente para grandes datasets
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
        int lastSwap;

        while (left < right) {
            // Pasada de izquierda a derecha (burbujas suben)
            lastSwap = left;
            for (int i = left; i < right; i++) {
                if (array[i] > array[i + 1]) {
                    swap(array, i, i + 1);
                    lastSwap = i;
                }
            }
            right = lastSwap;

            // Si no hubo intercambios, ya está ordenado
            if (left == right) {
                break;
            }

            // Pasada de derecha a izquierda (burbujas bajan)
            lastSwap = right;
            for (int i = right; i > left; i--) {
                if (array[i] < array[i - 1]) {
                    swap(array, i, i - 1);
                    lastSwap = i;
                }
            }
            left = lastSwap;
        }

        return array;
    }

    private static void swap(int[] array, int i, int j) {
        int temp = array[i];
        array[i] = array[j];
        array[j] = temp;
    }
}
