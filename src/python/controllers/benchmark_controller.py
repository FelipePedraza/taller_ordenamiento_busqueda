"""
Benchmark Controller - Orquesta la ejecución de benchmarks.
"""
import sys
from pathlib import Path
from typing import List

# Asegurar que src/python esté en el path
script_dir = Path(__file__).parent.parent
if str(script_dir) not in sys.path:
    sys.path.insert(0, str(script_dir))

from core.models import BenchmarkResult, BenchmarkConfig
from core.benchmark_service import BenchmarkService
from utils.data_loader import DataLoader
from utils.result_exporter import ResultExporter


class BenchmarkController:
    """Controlador que orquesta los benchmarks."""

    def __init__(self, config: BenchmarkConfig):
        self.config = config
        self.data_loader = DataLoader(config.input_dir)
        self.result_exporter = ResultExporter(config.output_dir)
        self.benchmark_service = BenchmarkService(self.data_loader)

    def ejecutar(self) -> List[BenchmarkResult]:
        """Ejecuta todos los benchmarks."""
        print("=" * 60)
        print("BENCHMARK DE ALGORITMOS DE ORDENAMIENTO Y BUSQUEDA")
        print("=" * 60)

        # Ejecutar ordenamiento
        print("\n[1/2] Ejecutando benchmarks de ordenamiento...")
        resultados_ordenamiento = self.benchmark_service.ejecutar_ordenamiento()
        self._mostrar_resumen_ordenamiento(resultados_ordenamiento)

        # Ejecutar búsqueda
        print("\n[2/2] Ejecutando benchmarks de búsqueda...")
        resultados_busqueda = self.benchmark_service.ejecutar_busqueda()
        self._mostrar_resumen_busqueda(resultados_busqueda)

        # Combinar resultados
        resultados_totales = resultados_ordenamiento + resultados_busqueda

        # Exportar
        self._exportar_resultados(resultados_totales)

        return resultados_totales

    @staticmethod
    def _es_estimado(notas: str) -> bool:
        """Indica si una nota corresponde a un resultado estimado. Las notas de estimacion comienzan con '~'."""
        return notas is not None and notas.startswith('~')

    def _mostrar_resumen_ordenamiento(self, resultados: List[BenchmarkResult]):
        """Muestra resumen de ordenamiento."""
        print(f"\n{'-' * 60}")
        print("Resumen de Ordenamiento (tiempos en ms):")
        print(f"{'-' * 60}")

        por_tamano = {}
        for r in resultados:
            if r.tamaño not in por_tamano:
                por_tamano[r.tamaño] = []
            por_tamano[r.tamaño].append(r)

        for tamano in sorted(por_tamano.keys(), key=lambda x: int(x)):
            print(f"\nTamano {int(tamano):,}:")
            for r in sorted(por_tamano[tamano], key=lambda x: x.tiempo_ms):
                if self._es_estimado(r.notas):
                    # Resultado estimado: mostrar tiempo junto con la nota aclaratoria
                    print(f"  {r.algoritmo:25s}: {r.tiempo_ms:10.2f} ms  [{r.notas}]")
                elif r.notas:
                    # Resultado descartado por otra razon (errores, etc.)
                    print(f"  {r.algoritmo:25s}: {r.notas}")
                else:
                    print(f"  {r.algoritmo:25s}: {r.tiempo_ms:10.2f} ms")

    def _mostrar_resumen_busqueda(self, resultados: List[BenchmarkResult]):
        """Muestra resumen de búsqueda."""
        print(f"\n{'-' * 60}")
        print("Resumen de Busqueda (tiempos en ns):")
        print(f"{'-' * 60}")

        por_tamano = {}
        for r in resultados:
            if r.tamaño not in por_tamano:
                por_tamano[r.tamaño] = []
            por_tamano[r.tamaño].append(r)

        for tamano in sorted(por_tamano.keys(), key=lambda x: int(x)):
            print(f"\nTamano {int(tamano):,}:")
            for r in sorted(por_tamano[tamano], key=lambda x: x.tiempo_ns):
                if r.notas:
                    print(f"  {r.algoritmo:25s}: {r.notas}")
                elif r.tiempo_ns < 1000:
                    print(f"  {r.algoritmo:25s}: {r.tiempo_ns:10.1f} ns")
                else:
                    print(f"  {r.algoritmo:25s}: {r.tiempo_ns/1000:10.2f} us")

    def _exportar_resultados(self, resultados: List[BenchmarkResult]):
        """Exporta resultados a CSV y JSON. Incluye resultados medidos y estimados."""
        print(f"\n{'=' * 60}")
        print("EXPORTANDO RESULTADOS")
        print(f"{'=' * 60}")

        try:
            paths = self.result_exporter.exportar_ambos(
                resultados, base_filename="resultados_python"
            )
            print(f"CSV: {paths['csv']}")
            print(f"JSON: {paths['json']}")
        except Exception as e:
            print(f"Error exportando: {e}")