package org.algoritmos;

import org.algoritmos.controller.BenchmarkController;

import java.io.IOException;

/**
 * Punto de entrada principal del benchmark de algoritmos.
 *
 * Este programa ejecuta benchmarks de ordenamiento y busqueda,
 * y exporta los resultados en CSV y JSON.
 */
public class Main {

    public static void main(String[] args) {
        BenchmarkController controller = new BenchmarkController();

        try {
            controller.ejecutar();
        } catch (IOException e) {
            System.err.println("Error de E/S: " + e.getMessage());
            e.printStackTrace();
            System.exit(1);
        } catch (Exception e) {
            System.err.println("Error inesperado: " + e.getMessage());
            e.printStackTrace();
            System.exit(1);
        }
    }
}
