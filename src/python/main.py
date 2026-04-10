#!/usr/bin/env python3
"""
Main - Punto de entrada principal del benchmark de algoritmos.

Este script ejecuta benchmarks de ordenamiento y busqueda,
exporta los resultados y genera graficos comparativos.

Uso:
    python main.py
    python main.py --skip-graficos
"""

import argparse
import sys
from pathlib import Path

from core.models import BenchmarkConfig
from controllers.benchmark_controller import BenchmarkController


def main():
    """Funcion principal."""
    parser = argparse.ArgumentParser(
        description='Benchmark de algoritmos de ordenamiento y busqueda'
    )
    parser.add_argument(
        '--input', '-i',
        default=None,
        help='Directorio de entrada para datos (default: data/input)'
    )
    parser.add_argument(
        '--output', '-o',
        default='data/output',
        help='Directorio de salida para resultados (default: data/output)'
    )
    parser.add_argument(
        '--graficos', '-g',
        default='docs/graficos',
        help='Directorio de salida para graficos (default: docs/graficos)'
    )
    parser.add_argument(
        '--skip-graficos',
        action='store_true',
        help='No generar graficos'
    )

    args = parser.parse_args()

    # Configuracion
    config = BenchmarkConfig(
        input_dir=args.input,
        output_dir=args.output,
        graficos_dir=args.graficos,
        skip_graficos=args.skip_graficos
    )

    # Ejecutar benchmark
    controller = BenchmarkController(config)
    resultados = controller.ejecutar()

    # Generar graficos si se solicita
    if not config.skip_graficos:
        from visualizacion.generar_graficos import GraficadorResultados
        try:
            graficador = GraficadorResultados(config.graficos_dir)
            # Cargar resultados y generar graficos
            resultados_python, resultados_java = graficador.cargar_resultados(
                f"{config.output_dir}/resultados_python.json",
                f"{config.output_dir}/resultados_java.json"
            )
            rutas = graficador.generar_todos(resultados_python, resultados_java)
            if rutas:
                print(f"\nGraficos generados: {len(rutas)}")
        except Exception as e:
            print(f"Error generando graficos: {e}")

    print(f"\n{'=' * 60}")
    print("Benchmark completado exitosamente!")
    print(f"{'=' * 60}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
