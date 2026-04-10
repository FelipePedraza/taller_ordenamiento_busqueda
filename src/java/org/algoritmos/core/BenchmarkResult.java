package org.algoritmos.core;

import java.time.Instant;

/**
 * Modelo de resultado de benchmark.
 */
public class BenchmarkResult {
    private final String algoritmo;
    private final String tipo;
    private final int tamaño;
    private final long tiempoNs;
    private final String timestamp;
    private final String notas;

    public BenchmarkResult(String algoritmo, String tipo, int tamaño, long tiempoNs) {
        this(algoritmo, tipo, tamaño, tiempoNs, null);
    }

    public BenchmarkResult(String algoritmo, String tipo, int tamaño, long tiempoNs, String notas) {
        this.algoritmo = algoritmo;
        this.tipo = tipo;
        this.tamaño = tamaño;
        this.tiempoNs = tiempoNs;
        this.timestamp = Instant.now().toString();
        this.notas = notas;
    }

    public String getAlgoritmo() { return algoritmo; }
    public String getTipo() { return tipo; }
    public int getTamaño() { return tamaño; }
    public long getTiempoNs() { return tiempoNs; }
    public double getTiempoMs() { return tiempoNs / 1_000_000.0; }
    public String getTimestamp() { return timestamp; }
    public String getNotas() { return notas; }
}
