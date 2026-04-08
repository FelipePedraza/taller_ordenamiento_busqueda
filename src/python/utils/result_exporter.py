"""
Result Exporter - Utilidad para exportar resultados de benchmarking.

Este módulo proporciona funcionalidades para exportar los resultados
de las pruebas de rendimiento a diferentes formatos (CSV, JSON).

Soporta:
- Exportación a CSV con formato compatible con Java
- Exportación a JSON con metadatos
- Lectura de resultados Java para comparación
- Formato unificado de resultados
"""

import csv
import json
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict


@dataclass
class ResultadoPrueba:
    """
    Representa el resultado de una prueba individual.

    Attributes:
        algoritmo: Nombre del algoritmo
        tipo: Tipo de prueba ('ordenamiento' o 'busqueda')
        tamaño: Tamaño de entrada (ej: '10000', '100000')
        tiempo_ms: Tiempo en milisegundos
        tiempo_ns: Tiempo en nanosegundos
        timestamp: Fecha y hora de la prueba
        notas: Notas adicionales opcionales
    """
    algoritmo: str
    tipo: str  # 'ordenamiento' | 'busqueda'
    tamaño: str  # '10000', '100000', '1000000'
    tiempo_ms: float
    tiempo_ns: float
    timestamp: Optional[str] = None
    notas: Optional[str] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()


