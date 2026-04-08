package org.algoritmos.ordenamiento;

import java.util.Arrays;

/**
 * Radix Sort (Base 10)
 *
 * Algoritmo de ordenamiento no comparativo que ordena dígito por dígito,
 * desde el dígito menos significativo (LSD) al más significativo (MSD).
 *
 * Usa Counting Sort como subrutina para ordenar por cada dígito.
 *
 * Complejidad:
 * - Peor caso: O(d * (n + k)) donde d=dígitos, k=base
 *   Para enteros de 32 bits en base 10: O(10 * n) ≈ O(n)
 * - Mejor caso: O(d * (n + k))
 * - Caso promedio: O(d * (n + k))
 * - Espacio auxiliar: O(n + k)
 *
 * Ventajas:
 * - Tiempo lineal O(n) para datos con rango limitado
 * - Estable
 * - Excelente para enteros y strings de longitud fija
 *
 * Desventajas:
 * - Requiere espacio extra O(n)
 * - Solo funciona con tipos que se pueden "digrerir" en dígitos
 * - Overhead de crear arreglos temporales
 */
public class RadixSort {

    private static final int BASE = 10;

    /**
     * Ordena el arreglo usando Radix Sort (base 10).
     *
     * @param array Arreglo de enteros positivos a ordenar
     * @return El mismo arreglo ordenado
     */
    public static int[] sort(int[] array) {
        if (array == null || array.length < 2) {
            return array;
        }

        // Encontrar el máximo para saber cuántos dígitos procesar
        int max = findMax(array);

        // Aplicar counting sort para cada dígito
        // exp representa la posición del dígito (1, 10, 100, ...)
        for (int exp = 1; max / exp > 0; exp *= BASE) {
            countingSortByDigit(array, exp);
        }

        return array;
    }

    /**
     * Encuentra el valor máximo en el arreglo.
     */
    private static int findMax(int[] array) {
        int max = array[0];
        for (int value : array) {
            if (value > max) {
                max = value;
            }
        }
        return max;
    }

    /**
     * Counting Sort para un dígito específico (posición dada por exp).
     *
     * @param array Arreglo a ordenar
     * @param exp 1 para unidades, 10 para decenas, 100 para centenas, etc.
     */
    private static void countingSortByDigit(int[] array, int exp) {
        int n = array.length;
        int[] output = new int[n];
        int[] count = new int[BASE];

        // Inicializar contadores
        Arrays.fill(count, 0);

        // Contar ocurrencias del dígito actual
        for (int value : array) {
            int digit = (value / exp) % BASE;
            count[digit]++;
        }

        // Calcular posiciones acumuladas
        for (int i = 1; i < BASE; i++) {
            count[i] += count[i - 1];
        }

        // Construir arreglo de salida (de atrás hacia adelante para estabilidad)
        for (int i = n - 1; i >= 0; i--) {
            int digit = (array[i] / exp) % BASE;
            output[count[digit] - 1] = array[i];
            count[digit]--;
        }

        // Copiar el resultado al arreglo original
        System.arraycopy(output, 0, array, 0, n);
    }
}
