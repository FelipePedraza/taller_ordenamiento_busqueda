#!/usr/bin/env python3
"""
Main Ordenamiento - Script para ejecutar pruebas de algoritmos de ordenamiento.

Este script ejecuta todos los algoritmos de ordenamiento implementados
sobre los datasets de diferentes tamanos y exporta los resultados.

Algoritmos probados:
- Shaker Sort (Cocktail Sort)
- Dual-Pivot QuickSort
- Heap Sort
- Merge Sort
- Radix Sort
"""

import sys
import argparse
from pathlib import Path

# Asegurar que el directorio src/python este en el path
script_dir = Path(__file__).parent
if str(script_dir) not in sys.path:
    sys.path.insert(0, str(script_dir))

from ordenamiento import (
    shaker_sort,
    dual_pivot_quicksort,
    heap_sort,
    merge_sort,
    radix_sort
)
from utils.data_loader import DataLoader
from utils.timer import medir_ordenamiento
from utils.result_exporter import ResultExporter, ResultadoPrueba


def run_ordenamiento_benchmark(
    data_loader: DataLoader,
    result_exporter: ResultExporter
) -> list:
    """
    Ejecuta el benchmark de todos los algoritmos de ordenamiento.

    Args:
        data_loader: Instancia de DataLoader para cargar datos
        result_exporter: Instancia de ResultExporter para guardar resultados

    Returns:
        Lista de resultados de las pruebas
    """
    resultados = []

    # Cargar datos de prueba
    print("=" * 60)
    print("BENCHMARK DE ALGORITMOS DE ORDENAMIENTO")
    print("=" * 60)
    print("\nCargando archivos de datos...")

    try:
        datos = data_loader.load_standard_files()
    except Exception as e:
        print(f"Error cargando datos: {e}")
        print("Generando datos de prueba...")
        datos = {
            '10000': DataLoader.generate_sample_data(10000),
            '100000': DataLoader.generate_sample_data(100000),
            '1000000': DataLoader.generate_sample_data(1000000),
        }

    # Definir algoritmos a probar
    algoritmos = [
        ('Shaker Sort', shaker_sort),
        ('Dual-Pivot QuickSort', dual_pivot_quicksort),
        ('Heap Sort', heap_sort),
        ('Merge Sort', merge_sort),
        ('Radix Sort', radix_sort),
    ]

    # Ejecutar pruebas
    for size_key, data in sorted(datos.items(), key=lambda x: int(x[0])):
        if not data:
            print(f"\n[!] No hay datos para tamano {size_key}, saltando...")
            continue

        print(f"\n{'-' * 60}")
        print(f"Tamano de entrada: {len(data):,} elementos")
        print(f"{'-' * 60}")

        for nombre, algoritmo in algoritmos:
            # Omitir Shaker Sort para n=1,000,000 por ser O(n^2)
            if nombre == 'Shaker Sort' and len(data) >= 1_000_000:
                print(f"  {nombre:20s}: [O(n^2) - omitido]")
                continue

            print(f"  Probando {nombre}...", end=" ", flush=True)

            try:
                # Medir tiempo (una sola ejecucion para datos grandes)
                repeticiones = 1 if len(data) >= 100000 else 3

                tiempo_ms = medir_ordenamiento(
                    algoritmo, data, repeticiones=repeticiones
                )

                # Crear resultado
                resultado = ResultadoPrueba(
                    algoritmo=nombre,
                    tipo='ordenamiento',
                    tamaño=size_key,
                    tiempo_ms=tiempo_ms,
                    tiempo_ns=tiempo_ms * 1_000_000
                )
                resultados.append(resultado)

                print(f"{tiempo_ms:.2f} ms")

            except Exception as e:
                print(f"ERROR: {e}")
                resultados.append(ResultadoPrueba(
                    algoritmo=nombre,
                    tipo='ordenamiento',
                    tamaño=size_key,
                    tiempo_ms=0.0,
                    tiempo_ns=0.0,
                    notas=f"Error: {str(e)}"
                ))

    return resultados


def main():
    """Funcion principal del script."""
    parser = argparse.ArgumentParser(
        description='Benchmark de algoritmos de ordenamiento'
    )
    parser.add_argument(
        '--output', '-o',
        default='data/output',
        help='Directorio de salida para resultados (default: data/output)'
    )
    parser.add_argument(
        '--input', '-i',
        default=None,
        help='Directorio de entrada para archivos de datos (default: data/input)'
    )

    args = parser.parse_args()

    # Crear instancias
    data_loader = DataLoader(args.input)
    result_exporter = ResultExporter(args.output)

    # Ejecutar benchmark
    resultados = run_ordenamiento_benchmark(data_loader, result_exporter)

    # Exportar resultados
    print(f"\n{'=' * 60}")
    print("EXPORTANDO RESULTADOS")
    print(f"{'=' * 60}")

    try:
        paths = result_exporter.exportar_ambos(resultados, base_filename="resultados_python_ordenamiento")
        print(f"CSV: {paths['csv']}")
        print(f"JSON: {paths['json']}")
    except Exception as e:
        print(f"Error exportando: {e}")

    # Mostrar resumen
    print(f"\n{'=' * 60}")
    print("RESUMEN DE RESULTADOS")
    print(f"{'=' * 60}")

    # Agrupar por tamano
    por_tamano = {}
    for r in resultados:
        if r.tamaño not in por_tamano:
            por_tamano[r.tamaño] = []
        por_tamano[r.tamaño].append(r)

    for tamano in sorted(por_tamano.keys(), key=lambda x: int(x)):
        print(f"\nTamano: {int(tamano):,} elementos")
        for r in sorted(por_tamano[tamano], key=lambda x: x.tiempo_ms):
            print(f"  {r.algoritmo:25s}: {r.tiempo_ms:10.2f} ms")

    print(f"\n{'=' * 60}")
    print("Benchmark completado exitosamente!")
    print(f"{'=' * 60}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
