"""
Servicio de Benchmark - Lógica de ejecución de pruebas.
"""
from typing import List, Callable, Any, Dict

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

        # Tiempos reales de Shaker Sort por tamaño, para la estimación cuadrática
        shaker_tiempos: Dict[int, float] = {}

        for size_key, data in sorted(datos.items(), key=lambda x: int(x[0])):
            if not data:
                continue

            size = len(data)

            for nombre, algoritmo in self.ALGORITMOS_ORDENAMIENTO:
                if nombre == 'Shaker Sort' and size >= 1_000_000:
                    # Estimar tiempo usando regresión cuadrática O(n²)
                    tiempo_ms = self._estimar_tiempo_shaker(shaker_tiempos, size)
                    resultados.append(BenchmarkResult(
                        algoritmo=nombre,
                        tipo='ordenamiento',
                        tamaño=size_key,
                        tiempo_ms=tiempo_ms,
                        tiempo_ns=tiempo_ms * 1_000_000,
                        notas='~estimado O(n²)'
                    ))
                    continue

                try:
                    tiempo_ms = self._medir_ordenamiento(algoritmo, data)

                    # Guardar tiempo real de Shaker Sort para usar en la estimación
                    if nombre == 'Shaker Sort':
                        shaker_tiempos[size] = tiempo_ms

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

    def _estimar_tiempo_shaker(self, tiempos_conocidos: Dict[int, float], target_size: int) -> float:
        """
        Estima el tiempo de Shaker Sort para un tamaño objetivo usando regresión O(n²).
        Ajusta la constante C promediando C_i = t_i / n_i² de los puntos conocidos
        y luego calcula t(n) = C_promedio * n².

        Args:
            tiempos_conocidos: Diccionario {tamaño: tiempo_ms} de mediciones reales
            target_size:       Tamaño objetivo a estimar

        Returns:
            Tiempo estimado en milisegundos
        """
        if not tiempos_conocidos:
            return 0.0

        # Calcular la constante C = t / n² para cada punto medido y promediarla
        c_valores = [t / (n ** 2) for n, t in tiempos_conocidos.items()]
        c_promedio = sum(c_valores) / len(c_valores)

        return c_promedio * (target_size ** 2)

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