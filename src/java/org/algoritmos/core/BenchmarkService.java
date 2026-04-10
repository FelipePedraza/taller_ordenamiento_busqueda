package org.algoritmos.core;

import org.algoritmos.ordenamiento.*;
import org.algoritmos.busqueda.*;
import org.algoritmos.util.DataGenerator;
import org.algoritmos.util.Timer;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/**
 * Servicio que ejecuta benchmarks de algoritmos.
 */
public class BenchmarkService {

    private static final int[] SIZES = {10_000, 100_000, 1_000_000};
    private static final int SEARCH_ITERATIONS = 1000;

    private final DataGenerator generator;
    private final Timer timer;

    public BenchmarkService() {
        this.generator = new DataGenerator();
        this.timer = new Timer();
    }

    public List<BenchmarkResult> ejecutarOrdenamiento() throws IOException {
        List<BenchmarkResult> resultados = new ArrayList<>();

        generator.generateAllDatasets();

        for (int size : SIZES) {
            int[] originalData = generator.loadFromFile(generator.getFilename(size));

            // Shaker Sort (omite para 1M)
            if (size <= 100_000) {
                int[] data = DataGenerator.copyArray(originalData);
                timer.start();
                ShakerSort.sort(data);
                resultados.add(new BenchmarkResult("ShakerSort", "ordenamiento", size, timer.stop()));
            } else {
                resultados.add(new BenchmarkResult("ShakerSort", "ordenamiento", size, 0, "O(n^2) - omitido"));
            }

            // Dual-Pivot QuickSort
            resultados.add(ejecutarOrdenamiento("DualPivotQuickSort", originalData,
                arr -> DualPivotQuickSort.sort(arr), size));

            // Heap Sort
            resultados.add(ejecutarOrdenamiento("HeapSort", originalData,
                arr -> HeapSort.sort(arr), size));

            // Merge Sort
            resultados.add(ejecutarOrdenamiento("MergeSort", originalData,
                arr -> MergeSort.sort(arr), size));

            // Radix Sort
            resultados.add(ejecutarOrdenamiento("RadixSort", originalData,
                arr -> RadixSort.sort(arr), size));
        }

        return resultados;
    }

    private BenchmarkResult ejecutarOrdenamiento(String nombre, int[] originalData,
                                                   java.util.function.Consumer<int[]> algoritmo, int size) {
        int[] data = DataGenerator.copyArray(originalData);
        timer.start();
        algoritmo.accept(data);
        return new BenchmarkResult(nombre, "ordenamiento", size, timer.stop());
    }

    public List<BenchmarkResult> ejecutarBusqueda() throws IOException {
        List<BenchmarkResult> resultados = new ArrayList<>();

        for (int size : SIZES) {
            int[] data = generator.loadFromFile(generator.getFilename(size));
            DualPivotQuickSort.sort(data);

            int target = data[size / 2];

            // Binary Search
            resultados.add(ejecutarBusqueda("BinarySearch", data, target,
                (arr, t) -> BinarySearch.search(arr, t), size));

            // Ternary Search
            resultados.add(ejecutarBusqueda("TernarySearch", data, target,
                (arr, t) -> TernarySearch.search(arr, t), size));

            // Jump Search
            resultados.add(ejecutarBusqueda("JumpSearch", data, target,
                (arr, t) -> JumpSearch.search(arr, t), size));
        }

        return resultados;
    }

    private BenchmarkResult ejecutarBusqueda(String nombre, int[] data, int target,
                                             java.util.function.BiFunction<int[], Integer, Integer> algoritmo,
                                             int size) {
        long tiempoTotal = 0;
        for (int i = 0; i < SEARCH_ITERATIONS; i++) {
            timer.start();
            algoritmo.apply(data, target);
            tiempoTotal += timer.stop();
        }
        return new BenchmarkResult(nombre, "busqueda", size, tiempoTotal / SEARCH_ITERATIONS);
    }
}