class ResultExporter:
    """
    Clase para exportar resultados de benchmarking.

    Attributes:
        output_dir: Directorio de salida para los archivos
    """

    def __init__(self, output_dir: Optional[str] = None):
        """
        Inicializa el ResultExporter.

        Args:
            output_dir: Directorio de salida. Si es None, usa data/output/
        """
        if output_dir:
            self.output_dir = Path(output_dir)
        else:
            self.output_dir = self._get_default_output_path()

        # Crear directorio si no existe
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _get_default_output_path(self) -> Path:
        """
        Obtiene la ruta por defecto para archivos de salida.

        Returns:
            Path al directorio data/output/
        """
        current = Path.cwd()

        for parent in [current] + list(current.parents):
            data_output = parent / "data" / "output"
            if data_output.parent.exists():
                return data_output

        return Path("data/output")

    def exportar_csv(
        self,
        resultados: List[ResultadoPrueba],
        filename: str = "resultados_python.csv"
    ) -> str:
        """
        Exporta resultados a formato CSV.

        Args:
            resultados: Lista de resultados a exportar
            filename: Nombre del archivo CSV

        Returns:
            Ruta completa del archivo creado
        """
        filepath = self.output_dir / filename

        headers = ['algoritmo', 'tipo', 'tamaño', 'tiempo_ms', 'tiempo_ns', 'timestamp']

        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)

            for resultado in resultados:
                writer.writerow([
                    resultado.algoritmo,
                    resultado.tipo,
                    resultado.tamaño,
                    f"{resultado.tiempo_ms:.6f}",
                    f"{resultado.tiempo_ns:.2f}",
                    resultado.timestamp or datetime.now().isoformat()
                ])

        return str(filepath)

    def exportar_json(
        self,
        resultados: List[ResultadoPrueba],
        filename: str = "resultados_python.json",
        metadatos: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Exporta resultados a formato JSON.

        Args:
            resultados: Lista de resultados a exportar
            filename: Nombre del archivo JSON
            metadatos: Metadatos adicionales del experimento

        Returns:
            Ruta completa del archivo creado
        """
        filepath = self.output_dir / filename

        data = {
            'lenguaje': 'Python',
            'version': self._get_python_version(),
            'fecha_ejecucion': datetime.now().isoformat(),
            'cantidad_resultados': len(resultados),
            'metadatos': metadatos or {},
            'resultados': [asdict(r) for r in resultados]
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return str(filepath)

    def exportar_ambos(
        self,
        resultados: List[ResultadoPrueba],
        base_filename: str = "resultados_python",
        metadatos: Optional[Dict[str, Any]] = None
    ) -> Dict[str, str]:
        """
        Exporta resultados a ambos formatos (CSV y JSON).

        Args:
            resultados: Lista de resultados a exportar
            base_filename: Nombre base para los archivos
            metadatos: Metadatos adicionales

        Returns:
            Diccionario con rutas {'csv': ruta_csv, 'json': ruta_json}
        """
        csv_path = self.exportar_csv(resultados, f"{base_filename}.csv")
        json_path = self.exportar_json(resultados, f"{base_filename}.json", metadatos)

        return {
            'csv': csv_path,
            'json': json_path
        }

    def leer_resultados_java(
        self,
        filename: str = "resultados_java.json"
    ) -> List[Dict[str, Any]]:
        """
        Lee los resultados exportados por Java.

        Args:
            filename: Nombre del archivo JSON de Java

        Returns:
            Lista de diccionarios con resultados de Java

        Raises:
            FileNotFoundError: Si el archivo no existe
        """
        filepath = self.output_dir / filename

        if not filepath.exists():
            raise FileNotFoundError(
                f"No se encontró el archivo de resultados de Java: {filepath}"
            )

        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Si el JSON tiene estructura anidada, extraer resultados
        if isinstance(data, dict) and 'resultados' in data:
            return data['resultados']

        return data if isinstance(data, list) else []

    def combinar_resultados(
        self,
        resultados_python: List[ResultadoPrueba],
        resultados_java: List[Dict[str, Any]]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Combina resultados de Python y Java para comparación.

        Args:
            resultados_python: Resultados de Python
            resultados_java: Resultados de Java

        Returns:
            Diccionario con resultados combinados
        """
        python_data = [asdict(r) for r in resultados_python]

        for r in python_data:
            r['lenguaje'] = 'Python'

        for r in resultados_java:
            r['lenguaje'] = 'Java'

        return {
            'python': python_data,
            'java': resultados_java,
            'todos': python_data + resultados_java
        }

    def exportar_comparacion(
        self,
        resultados_python: List[ResultadoPrueba],
        resultados_java: Optional[List[Dict[str, Any]]] = None,
        filename: str = "comparacion_completa.json"
    ) -> str:
        """
        Exporta un archivo JSON con comparación Python vs Java.

        Args:
            resultados_python: Resultados de Python
            resultados_java: Resultados de Java (opcional)
            filename: Nombre del archivo de salida

        Returns:
            Ruta del archivo creado
        """
        filepath = self.output_dir / filename

        data = {
            'fecha': datetime.now().isoformat(),
            'comparacion': {
                'python': {
                    'cantidad': len(resultados_python),
                    'resultados': [asdict(r) for r in resultados_python]
                }
            }
        }

        if resultados_java:
            data['comparacion']['java'] = {
                'cantidad': len(resultados_java),
                'resultados': resultados_java
            }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return str(filepath)

    def crear_resumen(
        self,
        resultados: List[ResultadoPrueba]
    ) -> Dict[str, Any]:
        """
        Crea un resumen estadístico de los resultados.

        Args:
            resultados: Lista de resultados

        Returns:
            Diccionario con estadísticas
        """
        if not resultados:
            return {'error': 'No hay resultados para resumir'}

        # Agrupar por algoritmo
        por_algoritmo: Dict[str, List[ResultadoPrueba]] = {}
        for r in resultados:
            if r.algoritmo not in por_algoritmo:
                por_algoritmo[r.algoritmo] = []
            por_algoritmo[r.algoritmo].append(r)

        resumen = {
            'total_pruebas': len(resultados),
            'algoritmos_probados': list(por_algoritmo.keys()),
            'por_algoritmo': {},
            'por_tamaño': {}
        }

        # Estadísticas por algoritmo
        for algoritmo, pruebas in por_algoritmo.items():
            tiempos_ms = [p.tiempo_ms for p in pruebas]
            resumen['por_algoritmo'][algoritmo] = {
                'cantidad_pruebas': len(pruebas),
                'tiempo_promedio_ms': sum(tiempos_ms) / len(tiempos_ms),
                'tiempo_minimo_ms': min(tiempos_ms),
                'tiempo_maximo_ms': max(tiempos_ms)
            }

        # Agrupar por tamaño
        por_tamaño: Dict[str, List[ResultadoPrueba]] = {}
        for r in resultados:
            if r.tamaño not in por_tamaño:
                por_tamaño[r.tamaño] = []
            por_tamaño[r.tamaño].append(r)

        for tamaño, pruebas in por_tamaño.items():
            tiempos_ms = [p.tiempo_ms for p in pruebas]
            resumen['por_tamaño'][tamaño] = {
                'cantidad_algoritmos': len(pruebas),
                'tiempo_promedio_ms': sum(tiempos_ms) / len(tiempos_ms)
            }

        return resumen

    def _get_python_version(self) -> str:
        """Obtiene la versión de Python."""
        import sys
        return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"


# Funciones de conveniencia
def exportar_resultados_simple(
    resultados: List[ResultadoPrueba],
    output_dir: str = "data/output"
) -> Dict[str, str]:
    """
    Exporta resultados de forma simple (función de conveniencia).

    Args:
        resultados: Lista de resultados
        output_dir: Directorio de salida

    Returns:
        Diccionario con rutas de archivos creados
    """
    exporter = ResultExporter(output_dir)
    return exporter.exportar_ambos(resultados)


def cargar_resultados_java(output_dir: str = "data/output") -> List[Dict[str, Any]]:
    """
    Carga resultados de Java de forma simple.

    Args:
        output_dir: Directorio donde están los resultados

    Returns:
        Lista de resultados de Java
    """
    exporter = ResultExporter(output_dir)
    try:
        return exporter.leer_resultados_java()
    except FileNotFoundError:
        return []