package org.algoritmos.main;

import org.algoritmos.ordenamiento.*;
import org.algoritmos.util.DataGenerator;
import org.algoritmos.util.Timer;
import org.algoritmos.util.ResultExporter;

import java.io.IOException;

/**
 * Clase principal para ejecutar todas las pruebas de ordenamiento.
 *
 * Ejecuta cada algoritmo de ordenamiento con datasets de diferentes tamaños:
 * - 10,000 elementos
 * - 100,000 elementos
 * - 1,000,000 elementos
 *
 * Para cada prueba:
 * 1. Carga los datos desde archivo (o genera si no existen)
 * 2. Hace una copia del arreglo original
 * 3. Mide el tiempo de ordenamiento SOLO (excluyendo I/O)
 * 4. Registra el resultado
 *
 * Algoritmos probados:
 * - Shaker Sort (Cocktail Sort)
 * - Dual-Pivot QuickSort
 * - Heap Sort
 * - Merge Sort
 * - Radix Sort (base 10)
 */
public class MainOrdenamiento {

    private static final int[] SIZES = {10_000, 100_000, 1_000_000};
    private static final Timer timer = new Timer();
    private static ResultExporter exporter;

    public static void main(String[] args) {
        System.out.println("========================================");
        System.out.println("    PRUEBAS DE ALGORITMOS DE ORDENAMIENTO");
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

                // Cargar datos originales
                int[] originalData = generator.loadFromFile(generator.getFilename(size));

                // Ejecutar cada algoritmo
                runShakerSort(originalData, size);
                runDualPivotQuickSort(originalData, size);
                runHeapSort(originalData, size);
                runMergeSort(originalData, size);
                runRadixSort(originalData, size);
            }

            // Mostrar y exportar resultados
            exporter.printSummary();
            exporter.exportToCsv("resultados_ordenamiento_java.csv");
            exporter.exportToJson("resultados_ordenamiento_java.json");

            System.out.println("\n✓ Pruebas de ordenamiento completadas.");

        } catch (IOException e) {
            System.err.println("Error de E/S: " + e.getMessage());
            e.printStackTrace();
            System.exit(1);
        }
    }

    private static void runShakerSort(int[] originalData, int size) {
        int[] data = DataGenerator.copyArray(originalData);

        timer.start();
        ShakerSort.sort(data);
        long tiempoNs = timer.stop();

        exporter.addResult("ShakerSort", "ordenamiento", size, tiempoNs);
        System.out.printf("%-20s: %10.6f ms%n", "ShakerSort", timer.getElapsedMillis());
    }

    private static void runDualPivotQuickSort(int[] originalData, int size) {
        int[] data = DataGenerator.copyArray(originalData);

        timer.start();
        DualPivotQuickSort.sort(data);
        long tiempoNs = timer.stop();

        exporter.addResult("DualPivotQuickSort", "ordenamiento", size, tiempoNs);
        System.out.printf("%-20s: %10.6f ms%n", "DualPivotQuickSort", timer.getElapsedMillis());
    }

    private static void runHeapSort(int[] originalData, int size) {
        int[] data = DataGenerator.copyArray(originalData);

        timer.start();
        HeapSort.sort(data);
        long tiempoNs = timer.stop();

        exporter.addResult("HeapSort", "ordenamiento", size, tiempoNs);
        System.out.printf("%-20s: %10.6f ms%n", "HeapSort", timer.getElapsedMillis());
    }

    private static void runMergeSort(int[] originalData, int size) {
        int[] data = DataGenerator.copyArray(originalData);

        timer.start();
        MergeSort.sort(data);
        long tiempoNs = timer.stop();

        exporter.addResult("MergeSort", "ordenamiento", size, tiempoNs);
        System.out.printf("%-20s: %10.6f ms%n", "MergeSort", timer.getElapsedMillis());
    }

    private static void runRadixSort(int[] originalData, int size) {
        int[] data = DataGenerator.copyArray(originalData);

        timer.start();
        RadixSort.sort(data);
        long tiempoNs = timer.stop();

        exporter.addResult("RadixSort", "ordenamiento", size, tiempoNs);
        System.out.printf("%-20s: %10.6f ms%n", "RadixSort", timer.getElapsedMillis());
    }
}
