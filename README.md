# Taller de Algoritmos de Ordenamiento y Búsqueda

Repositorio correspondiente al desarrollo del taller de análisis y comparación de algoritmos de ordenamiento, búsqueda y casos específicos.

## Descripción del proyecto

Este proyecto implementa y compara el desempeño de diferentes algoritmos en dos lenguajes de programación:

- Un lenguaje compilado
- Un lenguaje interpretado

El objetivo es medir el tiempo de ejecución de cada algoritmo, compararlo con su complejidad teórica y presentar los resultados en tablas, gráficos y archivos exportables.

El taller incluye:

1. **Análisis de algoritmos de ordenamiento**
2. **Análisis de algoritmos de búsqueda**
3. **Análisis de casos específicos**

Los datos de prueba se generan una sola vez, se almacenan en archivo de texto plano y en ejecuciones posteriores se reutilizan para asegurar que todos los algoritmos trabajen sobre el mismo conjunto de datos.

## Algoritmos implementados

### Ordenamiento
- Shaker Sort
- Dual-Pivot QuickSort
- Heap Sort
- Merge Sort
- Radix Sort

### Búsqueda
- Búsqueda Binaria
- Búsqueda Ternaria
- Búsqueda por Saltos (Jump Search)

### Casos específicos
- Ordenar números en el rango `0` a `n^2 - 1`
- Ordenar un arreglo según el orden definido por otro arreglo
- Ordenar una lista enlazada de `0s`, `1s` y `2s`

## Tamaños de prueba

Todos los algoritmos de ordenamiento y búsqueda deben probarse con:

- 10.000 elementos
- 100.000 elementos
- 1.000.000 elementos

## Requisitos de medición

Los tiempos reportados deben medir **únicamente la ejecución del algoritmo**, excluyendo:

- Lectura de archivos
- Escritura de archivos
- Generación de datos
- Exportación de resultados
- Construcción de gráficos

## Estructura del repositorio

```bash
.
├── README.md
├── docs/
│   ├── fuentes.md
│   ├── graficos/
│   └── resultados/
├── data/
│   ├── entrada/
│   └── salida/
├── src/
│   ├── compiled/
│   ├── interpreted/
│   └── common/
├── tests/
└── scripts/