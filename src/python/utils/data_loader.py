"""
Data Loader - Utilidad para cargar archivos de datos.

Este módulo proporciona funcionalidades para leer archivos de texto
con datos de entrada para los algoritmos de ordenamiento y búsqueda.

Soporta:
- Lectura de archivos con un número entero por línea
- Validación de datos
- Detección de codificación automática
- Manejo de errores robusto
"""

import os
from typing import List, Optional, Tuple
from pathlib import Path


class DataLoader:
    """
    Clase utilitaria para cargar datos desde archivos de texto.

    Attributes:
        base_path: Ruta base para los archivos de datos
    """

    def __init__(self, base_path: Optional[str] = None):
        """
        Inicializa el DataLoader.

        Args:
            base_path: Ruta base para los archivos. Si es None, usa
                      el directorio data/input/ relativo al proyecto.
        """
        if base_path:
            self.base_path = Path(base_path)
        else:
            # Determinar ruta automáticamente
            self.base_path = self._get_default_input_path()

    def _get_default_input_path(self) -> Path:
        """
        Obtiene la ruta por defecto para los archivos de entrada.

        Returns:
            Path al directorio data/input/
        """
        # Buscar desde el directorio actual o subir hasta encontrar data/input
        current = Path.cwd()

        # Intentar diferentes niveles
        for parent in [current] + list(current.parents):
            data_input = parent / "data" / "input"
            if data_input.exists():
                return data_input

        # Si no se encuentra, usar ruta relativa
        return Path("data/input")

    def load_file(self, filename: str) -> List[int]:
        """
        Carga datos desde un archivo de texto.

        El archivo debe contener un número entero por línea.

        Args:
            filename: Nombre del archivo a cargar

        Returns:
            Lista de enteros leídos del archivo

        Raises:
            FileNotFoundError: Si el archivo no existe
            ValueError: Si los datos no son válidos
            IOError: Si hay errores de lectura
        """
        filepath = self.base_path / filename

        if not filepath.exists():
            raise FileNotFoundError(
                f"Archivo no encontrado: {filepath.absolute()}"
            )

        data = []
        line_number = 0

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    line_number += 1
                    line = line.strip()

                    # Ignorar líneas vacías y comentarios
                    if not line or line.startswith('#'):
                        continue

                    try:
                        number = int(line)
                        data.append(number)
                    except ValueError as e:
                        raise ValueError(
                            f"Error en línea {line_number} de {filename}: "
                            f"'{line}' no es un entero válido"
                        ) from e

        except UnicodeDecodeError:
            # Intentar con codificación alternativa
            data = self._load_with_encoding(filepath, 'latin-1')

        except Exception as e:
            raise IOError(f"Error al leer {filename}: {str(e)}") from e

        return data

    def _load_with_encoding(self, filepath: Path, encoding: str) -> List[int]:
        """
        Carga archivo con codificación específica.

        Args:
            filepath: Ruta del archivo
            encoding: Codificación a usar

        Returns:
            Lista de enteros
        """
        data = []

        with open(filepath, 'r', encoding=encoding) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                data.append(int(line))

        return data

    def load_multiple_files(self, filenames: List[str]) -> dict:
        """
        Carga múltiples archivos y devuelve un diccionario.

        Args:
            filenames: Lista de nombres de archivos

        Returns:
            Diccionario {nombre_archivo: lista_de_datos}
        """
        result = {}
        for filename in filenames:
            try:
                result[filename] = self.load_file(filename)
            except Exception as e:
                result[filename] = []
                print(f"Advertencia: No se pudo cargar {filename}: {e}")
        return result

    def load_standard_files(self) -> dict:
        """
        Carga los archivos estándar del taller.

        Returns:
            Diccionario con los datos de cada tamaño:
            {
                '10000': [...],
                '100000': [...],
                '1000000': [...]
            }
        """
        standard_files = [
            ('datos_10000.txt', '10000'),
            ('datos_100000.txt', '100000'),
            ('datos_1000000.txt', '1000000'),
        ]

        result = {}
        for filename, size_key in standard_files:
            try:
                data = self.load_file(filename)
                result[size_key] = data
                print(f"  Cargado {filename}: {len(data)} elementos")
            except FileNotFoundError:
                print(f"  No encontrado: {filename}")
                result[size_key] = []

        return result

    def validate_data(self, data: List[int]) -> Tuple[bool, str]:
        """
        Valida que los datos sean apropiados para los algoritmos.

        Args:
            data: Lista de enteros a validar

        Returns:
            Tupla (es_valido, mensaje)
        """
        if not data:
            return False, "La lista está vacía"

        if len(data) == 0:
            return False, "La lista no contiene elementos"

        # Verificar que todos sean enteros
        if not all(isinstance(x, int) for x in data):
            return False, "La lista contiene elementos no enteros"

        # Verificar rango razonable (para Radix Sort)
        min_val = min(data)
        max_val = max(data)

        if min_val < 0:
            return (
                True,
                f"ADVERTENCIA: Contiene valores negativos "
                f"(min: {min_val}, max: {max_val}). "
                f"Radix Sort requiere versión especial."
            )

        return True, f"Datos válidos: {len(data)} elementos, rango [{min_val}, {max_val}]"

    def get_file_info(self, filename: str) -> dict:
        """
        Obtiene información sobre un archivo de datos.

        Args:
            filename: Nombre del archivo

        Returns:
            Diccionario con información del archivo
        """
        filepath = self.base_path / filename

        if not filepath.exists():
            return {'existe': False}

        try:
            data = self.load_file(filename)
            is_valid, msg = self.validate_data(data)

            return {
                'existe': True,
                'ruta': str(filepath.absolute()),
                'tamano_archivo': filepath.stat().st_size,
                'elementos': len(data),
                'minimo': min(data) if data else None,
                'maximo': max(data) if data else None,
                'datos_validos': is_valid,
                'mensaje': msg
            }
        except Exception as e:
            return {
                'existe': True,
                'ruta': str(filepath.absolute()),
                'error': str(e)
            }

    @staticmethod
    def generate_sample_data(size: int, min_val: int = 0, max_val: int = None) -> List[int]:
        """
        Genera datos de muestra para pruebas.

        Args:
            size: Cantidad de elementos
            min_val: Valor mínimo (default: 0)
            max_val: Valor máximo (default: size * 10)

        Returns:
            Lista de enteros aleatorios
        """
        import random

        if max_val is None:
            max_val = size * 10

        return [random.randint(min_val, max_val) for _ in range(size)]


# Funciones de conveniencia para uso directo
def load_data_file(filepath: str) -> List[int]:
    """
    Carga un archivo de datos directamente.

    Args:
        filepath: Ruta completa al archivo

    Returns:
        Lista de enteros
    """
    loader = DataLoader(os.path.dirname(filepath) or '.')
    return loader.load_file(os.path.basename(filepath))


def load_all_input_files(base_path: Optional[str] = None) -> dict:
    """
    Carga todos los archivos de entrada disponibles.

    Args:
        base_path: Ruta base opcional

    Returns:
        Diccionario con todos los datos cargados
    """
    loader = DataLoader(base_path)
    return loader.load_standard_files()