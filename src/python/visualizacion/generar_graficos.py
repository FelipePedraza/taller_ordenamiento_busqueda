"""
Generador de Gráficos - Visualización de resultados de benchmarking.

Este módulo genera gráficos comparativos usando matplotlib y seaborn
para visualizar los resultados de los algoritmos de ordenamiento y búsqueda.

Gráficos generados:
1. Comparación Java vs Python - Ordenamiento
2. Comparación Java vs Python - Búsqueda
3. Gráficos por tamaño de entrada

Características:
- Colores distintivos por lenguaje
- Etiquetas sobre cada barra
- Buena legibilidad y formato
- Exportación en alta calidad
"""

import json
import matplotlib
matplotlib.use('Agg')  # Usar backend no interactivo

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import pandas as pd


class GraficadorResultados:
    """
    Clase para generar gráficos comparativos de resultados.

    Attributes:
        output_dir: Directorio donde se guardarán los gráficos
        style: Estilo de seaborn/matplotlib a usar
    """

    # Paleta de colores distintiva
    COLORES = {
        'python': '#3776ab',      # Azul Python
        'java': '#e76f00',        # Naranja Java
        'python_light': '#6fa8dc',
        'java_light': '#f4a261',
    }

    # Configuración de estilos
    ESTILO_CONFIG = {
        'figure.figsize': (14, 8),
        'axes.titlesize': 14,
        'axes.labelsize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 11,
    }

    def __init__(self, output_dir: str = "docs/graficos"):
        """
        Inicializa el graficador.

        Args:
            output_dir: Directorio de salida para los gráficos
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Configurar estilo
        plt.style.use('seaborn-v0_8-whitegrid')
        plt.rcParams.update(self.ESTILO_CONFIG)

    def cargar_resultados(
        self,
        python_json: str = "data/output/resultados_python.json",
        java_json: str = "data/output/resultados_java.json"
    ) -> Tuple[List[Dict], List[Dict]]:
        """
        Carga resultados de Python y Java.

        Args:
            python_json: Ruta al JSON de Python
            java_json: Ruta al JSON de Java

        Returns:
            Tupla (resultados_python, resultados_java)
        """
        resultados_python = []
        resultados_java = []

        # Cargar Python
        try:
            with open(python_json, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if 'resultados' in data:
                    resultados_python = data['resultados']
                else:
                    resultados_python = data if isinstance(data, list) else []
            print(f"Cargados {len(resultados_python)} resultados de Python")
        except FileNotFoundError:
            print(f"No se encontró {python_json}")
        except Exception as e:
            print(f"Error cargando Python: {e}")

        # Cargar Java
        try:
            with open(java_json, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if 'resultados' in data:
                    resultados_java = data['resultados']
                else:
                    resultados_java = data if isinstance(data, list) else []
            print(f"Cargados {len(resultados_java)} resultados de Java")
        except FileNotFoundError:
            print(f"No se encontró {java_json}")
        except Exception as e:
            print(f"Error cargando Java: {e}")

        return resultados_python, resultados_java

    def graficar_comparacion_ordenamiento(
        self,
        resultados_python: List[Dict],
        resultados_java: List[Dict],
        filename: str = "comparacion_ordenamiento.png"
    ) -> str:
        """
        Genera gráfico de barras comparando Java vs Python para ordenamiento.

        Args:
            resultados_python: Lista de resultados de Python
            resultados_java: Lista de resultados de Java
            filename: Nombre del archivo de salida

        Returns:
            Ruta del gráfico generado
        """
        # Filtrar solo ordenamiento
        python_ord = [r for r in resultados_python if r.get('tipo') == 'ordenamiento']
        java_ord = [r for r in resultados_java if r.get('tipo') == 'ordenamiento']

        if not python_ord and not java_ord:
            print("No hay datos de ordenamiento para graficar")
            return ""

        # Crear DataFrame combinado
        datos = []

        for r in python_ord:
            datos.append({
                'algoritmo': r.get('algoritmo', 'Desconocido'),
                'lenguaje': 'Python',
                'tiempo_ms': float(r.get('tiempo_ms', 0)),
                'tamaño': r.get('tamaño', '0')
            })

        for r in java_ord:
            datos.append({
                'algoritmo': r.get('algoritmo', 'Desconocido'),
                'lenguaje': 'Java',
                'tiempo_ms': float(r.get('tiempo_ms', 0)),
                'tamaño': r.get('tamaño', '0')
            })

        df = pd.DataFrame(datos)

        if df.empty:
            print("No hay datos válidos para graficar")
            return ""

        # Crear figura
        fig, ax = plt.subplots(figsize=(14, 8))

        # Agrupar por algoritmo y lenguaje
        pivot_df = df.pivot_table(
            index='algoritmo',
            columns='lenguaje',
            values='tiempo_ms',
            aggfunc='mean'
        ).fillna(0)

        # Configurar posiciones de barras
        algoritmos = pivot_df.index.tolist()
        x = np.arange(len(algoritmos))
        width = 0.35

        # Crear barras
        bars_java = None
        bars_python = None

        if 'Java' in pivot_df.columns:
            bars_java = ax.bar(x - width/2, pivot_df['Java'], width,
                              label='Java', color=self.COLORES['java'],
                              edgecolor='black', linewidth=0.5)

        if 'Python' in pivot_df.columns:
            bars_python = ax.bar(x + width/2, pivot_df['Python'], width,
                                label='Python', color=self.COLORES['python'],
                                edgecolor='black', linewidth=0.5)

        # Configurar ejes
        ax.set_xlabel('Algoritmo de Ordenamiento', fontweight='bold')
        ax.set_ylabel('Tiempo (ms)', fontweight='bold')
        ax.set_title('Comparación de Rendimiento: Java vs Python\nAlgoritmos de Ordenamiento',
                     fontsize=16, fontweight='bold', pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels(algoritmos, rotation=45, ha='right')
        ax.legend(loc='upper right', framealpha=0.9)

        # Agregar valores sobre las barras
        def agregar_etiquetas(bars):
            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    ax.annotate(f'{height:.1f}',
                               xy=(bar.get_x() + bar.get_width() / 2, height),
                               xytext=(0, 3),
                               textcoords="offset points",
                               ha='center', va='bottom',
                               fontsize=8, fontweight='bold')

        if bars_java:
            agregar_etiquetas(bars_java)
        if bars_python:
            agregar_etiquetas(bars_python)

        ax.set_ylim(0, ax.get_ylim()[1] * 1.15)
        ax.grid(axis='y', alpha=0.3)

        plt.tight_layout()

        # Guardar
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=150, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        plt.close(fig)

        print(f"Gráfico guardado: {output_path}")
        return str(output_path)

    def graficar_comparacion_busqueda(
        self,
        resultados_python: List[Dict],
        resultados_java: List[Dict],
        filename: str = "comparacion_busqueda.png"
    ) -> str:
        """
        Genera gráfico de barras comparando Java vs Python para búsqueda.

        Args:
            resultados_python: Lista de resultados de Python
            resultados_java: Lista de resultados de Java
            filename: Nombre del archivo de salida

        Returns:
            Ruta del gráfico generado
        """
        # Filtrar solo búsqueda
        python_bus = [r for r in resultados_python if r.get('tipo') == 'busqueda']
        java_bus = [r for r in resultados_java if r.get('tipo') == 'busqueda']

        if not python_bus and not java_bus:
            print("No hay datos de búsqueda para graficar")
            return ""

        # Crear DataFrame
        datos = []

        for r in python_bus:
            tiempo_ns = float(r.get('tiempo_ns', 0))
            # Convertir a μs para mejor legibilidad
            tiempo_us = tiempo_ns / 1000
            datos.append({
                'algoritmo': r.get('algoritmo', 'Desconocido'),
                'lenguaje': 'Python',
                'tiempo_us': tiempo_us,
                'tamaño': r.get('tamaño', '0')
            })

        for r in java_bus:
            tiempo_ns = float(r.get('tiempo_ns', 0))
            tiempo_us = tiempo_ns / 1000
            datos.append({
                'algoritmo': r.get('algoritmo', 'Desconocido'),
                'lenguaje': 'Java',
                'tiempo_us': tiempo_us,
                'tamaño': r.get('tamaño', '0')
            })

        df = pd.DataFrame(datos)

        if df.empty:
            print("No hay datos válidos para graficar")
            return ""

        # Crear figura
        fig, ax = plt.subplots(figsize=(14, 8))

        # Pivot para gráfico de barras
        pivot_df = df.pivot_table(
            index='algoritmo',
            columns='lenguaje',
            values='tiempo_us',
            aggfunc='mean'
        ).fillna(0)

        algoritmos = pivot_df.index.tolist()
        x = np.arange(len(algoritmos))
        width = 0.35

        bars_java = None
        bars_python = None

        if 'Java' in pivot_df.columns:
            bars_java = ax.bar(x - width/2, pivot_df['Java'], width,
                              label='Java', color=self.COLORES['java'],
                              edgecolor='black', linewidth=0.5)

        if 'Python' in pivot_df.columns:
            bars_python = ax.bar(x + width/2, pivot_df['Python'], width,
                                label='Python', color=self.COLORES['python'],
                                edgecolor='black', linewidth=0.5)

        ax.set_xlabel('Algoritmo de Búsqueda', fontweight='bold')
        ax.set_ylabel('Tiempo (μs)', fontweight='bold')
        ax.set_title('Comparación de Rendimiento: Java vs Python\nAlgoritmos de Búsqueda',
                     fontsize=16, fontweight='bold', pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels(algoritmos, rotation=45, ha='right')
        ax.legend(loc='upper right', framealpha=0.9)

        # Agregar valores
        def agregar_etiquetas(bars):
            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    label = f'{height:.2f}' if height < 10 else f'{height:.1f}'
                    ax.annotate(label,
                               xy=(bar.get_x() + bar.get_width() / 2, height),
                               xytext=(0, 3),
                               textcoords="offset points",
                               ha='center', va='bottom',
                               fontsize=8, fontweight='bold')

        if bars_java:
            agregar_etiquetas(bars_java)
        if bars_python:
            agregar_etiquetas(bars_python)

        ax.set_ylim(0, ax.get_ylim()[1] * 1.15)
        ax.grid(axis='y', alpha=0.3)

        plt.tight_layout()

        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=150, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        plt.close(fig)

        print(f"Gráfico guardado: {output_path}")
        return str(output_path)

    def graficar_por_tamaño(
        self,
        resultados_python: List[Dict],
        resultados_java: List[Dict],
        filename: str = "comparacion_por_tamaño.png"
    ) -> str:
        """
        Genera gráficos separados por tamaño de entrada.

        Args:
            resultados_python: Lista de resultados de Python
            resultados_java: Lista de resultados de Java
            filename: Nombre del archivo de salida

        Returns:
            Ruta del gráfico generado
        """
        # Filtrar ordenamiento (más relevante para ver por tamaño)
        python_ord = [r for r in resultados_python if r.get('tipo') == 'ordenamiento']
        java_ord = [r for r in resultados_java if r.get('tipo') == 'ordenamiento']

        if not python_ord and not java_ord:
            print("No hay datos suficientes para graficar por tamaño")
            return ""

        # Crear DataFrame combinado
        datos = []
        for r in python_ord:
            datos.append({
                'algoritmo': r.get('algoritmo', 'Desconocido'),
                'lenguaje': 'Python',
                'tiempo_ms': float(r.get('tiempo_ms', 0)),
                'tamaño': r.get('tamaño', '0')
            })
        for r in java_ord:
            datos.append({
                'algoritmo': r.get('algoritmo', 'Desconocido'),
                'lenguaje': 'Java',
                'tiempo_ms': float(r.get('tiempo_ms', 0)),
                'tamaño': r.get('tamaño', '0')
            })

        df = pd.DataFrame(datos)

        if df.empty:
            print("No hay datos válidos")
            return ""

        # Obtener tamaños únicos ordenados
        tamaños = sorted(df['tamaño'].unique(), key=lambda x: int(x))

        # Crear subplots
        n_tamaños = len(tamaños)
        if n_tamaños == 0:
            print("No hay tamaños para graficar")
            return ""

        fig, axes = plt.subplots(1, n_tamaños, figsize=(6 * n_tamaños, 8))
        if n_tamaños == 1:
            axes = [axes]

        for idx, tamaño in enumerate(tamaños):
            ax = axes[idx]
            df_tamaño = df[df['tamaño'] == tamaño]

            pivot = df_tamaño.pivot_table(
                index='algoritmo',
                columns='lenguaje',
                values='tiempo_ms',
                aggfunc='mean'
            ).fillna(0)

            algoritmos = pivot.index.tolist()
            x = np.arange(len(algoritmos))
            width = 0.35

            if 'Java' in pivot.columns:
                bars_java = ax.bar(x - width/2, pivot['Java'], width,
                                  label='Java', color=self.COLORES['java'],
                                  edgecolor='black', linewidth=0.5)
            if 'Python' in pivot.columns:
                bars_python = ax.bar(x + width/2, pivot['Python'], width,
                                    label='Python', color=self.COLORES['python'],
                                    edgecolor='black', linewidth=0.5)

            ax.set_xlabel('Algoritmo')
            ax.set_ylabel('Tiempo (ms)')
            ax.set_title(f'Tamaño: {int(tamaño):,} elementos',
                        fontweight='bold')
            ax.set_xticks(x)
            ax.set_xticklabels(algoritmos, rotation=45, ha='right')
            ax.legend()
            ax.grid(axis='y', alpha=0.3)

            # Ajustar límite superior
            max_val = df_tamaño['tiempo_ms'].max()
            ax.set_ylim(0, max_val * 1.2 if max_val > 0 else 1)

        fig.suptitle('Comparación Java vs Python por Tamaño de Entrada\n(Algoritmos de Ordenamiento)',
                    fontsize=16, fontweight='bold', y=1.02)

        plt.tight_layout()

        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=150, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        plt.close(fig)

        print(f"Gráfico guardado: {output_path}")
        return str(output_path)

    def generar_todos(
        self,
        resultados_python: Optional[List[Dict]] = None,
        resultados_java: Optional[List[Dict]] = None
    ) -> List[str]:
        """
        Genera todos los gráficos de comparación.

        Args:
            resultados_python: Resultados de Python (opcional, carga si no se provee)
            resultados_java: Resultados de Java (opcional, carga si no se provee)

        Returns:
            Lista de rutas de los gráficos generados
        """
        if resultados_python is None or resultados_java is None:
            py, java = self.cargar_resultados()
            resultados_python = resultados_python or py
            resultados_java = resultados_java or java

        generados = []

        # Gráfico de ordenamiento
        if resultados_python or resultados_java:
            path = self.graficar_comparacion_ordenamiento(
                resultados_python, resultados_java
            )
            if path:
                generados.append(path)

        # Gráfico de búsqueda
            path = self.graficar_comparacion_busqueda(
                resultados_python, resultados_java
            )
            if path:
                generados.append(path)

        # Gráfico por tamaño
            path = self.graficar_por_tamaño(resultados_python, resultados_java)
            if path:
                generados.append(path)

        return generados


def generar_todos_los_graficos(
    output_dir: str = "docs/graficos",
    python_json: str = "data/output/resultados_python.json",
    java_json: str = "data/output/resultados_java.json"
) -> List[str]:
    """
    Función de conveniencia para generar todos los gráficos.

    Args:
        output_dir: Directorio de salida
        python_json: Ruta al JSON de Python
        java_json: Ruta al JSON de Java

    Returns:
        Lista de rutas de gráficos generados
    """
    graficador = GraficadorResultados(output_dir)
    resultados_python, resultados_java = graficador.cargar_resultados(python_json, java_json)

    return graficador.generar_todos(resultados_python, resultados_java)