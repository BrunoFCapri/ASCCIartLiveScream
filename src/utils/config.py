"""
Configuración del transformador ASCII multihilo
"""
import os
from typing import Dict, List, Tuple

# Configuración de ASCII
ASCII_CHARS = {
    'detailed': [".", ",", ":", ";", "+", "*", "?", "%", "S", "#", "@"],
    'gradient': [".", ":", "-", "=", "+", "*", "#", "%", "@"],
    'blocks': [" ", "░", "▒", "▓", "█"],
    'simple': [".", "-", "+", "#", "@"]
}

# Configuración de rendimiento
DEFAULT_FPS = 15
MAX_FPS = 60
DEFAULT_WIDTH_SCALE = 0.95
ASPECT_RATIO_CORRECTION = 0.55

# Configuración de threading
DEFAULT_THREAD_COUNT = 4  # Número de hilos para procesamiento
MAX_THREAD_COUNT = 8
CHUNK_OVERLAP = 2  # Píxeles de superposición entre chunks

# Configuración de colores
COLOR_MODES = {
    'grayscale': 0,
    'basic': 1,
    'extended': 2,
    'truecolor': 3
}

# Paleta básica ANSI (8 colores)
ANSI_BASIC_COLORS = [
    (0, 0, 0),       # Negro
    (128, 0, 0),     # Rojo oscuro
    (0, 128, 0),     # Verde oscuro
    (128, 128, 0),   # Amarillo oscuro
    (0, 0, 128),     # Azul oscuro
    (128, 0, 128),   # Magenta oscuro
    (0, 128, 128),   # Cian oscuro
    (192, 192, 192), # Gris claro
]

# Paleta extendida ANSI (16 colores)
ANSI_EXTENDED_COLORS = ANSI_BASIC_COLORS + [
    (128, 128, 128), # Gris oscuro
    (255, 0, 0),     # Rojo brillante
    (0, 255, 0),     # Verde brillante
    (255, 255, 0),   # Amarillo brillante
    (0, 0, 255),     # Azul brillante
    (255, 0, 255),   # Magenta brillante
    (0, 255, 255),   # Cian brillante
    (255, 255, 255), # Blanco
]

# Configuración de terminal
CLEAR_SCREEN = "\033[2J\033[H"
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"
RESET_COLOR = "\033[0m"

