"""
Servicio de Benchmark - Lógica de ejecución de pruebas.
"""
import random
from typing import List, Callable, Any

from ordenamiento import (
    shaker_sort,
    dual_pivot_quicksort,
    heap_sort,
    merge_sort,
    radix_sort
)
from busqueda import busqueda_binaria, busqueda_ternaria, jump_search
from utils.timer import medir_ordenamiento, medir_busqueda
from utils.data_loader import DataLoader
from .models import BenchmarkResult


class BenchmarkService:
    """Servicio que ejecuta benchmarks de algoritmos."""

    ALGORITMOS_ORDENAMIENTO = [
        ('Shaker Sort', shaker_sort),
        ('Dual-Pivot QuickSort', dual_pivot_quicksort),
        ('Heap Sort', heap_sort),
        ('Merge Sort', merge_sort),
        ('Radix Sort', radix_sort),
    ]

    ALGORITMOS_BUSQUEDA = [
        ('Busqueda Binaria', busqueda_binaria),
        ('Busqueda Ternaria', busqueda_ternaria),
        ('Jump Search', jump_search),
    ]

    def __init__(self, data_loader: DataLoader):
        self.data_loader = data_loader

    def ejecutar_ordenamiento(self) -> List[BenchmarkResult]:
        """Ejecuta benchmarks de ordenamiento."""
        resultados = []
        datos = self._cargar_datos()

        for size_key, data in sorted(datos.items(), key=lambda x: int(x[0])):
            if not data:
                continue

            for nombre, algoritmo in self.ALGORITMOS_ORDENAMIENTO:
                if nombre == 'Shaker Sort' and len(data) >= 1_000_000:
                    resultados.append(self._crear_resultado_omitido(nombre, size_key))
                    continue

                try:
                    tiempo_ms = self._medir_ordenamiento(algoritmo, data)
                    resultados.append(BenchmarkResult(
                        algoritmo=nombre,
                        tipo='ordenamiento',
                        tamaño=size_key,
                        tiempo_ms=tiempo_ms,
                        tiempo_ns=tiempo_ms * 1_000_000
                    ))
                except Exception as e:
                    resultados.append(self._crear_resultado_error(
                        nombre, size_key, 'ordenamiento', str(e)
                    ))

        return resultados

    def ejecutar_busqueda(self) -> List[BenchmarkResult]:
        """Ejecuta benchmarks de búsqueda."""
        resultados = []
        datos = self._cargar_datos()

        for size_key, data in sorted(datos.items(), key=lambda x: int(x[0])):
            if not data:
                continue

            data = sorted(data)
            target = data[len(data) // 2]

            for nombre, algoritmo in self.ALGORITMOS_BUSQUEDA:
                try:
                    resultado = algoritmo(data, target)
                    if resultado is None or data[resultado] != target:
                        raise RuntimeError("Resultado incorrecto")

                    tiempo_ns = self._medir_busqueda(algoritmo, data, target)
                    resultados.append(BenchmarkResult(
                        algoritmo=nombre,
                        tipo='busqueda',
                        tamaño=size_key,
                        tiempo_ms=tiempo_ns / 1_000_000,
                        tiempo_ns=tiempo_ns
                    ))
                except Exception as e:
                    resultados.append(self._crear_resultado_error(
                        nombre, size_key, 'busqueda', str(e)
                    ))

        return resultados

    def _cargar_datos(self) -> dict:
        """Carga datos de prueba o genera si no existen."""
        try:
            return self.data_loader.load_standard_files()
        except Exception:
            return {
                '10000': DataLoader.generate_sample_data(10000),
                '100000': DataLoader.generate_sample_data(100000),
                '1000000': DataLoader.generate_sample_data(1000000),
            }

    def _medir_ordenamiento(self, algoritmo: Callable, data: list) -> float:
        """Mide tiempo de ordenamiento en ms."""
        repeticiones = 1 if len(data) >= 100000 else 3
        return medir_ordenamiento(algoritmo, data, repeticiones)

    def _medir_busqueda(self, algoritmo: Callable, data: list, target: Any) -> float:
        """Mide tiempo de búsqueda en ns."""
        repeticiones = 10000 if len(data) < 100000 else 1000
        return medir_busqueda(algoritmo, data, target, repeticiones)

    def _crear_resultado_omitido(self, nombre: str, size_key: str) -> BenchmarkResult:
        return BenchmarkResult(
            algoritmo=nombre,
            tipo='ordenamiento',
            tamaño=size_key,
            tiempo_ms=0.0,
            tiempo_ns=0.0,
            notas='O(n^2) - omitido'
        )

    def _crear_resultado_error(self, nombre: str, size_key: str,
                                tipo: str, error: str) -> BenchmarkResult:
        return BenchmarkResult(
            algoritmo=nombre,
            tipo=tipo,
            tamaño=size_key,
            tiempo_ms=0.0,
            tiempo_ns=0.0,
            notas=f'Error: {error}'
        )
