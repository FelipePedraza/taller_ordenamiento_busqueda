package org.algoritmos.busqueda;

/**
 * Búsqueda Ternaria (Ternary Search)
 *
 * Variante de la búsqueda binaria que divide el espacio de búsqueda
 * en tres partes iguales usando dos puntos medios.
 *
 * Requiere: Arreglo ORDENADO
 *
 * Complejidad:
 * - Peor caso: O(log₃ n) ≈ 1.58 * log₂(n)
 * - Mejor caso: O(1)
 * - Caso promedio: O(log₃ n)
 * - Espacio auxiliar: O(1)
 *
 * Ventajas:
 * - Puede ser más rápida en algunos casos al reducir más el espacio
 * - Útil cuando comparar es más costoso que calcular índices
 *
 * Desventajas:
 * - En la práctica, suele ser más lenta que búsqueda binaria
 *   (más comparaciones por iteración: 2 vs 1)
 * - Requiere arreglo ordenado
 */
public class TernarySearch {

    /**
     * Busca un elemento en un arreglo ordenado.
     *
     * @param array Arreglo ORDENADO donde buscar
     * @param target Elemento a buscar
     * @return Índice del elemento encontrado, o -1 si no existe
     */
    public static int search(int[] array, int target) {
        if (array == null || array.length == 0) {
            return -1;
        }

        int left = 0;
        int right = array.length - 1;

        while (left <= right) {
            // Dividir en 3 partes
            int third = (right - left) / 3;
            int mid1 = left + third;
            int mid2 = right - third;

            if (array[mid1] == target) {
                return mid1;
            }

            if (array[mid2] == target) {
                return mid2;
            }

            // Determinar en qué tercio continuar
            if (target < array[mid1]) {
                right = mid1 - 1;
            } else if (target > array[mid2]) {
                left = mid2 + 1;
            } else {
                left = mid1 + 1;
                right = mid2 - 1;
            }
        }

        return -1;
    }

    /**
     * Versión recursiva de la búsqueda ternaria.
     *
     * @param array Arreglo ORDENADO
     * @param target Elemento a buscar
     * @return Índice del elemento encontrado, o -1 si no existe
     */
    public static int searchRecursive(int[] array, int target) {
        if (array == null || array.length == 0) {
            return -1;
        }
        return searchRecursive(array, target, 0, array.length - 1);
    }

    private static int searchRecursive(int[] array, int target, int left, int right) {
        if (left > right) {
            return -1;
        }

        int third = (right - left) / 3;
        int mid1 = left + third;
        int mid2 = right - third;

        if (array[mid1] == target) {
            return mid1;
        }

        if (array[mid2] == target) {
            return mid2;
        }

        if (target < array[mid1]) {
            return searchRecursive(array, target, left, mid1 - 1);
        } else if (target > array[mid2]) {
            return searchRecursive(array, target, mid2 + 1, right);
        } else {
            return searchRecursive(array, target, mid1 + 1, mid2 - 1);
        }
    }
}
