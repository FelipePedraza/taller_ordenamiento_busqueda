package org.algoritmos.core;

import org.algoritmos.ordenamiento.*;
import org.algoritmos.busqueda.*;
import org.algoritmos.util.DataGenerator;
import org.algoritmos.util.Timer;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

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

        // Tiempos reales de ShakerSort por tamaño, para la estimación cuadrática
        Map<Integer, Long> shakerTiempos = new HashMap<>();

        for (int size : SIZES) {
            int[] originalData = generator.loadFromFile(generator.getFilename(size));

            // Shaker Sort: ejecutar en tamaños pequeños, estimar en 1M
            if (size < 1_000_000) {
                int[] data = DataGenerator.copyArray(originalData);
                timer.start();
                ShakerSort.sort(data);
                long tiempo = timer.stop();
                shakerTiempos.put(size, tiempo);
                resultados.add(new BenchmarkResult("ShakerSort", "ordenamiento", size, tiempo));
            } else {
                long tiempoEstimado = estimarTiempoShakerSort(shakerTiempos, size);
                resultados.add(new BenchmarkResult(
                    "ShakerSort", "ordenamiento", size, tiempoEstimado, "~estimado O(n^2)"
                ));
            }

            // Dual-Pivot QuickSort
            resultados.add(ejecutarOrdenamientoAlgoritmo("DualPivotQuickSort", originalData,
                arr -> DualPivotQuickSort.sort(arr), size));

            // Heap Sort
            resultados.add(ejecutarOrdenamientoAlgoritmo("HeapSort", originalData,
                arr -> HeapSort.sort(arr), size));

            // Merge Sort
            resultados.add(ejecutarOrdenamientoAlgoritmo("MergeSort", originalData,
                arr -> MergeSort.sort(arr), size));

            // Radix Sort
            resultados.add(ejecutarOrdenamientoAlgoritmo("RadixSort", originalData,
                arr -> RadixSort.sort(arr), size));
        }

        return resultados;
    }

    /**
     * Estima el tiempo de ShakerSort para un tamaño objetivo usando regresión O(n²).
     * Ajusta la constante C promediando C_i = t_i / n_i² de los puntos conocidos
     * y luego calcula t(n) = C_promedio * n².
     *
     * @param tiemposConocidos Mapa de tiempos reales medidos por tamaño
     * @param targetSize       Tamaño objetivo a estimar
     * @return Tiempo estimado en nanosegundos
     */
    private long estimarTiempoShakerSort(Map<Integer, Long> tiemposConocidos, int targetSize) {
        if (tiemposConocidos.isEmpty()) {
            return 0L;
        }

        // Calcular la constante C = t / n² para cada punto conocido y promediarla
        double sumC = 0.0;
        for (Map.Entry<Integer, Long> entry : tiemposConocidos.entrySet()) {
            double n = entry.getKey();
            double t = entry.getValue();
            sumC += t / (n * n);
        }
        double cPromedio = sumC / tiemposConocidos.size();

        return (long) (cPromedio * (double) targetSize * (double) targetSize);
    }

    private BenchmarkResult ejecutarOrdenamientoAlgoritmo(String nombre, int[] originalData,
                                                           java.util.function.Consumer<int[]> algoritmo,
                                                           int size) {
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
            resultados.add(ejecutarBusquedaAlgoritmo("BinarySearch", data, target,
                (arr, t) -> BinarySearch.search(arr, t), size));

            // Ternary Search
            resultados.add(ejecutarBusquedaAlgoritmo("TernarySearch", data, target,
                (arr, t) -> TernarySearch.search(arr, t), size));

            // Jump Search
            resultados.add(ejecutarBusquedaAlgoritmo("JumpSearch", data, target,
                (arr, t) -> JumpSearch.search(arr, t), size));
        }

        return resultados;
    }

    private BenchmarkResult ejecutarBusquedaAlgoritmo(String nombre, int[] data, int target,
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