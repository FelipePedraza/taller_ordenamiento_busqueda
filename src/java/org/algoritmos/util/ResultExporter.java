package org.algoritmos.util;

import java.io.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/**
 * Exportador de resultados de las pruebas de algoritmos.
 *
 * Responsabilidades:
 * - Acumular resultados de múltiples ejecuciones
 * - Exportar a formato CSV para análisis en Excel/hojas de cálculo
 * - Exportar a formato JSON para análisis programático
 *
 * Formato JSON:
 * [
 *   {
 *     "algoritmo": "nombre",
 *     "tipo": "ordenamiento|busqueda",
 *     "tamaño": 10000,
 *     "tiempo_ms": 0.123456,
 *     "tiempo_ns": 123456
 *   }
 * ]
 *
 * Thread-safety: No es thread-safe. Usar desde un solo hilo o sincronizar.
 */
public class ResultExporter {

    private static final String OUTPUT_DIR = "data/output";
    private final List<Resultado> resultados;

    /**
     * Clase interna inmutable para representar un resultado.
     */
    public static class Resultado {
        public final String algoritmo;
        public final String tipo;
        public final int tamaño;
        public final double tiempoMs;
        public final long tiempoNs;

        public Resultado(String algoritmo, String tipo, int tamaño, long tiempoNs) {
            this.algoritmo = algoritmo;
            this.tipo = tipo;
            this.tamaño = tamaño;
            this.tiempoNs = tiempoNs;
            this.tiempoMs = tiempoNs / 1_000_000.0;
        }
    }

    public ResultExporter() {
        this.resultados = new ArrayList<>();
    }

    /**
     * Agrega un resultado a la colección.
     *
     * @param algoritmo Nombre del algoritmo
     * @param tipo "ordenamiento" o "busqueda"
     * @param tamaño Tamaño del dataset
     * @param tiempoNs Tiempo en nanosegundos
     */
    public void addResult(String algoritmo, String tipo, int tamaño, long tiempoNs) {
        resultados.add(new Resultado(algoritmo, tipo, tamaño, tiempoNs));
    }

    /**
     * Exporta todos los resultados acumulados a CSV.
     *
     * @param filename Nombre del archivo (sin ruta)
     * @throws IOException si ocurre error de E/S
     */
    public void exportToCsv(String filename) throws IOException {
        File dir = new File(OUTPUT_DIR);
        if (!dir.exists()) {
            dir.mkdirs();
        }

        File file = new File(dir, filename);
        try (PrintWriter writer = new PrintWriter(new BufferedWriter(new FileWriter(file)))) {
            // Encabezado
            writer.println("algoritmo,tipo,tamaño,tiempo_ms,tiempo_ns");

            // Datos
            for (Resultado r : resultados) {
                writer.printf(Locale.US, "%s,%s,%d,%.6f,%d%n",
                    r.algoritmo, r.tipo, r.tamaño, r.tiempoMs, r.tiempoNs);
            }
        }

        System.out.println("Resultados CSV exportados a: " + file.getAbsolutePath());
    }

    /**
     * Exporta todos los resultados acumulados a JSON.
     *
     * @param filename Nombre del archivo (sin ruta)
     * @throws IOException si ocurre error de E/S
     */
    public void exportToJson(String filename) throws IOException {
        File dir = new File(OUTPUT_DIR);
        if (!dir.exists()) {
            dir.mkdirs();
        }

        File file = new File(dir, filename);
        try (PrintWriter writer = new PrintWriter(new BufferedWriter(new FileWriter(file)))) {
            writer.println("[");

            for (int i = 0; i < resultados.size(); i++) {
                Resultado r = resultados.get(i);
                writer.println("  {");
                writer.printf(Locale.US, "    \"algoritmo\": \"%s\",%n", r.algoritmo);
                writer.printf(Locale.US, "    \"tipo\": \"%s\",%n", r.tipo);
                writer.printf(Locale.US, "    \"tamaño\": %d,%n", r.tamaño);
                writer.printf(Locale.US, "    \"tiempo_ms\": %.6f,%n", r.tiempoMs);
                writer.printf(Locale.US, "    \"tiempo_ns\": %d%n", r.tiempoNs);
                writer.print("  }");

                if (i < resultados.size() - 1) {
                    writer.print(",");
                }
                writer.println();
            }

            writer.println("]");
        }

        System.out.println("Resultados JSON exportados a: " + file.getAbsolutePath());
    }

    /**
     * Exporta a ambos formatos (CSV y JSON).
     *
     * @param baseName Nombre base (sin extensión)
     * @throws IOException si ocurre error de E/S
     */
    public void exportAll(String baseName) throws IOException {
        exportToCsv(baseName + ".csv");
        exportToJson(baseName + ".json");
    }

    /**
     * Limpia todos los resultados acumulados.
     */
    public void clear() {
        resultados.clear();
    }

    /**
     * Retorna la cantidad de resultados acumulados.
     */
    public int size() {
        return resultados.size();
    }

    /**
     * Imprime un resumen en consola.
     */
    public void printSummary() {
        System.out.println("\n========== RESUMEN DE RESULTADOS ==========");
        System.out.printf("%-25s %-12s %-10s %-15s %-15s%n",
            "Algoritmo", "Tipo", "Tamaño", "Tiempo (ms)", "Tiempo (ns)");
        System.out.println("-".repeat(80));

        for (Resultado r : resultados) {
            System.out.printf("%-25s %-12s %-10d %-15.6f %-15d%n",
                r.algoritmo, r.tipo, r.tamaño, r.tiempoMs, r.tiempoNs);
        }
        System.out.println("=".repeat(80));
    }
}
