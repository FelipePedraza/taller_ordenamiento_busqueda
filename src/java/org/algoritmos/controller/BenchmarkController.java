package org.algoritmos.controller;

import org.algoritmos.core.BenchmarkResult;
import org.algoritmos.core.BenchmarkService;
import org.algoritmos.util.ResultExporter;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

/**
 * Controlador que orquesta la ejecucion de benchmarks.
 */
public class BenchmarkController {

    private final BenchmarkService service;
    private final ResultExporter exporter;

    public BenchmarkController() {
        this.service = new BenchmarkService();
        this.exporter = new ResultExporter();
    }

    public void ejecutar() throws IOException {
        long tiempoInicio = System.currentTimeMillis();

        System.out.println("============================================================");
        System.out.println("  BENCHMARK DE ALGORITMOS DE ORDENAMIENTO Y BUSQUEDA");
        System.out.println("  Java Implementation");
        System.out.println("============================================================\n");

        // Ejecutar benchmarks
        List<BenchmarkResult> resultados = new ArrayList<>();

        System.out.println("[1/2] Ejecutando algoritmos de ordenamiento...");
        resultados.addAll(service.ejecutarOrdenamiento());
        mostrarResumenOrdenamiento(resultados.stream()
            .filter(r -> r.getTipo().equals("ordenamiento"))
            .collect(Collectors.toList()));

        System.out.println("\n[2/2] Ejecutando algoritmos de busqueda...");
        resultados.addAll(service.ejecutarBusqueda());
        mostrarResumenBusqueda(resultados.stream()
            .filter(r -> r.getTipo().equals("busqueda"))
            .collect(Collectors.toList()));

        // Exportar resultados: incluye tanto medidos como estimados, excluye solo los omitidos
        System.out.println("\n------------------------------------------------------------");
        System.out.println("Exportando resultados...");
        for (BenchmarkResult r : resultados) {
            if (r.getNotas() == null || esEstimado(r.getNotas())) {
                exporter.addResult(r.getAlgoritmo(), r.getTipo(), r.getTamaño(), r.getTiempoNs());
            }
        }
        exporter.exportAll("resultados_java");
        System.out.println("  Exportacion completada");

        // Resumen final
        long tiempoTotal = System.currentTimeMillis() - tiempoInicio;
        System.out.println("\n============================================================");
        System.out.println("  EJECUCION COMPLETADA");
        System.out.println("  Tiempo total: " + tiempoTotal + " ms");
        System.out.println("  Resultados: " + exporter.size());
        System.out.println("============================================================");
    }

    /**
     * Indica si una nota corresponde a un resultado estimado (y no simplemente omitido).
     * Las notas de estimacion comienzan con '~'.
     */
    private boolean esEstimado(String notas) {
        return notas != null && notas.startsWith("~");
    }

    private void mostrarResumenOrdenamiento(List<BenchmarkResult> resultados) {
        System.out.println("\n  --- ORDENAMIENTO (tiempos en ms) ---");

        Map<Integer, List<BenchmarkResult>> porTamano = resultados.stream()
            .collect(Collectors.groupingBy(BenchmarkResult::getTamaño));

        porTamano.forEach((tamano, lista) -> {
            System.out.println("\n  Dataset: " + tamano + " elementos");
            lista.stream()
                .sorted((a, b) -> Long.compare(a.getTiempoNs(), b.getTiempoNs()))
                .forEach(r -> {
                    if (esEstimado(r.getNotas())) {
                        // Resultado estimado: mostrar tiempo junto con la nota aclaratoria
                        System.out.printf("    %-20s: %10.3f ms  [%s]%n",
                            r.getAlgoritmo(), r.getTiempoMs(), r.getNotas());
                    } else if (r.getNotas() != null) {
                        // Resultado descartado por otra razon (nunca deberia ocurrir ahora)
                        System.out.printf("    %-20s: %s%n", r.getAlgoritmo(), r.getNotas());
                    } else {
                        System.out.printf("    %-20s: %10.3f ms%n", r.getAlgoritmo(), r.getTiempoMs());
                    }
                });
        });
    }

    private void mostrarResumenBusqueda(List<BenchmarkResult> resultados) {
        System.out.println("\n  --- BUSQUEDA (tiempos en ns) ---");

        Map<Integer, List<BenchmarkResult>> porTamano = resultados.stream()
            .collect(Collectors.groupingBy(BenchmarkResult::getTamaño));

        porTamano.forEach((tamano, lista) -> {
            System.out.println("\n  Dataset: " + tamano + " elementos (ordenado)");
            lista.stream()
                .sorted((a, b) -> Long.compare(a.getTiempoNs(), b.getTiempoNs()))
                .forEach(r -> System.out.printf("    %-20s: %10d ns%n", r.getAlgoritmo(), r.getTiempoNs()));
        });
    }
}