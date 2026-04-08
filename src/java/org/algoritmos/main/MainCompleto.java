package org.algoritmos.main;

import org.algoritmos.util.DataGenerator;
import org.algoritmos.util.ResultExporter;
import org.algoritmos.util.Timer;
import org.algoritmos.ordenamiento.*;
import org.algoritmos.busqueda.*;

import java.io.IOException;

/**
 * Clase principal que ejecuta TODAS las pruebas (ordenamiento y búsqueda)
 * y exporta los resultados completos.
 *
 * Esta es la clase recomendada para ejecutar el proyecto completo.
 *
 * Flujo de ejecución:
 * 1. Genera/carga datasets (10K, 100K, 1M elementos)
 * 2. Ejecuta algoritmos de ordenamiento con cada dataset
 * 3. Ordena los datasets y ejecuta algoritmos de búsqueda
 * 4. Exporta todos los resultados a CSV y JSON
 *
 * Archivos de salida:
 * - data/output/resultados_java.csv
 * - data/output/resultados_java.json
 */
public class MainCompleto {

    private static final int[] SIZES = {10_000, 100_000, 1_000_000};
    private static final Timer timer = new Timer();
    private static ResultExporter exporter;

    // Iteraciones para búsqueda (tiempos muy pequeños)
    private static final int SEARCH_ITERATIONS = 1000;

    public static void main(String[] args) {
        System.out.println("╔════════════════════════════════════════════════════════════╗");
        System.out.println("║     TALLER: ALGORITMOS DE ORDENAMIENTO Y BÚSQUEDA          ║");
        System.out.println("║     Java Implementation                                    ║");
        System.out.println("╚════════════════════════════════════════════════════════════╝\n");

        DataGenerator generator = new DataGenerator();
        exporter = new ResultExporter();

        long tiempoInicioTotal = System.currentTimeMillis();

        try {
            // Paso 1: Generar o cargar datasets
            System.out.println("[1/3] Generando/Cargando datasets...");
            generator.generateAllDatasets();
            System.out.println("    ✓ Datasets listos\n");

            // Paso 2: Ejecutar pruebas de ordenamiento
            System.out.println("[2/3] Ejecutando algoritmos de ordenamiento...");
            ejecutarPruebasOrdenamiento(generator);
            System.out.println("    ✓ Pruebas de ordenamiento completadas\n");

            // Paso 3: Ejecutar pruebas de búsqueda
            System.out.println("[3/3] Ejecutando algoritmos de búsqueda...");
            ejecutarPruebasBusqueda(generator);
            System.out.println("    ✓ Pruebas de búsqueda completadas\n");

            // Paso 4: Exportar resultados
            System.out.println("[4/4] Exportando resultados...");
            exporter.exportAll("resultados_java");
            System.out.println("    ✓ Exportación completada\n");

            // Resumen final
            long tiempoTotal = System.currentTimeMillis() - tiempoInicioTotal;
            System.out.println("═".repeat(60));
            System.out.println("  EJECUCIÓN COMPLETADA");
            System.out.println("  Tiempo total: " + tiempoTotal + " ms");
            System.out.println("  Resultados registrados: " + exporter.size());
            System.out.println("═".repeat(60));

            // Mostrar resumen detallado
            exporter.printSummary();

        } catch (IOException e) {
            System.err.println("\n❌ Error de E/S: " + e.getMessage());
            e.printStackTrace();
            System.exit(1);
        } catch (Exception e) {
            System.err.println("\n❌ Error inesperado: " + e.getMessage());
            e.printStackTrace();
            System.exit(1);
        }
    }

