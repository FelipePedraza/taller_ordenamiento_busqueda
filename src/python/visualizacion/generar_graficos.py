"""
Generador de Gráficos - Visualización de resultados de benchmarking.

Este módulo genera gráficos comparativos usando matplotlib y seaborn
para visualizar los resultados de los algoritmos de ordenamiento y búsqueda.

Gráficos generados:
1. Comparación Java vs Python - Ordenamiento (con escala logarítmica si aplica)
2. Comparación Java vs Python - Búsqueda (en nanosegundos, escala log)
3. Gráficos por tamaño de entrada (3 subplots, uno por tamaño)
4. Speedup Java vs Python (factor de aceleración)

Características:
- Escala logarítmica automática cuando hay grandes diferencias (>100x)
- Formato de tiempo legible (ej: "1.2 ms" en lugar de "1200.00")
- Colores distintivos por lenguaje
- Etiquetas rotadas para mejor legibilidad
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
        colores: Paleta de colores distintiva por lenguaje
    """

    # Paleta de colores distintiva
    COLORES = {
        'python': '#3776ab',      # Azul Python
        'java': '#e76f00',        # Naranja Java
        'python_light': '#6fa8dc',
        'java_light': '#f4a261',
        'grid': '#e0e0e0',        # Gris para grid
        'text': '#333333',        # Texto oscuro
    }

    # Mapeo de nombres de algoritmos para normalización
    MAPEO_ALGORITMOS = {
        # Ordenamiento - Java a nombre común
        'ShakerSort': 'Shaker Sort',
        'DualPivotQuickSort': 'Dual-Pivot QuickSort',
        'HeapSort': 'Heap Sort',
        'MergeSort': 'Merge Sort',
        'RadixSort': 'Radix Sort',
        # Búsqueda - Java a nombre común
        'BinarySearch': 'Búsqueda Binaria',
        'TernarySearch': 'Búsqueda Ternaria',
        'JumpSearch': 'Jump Search',
        # Ordenamiento - Python (ya está normalizado)
        'Shaker Sort': 'Shaker Sort',
        'Dual-Pivot QuickSort': 'Dual-Pivot QuickSort',
        'Heap Sort': 'Heap Sort',
        'Merge Sort': 'Merge Sort',
        'Radix Sort': 'Radix Sort',
        # Búsqueda - Python
        'Busqueda Binaria': 'Búsqueda Binaria',
        'Busqueda Ternaria': 'Búsqueda Ternaria',
        'Jump Search': 'Jump Search',
    }

    # Abreviaturas para etiquetas cortas
    ABREVIATURAS = {
        'Shaker Sort': 'Shaker',
        'Dual-Pivot QuickSort': 'Dual-Pivot\nQuickSort',
        'Heap Sort': 'Heap',
        'Merge Sort': 'Merge',
        'Radix Sort': 'Radix',
        'Búsqueda Binaria': 'Binaria',
        'Búsqueda Ternaria': 'Ternaria',
        'Jump Search': 'Jump',
    }

    def __init__(self, output_dir: str = "docs/graficos"):
        """
        Inicializa el graficador.

        Args:
            output_dir: Directorio de salida para los gráficos
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Configurar estilo profesional
        self._configurar_estilo()

    def _configurar_estilo(self):
        """Configura el estilo visual de matplotlib."""
        plt.style.use('seaborn-v0_8-whitegrid')

        # Configuración personalizada profesional
        plt.rcParams.update({
            'figure.figsize': (14, 8),
            'axes.titlesize': 14,
            'axes.labelsize': 12,
            'xtick.labelsize': 10,
            'ytick.labelsize': 10,
            'legend.fontsize': 11,
            'axes.grid': True,
            'grid.alpha': 0.3,
            'axes.edgecolor': '#cccccc',
            'axes.linewidth': 1.2,
            'figure.dpi': 150,
            'savefig.dpi': 150,
            'savefig.bbox': 'tight',
            'savefig.facecolor': 'white',
        })

    def _normalizar_nombre_algoritmo(self, nombre: str) -> str:
        """
        Normaliza el nombre del algoritmo a un formato común.

        Args:
            nombre: Nombre original del algoritmo

        Returns:
            Nombre normalizado
        """
        return self.MAPEO_ALGORITMOS.get(nombre, nombre)

    def _obtener_abreviatura(self, nombre: str) -> str:
        """
        Obtiene una versión abreviada del nombre para etiquetas.

        Args:
            nombre: Nombre normalizado del algoritmo

        Returns:
            Nombre abreviado si existe, sino el original
        """
        return self.ABREVIATURAS.get(nombre, nombre)

    def _formatear_tiempo(self, valor: float, unidad_base: str = 'ms') -> str:
        """
        Formatea un valor de tiempo de manera legible.

        Args:
            valor: Valor numérico del tiempo
            unidad_base: Unidad base ('ms', 'us', 'ns')

        Returns:
            String formateado (ej: "1.2 ms", "850 ns")
        """
        # Convertir todo a nanosegundos primero
        multiplicadores = {
            'ms': 1_000_000,
            'us': 1_000,
            'ns': 1
        }

        valor_ns = valor * multiplicadores.get(unidad_base, 1)

        # Elegir la unidad más apropiada
        if valor_ns >= 1_000_000_000:
            return f"{valor_ns / 1_000_000_000:.2f} s"
        elif valor_ns >= 1_000_000:
            return f"{valor_ns / 1_000_000:.2f} ms"
        elif valor_ns >= 1_000:
            return f"{valor_ns / 1_000:.2f} us"
        else:
            return f"{valor_ns:.0f} ns"

    def _necesita_escala_log(self, valores: List[float], umbral: float = 100.0) -> bool:
        """
        Determina si se necesita escala logarítmica.

        Args:
            valores: Lista de valores numéricos
            umbral: Ratio mínimo entre max/min para activar escala log

        Returns:
            True si se recomienda escala logarítmica
        """
        valores_filtrados = [v for v in valores if v > 0]
        if len(valores_filtrados) < 2:
            return False

        min_val = min(valores_filtrados)
        max_val = max(valores_filtrados)

        return (max_val / min_val) > umbral

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
                if isinstance(data, dict) and 'resultados' in data:
                    resultados_python = data['resultados']
                elif isinstance(data, list):
                    resultados_python = data
            print(f"[OK] Cargados {len(resultados_python)} resultados de Python")
        except FileNotFoundError:
            print(f"[WARN] No se encontro {python_json}")
        except Exception as e:
            print(f"[ERROR] Error cargando Python: {e}")

        # Cargar Java
        try:
            with open(java_json, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict) and 'resultados' in data:
                    resultados_java = data['resultados']
                elif isinstance(data, list):
                    resultados_java = data
            print(f"[OK] Cargados {len(resultados_java)} resultados de Java")
        except FileNotFoundError:
            print(f"[WARN] No se encontro {java_json}")
        except Exception as e:
            print(f"[ERROR] Error cargando Java: {e}")

        return resultados_python, resultados_java

    def _preparar_dataframe_combinado(
        self,
        resultados_python: List[Dict],
        resultados_java: List[Dict],
        tipo: str,
        campo_tiempo: str = 'tiempo_ms'
    ) -> pd.DataFrame:
        """
        Prepara un DataFrame combinado con datos normalizados.

        Args:
            resultados_python: Resultados de Python
            resultados_java: Resultados de Java
            tipo: 'ordenamiento' o 'busqueda'
            campo_tiempo: Campo de tiempo a usar ('tiempo_ms' o 'tiempo_ns')

        Returns:
            DataFrame combinado y normalizado
        """
        datos = []

        # Procesar Python
        for r in resultados_python:
            if r.get('tipo') == tipo:
                datos.append({
                    'algoritmo': self._normalizar_nombre_algoritmo(r.get('algoritmo', 'Desconocido')),
                    'lenguaje': 'Python',
                    'tiempo': float(r.get(campo_tiempo, 0)),
                    'tamaño': str(r.get('tamaño', '0'))
                })

        # Procesar Java
        for r in resultados_java:
            if r.get('tipo') == tipo:
                datos.append({
                    'algoritmo': self._normalizar_nombre_algoritmo(r.get('algoritmo', 'Desconocido')),
                    'lenguaje': 'Java',
                    'tiempo': float(r.get(campo_tiempo, 0)),
                    'tamaño': str(r.get('tamaño', '0'))
                })

        return pd.DataFrame(datos)

    def graficar_comparacion_ordenamiento(
        self,
        resultados_python: List[Dict],
        resultados_java: List[Dict],
        filename: str = "comparacion_ordenamiento.png"
    ) -> str:
        """
        Genera gráfico de barras comparando Java vs Python para ordenamiento.
        Usa escala logarítmica cuando hay grandes diferencias de tiempo.

        Args:
            resultados_python: Lista de resultados de Python
            resultados_java: Lista de resultados de Java
            filename: Nombre del archivo de salida

        Returns:
            Ruta del gráfico generado
        """
        df = self._preparar_dataframe_combinado(
            resultados_python, resultados_java, 'ordenamiento', 'tiempo_ms'
        )

        if df.empty:
            print("[WARN] No hay datos de ordenamiento para graficar")
            return ""

        # Crear figura
        fig, ax = plt.subplots(figsize=(14, 8))

        # Agrupar por algoritmo y lenguaje
        pivot_df = df.pivot_table(
            index='algoritmo',
            columns='lenguaje',
            values='tiempo',
            aggfunc='mean'
        ).fillna(0)

        # Ordenar algoritmos por tiempo promedio
        if 'Java' in pivot_df.columns:
            pivot_df = pivot_df.sort_values('Java', ascending=True)

        algoritmos = pivot_df.index.tolist()
        x = np.arange(len(algoritmos))
        width = 0.35

        # Crear barras
        bars_java = None
        bars_python = None

        if 'Java' in pivot_df.columns:
            bars_java = ax.barh(x - width/2, pivot_df['Java'], width,
                               label='Java', color=self.COLORES['java'],
                               edgecolor='black', linewidth=0.5)

        if 'Python' in pivot_df.columns:
            bars_python = ax.barh(x + width/2, pivot_df['Python'], width,
                                 label='Python', color=self.COLORES['python'],
                                 edgecolor='black', linewidth=0.5)

        # Determinar si necesitamos escala logarítmica
        todos_los_tiempos = df['tiempo'].tolist()
        usar_log = self._necesita_escala_log(todos_los_tiempos, umbral=100.0)

        if usar_log:
            ax.set_xscale('log')
            ax.set_xlabel('Tiempo (ms) - Escala Logarítmica', fontweight='bold')
        else:
            ax.set_xlabel('Tiempo (ms)', fontweight='bold')

        ax.set_ylabel('Algoritmo de Ordenamiento', fontweight='bold')
        ax.set_title('Comparación de Rendimiento: Java vs Python\nAlgoritmos de Ordenamiento',
                     fontsize=16, fontweight='bold', pad=20)
        ax.set_yticks(x)
        ax.set_yticklabels([self._obtener_abreviatura(a) for a in algoritmos])
        ax.legend(loc='lower right', framealpha=0.9)

        # Agregar valores al final de las barras
        def agregar_etiquetas_horizontales(bars, unidad='ms'):
            for bar in bars:
                width_val = bar.get_width()
                if width_val > 0:
                    label = self._formatear_tiempo(width_val, unidad)
                    ax.annotate(label,
                               xy=(width_val, bar.get_y() + bar.get_height() / 2),
                               xytext=(5, 0),
                               textcoords="offset points",
                               ha='left', va='center',
                               fontsize=8, fontweight='bold',
                               color=self.COLORES['text'])

        if bars_java:
            agregar_etiquetas_horizontales(bars_java, 'ms')
        if bars_python:
            agregar_etiquetas_horizontales(bars_python, 'ms')

        # Ajustar límites
        if usar_log:
            min_val = min([v for v in todos_los_tiempos if v > 0]) * 0.5
            max_val = max(todos_los_tiempos) * 2
            ax.set_xlim(min_val, max_val)
        else:
            ax.set_xlim(0, ax.get_xlim()[1] * 1.2)

        ax.grid(axis='x', alpha=0.3)

        # Agregar nota sobre escala logarítmica
        if usar_log:
            ax.text(0.02, 0.98, 'Escala logarítmica (grandes diferencias de tiempo)',
                   transform=ax.transAxes, fontsize=9, color='gray',
                   verticalalignment='top')

        plt.tight_layout()

        # Guardar
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=150, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        plt.close(fig)

        print(f"[OK] Gráfico guardado: {output_path}")
        return str(output_path)

    def graficar_comparacion_busqueda(
        self,
        resultados_python: List[Dict],
        resultados_java: List[Dict],
        filename: str = "comparacion_busqueda.png"
    ) -> str:
        """
        Genera gráfico de barras comparando Java vs Python para búsqueda.
        Usa nanosegundos y escala logarítmica.

        Args:
            resultados_python: Lista de resultados de Python
            resultados_java: Lista de resultados de Java
            filename: Nombre del archivo de salida

        Returns:
            Ruta del gráfico generado
        """
        df = self._preparar_dataframe_combinado(
            resultados_python, resultados_java, 'busqueda', 'tiempo_ns'
        )

        if df.empty:
            print("[WARN] No hay datos de búsqueda para graficar")
            return ""

        # Crear figura
        fig, ax = plt.subplots(figsize=(12, 7))

        # Agrupar por algoritmo y lenguaje
        pivot_df = df.pivot_table(
            index='algoritmo',
            columns='lenguaje',
            values='tiempo',
            aggfunc='mean'
        ).fillna(0)

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

        # Usar escala logarítmica para búsqueda (siempre hay diferencias significativas)
        todos_los_tiempos = df['tiempo'].tolist()
        usar_log = self._necesita_escala_log(todos_los_tiempos, umbral=10.0)

        if usar_log:
            ax.set_yscale('log')
            ax.set_ylabel('Tiempo (ns) - Escala Logarítmica', fontweight='bold')
        else:
            ax.set_ylabel('Tiempo (ns)', fontweight='bold')

        ax.set_xlabel('Algoritmo de Búsqueda', fontweight='bold')
        ax.set_title('Comparación de Rendimiento: Java vs Python\nAlgoritmos de Búsqueda (nanosegundos)',
                     fontsize=16, fontweight='bold', pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels([self._obtener_abreviatura(a) for a in algoritmos],
                          rotation=0, ha='center')
        ax.legend(loc='upper right', framealpha=0.9)

        # Agregar valores sobre las barras
        def agregar_etiquetas_verticales(bars):
            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    label = self._formatear_tiempo(height, 'ns')
                    ax.annotate(label,
                               xy=(bar.get_x() + bar.get_width() / 2, height),
                               xytext=(0, 3),
                               textcoords="offset points",
                               ha='center', va='bottom',
                               fontsize=8, fontweight='bold',
                               rotation=0)

        if bars_java:
            agregar_etiquetas_verticales(bars_java)
        if bars_python:
            agregar_etiquetas_verticales(bars_python)

        # Ajustar límites
        if usar_log:
            min_val = min([v for v in todos_los_tiempos if v > 0]) * 0.7
            max_val = max(todos_los_tiempos) * 1.5
            ax.set_ylim(min_val, max_val)
        else:
            ax.set_ylim(0, ax.get_ylim()[1] * 1.2)

        ax.grid(axis='y', alpha=0.3)

        # Agregar nota
        if usar_log:
            ax.text(0.02, 0.98, 'Escala logarítmica (diferencias significativas)',
                   transform=ax.transAxes, fontsize=9, color='gray',
                   verticalalignment='top')

        plt.tight_layout()

        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=150, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        plt.close(fig)

        print(f"[OK] Gráfico guardado: {output_path}")
        return str(output_path)

    def graficar_por_tamaño(
        self,
        resultados_python: List[Dict],
        resultados_java: List[Dict],
        filename: str = "comparacion_por_tamano.png"
    ) -> str:
        """
        Genera gráficos separados por tamaño de entrada (3 subplots).

        Args:
            resultados_python: Lista de resultados de Python
            resultados_java: Lista de resultados de Java
            filename: Nombre del archivo de salida

        Returns:
            Ruta del gráfico generado
        """
        df = self._preparar_dataframe_combinado(
            resultados_python, resultados_java, 'ordenamiento', 'tiempo_ms'
        )

        if df.empty:
            print("[WARN] No hay datos suficientes para graficar por tamaño")
            return ""

        # Obtener tamaños únicos ordenados
        tamaños = sorted(df['tamaño'].unique(), key=lambda x: int(x))

        if not tamaños:
            print("[WARN] No hay tamaños para graficar")
            return ""

        # Crear subplots
        n_tamaños = len(tamaños)
        fig, axes = plt.subplots(1, n_tamaños, figsize=(6 * n_tamaños, 7))

        if n_tamaños == 1:
            axes = [axes]

        for idx, tamaño in enumerate(tamaños):
            ax = axes[idx]
            df_tamaño = df[df['tamaño'] == tamaño]

            pivot = df_tamaño.pivot_table(
                index='algoritmo',
                columns='lenguaje',
                values='tiempo',
                aggfunc='mean'
            ).fillna(0)

            # Ordenar por tiempo de Java
            if 'Java' in pivot.columns:
                pivot = pivot.sort_values('Java', ascending=True)

            algoritmos = pivot.index.tolist()
            y = np.arange(len(algoritmos))
            width = 0.35

            # Determinar si usar escala log
            tiempos_tamaño = df_tamaño['tiempo'].tolist()
            usar_log = self._necesita_escala_log(tiempos_tamaño, umbral=50.0)

            if 'Java' in pivot.columns:
                bars_java = ax.barh(y - width/2, pivot['Java'], width,
                                   label='Java', color=self.COLORES['java'],
                                   edgecolor='black', linewidth=0.5)
            if 'Python' in pivot.columns:
                bars_python = ax.barh(y + width/2, pivot['Python'], width,
                                     label='Python', color=self.COLORES['python'],
                                     edgecolor='black', linewidth=0.5)

            if usar_log:
                ax.set_xscale('log')

            ax.set_xlabel('Tiempo (ms)' + (' - Escala Log' if usar_log else ''), fontsize=10)
            ax.set_title(f'{int(tamaño):,} elementos', fontweight='bold', fontsize=12)
            ax.set_yticks(y)
            ax.set_yticklabels([self._obtener_abreviatura(a) for a in algoritmos], fontsize=9)

            if idx == 0:
                ax.legend(loc='lower right', fontsize=9)

            ax.grid(axis='x', alpha=0.3)

            # Ajustar límites
            if usar_log:
                min_val = min([v for v in tiempos_tamaño if v > 0]) * 0.5
                max_val = max(tiempos_tamaño) * 2
                ax.set_xlim(min_val, max_val)
            else:
                ax.set_xlim(0, ax.get_xlim()[1] * 1.15)

        fig.suptitle('Comparación Java vs Python por Tamaño de Entrada\n(Algoritmos de Ordenamiento)',
                    fontsize=16, fontweight='bold', y=1.02)

        plt.tight_layout()

        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=150, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        plt.close(fig)

        print(f"[OK] Gráfico guardado: {output_path}")
        return str(output_path)

    def graficar_speedup(
        self,
        resultados_python: List[Dict],
        resultados_java: List[Dict],
        filename: str = "speedup_java_vs_python.png"
    ) -> str:
        """
        Genera gráfico de speedup (factor de aceleración Java vs Python).
        Speedup = tiempo_python / tiempo_java

        Args:
            resultados_python: Lista de resultados de Python
            resultados_java: Lista de resultados de Java
            filename: Nombre del archivo de salida

        Returns:
            Ruta del gráfico generado
        """
        df = self._preparar_dataframe_combinado(
            resultados_python, resultados_java, 'ordenamiento', 'tiempo_ms'
        )

        if df.empty:
            print("[WARN] No hay datos para calcular speedup")
            return ""

        # Calcular speedup para cada algoritmo y tamaño
        datos_speedup = []

        for (algoritmo, tamaño), grupo in df.groupby(['algoritmo', 'tamaño']):
            tiempos_java = grupo[grupo['lenguaje'] == 'Java']['tiempo'].values
            tiempos_python = grupo[grupo['lenguaje'] == 'Python']['tiempo'].values

            if len(tiempos_java) > 0 and len(tiempos_python) > 0:
                tiempo_java = tiempos_java[0]
                tiempo_python = tiempos_python[0]

                if tiempo_java > 0:
                    speedup = tiempo_python / tiempo_java
                    datos_speedup.append({
                        'algoritmo': algoritmo,
                        'tamaño': tamaño,
                        'speedup': speedup,
                        'tiempo_java': tiempo_java,
                        'tiempo_python': tiempo_python
                    })

        if not datos_speedup:
            print("[WARN] No se pudo calcular speedup (datos incompletos)")
            return ""

        df_speedup = pd.DataFrame(datos_speedup)

        # Crear figura
        fig, ax = plt.subplots(figsize=(12, 8))

        # Crear pivot para heatmap de barras
        pivot_speedup = df_speedup.pivot_table(
            index='algoritmo',
            columns='tamaño',
            values='speedup',
            aggfunc='mean'
        ).fillna(0)

        # Ordenar por speedup promedio
        pivot_speedup['promedio'] = pivot_speedup.mean(axis=1)
        pivot_speedup = pivot_speedup.sort_values('promedio', ascending=True)
        pivot_speedup = pivot_speedup.drop('promedio', axis=1)

        # Crear barras horizontales agrupadas por tamaño
        algoritmos = pivot_speedup.index.tolist()
        tamaños = pivot_speedup.columns.tolist()

        y = np.arange(len(algoritmos))
        height = 0.25

        colores_tamaño = ['#2ecc71', '#3498db', '#e74c3c']  # Verde, Azul, Rojo

        for idx, tamaño in enumerate(tamaños):
            offset = (idx - 1) * height
            valores = pivot_speedup[tamaño].values
            bars = ax.barh(y + offset, valores, height,
                          label=f'{int(tamaño):,} elementos',
                          color=colores_tamaño[idx % len(colores_tamaño)],
                          edgecolor='black', linewidth=0.5)

            # Agregar valores
            for i, (bar, val) in enumerate(zip(bars, valores)):
                if val > 0:
                    ax.annotate(f'{val:.1f}x',
                               xy=(val, bar.get_y() + bar.get_height() / 2),
                               xytext=(3, 0),
                               textcoords="offset points",
                               ha='left', va='center',
                               fontsize=8, fontweight='bold')

        # Línea de referencia en 1x
        ax.axvline(x=1, color='red', linestyle='--', linewidth=2, alpha=0.7, label='Sin diferencia (1x)')

        ax.set_xlabel('Speedup (factor de aceleración)', fontweight='bold')
        ax.set_ylabel('Algoritmo de Ordenamiento', fontweight='bold')
        ax.set_title('Speedup: Java vs Python\nCuántas veces es más rápido Java (valores > 1)',
                     fontsize=16, fontweight='bold', pad=20)
        ax.set_yticks(y)
        ax.set_yticklabels([self._obtener_abreviatura(a) for a in algoritmos])
        ax.legend(loc='lower right', framealpha=0.9, title='Tamaño de entrada')

        ax.set_xlim(0, max(df_speedup['speedup']) * 1.15)
        ax.grid(axis='x', alpha=0.3)

        # Agregar explicación
        ax.text(0.02, 0.02,
               'Speedup = tiempo_python / tiempo_java\n>1: Java es más rápido | <1: Python es más rápido',
               transform=ax.transAxes, fontsize=9, color='gray',
               verticalalignment='bottom',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

        plt.tight_layout()

        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=150, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        plt.close(fig)

        print(f"[OK] Gráfico guardado: {output_path}")
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

        if not resultados_python and not resultados_java:
            print("[WARN] No hay datos para generar gráficos")
            return generados

        print("\n" + "="*60)
        print("GENERANDO GRÁFICOS DE COMPARACIÓN")
        print("="*60 + "\n")

        # 1. Gráfico de ordenamiento
        path = self.graficar_comparacion_ordenamiento(resultados_python, resultados_java)
        if path:
            generados.append(path)

        # 2. Gráfico de búsqueda
        path = self.graficar_comparacion_busqueda(resultados_python, resultados_java)
        if path:
            generados.append(path)

        # 3. Gráfico por tamaño
        path = self.graficar_por_tamaño(resultados_python, resultados_java)
        if path:
            generados.append(path)

        # 4. Gráfico de speedup
        path = self.graficar_speedup(resultados_python, resultados_java)
        if path:
            generados.append(path)

        print("\n" + "="*60)
        print(f"TOTAL GRÁFICOS GENERADOS: {len(generados)}")
        print("="*60)

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


if __name__ == "__main__":
    # Ejecución directa
    generar_todos_los_graficos()
