package org.algoritmos.main;

import org.algoritmos.busqueda.*;
import org.algoritmos.ordenamiento.DualPivotQuickSort;
import org.algoritmos.util.DataGenerator;
import org.algoritmos.util.Timer;
import org.algoritmos.util.ResultExporter;

import java.io.IOException;

/**
 * Clase principal para ejecutar todas las pruebas de búsqueda.
 *
 * Ejecuta cada algoritmo de búsqueda con datasets ordenados de diferentes tamaños:
 * - 10,000 elementos
 * - 100,000 elementos
 * - 1,000,000 elementos
 *
 * Proceso para cada prueba:
 * 1. Carga los datos desde archivo
 * 2. Ordena los datos (prerrequisito para búsqueda)
 * 3. Selecciona elemento en posición media como target
 * 4. Mide el tiempo de búsqueda SOLO (excluyendo ordenamiento e I/O)
 * 5. Registra el resultado
 *
 * Algoritmos probados:
 * - Búsqueda Binaria (Binary Search)
 * - Búsqueda Ternaria (Ternary Search)
 * - Búsqueda por Saltos (Jump Search)
 *
 * Nota: Los tiempos de búsqueda son muy pequeños (nanosegundos),
 * por lo que se ejecutan múltiples iteraciones para obtener medidas precisas.
 */
public class MainBusqueda {

    private static final int[] SIZES = {10_000, 100_000, 1_000_000};
    private static final Timer timer = new Timer();
    private static ResultExporter exporter;

    // Número de iteraciones para medir tiempos muy pequeños
    private static final int ITERATIONS = 1000;

    public static void main(String[] args) {
        System.out.println("========================================");
        System.out.println("    PRUEBAS DE ALGORITMOS DE BÚSQUEDA");
        System.out.println("========================================\n");

        DataGenerator generator = new DataGenerator();
        exporter = new ResultExporter();

        try {
            // Generar o cargar todos los datasets
            generator.generateAllDatasets();
            System.out.println();

            // Ejecutar pruebas para cada tamaño
            for (int size : SIZES) {
                System.out.println("\n" + "=".repeat(50));
                System.out.println("DATASET: " + size + " elementos");
                System.out.println("=".repeat(50));

                // Cargar y ordenar datos
                int[] originalData = generator.loadFromFile(generator.getFilename(size));
                System.out.println("Ordenando datos para búsqueda...");
                DualPivotQuickSort.sort(originalData);

                // Seleccionar target en la posición media
                int targetIndex = size / 2;
                int target = originalData[targetIndex];
                System.out.println("Elemento a buscar (posición " + targetIndex + "): " + target);

                // Verificar que el elemento existe
                if (targetIndex < 0 || targetIndex >= size) {
                    System.err.println("Error: Índice de target inválido");
                    continue;
                }

                // Ejecutar cada algoritmo de búsqueda
                runBinarySearch(originalData, target, size);
                runTernarySearch(originalData, target, size);
                runJumpSearch(originalData, target, size);
            }

            // Mostrar y exportar resultados
            exporter.printSummary();
            exporter.exportToCsv("resultados_busqueda_java.csv");
            exporter.exportToJson("resultados_busqueda_java.json");

            System.out.println("\n✓ Pruebas de búsqueda completadas.");

        } catch (IOException e) {
            System.err.println("Error de E/S: " + e.getMessage());
            e.printStackTrace();
            System.exit(1);
        }
    }

    private static void runBinarySearch(int[] sortedData, int target, int size) {
        // Validar que el elemento existe
        int foundIndex = BinarySearch.search(sortedData, target);
        if (foundIndex == -1) {
            System.err.println("Error: Elemento no encontrado en BinarySearch");
            return;
        }

        // Medir tiempo promedio sobre múltiples iteraciones
        timer.start();
        for (int i = 0; i < ITERATIONS; i++) {
            BinarySearch.search(sortedData, target);
        }
        long tiempoTotalNs = timer.stop();
        long tiempoPromedioNs = tiempoTotalNs / ITERATIONS;

        exporter.addResult("BinarySearch", "busqueda", size, tiempoPromedioNs);
        System.out.printf("%-20s: %10d ns (encontrado en índice %d)%n",
            "BinarySearch", tiempoPromedioNs, foundIndex);
    }

    private static void runTernarySearch(int[] sortedData, int target, int size) {
        // Validar que el elemento existe
        int foundIndex = TernarySearch.search(sortedData, target);
        if (foundIndex == -1) {
            System.err.println("Error: Elemento no encontrado en TernarySearch");
            return;
        }

        // Medir tiempo promedio sobre múltiples iteraciones
        timer.start();
        for (int i = 0; i < ITERATIONS; i++) {
            TernarySearch.search(sortedData, target);
        }
        long tiempoTotalNs = timer.stop();
        long tiempoPromedioNs = tiempoTotalNs / ITERATIONS;

        exporter.addResult("TernarySearch", "busqueda", size, tiempoPromedioNs);
        System.out.printf("%-20s: %10d ns (encontrado en índice %d)%n",
            "TernarySearch", tiempoPromedioNs, foundIndex);
    }

    private static void runJumpSearch(int[] sortedData, int target, int size) {
        // Validar que el elemento existe
        int foundIndex = JumpSearch.search(sortedData, target);
        if (foundIndex == -1) {
            System.err.println("Error: Elemento no encontrado en JumpSearch");
            return;
        }

        // Medir tiempo promedio sobre múltiples iteraciones
        timer.start();
        for (int i = 0; i < ITERATIONS; i++) {
            JumpSearch.search(sortedData, target);
        }
        long tiempoTotalNs = timer.stop();
        long tiempoPromedioNs = tiempoTotalNs / ITERATIONS;

        exporter.addResult("JumpSearch", "busqueda", size, tiempoPromedioNs);
        System.out.printf("%-20s: %10d ns (encontrado en índice %d)%n",
            "JumpSearch", tiempoPromedioNs, foundIndex);
    }
}
