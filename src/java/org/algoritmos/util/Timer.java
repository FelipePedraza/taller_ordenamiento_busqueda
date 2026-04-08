package org.algoritmos.util;

/**
 * Clase utilitaria para medición precisa de tiempos de ejecución.
 *
 * Utiliza System.nanoTime() para máxima precisión, ya que está optimizado
 * para medir intervalos de tiempo y no está sujeto a cambios de reloj del sistema.
 *
 * Diseño:
 * - start(): inicia la medición
 * * stop(): detiene y retorna el tiempo transcurrido
 * - getElapsedNanos(): obtiene el tiempo en nanosegundos
 * - getElapsedMillis(): obtiene el tiempo en milisegundos
 *
 * Thread-safety: No es thread-safe por diseño para máxima performance.
 * Cada hilo debe usar su propia instancia.
 */
public class Timer {

    private long startTime;
    private long elapsedNanos;
    private boolean running;

    /**
     * Inicia el temporizador.
     * Si ya estaba corriendo, reinicia la medición.
     */
    public void start() {
        this.startTime = System.nanoTime();
        this.running = true;
    }

    /**
     * Detiene el temporizador y retorna el tiempo transcurrido en nanosegundos.
     *
     * @return Tiempo transcurrido en nanosegundos
     * @throws IllegalStateException si el timer no estaba corriendo
     */
    public long stop() {
        if (!running) {
            throw new IllegalStateException("Timer no estaba corriendo. Llame start() primero.");
        }
        this.elapsedNanos = System.nanoTime() - startTime;
        this.running = false;
        return this.elapsedNanos;
    }

    /**
     * Obtiene el último tiempo medido en nanosegundos.
     *
     * @return Tiempo en nanosegundos
     */
    public long getElapsedNanos() {
        if (running) {
            return System.nanoTime() - startTime;
        }
        return elapsedNanos;
    }

    /**
     * Obtiene el último tiempo medido en milisegundos (con decimales).
     *
     * @return Tiempo en milisegundos (precisión de 6 decimales)
     */
    public double getElapsedMillis() {
        return getElapsedNanos() / 1_000_000.0;
    }

    /**
     * Resetea el temporizador a su estado inicial.
     */
    public void reset() {
        this.startTime = 0;
        this.elapsedNanos = 0;
        this.running = false;
    }

    /**
     * Versión estática para mediciones de un solo uso.
     *
     * Ejemplo: long tiempo = Timer.measure(() -> algoritmo.sort(array));
     *
     * @param runnable El código a medir
     * @return Tiempo en nanosegundos
     */
    public static long measureNanos(Runnable runnable) {
        long start = System.nanoTime();
        runnable.run();
        return System.nanoTime() - start;
    }
}
