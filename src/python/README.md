# Componente Python - Taller de Algoritmos

Este directorio contiene la implementación completa en Python de los algoritmos de ordenamiento y búsqueda para el taller.

## Estructura del Proyecto

```
src/python/
├── ordenamiento/              # Algoritmos de ordenamiento
│   ├── __init__.py
│   ├── shaker_sort.py        # Shaker/Cocktail Sort
│   ├── dual_pivot_quicksort.py  # Dual-Pivot QuickSort
│   ├── heap_sort.py          # Heap Sort
│   ├── merge_sort.py         # Merge Sort
│   └── radix_sort.py         # Radix Sort (base 10)
│
├── busqueda/                  # Algoritmos de búsqueda
│   ├── __init__.py
│   ├── busqueda_binaria.py   # Búsqueda Binaria
│   ├── busqueda_ternaria.py  # Búsqueda Ternaria
│   └── jump_search.py        # Jump Search
│
├── utils/                     # Utilidades
│   ├── __init__.py
│   ├── data_loader.py        # Carga de archivos de datos
│   ├── timer.py              # Medición de tiempos
│   └── result_exporter.py    # Exportación de resultados
│
├── visualizacion/             # Generación de gráficos
│   ├── __init__.py
│   └── generar_graficos.py   # Gráficos comparativos
│
├── main_ordenamiento.py       # Script de ordenamiento
├── main_busqueda.py           # Script de búsqueda
├── main_completo.py           # Script principal (todo)
├── requirements.txt           # Dependencias
└── README.md                  # Este archivo
```

## Requisitos

- Python 3.8+
- Dependencias: `matplotlib`, `seaborn`, `numpy`, `pandas`

## Instalación de Dependencias

```bash
pip install -r requirements.txt
```

## Ejecución

### Opción 1: Script Principal (Recomendado)
Ejecuta todo el benchmark y genera los gráficos:

```bash
# Windows
..\..\scripts\run_python_benchmarks.bat

# Linux/Mac
../../scripts/run_python_benchmarks.sh
```

O directamente:

```bash
python main_completo.py
```

### Opción 2: Ejecutar Solo Ordenamiento

```bash
python main_ordenamiento.py
```

### Opción 3: Ejecutar Solo Búsqueda

```bash
python main_busqueda.py
```

### Opción 4: Solo Generar Gráficos

```bash
python main_completo.py --solo-graficos
```

## Opciones de Línea de Comandos

```bash
python main_completo.py [opciones]

Opciones:
  -i, --input DIR       Directorio de datos (default: ../../data/input)
  -o, --output DIR      Directorio de salida (default: ../../data/output)
  -g, --graficos DIR    Directorio de gráficos (default: ../../docs/graficos)
  --skip-graficos       Solo ejecutar pruebas, no generar gráficos
  --solo-graficos       Solo generar gráficos
  -v, --verbose         Modo verbose
  -h, --help            Mostrar ayuda
```

## Algoritmos Implementados

### Ordenamiento

| Algoritmo | Complejidad Promedio | Espacio | Estable |
|-----------|---------------------|---------|---------|
| Shaker Sort | O(n²) | O(1) | Sí |
| Dual-Pivot QuickSort | O(n log n) | O(log n) | No |
| Heap Sort | O(n log n) | O(1) | No |
| Merge Sort | O(n log n) | O(n) | Sí |
| Radix Sort | O(d×n) | O(n+k) | Sí |

### Búsqueda

| Algoritmo | Complejidad | Requisito |
|-----------|-------------|-----------|
| Búsqueda Binaria | O(log n) | Arreglo ordenado |
| Búsqueda Ternaria | O(log₃ n) | Arreglo ordenado |
| Jump Search | O(√n) | Arreglo ordenado |

## Salida de Resultados

Los resultados se guardan en:

- `data/output/resultados_python.csv` - Formato CSV
- `data/output/resultados_python.json` - Formato JSON con metadatos
- `docs/graficos/` - Gráficos comparativos:
  - `comparacion_ordenamiento.png`
  - `comparacion_busqueda.png`
  - `comparacion_por_tamaño.png`

## Formato de Datos de Entrada

Los archivos en `data/input/` deben contener un número entero por línea:

```
12345
67890
...
```

Archivos esperados:
- `datos_10000.txt` - 10,000 elementos
- `datos_100000.txt` - 100,000 elementos
- `datos_1000000.txt` - 1,000,000 elementos

## Notas de Implementación

1. **Medición de tiempos**: Se usa `time.perf_counter()` para alta precisión
2. **Copias de datos**: Se hace `.copy()` del arreglo para cada prueba
3. **Búsqueda**: El arreglo se ordena previamente; se busca el elemento medio
4. **Radix Sort**: Implementación base 10 con Counting Sort como subrutina
5. **Dual-Pivot QuickSort**: Divide en 3 particiones usando 2 pivotes

## Integración con Java

El componente Python lee automáticamente los resultados de Java desde
`data/output/resultados_java.json` para generar gráficos comparativos.

El formato JSON es compatible:
```json
{
  "resultados": [
    {
      "algoritmo": "nombre",
      "tipo": "ordenamiento|busqueda",
      "tamaño": "10000",
      "tiempo_ms": 123.456,
      "tiempo_ns": 123456789.0
    }
  ]
}
```