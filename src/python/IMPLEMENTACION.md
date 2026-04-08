# Resumen de Implementación - Componente Python

## Estructura Completa del Proyecto

```
src/python/
├── ordenamiento/                    # 5 algoritmos de ordenamiento
│   ├── shaker_sort.py              # Shaker Sort (Cocktail Sort)
│   ├── dual_pivot_quicksort.py     # Dual-Pivot QuickSort
│   ├── heap_sort.py                # Heap Sort
│   ├── merge_sort.py               # Merge Sort
│   └── radix_sort.py               # Radix Sort (base 10)
│
├── busqueda/                        # 3 algoritmos de búsqueda
│   ├── busqueda_binaria.py         # Búsqueda Binaria
│   ├── busqueda_ternaria.py        # Búsqueda Ternaria
│   └── jump_search.py              # Jump Search
│
├── utils/                           # Utilidades del proyecto
│   ├── data_loader.py              # Carga de archivos de datos
│   ├── timer.py                    # Medición precisa de tiempos
│   └── result_exporter.py          # Exportación CSV/JSON
│
├── visualizacion/                   # Generación de gráficos
│   └── generar_graficos.py         # Gráficos comparativos
│
├── main_ordenamiento.py            # Script de ordenamiento
├── main_busqueda.py                # Script de búsqueda
├── main_completo.py                # Script principal completo
├── generar_datos_prueba.py         # Generador de datos de prueba
├── requirements.txt                # Dependencias
└── README.md                       # Documentación
```

## Algoritmos Implementados

### Ordenamiento (Punto 1)

| Algoritmo | Complejidad | Características |
|-----------|-------------|-----------------|
| **Shaker Sort** | O(n²) | Variante bidireccional de Bubble Sort |
| **Dual-Pivot QuickSort** | O(n log n) | Divide en 3 particiones con 2 pivotes |
| **Heap Sort** | O(n log n) | Usa Max-Heap, espacio O(1) |
| **Merge Sort** | O(n log n) | Divide y conquista, estable |
| **Radix Sort** | O(d×n) | Ordenamiento por dígitos base 10 |

### Búsqueda (Punto 2)

| Algoritmo | Complejidad | Características |
|-----------|-------------|-----------------|
| **Búsqueda Binaria** | O(log n) | Divide intervalo a la mitad |
| **Búsqueda Ternaria** | O(log₃ n) | Divide en 3 partes |
| **Jump Search** | O(√n) | Saltos de √n + búsqueda lineal |

## Características Técnicas

### Medición de Tiempos
- Usa `time.perf_counter()` para alta precisión
- Medición SOLO del algoritmo, excluyendo I/O
- Copias del arreglo con `.copy()` para cada prueba
- Tiempos en **ms** para ordenamiento
- Tiempos en **ns** para búsqueda

### Exportación de Resultados
- **CSV**: Formato compatible con Java
- **JSON**: Con metadatos completos
- **Comparación**: Lee automáticamente resultados de Java

### Visualización
- Gráfico de barras comparativas Java vs Python
- Colores distintivos (Azul Python, Naranja Java)
- Tiempos visibles sobre cada barra
- 3 gráficos generados automáticamente

## Ejecución

### Requisitos
```bash
pip install -r requirements.txt
```

### Ejecutar Todo
```bash
# Windows
python main_completo.py

# Con scripts
../../scripts/run_python_benchmarks.bat
```

### Opciones Disponibles
```bash
python main_completo.py --help

# Ejecutar solo pruebas
python main_completo.py --skip-graficos

# Solo generar gráficos (datos existentes)
python main_completo.py --solo-graficos

# Directorios personalizados
python main_completo.py -i data/input -o data/output -g docs/graficos
```

## Archivos de Salida

### Resultados
- `data/output/resultados_python.csv`
- `data/output/resultados_python.json`

### Gráficos
- `docs/graficos/comparacion_ordenamiento.png`
- `docs/graficos/comparacion_busqueda.png`
- `docs/graficos/comparacion_por_tamaño.png`

## Formato de Datos de Entrada

Archivos esperados en `data/input/`:
- `datos_10000.txt` (10,000 elementos)
- `datos_100000.txt` (100,000 elementos)
- `datos_1000000.txt` (1,000,000 elementos)

Formato: un número entero por línea

## Generar Datos de Prueba

```bash
python generar_datos_prueba.py
```

## Notas de Implementación

1. **Shaker Sort**: Implementado con pasadas bidireccionales
2. **Dual-Pivot QuickSort**: Usa insertion sort para subarreglos pequeños
3. **Heap Sort**: Construcción bottom-up del max-heap
4. **Merge Sort**: Implementación recursiva con merge optimizado
5. **Radix Sort**: Base 10 usando counting sort como subrutina
6. **Búsquedas**: Todas tienen versión recursiva e iterativa
7. **Timer**: Clase `TimingResult` para manejo de unidades
8. **Gráficos**: Usa matplotlib + seaborn con estilo consistente