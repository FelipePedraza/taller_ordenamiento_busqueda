"""
Modelos de datos para los benchmarks.
"""
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional


@dataclass
class BenchmarkResult:
    """Representa el resultado de una prueba individual."""
    algoritmo: str
    tipo: str  # 'ordenamiento' | 'busqueda'
    tamaño: str
    tiempo_ms: float
    tiempo_ns: float
    timestamp: Optional[str] = None
    notas: Optional[str] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()

    def to_dict(self):
        return asdict(self)


@dataclass
class BenchmarkConfig:
    """Configuración para un benchmark."""
    input_dir: Optional[str]
    output_dir: str
    graficos_dir: str
    skip_graficos: bool = False
