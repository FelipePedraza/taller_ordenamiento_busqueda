"""
Result Exporter - Utilidad para exportar resultados de benchmarking.
"""

import csv
import json
import os
import sys
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict

# Importar BenchmarkResult del core
sys.path.insert(0, str(Path(__file__).parent.parent))
from core.models import BenchmarkResult


class ResultExporter:
    """Exporta resultados de benchmarking a diferentes formatos."""

    def __init__(self, output_dir: Optional[str] = None):
        if output_dir:
            self.output_dir = Path(output_dir)
        else:
            self.output_dir = Path("data/output")

        self.output_dir.mkdir(parents=True, exist_ok=True)

    def exportar_csv(self, resultados: List[BenchmarkResult],
                     filename: str = "resultados_python.csv") -> str:
        """Exporta resultados a CSV."""
        filepath = self.output_dir / filename

        headers = ['algoritmo', 'tipo', 'tamaño', 'tiempo_ms', 'tiempo_ns', 'timestamp']

        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)

            for r in resultados:
                writer.writerow([
                    r.algoritmo,
                    r.tipo,
                    r.tamaño,
                    f"{r.tiempo_ms:.6f}",
                    f"{r.tiempo_ns:.2f}",
                    r.timestamp or datetime.now().isoformat()
                ])

        return str(filepath)

    def exportar_json(self, resultados: List[BenchmarkResult],
                      filename: str = "resultados_python.json",
                      metadatos: Optional[Dict[str, Any]] = None) -> str:
        """Exporta resultados a JSON."""
        filepath = self.output_dir / filename

        data = {
            'lenguaje': 'Python',
            'fecha_ejecucion': datetime.now().isoformat(),
            'cantidad_resultados': len(resultados),
            'metadatos': metadatos or {},
            'resultados': [r.to_dict() for r in resultados]
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return str(filepath)

    def exportar_ambos(self, resultados: List[BenchmarkResult],
                       base_filename: str = "resultados_python",
                       metadatos: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        """Exporta a ambos formatos."""
        csv_path = self.exportar_csv(resultados, f"{base_filename}.csv")
        json_path = self.exportar_json(resultados, f"{base_filename}.json", metadatos)

        return {'csv': csv_path, 'json': json_path}

    def leer_resultados_java(self, filename: str = "resultados_java.json") -> List[Dict[str, Any]]:
        """Lee resultados exportados por Java."""
        filepath = self.output_dir / filename

        if not filepath.exists():
            raise FileNotFoundError(f"No se encontro el archivo: {filepath}")

        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if isinstance(data, dict) and 'resultados' in data:
            return data['resultados']
        return data if isinstance(data, list) else []
