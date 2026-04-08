#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
# Forzar UTF-8 para stdout/stderr en Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

"""
Main Completo - Script principal del taller de algoritmos.

Este script ejecuta todas las pruebas de ordenamiento y búsqueda,
exporta los resultados y genera los gráficos comparativos.

Uso:
    python main_completo.py
    python main_completo.py --skip-graficos  # Solo ejecutar pruebas
    python main_completo.py --solo-graficos  # Solo generar gráficos

Este es el punto de entrada principal para el componente Python del taller.
"""

import argparse
from pathlib import Path

# Asegurar que el directorio src/python esté en el path
script_dir = Path(__file__).parent
if str(script_dir) not in sys.path:
    sys.path.insert(0, str(script_dir))

# Importar módulos del proyecto
from main_ordenamiento import run_ordenamiento_benchmark
from main_busqueda import run_busqueda_benchmark
from visualizacion.generar_graficos import GraficadorResultados
from utils.data_loader import DataLoader
from utils.result_exporter import ResultExporter


def ejecutar_pruebas_completas(
    data_loader: DataLoader,
    result_exporter: ResultExporter
) -> list:
    """
    Ejecuta todas las pruebas de ordenamiento y búsqueda.

    Args:
        data_loader: Instancia de DataLoader
        result_exporter: Instancia de ResultExporter

    Returns:
        Lista completa de resultados
    """
    resultados_totales = []

    # Ejecutar pruebas de ordenamiento
    print("\n" + "=" * 70)
    print("EJECUTANDO PRUEBAS DE ORDENAMIENTO")
    print("=" * 70)
    resultados_ordenamiento = run_ordenamiento_benchmark(data_loader, result_exporter)
    resultados_totales.extend(resultados_ordenamiento)

    # Ejecutar pruebas de búsqueda
    print("\n" + "=" * 70)
    print("EJECUTANDO PRUEBAS DE BÚSQUEDA")
    print("=" * 70)
    resultados_busqueda = run_busqueda_benchmark(data_loader, result_exporter)
    resultados_totales.extend(resultados_busqueda)

    return resultados_totales


def exportar_resultados_combinados(
    resultados: list,
    result_exporter: ResultExporter
) -> dict:
    """
    Exporta los resultados en múltiples formatos.

    Args:
        resultados: Lista de resultados de pruebas
        result_exporter: Instancia de ResultExporter

    Returns:
        Diccionario con rutas de archivos exportados
    """
    print("\n" + "=" * 70)
    print("EXPORTANDO RESULTADOS")
    print("=" * 70)

    try:
        # Exportar a CSV
        csv_path = result_exporter.exportar_csv(
            resultados, "resultados_python.csv"
        )
        print(f"[OK] CSV: {csv_path}")

        # Exportar a JSON
        json_path = result_exporter.exportar_json(
            resultados, "resultados_python.json",
            metadatos={
                'descripcion': 'Resultados completos del benchmark Python',
                'algoritmos_ordenamiento': ['Shaker Sort', 'Dual-Pivot QuickSort',
                                            'Heap Sort', 'Merge Sort', 'Radix Sort'],
                'algoritmos_busqueda': ['Busqueda Binaria', 'Busqueda Ternaria',
                                       'Jump Search']
            }
        )
        print(f"[OK] JSON: {json_path}")

        # Intentar crear comparación con Java si existe
        try:
            resultados_java = result_exporter.leer_resultados_java()
            comparacion_path = result_exporter.exportar_comparacion(
                resultados, resultados_java, "comparacion_python_java.json"
            )
            print(f"[OK] Comparación: {comparacion_path}")
        except FileNotFoundError:
            print("[INFO] No se encontraron resultados de Java para comparación")

        # Crear resumen
        resumen = result_exporter.crear_resumen(resultados)
        print("\nResumen estadístico:")
        print(f"  - Total pruebas: {resumen.get('total_pruebas', 0)}")
        print(f"  - Algoritmos: {', '.join(resumen.get('algoritmos_probados', []))}")

        return {
            'csv': csv_path,
            'json': json_path
        }

    except Exception as e:
        print(f"[ERROR] Error exportando resultados: {e}")
        return {}


def generar_visualizaciones(
    graficos_dir: str = "docs/graficos",
    output_dir: str = "data/output"
) -> list:
    """
    Genera todos los gráficos comparativos.

    Args:
        graficos_dir: Directorio para guardar gráficos
        output_dir: Directorio con resultados

    Returns:
        Lista de rutas de gráficos generados
    """
    print("\n" + "=" * 70)
    print("GENERANDO GRÁFICOS COMPARATIVOS")
    print("=" * 70)

    try:
        graficador = GraficadorResultados(graficos_dir)

        # Cargar resultados
        resultados_python, resultados_java = graficador.cargar_resultados(
            f"{output_dir}/resultados_python.json",
            f"{output_dir}/resultados_java.json"
        )

        # Generar todos los gráficos
        rutas = graficador.generar_todos(resultados_python, resultados_java)

        if rutas:
            print("\nGráficos generados:")
            for ruta in rutas:
                print(f"  - {ruta}")
        else:
            print("\n[!] No se generaron gráficos (verificar datos disponibles)")

        return rutas

    except Exception as e:
        print(f"[ERROR] Error generando gráficos: {e}")
        import traceback
        traceback.print_exc()
        return []


