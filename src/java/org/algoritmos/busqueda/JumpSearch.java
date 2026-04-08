package org.algoritmos.busqueda;

/**
 * Búsqueda por Saltos (Jump Search)
 *
 * Algoritmo de búsqueda para arreglos ordenados que salta bloques
 * de tamaño √n hasta encontrar el rango donde podría estar el elemento,
 * y luego hace una búsqueda lineal en ese bloque.
 *
 * Requiere: Arreglo ORDENADO
 *
 * Complejidad:
 * - Peor caso: O(√n)
 * - Mejor caso: O(1) - elemento en el primer salto
 * - Caso promedio: O(√n)
 * - Espacio auxiliar: O(1)
 *
 * Ventajas:
 * - Mejor que búsqueda lineal O(n)
 * - Menos comparaciones que búsqueda lineal
 * - Acceso secuencial amigable con cache
 *
 * Desventajas:
 * - Peor que búsqueda binaria O(log n)
 * - Requiere arreglo ordenado
 * - El tamaño óptimo de salto es √n, pero puede variar según el patrón de datos
 *
 * Casos de uso:
 * - Útil cuando saltar atrás es costoso (listas enlazadas, acceso secuencial)
 * - Cuando el costo de comparar elementos es menor que el de saltar índices
 */
public class JumpSearch {

    /**
     * Busca un elemento en un arreglo ordenado.
     *
     * Tamaño de salto: √n (óptimo teórico)
     *
     * @param array Arreglo ORDENADO donde buscar
     * @param target Elemento a buscar
     * @return Índice del elemento encontrado, o -1 si no existe
     */
    public static int search(int[] array, int target) {
        if (array == null || array.length == 0) {
            return -1;
        }

        int n = array.length;
        int step = (int) Math.sqrt(n);

        // Encontrar el bloque donde podría estar el elemento
        int prev = 0;
        int curr = Math.min(step, n) - 1;

        // Saltar mientras el target sea mayor que el último del bloque
        while (curr < n && array[curr] < target) {
            prev = curr + 1;
            curr = Math.min(curr + step, n) - 1;

            // Si saltamos más allá del final, no existe
            if (prev >= n) {
                return -1;
            }
        }

        // Ajustar curr si nos pasamos
        curr = Math.min(curr, n - 1);

        // Búsqueda lineal en el bloque encontrado
        for (int i = prev; i <= curr; i++) {
            if (array[i] == target) {
                return i;
            }
            if (array[i] > target) {
                return -1; // No puede estar más adelante (arreglo ordenado)
            }
        }

        return -1;
    }

    /**
     * Versión con tamaño de salto personalizado.
     *
     * @param array Arreglo ORDENADO
     * @param target Elemento a buscar
     * @param jumpSize Tamaño del salto (recomendado: √n)
     * @return Índice del elemento encontrado, o -1 si no existe
     */
    public static int searchWithJumpSize(int[] array, int target, int jumpSize) {
        if (array == null || array.length == 0) {
            return -1;
        }

        if (jumpSize <= 0) {
            throw new IllegalArgumentException("El tamaño de salto debe ser positivo");
        }

        int n = array.length;
        int step = jumpSize;

        int prev = 0;
        int curr = Math.min(step, n) - 1;

        while (curr < n && array[curr] < target) {
            prev = curr + 1;
            curr = Math.min(curr + step, n) - 1;

            if (prev >= n) {
                return -1;
            }
        }

        curr = Math.min(curr, n - 1);

        for (int i = prev; i <= curr; i++) {
            if (array[i] == target) {
                return i;
            }
            if (array[i] > target) {
                return -1;
            }
        }

        return -1;
    }
}
