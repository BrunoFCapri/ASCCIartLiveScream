"""
Procesador de matrices con multithreading para conversión ASCII con soporte de colores
"""
import numpy as np
from typing import List, Tuple, Optional
from PIL import Image
import threading
from queue import Queue
import time
from utils.config import (get_color_escape, RESET_COLOR, 
                         calculate_dynamic_thread_count, 
                         calculate_optimal_chunk_distribution,
                         auto_tune_thread_count)

class MatrixChunk:
    """Representa un fragmento de la matriz para procesamiento"""
    def __init__(self, data: np.ndarray, start_row: int, end_row: int, 
                 start_col: int, end_col: int, chunk_id: int):
        self.data = data
        self.start_row = start_row
        self.end_row = end_row
        self.start_col = start_col
        self.end_col = end_col
        self.chunk_id = chunk_id
        self.result: Optional[List[str]] = None
        self.processing_time = 0.0

class ThreadedMatrixProcessor:
    """Procesador ULTRA-OPTIMIZADO con threading dinámico y cache inteligente"""
    
    def __init__(self, ascii_chars: List[str], thread_count: int = 4):
        self.ascii_chars = np.array(ascii_chars)  # Numpy array para acceso rápido
        self.base_thread_count = thread_count
        self.char_count = len(ascii_chars)
        
        # Sistema de threading dinámico
        self.dynamic_threading = True
        self.performance_history = []
        self.current_thread_count = thread_count
        
        # Pre-calcular tabla de conversión OPTIMIZADA
        self._build_optimized_conversion_table()
        
        # Cache para strings pre-formateadas
        self._build_string_cache()
        
        # Cache inteligente para frames similares
        self._init_frame_cache()
        
        # Importar función optimizada
        try:
            from utils.config import get_color_escape_fast, _build_color_lookup_tables
            self.get_color_escape = get_color_escape_fast
            _build_color_lookup_tables()  # Pre-construir lookup tables
        except ImportError:
            from utils.config import get_color_escape
            self.get_color_escape = get_color_escape
        
    def _build_optimized_conversion_table(self):
        """Construye tabla de conversión ULTRA-OPTIMIZADA"""
        # Usar operaciones vectorizadas para máxima velocidad
        indices = np.arange(256, dtype=np.float32)
        char_indices = (indices * (self.char_count - 1) / 255.0).astype(np.uint8)
        char_indices = np.clip(char_indices, 0, self.char_count - 1)
        self.conversion_table = char_indices
        
        # Pre-calcular multiplicadores de brillo optimizados
        self.brightness_weights = np.array([0.299, 0.587, 0.114], dtype=np.float32)
        
    def _build_string_cache(self):
        """Pre-construye cache de strings comunes para evitar concatenaciones"""
        self.char_cache = {}
        for i, char in enumerate(self.ascii_chars):
            self.char_cache[i] = char
    
    def _init_frame_cache(self):
        """Inicializa el sistema de cache inteligente"""
        self.frame_cache = {}
        self.previous_frame_hash = None
        self.cache_hits = 0
        self.cache_misses = 0
        self.similarity_threshold = 0.95  # 95% similitud para considerar cache
        self.max_cache_size = 10  # Máximo frames en cache
        
    def _calculate_frame_similarity(self, frame1: np.ndarray, frame2: np.ndarray) -> float:
        """Calcula la similitud entre dos frames usando sampling optimizado"""
        if frame1.shape != frame2.shape:
            return 0.0
        
        # Usar muestreo para velocidad - solo comparar cada 4to pixel
        sample1 = frame1[::4, ::4]
        sample2 = frame2[::4, ::4]
        
        # Calcular diferencia usando operaciones vectorizadas
        diff = np.abs(sample1.astype(np.int16) - sample2.astype(np.int16))
        max_diff = np.max(diff)
        
        if max_diff == 0:
            return 1.0
        
        # Normalizar diferencia
        similarity = 1.0 - (np.mean(diff) / 255.0)
        return max(0.0, similarity)
    
    def _get_frame_hash(self, image_array: np.ndarray) -> int:
        """Genera hash rápido para identificación de frames"""
        # Usar muestreo para generar hash rápido
        sample = image_array[::8, ::8]  # Muestrear cada 8vo pixel
        return hash(sample.tobytes())
    
    def split_matrix(self, image_array: np.ndarray, color_mode: int = 0) -> List[MatrixChunk]:
        """OPTIMIZADO: Divide matriz usando distribución inteligente de chunks"""
        height, width = image_array.shape[:2]
        total_characters = height * width
        
        # Calcular threading dinámico
        if self.dynamic_threading:
            self.current_thread_count = calculate_dynamic_thread_count(
                total_characters, color_mode, (width, height)
            )
            
            # Auto-tuning basado en historial
            if len(self.performance_history) > 0:
                self.current_thread_count = auto_tune_thread_count(
                    self.current_thread_count, self.performance_history
                )
        else:
            self.current_thread_count = self.base_thread_count
        
        # Distribución inteligente de chunks
        chunks_horizontal, chunks_vertical = calculate_optimal_chunk_distribution(
            total_characters, self.current_thread_count, (height, width)
        )
        
        # Calcular tamaños de chunk
        chunk_height = height // chunks_vertical
        chunk_width = width // chunks_horizontal
        
        chunks = []
        chunk_id = 0
        
        # Crear chunks usando distribución inteligente
        for row in range(chunks_vertical):
            for col in range(chunks_horizontal):
                start_row = row * chunk_height
                end_row = min((row + 1) * chunk_height, height)
                start_col = col * chunk_width
                end_col = min((col + 1) * chunk_width, width)
                
                # Evitar chunks vacíos
                if start_row < height and start_col < width:
                    chunk_data = image_array[start_row:end_row, start_col:end_col]
                    chunk = MatrixChunk(chunk_data, start_row, end_row, 
                                      start_col, end_col, chunk_id)
                    chunks.append(chunk)
                    chunk_id += 1
        
        return chunks
    
    def process_chunk(self, chunk: MatrixChunk, color_mode: int = 0) -> List[str]:
        """ULTRA-OPTIMIZADO: Procesa un chunk usando operaciones vectorizadas"""
        start_time = time.time()
        
        # Optimización 1: Operaciones vectorizadas para RGB->Gray
        if len(chunk.data.shape) == 3:
            color_data = chunk.data[...,:3].astype(np.uint8)
            # Usar dot product vectorizado ultra-rápido
            gray_data = np.dot(color_data, self.brightness_weights).astype(np.uint8)
        else:
            gray_data = chunk.data.astype(np.uint8)
            color_data = np.stack([gray_data] * 3, axis=-1)
        
        # Optimización 2: Lookup vectorizado usando fancy indexing
        char_indices = self.conversion_table[gray_data]
        height, width = char_indices.shape
        
        # Optimización 3: Construcción vectorizada de strings
        if color_mode == 0:
            # Modo sin colores - construcción ultrarrápida
            result_lines = []
            for row in char_indices:
                # Usar fancy indexing para acceso rápido a caracteres
                chars = self.ascii_chars[row]
                line = ''.join(chars)
                result_lines.append(line)
        else:
            # Modo con colores - optimizado para velocidad
            result_lines = []
            for row_idx in range(height):
                line_parts = []
                row_chars = char_indices[row_idx]
                row_colors = color_data[row_idx]
                
                # Procesar en lotes para reducir overhead
                for col_idx in range(width):
                    char = self.ascii_chars[row_chars[col_idx]]
                    r, g, b = row_colors[col_idx]
                    
                    # Usar función optimizada de escape
                    color_escape = self.get_color_escape(color_mode, int(r), int(g), int(b))
                    if color_escape:
                        line_parts.append(f"{color_escape}{char}{RESET_COLOR}")
                    else:
                        line_parts.append(char)
                
                result_lines.append(''.join(line_parts))
        
        chunk.processing_time = time.time() - start_time
        return result_lines
    
    def process_matrix_threaded(self, image_array: np.ndarray, 
                              color_mode: int = 0) -> Tuple[List[str], dict]:
        """ULTRA-OPTIMIZADO: Procesa matriz con cache inteligente y multithreading"""
        start_time = time.time()
        
        # Cache inteligente - verificar similitud con frame anterior
        frame_hash = self._get_frame_hash(image_array)
        
        if self.previous_frame_hash is not None:
            # Verificar si el frame es muy similar al anterior
            if frame_hash in self.frame_cache:
                self.cache_hits += 1
                cached_result = self.frame_cache[frame_hash]
                
                # Estadísticas de cache hit
                stats = {
                    'total_time': time.time() - start_time,
                    'chunks_processed': cached_result['chunks_processed'],
                    'threads_used': 0,  # No se usaron hilos
                    'avg_chunk_time': 0.001,  # Tiempo mínimo por cache hit
                    'cache_hit': True,
                    'cache_hits': self.cache_hits,
                    'cache_misses': self.cache_misses
                }
                
                return cached_result['lines'], stats
        
        # Cache miss - procesar normalmente
        self.cache_misses += 1
        
        # Dividir en chunks usando distribución inteligente
        chunks = self.split_matrix(image_array, color_mode)
        
        # Cola de trabajo optimizada con menor overhead
        work_queue = Queue(maxsize=len(chunks))
        result_dict = {}
        
        # Llenar cola de trabajo
        for chunk in chunks:
            work_queue.put(chunk)
        
        def optimized_worker():
            """Worker optimizado con menor overhead"""
            local_results = {}
            while True:
                try:
                    chunk = work_queue.get_nowait()
                    result = self.process_chunk(chunk, color_mode)
                    local_results[chunk.chunk_id] = {
                        'lines': result,
                        'start_row': chunk.start_row,
                        'end_row': chunk.end_row,
                        'start_col': chunk.start_col,
                        'end_col': chunk.end_col,
                        'processing_time': chunk.processing_time
                    }
                except:
                    break
            
            # Actualizar resultado global de manera thread-safe
            result_dict.update(local_results)
        
        # Crear hilos usando conteo dinámico optimizado
        threads = []
        optimal_thread_count = min(self.current_thread_count, len(chunks))
        
        # Evitar crear más hilos que chunks
        if optimal_thread_count > len(chunks):
            optimal_thread_count = len(chunks)
        
        for _ in range(optimal_thread_count):
            thread = threading.Thread(target=optimized_worker)
            thread.daemon = True
            thread.start()
            threads.append(thread)
        
        # Esperar a que terminen todos los hilos
        for thread in threads:
            thread.join(timeout=2)
        
        # Reconstruir imagen completa
        final_lines = self._reconstruct_image(result_dict, image_array.shape)
        
        # Guardar en cache si es beneficioso
        if len(result_dict) == len(chunks):  # Solo si se procesaron todos los chunks
            # Mantener cache limitado en tamaño
            if len(self.frame_cache) >= self.max_cache_size:
                # Remover entrada más antigua (simple FIFO)
                oldest_key = next(iter(self.frame_cache))
                del self.frame_cache[oldest_key]
            
            # Almacenar resultado en cache
            self.frame_cache[frame_hash] = {
                'lines': final_lines,
                'chunks_processed': len(result_dict),
                'timestamp': time.time()
            }
            
            self.previous_frame_hash = frame_hash
        
        # Estadísticas extendidas con métricas dinámicas
        total_time = time.time() - start_time
        avg_chunk_time = sum(r['processing_time'] for r in result_dict.values()) / max(len(result_dict), 1)
        current_fps = 1.0 / total_time if total_time > 0 else 0
        
        stats = {
            'total_time': total_time,
            'chunks_processed': len(result_dict),
            'threads_used': len(threads),
            'dynamic_thread_count': self.current_thread_count,
            'avg_chunk_time': avg_chunk_time,
            'fps': current_fps,
            'cache_hit': False,
            'cache_hits': self.cache_hits,
            'cache_misses': self.cache_misses,
            'cache_size': len(self.frame_cache)
        }
        
        # Registrar métricas para auto-tuning
        self.performance_history.append(stats.copy())
        
        # Mantener historial limitado (últimos 20 frames)
        if len(self.performance_history) > 20:
            self.performance_history.pop(0)
        
        return final_lines, stats
    
    def _reconstruct_image(self, result_dict: dict, original_shape: tuple) -> List[str]:
        """Reconstruye la imagen completa desde los chunks procesados correctamente"""
        if not result_dict:
            return []
        
        height, width = original_shape[:2]
        
        # Determinar dimensiones de la cuadrícula de chunks
        unique_rows = set(chunk_data['start_row'] for chunk_data in result_dict.values())
        unique_cols = set(chunk_data['start_col'] for chunk_data in result_dict.values())
        
        chunks_vertical = len(unique_rows)
        chunks_horizontal = len(unique_cols)
        
        # Crear matriz de chunks organizados por posición
        chunk_matrix = {}
        for chunk_id, chunk_data in result_dict.items():
            start_row = chunk_data['start_row']
            start_col = chunk_data['start_col']
            
            # Encontrar índices de fila y columna en la cuadrícula
            row_idx = sorted(unique_rows).index(start_row)
            col_idx = sorted(unique_cols).index(start_col)
            
            chunk_matrix[(row_idx, col_idx)] = chunk_data['lines']
        
        # Reconstruir imagen línea por línea, intercalando chunks horizontalmente
        final_lines = []
        
        # Para cada fila de chunks
        for chunk_row in range(chunks_vertical):
            # Encontrar la altura máxima de los chunks en esta fila
            max_chunk_height = 0
            for chunk_col in range(chunks_horizontal):
                if (chunk_row, chunk_col) in chunk_matrix:
                    chunk_lines = chunk_matrix[(chunk_row, chunk_col)]
                    max_chunk_height = max(max_chunk_height, len(chunk_lines))
            
            # Para cada línea dentro de los chunks de esta fila
            for line_idx in range(max_chunk_height):
                combined_line = ""
                
                # Combinar horizontalmente los chunks de esta fila
                for chunk_col in range(chunks_horizontal):
                    if (chunk_row, chunk_col) in chunk_matrix:
                        chunk_lines = chunk_matrix[(chunk_row, chunk_col)]
                        if line_idx < len(chunk_lines):
                            combined_line += chunk_lines[line_idx]
                        else:
                            # Rellenar con espacios si el chunk es más corto
                            if chunk_lines:  # Solo si el chunk tiene líneas
                                chunk_width = len(chunk_lines[0]) if chunk_lines else 0
                                combined_line += " " * chunk_width
                
                if combined_line.strip():  # Solo agregar líneas no vacías
                    final_lines.append(combined_line)
        
        return final_lines