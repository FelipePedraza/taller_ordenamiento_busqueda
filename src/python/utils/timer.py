"""
Timer - Utilidad para medición precisa de tiempos de ejecución.

Este módulo proporciona funcionalidades para medir el tiempo de
ejecución de algoritmos con alta precisión usando time.perf_counter().

Soporta:
- Medición en milisegundos (para ordenamiento)
- Medición en nanosegundos (para búsqueda)
- Context manager para medición automática
- Múltiples mediciones y promedios
- Exclusión de tiempo de I/O
"""

import time
from typing import Callable, Any, Optional, List
from dataclasses import dataclass


class TimerError(Exception):
    """Excepción personalizada para errores del Timer."""
    pass


@dataclass
class TimingResult:
    """
    Resultado de una medición de tiempo.

    Attributes:
        tiempo_ms: Tiempo en milisegundos
        tiempo_ns: Tiempo en nanosegundos
        tiempo_s: Tiempo en segundos
        repeticiones: Número de repeticiones realizadas
    """
    tiempo_ms: float
    tiempo_ns: float
    tiempo_s: float
    repeticiones: int = 1

    def __str__(self) -> str:
        """Representación legible del resultado."""
        if self.tiempo_ms >= 1:
            return f"{self.tiempo_ms:.3f} ms"
        elif self.tiempo_ns >= 1000:
            return f"{self.tiempo_ns:.2f} ns"
        else:
            return f"{self.tiempo_s:.6f} s"


