# Taller de Algoritmos de Ordenamiento y Búsqueda

## Descripción

Este proyecto implementa y compara el rendimiento de diversos algoritmos de ordenamiento y búsqueda en **Java** y **Python**. El objetivo principal es analizar empíricamente la complejidad temporal de los algoritmos mediante mediciones de tiempo de ejecución con diferentes tamaños de datos (10K, 100K y 1M elementos).

Se generan visualizaciones comparativas y se exportan los resultados en formatos CSV y JSON para análisis posterior.

---

## Estructura del Proyecto

```
taller_ordenamiento_busqueda/
├── src/
│   ├── java/               # Código fuente Java
│   │   └── org/algoritmos/
│   │       ├── ordenamiento/   # 5 algoritmos de ordenamiento
│   │       ├── busqueda/       # 3 algoritmos de búsqueda
│   │       ├── util/           # Utilidades (Timer, DataGenerator, ResultExporter)
│   │       └── main/           # Clases ejecutables
│   └── python/             # Código fuente Python
│       ├── ordenamiento/   # 5 algoritmos (Shaker, QuickSort, Heap, Merge, Radix)
│       ├── busqueda/       # 3 algoritmos (Binaria, Ternaria, Jump)
│       ├── utils/          # DataLoader, Timer, ResultExporter
│       ├── visualizacion/  # Generador de gráficos
│       ├── main_ordenamiento.py
│       ├── main_busqueda.py
│       └── main_completo.py
├── data/
│   ├── input/              # Datos de prueba generados (10K, 100K, 1M)
│   └── output/             # Resultados CSV y JSON
├── docs/
│   ├── graficos/           # Gráficos comparativos PNG
│   └── resultados/         # Documentación adicional
├── build.bat               # Script de compilación Java
└── requirements.txt        # Dependencias Python
```

---

## Requisitos Previos

- **Java**: JDK 8 o superior
- **Python**: 3.8 o superior
- **pip**: Para instalar dependencias de Python

---

## Instalación

### Java
No requiere instalación especial. Solo asegúrate de tener el JDK instalado y configurado en el PATH.

### Python
```bash
cd src/python
pip install -r requirements.txt
```

Las dependencias principales son:
- `matplotlib>=3.5.0` - Visualización de gráficos
- `seaborn>=0.12.0` - Gráficos estadísticos mejorados
- `numpy>=1.21.0` - Operaciones numéricas
- `pandas>=1.3.0` - Manipulación de datos

---

## Uso Paso a Paso

### Opción 1: Ejecutar todo desde Java (recomendado)

Desde la raíz del proyecto, ejecuta:

```
build.bat
```

Esto compila y ejecuta Java, generando los datos de prueba y los resultados.

Luego, para generar los gráficos con Python:

```bash
cd src/python
python main_completo.py
```

### Opción 2: Ejecutar componentes por separado

#### Solo Java:
```
build.bat
```

#### Solo Python (requiere datos existentes en `data/input/`):
```bash
cd src/python
python main_ordenamiento.py
python main_busqueda.py
python main_completo.py
```

**Scripts adicionales disponibles:**
- `run.bat` - Ejecuta Java precompilado
- `run-ordenamiento.bat` - Solo módulo de ordenamiento Java
- `run-busqueda.bat` - Solo módulo de búsqueda Java
- `scripts/run_python_benchmarks.bat` - Ejecuta benchmarks Python

---

## Archivos Generados

### Datos de entrada (`data/input/`):
- `datos_10000.txt` - 10,000 elementos
- `datos_100000.txt` - 100,000 elementos
- `datos_1000000.txt` - 1,000,000 elementos

### Resultados (`data/output/`):
- `resultados_java.csv` y `resultados_java.json` - Tiempos Java
- `resultados_python.csv` y `resultados_python.json` - Tiempos Python
- `comparacion_python_java.json` - Comparación cruzada

### Gráficos (`docs/graficos/`):
- `comparacion_ordenamiento.png` - Rendimiento algoritmos de ordenamiento
- `comparacion_busqueda.png` - Rendimiento algoritmos de búsqueda
- `comparacion_por_tamaño.png` - Comparación por tamaño de datos

---

## Algoritmos Implementados

### Ordenamiento:

| Algoritmo | Complejidad (promedio) | Descripción |
|-----------|------------------------|-------------|
| **Shaker Sort** | O(n²) | Variante de Bubble Sort que ordena en ambas direcciones |
| **Dual-Pivot QuickSort** | O(n log n) | QuickSort optimizado con dos pivotes |
| **Heap Sort** | O(n log n) | Ordenamiento basado en montículos |
| **Merge Sort** | O(n log n) | Ordenamiento por división y fusión |
| **Radix Sort** | O(nk) | Ordenamiento por dígitos (lineal para datos enteros) |

### Búsqueda:

| Algoritmo | Complejidad | Requisito | Descripción |
|-----------|-------------|-----------|-------------|
| **Búsqueda Binaria** | O(log n) | Datos ordenados | Divide el espacio de búsqueda por la mitad |
| **Búsqueda Ternaria** | O(log₃ n) | Datos ordenados | Divide el espacio en tres partes |
| **Jump Search** | O(√n) | Datos ordenados | Salta bloques de tamaño √n |

---

## Notas Importantes

- **Generación de datos**: Los archivos de datos se generan una sola vez y se reutilizan entre ejecuciones para garantizar comparaciones consistentes.

- **Optimizaciones**: Shaker Sort se omite automáticamente para el conjunto de 1 millón de elementos debido a su complejidad O(n²), que lo hace impracticable para grandes volúmenes de datos.

- **Medición de tiempos**: Los tiempos medidos excluyen operaciones de I/O (lectura/escritura de archivos) para enfocarse únicamente en el rendimiento del algoritmo.

- **Repeticiones**: Cada algoritmo se ejecuta múltiples veces y se calcula el tiempo promedio para minimizar el ruido de medición.

- **Formato de salida**: Los resultados se guardan en CSV para análisis en Excel/similar y en JSON para integración con otros sistemas.

---

## Comparación Java vs Python

El proyecto está diseñado para comparar el rendimiento entre ambos lenguajes:

| Aspecto | Java | Python |
|---------|------|--------|
| **Compilación** | Compilado (JIT) | Interpretado |
| **Rendimiento** | Mayor velocidad de ejecución | Menor velocidad pero más flexibilidad |
| **Visualización** | No incluida | Matplotlib/Seaborn |
| **Caso de uso** | Procesamiento intensivo | Análisis y visualización |

---

## Licencia

Este proyecto es de uso educativo para el curso de Análisis de Algoritmos.

---

## Autor

Desarrollado como parte del taller de algoritmos de ordenamiento y búsqueda.