def get_optimal_thread_count() -> int:
    """Calcula el número óptimo de hilos basado en el CPU"""
    cpu_count = os.cpu_count() or 4
    return min(max(2, cpu_count // 2), MAX_THREAD_COUNT)

# ==================== THREADING DINÁMICO AVANZADO ====================

def calculate_dynamic_thread_count(total_characters: int, color_mode: int = 0, 
                                 image_dimensions: tuple = None) -> int:
    """
    Calcula dinámicamente el número óptimo de hilos basado en:
    - Cantidad total de caracteres a procesar
    - Modo de color (afecta complejidad de procesamiento)
    - Dimensiones de la imagen
    """
    cpu_count = os.cpu_count() or 4
    
    # Factores de complejidad
    color_complexity_factor = {
        0: 1.0,    # Escala de grises (más rápido)
        1: 1.3,    # 8 colores básicos
        2: 1.5,    # 16 colores extendidos
        3: 2.0,    # 256 colores
        4: 2.5     # Truecolor (más lento)
    }.get(color_mode, 1.5)
    
    # Calcular carga de trabajo total
    effective_load = total_characters * color_complexity_factor
    
    # Umbrales dinámicos basados en carga
    if effective_load < 5000:
        # Trabajo pequeño - pocos hilos para evitar overhead
        optimal_threads = min(2, cpu_count)
    elif effective_load < 25000:
        # Trabajo mediano - usar hilos moderados
        optimal_threads = min(4, cpu_count)
    elif effective_load < 100000:
        # Trabajo grande - aprovechar más hilos
        optimal_threads = min(cpu_count, MAX_THREAD_COUNT)
    else:
        # Trabajo muy grande - usar todos los hilos disponibles
        optimal_threads = min(cpu_count + 2, MAX_THREAD_COUNT)
    
    # Ajuste basado en dimensiones si están disponibles
    if image_dimensions:
        width, height = image_dimensions[:2]
        aspect_ratio = width / height if height > 0 else 1.0
        
        # Para imágenes muy anchas o altas, usar más hilos
        if aspect_ratio > 3.0 or aspect_ratio < 0.33:
            optimal_threads = min(optimal_threads + 1, MAX_THREAD_COUNT)
    
    return max(1, optimal_threads)

def calculate_optimal_chunk_distribution(total_characters: int, thread_count: int, 
                                       image_shape: tuple) -> tuple:
    """
    Calcula la distribución óptima de chunks FAVORIZANDO DIVISIÓN POR FILAS:
    - Total de caracteres
    - Número de hilos  
    - Forma de la imagen
    """
    height, width = image_shape[:2]
    
    # ESTRATEGIA: Dividir principalmente por filas para evitar problemas de reconstrucción
    # Solo usar división horizontal (chunks_horizontal = 1) a menos que sea absolutamente necesario
    
    chunks_horizontal = 1  # Preferir siempre 1 columna de chunks
    chunks_vertical = min(thread_count, height // 10)  # Al menos 10 filas por chunk
    
    # Asegurar que no tengamos más chunks que filas disponibles
    chunks_vertical = min(chunks_vertical, height)
    
    # Si tenemos muy pocos chunks comparado con los hilos disponibles, 
    # considerar división horizontal solo si es realmente necesario
    if chunks_vertical < thread_count and width > height:
        # Solo para imágenes muy anchas, permitir división horizontal
        chunks_horizontal = min(2, thread_count // chunks_vertical)
        
    # Asegurar valores mínimos
    chunks_horizontal = max(1, chunks_horizontal)
    chunks_vertical = max(1, chunks_vertical)
    
    return (chunks_horizontal, chunks_vertical)

def get_performance_metrics():
    """
    Obtiene métricas de rendimiento del sistema
    Returns:
        dict: Métricas de CPU, memoria y disco (o valores por defecto si psutil no está disponible)
    """
    try:
        import psutil
        return {
            'cpu_percent': psutil.cpu_percent(interval=0.1),
            'memory_percent': psutil.virtual_memory().percent,
            'available_memory': psutil.virtual_memory().available,
            'disk_usage': psutil.disk_usage('/').percent if psutil.disk_usage('/') else 0
        }
    except ImportError:
        # Valores por defecto cuando psutil no está disponible
        return {
            'cpu_percent': 50.0,  # Asume carga media
            'memory_percent': 60.0,  # Asume uso medio de memoria
            'available_memory': 1024 * 1024 * 1024,  # 1GB por defecto
            'disk_usage': 50.0
        }

def auto_tune_thread_count(base_thread_count: int, performance_history: list) -> int:
    """
    Auto-tunea el número de hilos basado en historial de rendimiento
    """
    try:
        if len(performance_history) < 3:
            return base_thread_count
        
        # Analizar tendencia de rendimiento
        recent_fps = [p.get('fps', 0) for p in performance_history[-5:]]
        avg_fps = sum(recent_fps) / len(recent_fps)
        
        # Obtener métricas actuales del sistema
        metrics = get_performance_metrics()
        
        # Decidir ajuste basado en rendimiento y carga del sistema
        cpu_key = 'cpu_percent' if 'cpu_percent' in metrics else 'cpu_usage'
        memory_key = 'memory_percent' if 'memory_percent' in metrics else 'memory_usage'
        
        if avg_fps < 15 and metrics[cpu_key] < 70:
            # Rendimiento bajo pero CPU disponible - aumentar hilos
            return min(base_thread_count + 1, MAX_THREAD_COUNT)
        elif avg_fps > 35 and metrics[cpu_key] > 85:
            # Rendimiento alto pero CPU saturada - reducir hilos
            return max(base_thread_count - 1, 2)
        elif metrics[memory_key] > 80:
            # Memoria alta - reducir ligeramente hilos
            return max(base_thread_count - 1, 2)
        
        return base_thread_count
    
    except Exception as e:
        # En caso de error, mantener la cantidad actual de hilos
        return base_thread_count

def rgb_to_ansi_basic(r: int, g: int, b: int) -> int:
    """Convierte RGB a color ANSI básico (8 colores)"""
    # Mapear a los colores básicos más cercanos
    colors = [
        30,  # Negro
        31,  # Rojo
        32,  # Verde
        33,  # Amarillo
        34,  # Azul
        35,  # Magenta
        36,  # Cian
        37   # Blanco
    ]
    
    # Calcular brillo promedio
    brightness = (r + g + b) // 3
    
    # Determinar color dominante
    if r > g and r > b:
        return 31 if brightness > 127 else 31  # Rojo
    elif g > r and g > b:
        return 32 if brightness > 127 else 32  # Verde
    elif b > r and b > g:
        return 34 if brightness > 127 else 34  # Azul
    elif r > 200 and g > 200 and b < 100:
        return 33  # Amarillo
    elif r > 150 and b > 150 and g < 100:
        return 35  # Magenta
    elif g > 150 and b > 150 and r < 100:
        return 36  # Cian
    elif brightness > 200:
        return 37  # Blanco
    elif brightness < 50:
        return 30  # Negro
    else:
        return 37  # Por defecto blanco

def rgb_to_ansi_extended(r: int, g: int, b: int) -> int:
    """Convierte RGB a color ANSI extendido (16 colores)"""
    basic_color = rgb_to_ansi_basic(r, g, b)
    brightness = (r + g + b) // 3
    
    # Si es brillante, usar la versión brillante (90-97)
    if brightness > 150:
        return basic_color + 60  # Convertir a brillante
    return basic_color

def rgb_to_ansi_256(r: int, g: int, b: int) -> int:
    """Convierte RGB a color ANSI de 256 colores"""
    # Convertir de 0-255 a 0-5 para cada componente
    r_256 = min(5, r * 6 // 256)
    g_256 = min(5, g * 6 // 256)
    b_256 = min(5, b * 6 // 256)
    
    # Fórmula para colores de 256: 16 + 36*r + 6*g + b
    return 16 + 36 * r_256 + 6 * g_256 + b_256

def rgb_to_ansi_truecolor(r: int, g: int, b: int) -> str:
    """Convierte RGB a color ANSI truecolor (24-bit)"""
    return f"38;2;{r};{g};{b}"

def get_color_escape(color_mode: int, r: int, g: int, b: int) -> str:
    """Obtiene el código de escape ANSI para el color especificado"""
    if color_mode == 0:  # Grayscale
        return ""
    elif color_mode == 1:  # Basic (8 colors)
        color_code = rgb_to_ansi_basic(r, g, b)
        return f"\033[{color_code}m"
    elif color_mode == 2:  # Extended (16 colors)
        color_code = rgb_to_ansi_extended(r, g, b)
        return f"\033[{color_code}m"
    elif color_mode == 3:  # 256 colors
        color_code = rgb_to_ansi_256(r, g, b)
        return f"\033[38;5;{color_code}m"
    elif color_mode == 4:  # Truecolor
        color_code = rgb_to_ansi_truecolor(r, g, b)
        return f"\033[{color_code}m"
    return ""

def distance_rgb(rgb1: Tuple[int, int, int], rgb2: Tuple[int, int, int]) -> float:
    """Calcula la distancia euclidiana entre dos colores RGB"""
    return ((rgb1[0] - rgb2[0]) ** 2 + (rgb1[1] - rgb2[1]) ** 2 + (rgb1[2] - rgb2[2]) ** 2) ** 0.5

# ==================== OPTIMIZACIONES DE RENDIMIENTO ====================

# Lookup tables globales para conversión ultrarrápida
_COLOR_LOOKUP_BASIC = None  # Lookup table para colores básicos
_COLOR_LOOKUP_256 = None    # Lookup table para 256 colores
_GRAYSCALE_LOOKUP = None    # Lookup table para escala de grises

def _build_color_lookup_tables():
    """Construye lookup tables para conversión ultrarrápida de colores"""
    global _COLOR_LOOKUP_BASIC, _COLOR_LOOKUP_256, _GRAYSCALE_LOOKUP
    
    if _COLOR_LOOKUP_BASIC is not None:
        return  # Ya construidas
    
    import numpy as np
    
    # Crear lookup table básica (8 bits por canal = 16M combinaciones reducidas)
    # Reducimos a 64x64x64 para ahorrar memoria pero mantener velocidad
    lookup_size = 64
    _COLOR_LOOKUP_BASIC = np.zeros((lookup_size, lookup_size, lookup_size), dtype=np.uint8)
    _COLOR_LOOKUP_256 = np.zeros((lookup_size, lookup_size, lookup_size), dtype=np.uint16)
    _GRAYSCALE_LOOKUP = np.zeros(256, dtype=np.uint8)
    
    # Pre-calcular conversiones de escala de grises
    for i in range(256):
        # Usar fast integer division
        _GRAYSCALE_LOOKUP[i] = i >> 4  # Equivale a i // 16, más rápido
    
    # Pre-calcular conversiones de color
    step = 256 // lookup_size
    for r in range(lookup_size):
        for g in range(lookup_size):
            for b in range(lookup_size):
                # Convertir índices de vuelta a RGB
                rgb_r = r * step
                rgb_g = g * step
                rgb_b = b * step
                
                # Conversión básica optimizada
                brightness = (rgb_r + rgb_g + rgb_b) // 3
                if rgb_r > rgb_g and rgb_r > rgb_b and brightness > 127:
                    _COLOR_LOOKUP_BASIC[r, g, b] = 31  # Rojo
                elif rgb_g > rgb_r and rgb_g > rgb_b and brightness > 127:
                    _COLOR_LOOKUP_BASIC[r, g, b] = 32  # Verde  
                elif rgb_b > rgb_r and rgb_b > rgb_g and brightness > 127:
                    _COLOR_LOOKUP_BASIC[r, g, b] = 34  # Azul
                elif brightness > 200:
                    _COLOR_LOOKUP_BASIC[r, g, b] = 37  # Blanco
                elif brightness < 50:
                    _COLOR_LOOKUP_BASIC[r, g, b] = 30  # Negro
                else:
                    _COLOR_LOOKUP_BASIC[r, g, b] = 37  # Default blanco
                
                # Conversión 256 colores optimizada
                r_256 = min(5, rgb_r * 6 >> 8)  # Más rápido que // 256
                g_256 = min(5, rgb_g * 6 >> 8)
                b_256 = min(5, rgb_b * 6 >> 8)
                _COLOR_LOOKUP_256[r, g, b] = 16 + 36 * r_256 + 6 * g_256 + b_256

def get_color_escape_fast(color_mode: int, r: int, g: int, b: int) -> str:
    """Versión ultrarrápida de get_color_escape usando lookup tables"""
    global _COLOR_LOOKUP_BASIC, _COLOR_LOOKUP_256, _GRAYSCALE_LOOKUP
    
    if _COLOR_LOOKUP_BASIC is None:
        _build_color_lookup_tables()
    
    if color_mode == 0:  # Grayscale
        return ""
    elif color_mode == 1:  # Basic (8 colors)
        # Reducir resolución para lookup
        r_idx = min(63, r >> 2)  # r // 4, más rápido
        g_idx = min(63, g >> 2)
        b_idx = min(63, b >> 2)
        color_code = _COLOR_LOOKUP_BASIC[r_idx, g_idx, b_idx]
        return f"\033[{color_code}m"
    elif color_mode == 2:  # Extended (16 colors) - usar básico + brillo
        r_idx = min(63, r >> 2)
        g_idx = min(63, g >> 2)
        b_idx = min(63, b >> 2)
        basic_color = _COLOR_LOOKUP_BASIC[r_idx, g_idx, b_idx]
        brightness = (r + g + b) // 3
        if brightness > 150:
            color_code = basic_color + 60  # Versión brillante
        else:
            color_code = basic_color
        return f"\033[{color_code}m"
    elif color_mode == 3:  # 256 colors
        r_idx = min(63, r >> 2)
        g_idx = min(63, g >> 2)
        b_idx = min(63, b >> 2)
        color_code = _COLOR_LOOKUP_256[r_idx, g_idx, b_idx]
        return f"\033[38;5;{color_code}m"
    elif color_mode == 4:  # Truecolor - no lookup, ya es rápido
        return f"\033[38;2;{r};{g};{b}m"
    return ""

# Constantes para optimización de strings
RESET_COLOR_CACHED = "\033[0m"
COLOR_FORMAT_BASIC = "\033[{}m"
COLOR_FORMAT_256 = "\033[38;5;{}m"
COLOR_FORMAT_TRUECOLOR = "\033[38;2;{};{};{}m"

# Logging settings
LOG_PERFORMANCE = True  # Enable or disable performance logging
LOG_FILE_PATH = "performance.log"  # Path to the log file for performance metrics