class Timer:
    """
    Clase para medición precisa de tiempos de ejecución.

    Utiliza time.perf_counter() que proporciona la mayor
    precisión disponible en el sistema.

    Attributes:
        precision: Precisión de salida ('ms', 'ns', 's')
        name: Nombre identificador del timer
    """

    def __init__(self, name: str = "Timer", precision: str = "ms"):
        """
        Inicializa el Timer.

        Args:
            name: Nombre identificador
            precision: Unidad de precisión ('ms', 'ns', 's', 'auto')
        """
        self.name = name
        self.precision = precision
        self._start_time: Optional[float] = None
        self._elapsed: Optional[float] = None
        self._measurements: List[float] = []

    def start(self) -> 'Timer':
        """
        Inicia la medición del tiempo.

        Returns:
            Self para permitir encadenamiento

        Raises:
            TimerError: Si el timer ya está corriendo
        """
        if self._start_time is not None:
            raise TimerError(f"Timer '{self.name}' ya está en ejecución. "
                           f"Use stop() antes de start() nuevamente.")

        self._start_time = time.perf_counter()
        return self

    def stop(self) -> float:
        """
        Detiene la medición y retorna el tiempo transcurrido.

        Returns:
            Tiempo transcurrido en segundos

        Raises:
            TimerError: Si el timer no está corriendo
        """
        if self._start_time is None:
            raise TimerError(f"Timer '{self.name}' no está en ejecución. "
                           f"Use start() primero.")

        end_time = time.perf_counter()
        self._elapsed = end_time - self._start_time
        self._measurements.append(self._elapsed)
        self._start_time = None

        return self._elapsed

    def reset(self) -> 'Timer':
        """
        Reinicia el timer eliminando todas las mediciones.

        Returns:
            Self para permitir encadenamiento
        """
        self._start_time = None
        self._elapsed = None
        self._measurements.clear()
        return self

    @property
    def elapsed(self) -> float:
        """
        Retorna el tiempo transcurrido de la última medición.

        Returns:
            Tiempo en segundos

        Raises:
            TimerError: Si no hay mediciones disponibles
        """
        if self._elapsed is None and not self._measurements:
            raise TimerError(f"No hay mediciones disponibles en '{self.name}'")

        return self._elapsed or self._measurements[-1]

    @property
    def elapsed_ms(self) -> float:
        """Tiempo transcurrido en milisegundos."""
        return self.elapsed * 1000

    @property
    def elapsed_ns(self) -> float:
        """Tiempo transcurrido en nanosegundos."""
        return self.elapsed * 1_000_000_000

    @property
    def elapsed_us(self) -> float:
        """Tiempo transcurrido en microsegundos."""
        return self.elapsed * 1_000_000

    def get_result(self) -> TimingResult:
        """
        Obtiene el resultado de la última medición.

        Returns:
            TimingResult con el tiempo en diferentes unidades
        """
        elapsed = self.elapsed
        return TimingResult(
            tiempo_ms=elapsed * 1000,
            tiempo_ns=elapsed * 1_000_000_000,
            tiempo_s=elapsed,
            repeticiones=len(self._measurements)
        )

    def get_average(self, n: Optional[int] = None) -> TimingResult:
        """
        Calcula el promedio de las últimas n mediciones.

        Args:
            n: Cantidad de mediciones a promediar (None = todas)

        Returns:
            TimingResult con el tiempo promedio
        """
        if not self._measurements:
            raise TimerError("No hay mediciones para promediar")

        measurements = (self._measurements[-n:]
                       if n is not None
                       else self._measurements)

        avg = sum(measurements) / len(measurements)

        return TimingResult(
            tiempo_ms=avg * 1000,
            tiempo_ns=avg * 1_000_000_000,
            tiempo_s=avg,
            repeticiones=len(measurements)
        )

    def __enter__(self) -> 'Timer':
        """Context manager - inicia el timer."""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager - detiene el timer."""
        self.stop()

    def __repr__(self) -> str:
        """Representación del timer."""
        status = "corriendo" if self._start_time else "detenido"
        mediciones = len(self._measurements)
        return f"Timer(name='{self.name}', status={status}, mediciones={mediciones})"


class AlgorithmTimer:
    """
    Timer especializado para medir algoritmos.

    Proporciona métodos específicos para medir algoritmos
    de ordenamiento y búsqueda con el formato requerido.
    """

    @staticmethod
    def medir_ordenamiento(
        algoritmo: Callable[[List[Any]], List[Any]],
        datos: List[Any],
        repeticiones: int = 1
    ) -> TimingResult:
        """
        Mide el tiempo de un algoritmo de ordenamiento.

        El tiempo se reporta en milisegundos.
        Se hace copia de los datos para cada repetición.

        Args:
            algoritmo: Función de ordenamiento a medir
            datos: Lista de datos de entrada
            repeticiones: Número de veces a ejecutar

        Returns:
            TimingResult con el tiempo promedio
        """
        timer = Timer("Ordenamiento", precision="ms")
        measurements = []

        for _ in range(repeticiones):
            # Copiar datos para no modificar originales
            datos_copia = datos.copy()

            timer.start()
            algoritmo(datos_copia)
            elapsed = timer.stop()
            measurements.append(elapsed)

        # Calcular promedio
        avg_time = sum(measurements) / len(measurements)

        return TimingResult(
            tiempo_ms=avg_time * 1000,
            tiempo_ns=avg_time * 1_000_000_000,
            tiempo_s=avg_time,
            repeticiones=repeticiones
        )

    @staticmethod
    def medir_busqueda(
        algoritmo: Callable[..., Any],
        datos: List[Any],
        valor_busqueda: Any,
        repeticiones: int = 10
    ) -> TimingResult:
        """
        Mide el tiempo de un algoritmo de búsqueda.

        El tiempo se reporta en nanosegundos.
        Ejecuta múltiples repeticiones para obtener mejor precisión.

        Args:
            algoritmo: Función de búsqueda a medir
            datos: Lista de datos (debe estar ordenada)
            valor_busqueda: Valor a buscar
            repeticiones: Número de veces a ejecutar

        Returns:
            TimingResult con el tiempo promedio
        """
        timer = Timer("Busqueda", precision="ns")
        measurements = []

        # Verificar que el valor existe
        if valor_busqueda not in datos:
            raise ValueError(f"El valor {valor_busqueda} no existe en los datos")

        for _ in range(repeticiones):
            timer.start()
            resultado = algoritmo(datos, valor_busqueda)
            elapsed = timer.stop()

            # Verificar que el resultado es correcto
            if resultado is None or datos[resultado] != valor_busqueda:
                raise RuntimeError("El algoritmo de búsqueda no retornó el resultado correcto")

            measurements.append(elapsed)

        # Calcular promedio
        avg_time = sum(measurements) / len(measurements)

        return TimingResult(
            tiempo_ms=avg_time * 1000,
            tiempo_ns=avg_time * 1_000_000_000,
            tiempo_s=avg_time,
            repeticiones=repeticiones
        )

    @staticmethod
    def medir_funcion(
        funcion: Callable[..., Any],
        *args,
        repeticiones: int = 1,
        **kwargs
    ) -> TimingResult:
        """
        Mide el tiempo de cualquier función.

        Args:
            funcion: Función a medir
            *args: Argumentos posicionales
            repeticiones: Número de repeticiones
            **kwargs: Argumentos nombrados

        Returns:
            TimingResult con el tiempo promedio
        """
        timer = Timer()
        measurements = []

        for _ in range(repeticiones):
            timer.start()
            funcion(*args, **kwargs)
            elapsed = timer.stop()
            measurements.append(elapsed)

        avg_time = sum(measurements) / len(measurements)

        return TimingResult(
            tiempo_ms=avg_time * 1000,
            tiempo_ns=avg_time * 1_000_000_000,
            tiempo_s=avg_time,
            repeticiones=repeticiones
        )


# Funciones de conveniencia
def timeit(func: Callable, *args, **kwargs) -> TimingResult:
    """
    Mide el tiempo de ejecución de una función (conveniencia).

    Args:
        func: Función a medir
        *args: Argumentos posicionales
        **kwargs: Argumentos nombrados

    Returns:
        TimingResult con el tiempo
    """
    return AlgorithmTimer.medir_funcion(func, *args, **kwargs)


def timeit_ms(func: Callable, *args, **kwargs) -> float:
    """
    Mide el tiempo y retorna solo los milisegundos.

    Args:
        func: Función a medir
        *args: Argumentos posicionales
        **kwargs: Argumentos nombrados

    Returns:
        Tiempo en milisegundos
    """
    result = AlgorithmTimer.medir_funcion(func, *args, **kwargs)
    return result.tiempo_ms


def timeit_ns(func: Callable, *args, **kwargs) -> float:
    """
    Mide el tiempo y retorna solo los nanosegundos.

    Args:
        func: Función a medir
        *args: Argumentos posicionales
        **kwargs: Argumentos nombrados

    Returns:
        Tiempo en nanosegundos
    """
    result = AlgorithmTimer.medir_funcion(func, *args, **kwargs)
    return result.tiempo_ns