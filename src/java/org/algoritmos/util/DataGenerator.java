package org.algoritmos.util;

import java.io.*;
import java.util.Random;

/**
 * Generador de datos aleatorios para las pruebas de algoritmos.
 *
 * Genera enteros aleatorios de 8 dígitos (10,000,000 a 99,999,999)
 * y los guarda en archivos de texto para reutilización.
 *
 * Responsabilidades:
 * - Generar arreglos aleatorios en memoria
 * - Persistir datos en archivos de texto
 * - Cargar datos existentes desde archivos
 * - Verificar existencia de archivos para evitar regeneración
 *
 * Los archivos se guardan en: data/input/
 * - datos_10000.txt
 * - datos_100000.txt
 * - datos_1000000.txt
 */
public class DataGenerator {

    private static final int MIN_VALUE = 10_000_000;
    private static final int MAX_VALUE = 99_999_999;
    private static final String INPUT_DIR = "data/input";

    private final Random random;
    private final String basePath;

    /**
     * Constructor por defecto. Usa el directorio de trabajo actual.
     */
    public DataGenerator() {
        this("");
    }

    /**
     * Constructor con ruta base configurable.
     *
     * @param basePath Ruta base para los archivos de datos (relativa o absoluta)
     */
    public DataGenerator(String basePath) {
        this.random = new Random(42); // Semilla fija para reproducibilidad
        this.basePath = basePath != null ? basePath : "";
    }

    /**
     * Genera un arreglo de enteros aleatorios del tamaño especificado.
     *
     * @param size Cantidad de elementos
     * @return Arreglo de enteros aleatorios de 8 dígitos
     */
    public int[] generateArray(int size) {
        int[] array = new int[size];
        int range = MAX_VALUE - MIN_VALUE + 1;

        for (int i = 0; i < size; i++) {
            array[i] = MIN_VALUE + random.nextInt(range);
        }

        return array;
    }

    /**
     * Guarda un arreglo en un archivo de texto.
     * Cada número en una línea independiente.
     *
     * @param array Arreglo a guardar
     * @param filename Nombre del archivo (sin ruta)
     * @throws IOException si ocurre error de E/S
     */
    private File getInputDir() {
        return basePath.isEmpty() ? new File(INPUT_DIR) : new File(basePath, INPUT_DIR);
    }

    /**
     * Guarda un arreglo en un archivo de texto.
     * Cada número en una línea independiente.
     *
     * @param array Arreglo a guardar
     * @param filename Nombre del archivo (sin ruta)
     * @throws IOException si ocurre error de E/S
     */
    public void saveToFile(int[] array, String filename) throws IOException {
        File dir = getInputDir();
        if (!dir.exists()) {
            dir.mkdirs();
        }

        File file = new File(dir, filename);
        try (PrintWriter writer = new PrintWriter(new BufferedWriter(new FileWriter(file)))) {
            for (int value : array) {
                writer.println(value);
            }
        }
    }

    /**
     * Carga un arreglo desde un archivo de texto.
     *
     * @param filename Nombre del archivo
     * @return Arreglo de enteros cargado
     * @throws IOException si el archivo no existe o hay error de lectura
     */
    /**
     * Carga un arreglo desde un archivo de texto.
     *
     * @param filename Nombre del archivo
     * @return Arreglo de enteros cargado
     * @throws IOException si el archivo no existe o hay error de lectura
     */
    public int[] loadFromFile(String filename) throws IOException {
        File file = new File(getInputDir(), filename);

        if (!file.exists()) {
            throw new FileNotFoundException("Archivo no encontrado: " + file.getAbsolutePath());
        }

        // Primero contamos las líneas
        int count = 0;
        try (BufferedReader reader = new BufferedReader(new FileReader(file))) {
            while (reader.readLine() != null) {
                count++;
            }
        }

        // Luego cargamos los datos
        int[] array = new int[count];
        try (BufferedReader reader = new BufferedReader(new FileReader(file))) {
            String line;
            int index = 0;
            while ((line = reader.readLine()) != null) {
                array[index++] = Integer.parseInt(line.trim());
            }
        }

        return array;
    }

    /**
     * Verifica si el archivo de datos existe.
     *
     * @param size Tamaño del dataset
     * @return true si el archivo existe
     */
    public boolean dataExists(int size) {
        File file = new File(INPUT_DIR, getFilename(size));
        return file.exists();
    }

    /**
     * Genera o carga datos del tamaño especificado.
     * Si el archivo existe, lo carga. Si no, genera y guarda.
     *
     * @param size Tamaño del dataset
     * @return Arreglo de enteros
     * @throws IOException si ocurre error de E/S
     */
    public int[] getOrCreateData(int size) throws IOException {
        String filename = getFilename(size);

        if (dataExists(size)) {
            System.out.println("Cargando datos existentes desde " + filename);
            return loadFromFile(filename);
        }

        System.out.println("Generando " + size + " números aleatorios...");
        int[] data = generateArray(size);
        saveToFile(data, filename);
        System.out.println("Datos guardados en " + INPUT_DIR + "/" + filename);
        return data;
    }

    /**
     * Obtiene el nombre del archivo basado en el tamaño.
     *
     * @param size Tamaño del dataset
     * @return Nombre del archivo
     */
    public String getFilename(int size) {
        return "datos_" + size + ".txt";
    }

    /**
     * Crea una copia profunda del arreglo.
     * Útil para no modificar los datos originales.
     *
     * @param original Arreglo original
     * @return Copia del arreglo
     */
    public static int[] copyArray(int[] original) {
        return original.clone();
    }

    /**
     * Genera todos los datasets necesarios para las pruebas.
     * Tamaños: 10,000 / 100,000 / 1,000,000
     *
     * @throws IOException si ocurre error de E/S
     */
    public void generateAllDatasets() throws IOException {
        int[] sizes = {10_000, 100_000, 1_000_000};

        for (int size : sizes) {
            getOrCreateData(size);
        }
    }
}
