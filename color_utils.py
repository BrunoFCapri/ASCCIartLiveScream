#!/usr/bin/env python3
"""
Utilidades de color para el transformador ASCII
Maneja conversiones RGB a ANSI y diferentes modos de color
"""

import colorsys
from config import *

class ColorConverter:
    def __init__(self):
        """Inicializa el convertidor de colores"""
        # Paleta básica de 8 colores ANSI
        self.basic_colors = [
            (0, 0, 0),       # Negro
            (128, 0, 0),     # Rojo oscuro
            (0, 128, 0),     # Verde oscuro
            (128, 128, 0),   # Amarillo oscuro
            (0, 0, 128),     # Azul oscuro
            (128, 0, 128),   # Magenta oscuro
            (0, 128, 128),   # Cian oscuro
            (192, 192, 192), # Gris claro
        ]
        
        # Paleta extendida de colores brillantes
        self.bright_colors = [
            (128, 128, 128), # Gris oscuro
            (255, 0, 0),     # Rojo brillante
            (0, 255, 0),     # Verde brillante
            (255, 255, 0),   # Amarillo brillante
            (0, 0, 255),     # Azul brillante
            (255, 0, 255),   # Magenta brillante
            (0, 255, 255),   # Cian brillante
            (255, 255, 255), # Blanco
        ]
        
        self.all_basic_colors = self.basic_colors + self.bright_colors
    
    def rgb_to_ansi_basic(self, r, g, b):
        """
        Convierte RGB a código ANSI de 8 colores básicos
        
        Args:
            r, g, b: Valores RGB (0-255)
        
        Returns:
            str: Código ANSI para el color más cercano
        """
        # Encontrar el color más cercano en la paleta básica
        min_distance = float('inf')
        closest_color_index = 0
        
        for i, (cr, cg, cb) in enumerate(self.all_basic_colors):
            # Calcular distancia euclidiana en el espacio RGB
            distance = ((r - cr) ** 2 + (g - cg) ** 2 + (b - cb) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                closest_color_index = i
        
        # Convertir índice a código ANSI
        if closest_color_index < 8:
            return f"\033[{30 + closest_color_index}m"
        else:
            return f"\033[{82 + closest_color_index}m"  # Colores brillantes
    
    def rgb_to_ansi_256(self, r, g, b):
        """
        Convierte RGB a código ANSI de 256 colores
        
        Args:
            r, g, b: Valores RGB (0-255)
        
        Returns:
            str: Código ANSI para color de 256 colores
        """
        # Convertir RGB a índice de 256 colores
        # Fórmula estándar para terminal de 256 colores
        if r == g == b:
            # Escala de grises
            if r < 8:
                color_index = 16
            elif r > 248:
                color_index = 231
            else:
                color_index = 232 + int((r - 8) / 10)
        else:
            # Colores RGB
            color_index = 16 + (36 * int(r / 51)) + (6 * int(g / 51)) + int(b / 51)
        
        return f"\033[38;5;{color_index}m"
    
    def rgb_to_ansi_truecolor(self, r, g, b):
        """
        Convierte RGB a código ANSI de color verdadero (24-bit)
        
        Args:
            r, g, b: Valores RGB (0-255)
        
        Returns:
            str: Código ANSI para color verdadero
        """
        return f"\033[38;2;{r};{g};{b}m"
    
    def get_background_color(self, r, g, b, mode="truecolor"):
        """
        Obtiene código ANSI para color de fondo
        
        Args:
            r, g, b: Valores RGB (0-255)
            mode: Modo de color ("basic", "extended", "truecolor")
        
        Returns:
            str: Código ANSI para color de fondo
        """
        if mode == "basic":
            # Para colores básicos, usar códigos de fondo
            return self.rgb_to_ansi_basic(r, g, b).replace("3", "4").replace("9", "10")
        elif mode == "extended":
            return f"\033[48;5;{self._rgb_to_256_index(r, g, b)}m"
        else:  # truecolor
            return f"\033[48;2;{r};{g};{b}m"
    
    def _rgb_to_256_index(self, r, g, b):
        """Convierte RGB a índice de 256 colores (helper)"""
        if r == g == b:
            if r < 8:
                return 16
            elif r > 248:
                return 231
            else:
                return 232 + int((r - 8) / 10)
        else:
            return 16 + (36 * int(r / 51)) + (6 * int(g / 51)) + int(b / 51)
    
    def enhance_color(self, r, g, b, intensity="medium"):
        """
        Mejora la intensidad del color
        
        Args:
            r, g, b: Valores RGB (0-255)
            intensity: "low", "medium", "high"
        
        Returns:
            tuple: RGB mejorado
        """
        factor = COLOR_INTENSITY.get(intensity, 1.0)
        
        # Convertir a HSV para manipular saturación
        h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
        
        # Aumentar saturación según la intensidad
        s = min(1.0, s * factor)
        v = min(1.0, v * factor)
        
        # Convertir de vuelta a RGB
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        
        return int(r * 255), int(g * 255), int(b * 255)
    
    def get_dominant_color(self, image_region):
        """
        Obtiene el color dominante de una región de imagen
        
        Args:
            image_region: PIL.Image region
        
        Returns:
            tuple: RGB del color dominante
        """
        # Redimensionar a 1x1 para obtener color promedio
        tiny = image_region.resize((1, 1))
        return tiny.getpixel((0, 0))
    
    def color_distance(self, color1, color2):
        """
        Calcula la distancia entre dos colores RGB
        
        Args:
            color1, color2: tuplas RGB
        
        Returns:
            float: Distancia entre colores
        """
        r1, g1, b1 = color1
        r2, g2, b2 = color2
        return ((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2) ** 0.5
    
    def should_use_background_color(self, r, g, b, char_density):
        """
        Determina si usar color de fondo en lugar de texto
        
        Args:
            r, g, b: Valores RGB
            char_density: Densidad del carácter (0.0 a 1.0)
        
        Returns:
            bool: True si usar color de fondo
        """
        brightness = (r + g + b) / 3
        return brightness > COLOR_THRESHOLD and char_density < 0.5


def test_colors():
    """Función de prueba para mostrar colores disponibles"""
    converter = ColorConverter()
    
    print("🎨 PRUEBA DE COLORES ASCII")
    print("=" * 50)
    
    # Probar colores básicos
    print("\n🌈 Colores básicos (8 colores):")
    test_colors_rgb = [
        (255, 0, 0),    # Rojo
        (0, 255, 0),    # Verde
        (0, 0, 255),    # Azul
        (255, 255, 0),  # Amarillo
        (255, 0, 255),  # Magenta
        (0, 255, 255),  # Cian
        (255, 255, 255),# Blanco
        (128, 128, 128) # Gris
    ]
    
    for r, g, b in test_colors_rgb:
        ansi_code = converter.rgb_to_ansi_basic(r, g, b)
        print(f"{ansi_code}████ RGB({r},{g},{b})\033[0m")
    
    # Probar colores de 256
    print("\n🎯 Colores extendidos (256 colores) - Muestra:")
    for i in range(0, 256, 32):
        r = (i * 3) % 256
        g = (i * 5) % 256  
        b = (i * 7) % 256
        ansi_code = converter.rgb_to_ansi_256(r, g, b)
        print(f"{ansi_code}██\033[0m", end="")
    print()
    
    # Probar colores verdaderos
    print("\n✨ Colores verdaderos (RGB) - Degradado:")
    for i in range(0, 256, 8):
        ansi_code = converter.rgb_to_ansi_truecolor(i, 255-i, 128)
        print(f"{ansi_code}█\033[0m", end="")
    print()
    
    print("\n✅ Prueba de colores completada!")


if __name__ == "__main__":
    test_colors()