    private static void ejecutarPruebasOrdenamiento(DataGenerator generator) throws IOException {
        System.out.println("\n  --- ALGORITMOS DE ORDENAMIENTO ---");

        for (int size : SIZES) {
            System.out.println("\n  Dataset: " + size + " elementos");
            System.out.println("  " + "-".repeat(40));

            // Cargar datos originales
            int[] originalData = generator.loadFromFile(generator.getFilename(size));

            // Shaker Sort (se salta para n=1M por ser O(n²) - tomaría ~25 minutos)
            if (size <= 100_000) {
                int[] data1 = DataGenerator.copyArray(originalData);
                timer.start();
                ShakerSort.sort(data1);
                exporter.addResult("ShakerSort", "ordenamiento", size, timer.stop());
                System.out.printf("    %-20s: %10.3f ms%n", "ShakerSort", timer.getElapsedMillis());
            } else {
                System.out.printf("    %-20s: %10s %n", "ShakerSort", "[O(n²) - omitido]");
            }

            // Dual-Pivot QuickSort
            int[] data2 = DataGenerator.copyArray(originalData);
            timer.start();
            DualPivotQuickSort.sort(data2);
            exporter.addResult("DualPivotQuickSort", "ordenamiento", size, timer.stop());
            System.out.printf("    %-20s: %10.3f ms%n", "DualPivotQuickSort", timer.getElapsedMillis());

            // Heap Sort
            int[] data3 = DataGenerator.copyArray(originalData);
            timer.start();
            HeapSort.sort(data3);
            exporter.addResult("HeapSort", "ordenamiento", size, timer.stop());
            System.out.printf("    %-20s: %10.3f ms%n", "HeapSort", timer.getElapsedMillis());

            // Merge Sort
            int[] data4 = DataGenerator.copyArray(originalData);
            timer.start();
            MergeSort.sort(data4);
            exporter.addResult("MergeSort", "ordenamiento", size, timer.stop());
            System.out.printf("    %-20s: %10.3f ms%n", "MergeSort", timer.getElapsedMillis());

            // Radix Sort
            int[] data5 = DataGenerator.copyArray(originalData);
            timer.start();
            RadixSort.sort(data5);
            exporter.addResult("RadixSort", "ordenamiento", size, timer.stop());
            System.out.printf("    %-20s: %10.3f ms%n", "RadixSort", timer.getElapsedMillis());
        }
    }

    private static void ejecutarPruebasBusqueda(DataGenerator generator) throws IOException {
        System.out.println("\n  --- ALGORITMOS DE BÚSQUEDA ---");

        for (int size : SIZES) {
            System.out.println("\n  Dataset: " + size + " elementos (ordenado)");
            System.out.println("  " + "-".repeat(40));

            // Cargar y ordenar datos
            int[] data = generator.loadFromFile(generator.getFilename(size));
            DualPivotQuickSort.sort(data);

            // Seleccionar target en posición media
            int targetIndex = size / 2;
            int target = data[targetIndex];

            // Binary Search
            long tiempoTotal = 0;
            for (int i = 0; i < SEARCH_ITERATIONS; i++) {
                timer.start();
                BinarySearch.search(data, target);
                tiempoTotal += timer.stop();
            }
            long tiempoPromedio = tiempoTotal / SEARCH_ITERATIONS;
            exporter.addResult("BinarySearch", "busqueda", size, tiempoPromedio);
            System.out.printf("    %-20s: %10d ns%n", "BinarySearch", tiempoPromedio);

            // Ternary Search
            tiempoTotal = 0;
            for (int i = 0; i < SEARCH_ITERATIONS; i++) {
                timer.start();
                TernarySearch.search(data, target);
                tiempoTotal += timer.stop();
            }
            tiempoPromedio = tiempoTotal / SEARCH_ITERATIONS;
            exporter.addResult("TernarySearch", "busqueda", size, tiempoPromedio);
            System.out.printf("    %-20s: %10d ns%n", "TernarySearch", tiempoPromedio);

            // Jump Search
            tiempoTotal = 0;
            for (int i = 0; i < SEARCH_ITERATIONS; i++) {
                timer.start();
                JumpSearch.search(data, target);
                tiempoTotal += timer.stop();
            }
            tiempoPromedio = tiempoTotal / SEARCH_ITERATIONS;
            exporter.addResult("JumpSearch", "busqueda", size, tiempoPromedio);
            System.out.printf("    %-20s: %10d ns%n", "JumpSearch", tiempoPromedio);
        }
    }
}
