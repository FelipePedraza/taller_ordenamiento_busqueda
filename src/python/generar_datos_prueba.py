#!/usr/bin/env python3
"""
Generador de Datos de Prueba.

Genera archivos de datos de diferentes tamaños para el benchmark.
Crea archivos en data/input/ con números enteros aleatorios.

Uso:
    python generar_datos_prueba.py
    python generar_datos_prueba.py --min 0 --max 1000000
"""

import random
import argparse
from pathlib import Path


def generar_archivo_datos(
    filename: str,
    cantidad: int,
    min_val: int,
    max_val: int,
    output_dir: str
) -> str:
    """
    Genera un archivo con números enteros aleatorios.

    Args:
        filename: Nombre del archivo a crear
        cantidad: Cantidad de números a generar
        min_val: Valor mínimo (inclusive)
        max_val: Valor máximo (inclusive)
        output_dir: Directorio de salida

    Returns:
        Ruta completa del archivo generado
    """
    output_path = Path(output_dir) / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Generando {filename} ({cantidad:,} números)...", end=" ", flush=True)

    # Generar datos
    datos = [random.randint(min_val, max_val) for _ in range(cantidad)]

    # Escribir archivo
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"# Archivo de datos: {filename}\n")
        f.write(f"# Cantidad: {cantidad:,} elementos\n")
        f.write(f"# Rango: [{min_val}, {max_val}]\n")
        f.write(f"# Generado para el taller de algoritmos\n")
        f.write("#\n")

        for numero in datos:
            f.write(f"{numero}\n")

    print(f"OK ({output_path.stat().st_size / 1024:.1f} KB)")
    return str(output_path)


def main():
    """Función principal."""
    parser = argparse.ArgumentParser(
        description='Genera archivos de datos de prueba para el benchmark'
    )
    parser.add_argument(
        '--output', '-o',
        default='../../data/input',
        help='Directorio de salida (default: ../../data/input)'
    )
    parser.add_argument(
        '--min', type=int,
        default=0,
        help='Valor mínimo (default: 0)'
    )
    parser.add_argument(
        '--max', type=int,
        default=None,
        help='Valor máximo (default: 10 * cantidad)'
    )
    parser.add_argument(
        '--semilla', '-s', type=int,
        default=42,
        help='Semilla para reproducibilidad (default: 42)'
    )

    args = parser.parse_args()

    # Configurar semilla
    random.seed(args.semilla)

    print("=" * 60)
    print("GENERADOR DE DATOS DE PRUEBA")
    print("=" * 60)
    print(f"Directorio de salida: {args.output}")
    print(f"Semilla: {args.semilla}")
    print()

    # Definir archivos a generar
    archivos = [
        ('datos_10000.txt', 10000),
        ('datos_100000.txt', 100000),
        ('datos_1000000.txt', 1000000),
    ]

    generados = []

    for filename, cantidad in archivos:
        max_val = args.max if args.max is not None else cantidad * 10

        try:
            ruta = generar_archivo_datos(
                filename,
                cantidad,
                args.min,
                max_val,
                args.output
            )
            generados.append(ruta)
        except Exception as e:
            print(f"\nError generando {filename}: {e}")

    print()
    print("=" * 60)
    print("ARCHIVOS GENERADOS")
    print("=" * 60)
    for ruta in generados:
        print(f"  - {ruta}")
    print()

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())