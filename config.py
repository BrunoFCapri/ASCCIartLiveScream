# Configuración del Transformador de Pantalla a ASCII

# Caracteres ASCII por densidad (de claro a oscuro)
ASCII_CHARS_DETAILED = [".", ",", ":", ";", "+", "*", "?", "%", "S", "#", "@"]
ASCII_CHARS_SIMPLE = [" ", "░", "▒", "▓", "█"]
ASCII_CHARS_GRADIENT = ["@", "%", "#", "*", "+", "=", "-", ":", ".", " "]

# Configuración de rendimiento (optimizada)
DEFAULT_FPS = 15  # Aumentado para mejor fluidez
MAX_FPS = 60     # Máximo aumentado
MIN_FPS = 1

# Configuración de imagen (tamaño dinámico grande)
DEFAULT_WIDTH_SCALE = 0.95  # Usar 95% del ancho de la terminal (más grande)
ASPECT_RATIO_CORRECTION = 0.55  # Corrección para caracteres más altos que anchos

# Configuración de terminal
DEFAULT_TERMINAL_WIDTH = 80
DEFAULT_TERMINAL_HEIGHT = 24

# Configuración de colores
COLOR_MODES = {
    "grayscale": "Escala de grises (sin color)",
    "basic": "8 colores básicos ANSI", 
    "extended": "256 colores extendidos",
    "truecolor": "16.7M colores RGB verdaderos"
}

# Códigos ANSI para colores básicos
ANSI_COLORS_BASIC = {
    "black": "\033[30m",
    "red": "\033[31m", 
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "reset": "\033[0m"
}

# Configuración de intensidad de color
COLOR_INTENSITY = {
    "low": 0.7,      # Colores más suaves
    "medium": 1.0,   # Colores normales
    "high": 1.3      # Colores más vivos
}

# Umbral para mapeo de colores
COLOR_THRESHOLD = 128  # Punto medio para determinar colores oscuros/claros
COLOR_SENSITIVITY = 50  # Sensibilidad para detectar diferencias de color

# Mensajes
MESSAGES = {
    "starting": "🎥 Iniciando captura de pantalla a ASCII...",
    "stop_instruction": "⚠️  Presiona Ctrl+C para detener",
    "fps_info": "📺 FPS: {}",
    "countdown": "⏳ Iniciando en {} segundos...",
    "stopping": "\n🛑 Deteniendo captura...",
    "finished": "✅ ¡Programa terminado!",
    "goodbye": "👋 ¡Hasta luego!",
    "error": "❌ Error: {}",
    "invalid_option": "❌ Opción inválida",
    "region_top_left": "Mueve el mouse a la esquina superior izquierda y presiona Enter...",
    "region_bottom_right": "Mueve el mouse a la esquina inferior derecha y presiona Enter...",
    "region_selected": "Región seleccionada: {}",
    "color_mode": "🎨 Modo de color: {}",
    "color_preview": "Vista previa de colores disponible"
}