def mostrar_resumen_final(resultados: list) -> None:
    """
    Muestra un resumen final de todas las pruebas.

    Args:
        resultados: Lista de resultados de pruebas
    """
    if not resultados:
        print("\n[!] No hay resultados para mostrar")
        return

    print("\n" + "=" * 70)
    print("RESUMEN FINAL DEL BENCHMARK")
    print("=" * 70)

    # Separar por tipo
    ordenamiento = [r for r in resultados if r.tipo == 'ordenamiento']
    busqueda = [r for r in resultados if r.tipo == 'busqueda']

    # Ordenamiento
    if ordenamiento:
        print("\n📊 ORDENAMIENTO (tiempos en ms):")
        por_tamaño = {}
        for r in ordenamiento:
            if r.tamaño not in por_tamaño:
                por_tamaño[r.tamaño] = []
            por_tamaño[r.tamaño].append(r)

        for tamaño in sorted(por_tamaño.keys(), key=lambda x: int(x)):
            print(f"\n  Tamaño {int(tamaño):,}:")
            for r in sorted(por_tamaño[tamaño], key=lambda x: x.tiempo_ms):
                print(f"    {r.algoritmo:25s}: {r.tiempo_ms:10.2f} ms")

    # Búsqueda
    if busqueda:
        print("\n🔍 BÚSQUEDA (tiempos en ns):")
        por_tamaño = {}
        for r in busqueda:
            if r.tamaño not in por_tamaño:
                por_tamaño[r.tamaño] = []
            por_tamaño[r.tamaño].append(r)

        for tamaño in sorted(por_tamaño.keys(), key=lambda x: int(x)):
            print(f"\n  Tamaño {int(tamaño):,}:")
            for r in sorted(por_tamaño[tamaño], key=lambda x: x.tiempo_ns):
                if r.tiempo_ns < 1000:
                    print(f"    {r.algoritmo:25s}: {r.tiempo_ns:10.1f} ns")
                else:
                    print(f"    {r.algoritmo:25s}: {r.tiempo_ns/1000:10.2f} μs")

    print("\n" + "=" * 70)
    print("✅ Benchmark completado exitosamente!")
    print("=" * 70)


def main():
    """Función principal del script."""
    parser = argparse.ArgumentParser(
        description='Benchmark completo de algoritmos de ordenamiento y búsqueda',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python main_completo.py
    Ejecuta todo el benchmark y genera gráficos

  python main_completo.py --skip-graficos
    Solo ejecuta las pruebas sin generar gráficos

  python main_completo.py --solo-graficos
    Solo genera gráficos usando resultados existentes

  python main_completo.py -i data/input -o data/output -g docs/graficos
    Usa directorios personalizados
        """
    )

    parser.add_argument(
        '--input', '-i',
        default=None,
        help='Directorio de entrada para archivos de datos (default: data/input)'
    )
    parser.add_argument(
        '--output', '-o',
        default='data/output',
        help='Directorio de salida para resultados (default: data/output)'
    )
    parser.add_argument(
        '--graficos', '-g',
        default='docs/graficos',
        help='Directorio de salida para gráficos (default: docs/graficos)'
    )
    parser.add_argument(
        '--skip-graficos',
        action='store_true',
        help='No generar gráficos, solo ejecutar pruebas'
    )
    parser.add_argument(
        '--solo-graficos',
        action='store_true',
        help='Solo generar gráficos, no ejecutar pruebas'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Mostrar información detallada'
    )

    args = parser.parse_args()

    print("\n" + "=" * 70)
    print("||" + " " * 66 + "||")
    print("||" + "  TALLER: ALGORITMOS DE ORDENAMIENTO Y BUSQUEDA - PYTHON".center(66) + "||")
    print("||" + " " * 66 + "||")
    print("=" * 70)

    # Solo generar gráficos
    if args.solo_graficos:
        generar_visualizaciones(args.graficos, args.output)
        return 0

    # Configurar instancias
    data_loader = DataLoader(args.input)
    result_exporter = ResultExporter(args.output)

    # Ejecutar pruebas
    resultados = ejecutar_pruebas_completas(data_loader, result_exporter)

    # Exportar resultados
    exportar_resultados_combinados(resultados, result_exporter)

    # Generar gráficos (si no se solicita saltar)
    if not args.skip_graficos:
        generar_visualizaciones(args.graficos, args.output)

    # Mostrar resumen final
    mostrar_resumen_final(resultados)

    return 0


if __name__ == "__main__":
    sys.exit(main())