"""
Módulo de algoritmos de búsqueda.
"""

from .busqueda_binaria import busqueda_binaria
from .busqueda_ternaria import busqueda_ternaria
from .jump_search import jump_search

__all__ = [
    'busqueda_binaria',
    'busqueda_ternaria',
    'jump_search',
]