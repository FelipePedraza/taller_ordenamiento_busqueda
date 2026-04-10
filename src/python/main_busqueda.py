#!/usr/bin/env python3
"""
Main Busqueda - Script para ejecutar pruebas de algoritmos de busqueda.

Este script ejecuta todos los algoritmos de busqueda implementados
sobre los datasets ordenados de diferentes tamanos.

Algoritmos probados:
- Busqueda Binaria
- Busqueda Ternaria
- Jump Search

Nota: Los arreglos deben estar ordenados para estos algoritmos.
Se busca el elemento en la posicion media del arreglo.
"""

import sys
import argparse
from pathlib import Path

# Asegurar que el directorio src/python este en el path
script_dir = Path(__file__).parent
if str(script_dir) not in sys.path:
    sys.path.insert(0, str(script_dir))

from busqueda import busqueda_binaria, busqueda_ternaria, jump_search
from utils.data_loader import DataLoader
from utils.timer import medir_busqueda
from utils.result_exporter import ResultExporter, ResultadoPrueba


def run_busqueda_benchmark(
    data_loader: DataLoader,
    result_exporter: ResultExporter
) -> list:
    """
    Ejecuta el benchmark de todos los algoritmos de busqueda.

    Args:
        data_loader: Instancia de DataLoader para cargar datos
        result_exporter: Instancia de ResultExporter para guardar resultados

    Returns:
        Lista de resultados de las pruebas
    """
    resultados = []

    # Cargar datos de prueba
    print("=" * 60)
    print("BENCHMARK DE ALGORITMOS DE BUSQUEDA")
    print("=" * 60)
    print("\nCargando archivos de datos...")

    try:
        datos = data_loader.load_standard_files()
    except Exception as e:
        print(f"Error cargando datos: {e}")
        print("Generando datos de prueba ordenados...")
        import random
        datos = {
            '10000': sorted([random.randint(0, 100000) for _ in range(10000)]),
            '100000': sorted([random.randint(0, 1000000) for _ in range(100000)]),
            '1000000': sorted([random.randint(0, 10000000) for _ in range(1000000)]),
        }

    # Definir algoritmos a probar
    algoritmos = [
        ('Busqueda Binaria', busqueda_binaria),
        ('Busqueda Ternaria', busqueda_ternaria),
        ('Jump Search', jump_search),
    ]

    # Ejecutar pruebas
    for size_key, data in sorted(datos.items(), key=lambda x: int(x[0])):
        if not data:
            print(f"\n[!] No hay datos para tamano {size_key}, saltando...")
            continue

        # Asegurar que los datos esten ordenados
        if data != sorted(data):
            print(f"\n  Ordenando datos para busqueda...")
            data = sorted(data)

        # Buscar elemento en la posicion media
        target_index = len(data) // 2
        target_value = data[target_index]

        print(f"\n{'-' * 60}")
        print(f"Tamano de entrada: {len(data):,} elementos")
        print(f"Valor a buscar: {target_value} (indice {target_index})")
        print(f"{'-' * 60}")

        for nombre, algoritmo in algoritmos:
            print(f"  Probando {nombre}...", end=" ", flush=True)

            try:
                # Verificar que el algoritmo funciona correctamente
                resultado = algoritmo(data, target_value)
                if resultado is None or data[resultado] != target_value:
                    raise RuntimeError(f"Resultado incorrecto: indice {resultado}")

                # Medir tiempo (mas repeticiones para busqueda por ser muy rapida)
                repeticiones = 10000 if len(data) < 100000 else 1000

                tiempo_ns = medir_busqueda(
                    algoritmo, data, target_value, repeticiones=repeticiones
                )

                # Crear resultado
                resultado_prueba = ResultadoPrueba(
                    algoritmo=nombre,
                    tipo='busqueda',
                    tamaño=size_key,
                    tiempo_ms=tiempo_ns / 1_000_000,
                    tiempo_ns=tiempo_ns
                )
                resultados.append(resultado_prueba)

                # Mostrar tiempo en unidades apropiadas
                if tiempo_ns < 1000:
                    print(f"{tiempo_ns:.1f} ns")
                else:
                    print(f"{tiempo_ns/1000:.2f} μs")

            except Exception as e:
                print(f"ERROR: {e}")
                resultados.append(ResultadoPrueba(
                    algoritmo=nombre,
                    tipo='busqueda',
                    tamaño=size_key,
                    tiempo_ms=0.0,
                    tiempo_ns=0.0,
                    notas=f"Error: {str(e)}"
                ))

    return resultados


def main():
    """Funcion principal del script."""
    parser = argparse.ArgumentParser(
        description='Benchmark de algoritmos de busqueda'
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
    resultados = run_busqueda_benchmark(data_loader, result_exporter)

    # Exportar resultados
    print(f"\n{'=' * 60}")
    print("EXPORTANDO RESULTADOS")
    print(f"{'=' * 60}")

    try:
        paths = result_exporter.exportar_ambos(resultados, base_filename="resultados_python_busqueda")
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
        for r in sorted(por_tamano[tamano], key=lambda x: x.tiempo_ns):
            if r.tiempo_ns < 1000:
                print(f"  {r.algoritmo:25s}: {r.tiempo_ns:10.1f} ns")
            else:
                print(f"  {r.algoritmo:25s}: {r.tiempo_ns/1000:10.2f} μs")

    print(f"\n{'=' * 60}")
    print("Benchmark completado exitosamente!")
    print(f"{'=' * 60}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
