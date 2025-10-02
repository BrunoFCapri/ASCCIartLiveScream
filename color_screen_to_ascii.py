#!/usr/bin/env python3
"""
Transformador de pantalla a ASCII CON COLORES
Versión mejorada que incluye soporte completo para colores ANSI
"""

import pyautogui
import os
import time
import shutil
import threading
from PIL import Image
from colorama import init, Fore, Back, Style
from config import *
from color_utils import ColorConverter

# Inicializar colorama para Windows
init()

class ColorScreenToASCII:
    def __init__(self, ascii_style="detailed", color_mode="truecolor", invert_colors=False):
        """
        Inicializa el convertidor con soporte para colores
        
        Args:
            ascii_style: "detailed", "simple", o "gradient"
            color_mode: "grayscale", "basic", "extended", "truecolor"
            invert_colors: True para invertir la relación brillo-carácter
        """
        self.ascii_styles = {
            "detailed": ASCII_CHARS_DETAILED,
            "simple": ASCII_CHARS_SIMPLE,
            "gradient": ASCII_CHARS_GRADIENT
        }
        
        self.ascii_chars = self.ascii_styles.get(ascii_style, ASCII_CHARS_DETAILED)
        if invert_colors:
            self.ascii_chars = self.ascii_chars[::-1]  # Invertir el orden
        self.color_mode = color_mode
        self.color_converter = ColorConverter()
        pyautogui.FAILSAFE = False
        
        # Variables para estadísticas
        self.frame_count = 0
        self.start_time = None
        self.last_fps_update = 0
        self.current_fps = 0
        
        # Cache para optimización
        self._cached_terminal_size = None
        self._last_screenshot = None
        self._adaptive_sizing = True  # Habilitar tamaño adaptativo
        
        # Cache de códigos de color para máxima velocidad
        self._color_cache = {}
        self._cache_hits = 0
        self._cache_misses = 0
        
    def capture_screen_fast(self, region=None):
        """Captura ULTRA-rápida de pantalla con máximas optimizaciones"""
        try:
            # Captura optimizada
            screenshot = pyautogui.screenshot(region=region) if region else pyautogui.screenshot()
            
            # Optimización: Convertir inmediatamente a RGB si es necesario
            if screenshot.mode != 'RGB':
                screenshot = screenshot.convert('RGB')
            
            # Optimización adicional: Pre-cargar datos de píxeles para acelerar getdata()
            screenshot.load()
                
            return screenshot
        except Exception as e:
            return None
    
    def get_terminal_size(self):
        """Obtiene el tamaño actual de la terminal de forma dinámica"""
        # Actualizar cache cada cierto número de frames para detectar cambios de tamaño
        if self._cached_terminal_size is None or self.frame_count % 30 == 0:
            try:
                columns, rows = shutil.get_terminal_size()
                self._cached_terminal_size = (columns, rows)
            except:
                self._cached_terminal_size = (DEFAULT_TERMINAL_WIDTH, DEFAULT_TERMINAL_HEIGHT)
        return self._cached_terminal_size
    
    def resize_image_fast(self, image, max_width=None, max_height=None):
        """Redimensiona la imagen de forma dinámica y grande"""
        if self._adaptive_sizing and max_width is None and max_height is None:
            # Usar tamaño adaptativo inteligente
            max_width, max_height = self.get_adaptive_size(image)
        elif max_width is None or max_height is None:
            columns, rows = self.get_terminal_size()
            # Usar tamaño grande y dinámico
            max_width = int(columns * DEFAULT_WIDTH_SCALE)
            max_height = rows - 3
            
        width, height = image.size
        aspect_ratio = height / width
        
        # Calcular nuevo tamaño manteniendo proporción
        new_width = min(max_width, width)
        new_height = int(aspect_ratio * new_width * ASPECT_RATIO_CORRECTION)
        
        # Ajustar si excede la altura máxima
        if new_height > max_height:
            new_height = max_height
            new_width = int(new_height / aspect_ratio / ASPECT_RATIO_CORRECTION)
        
        # Asegurar tamaños mínimos para buena visualización
        new_width = max(new_width, 40)  # Mínimo 40 caracteres de ancho
        new_height = max(new_height, 20)  # Mínimo 20 líneas de alto
        
        # Usar método de alta calidad para mejor resultado visual
        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    def get_adaptive_size(self, image):
        """Calcula el tamaño óptimo basado en la terminal y la imagen"""
        columns, rows = self.get_terminal_size()
        
        # Usar el máximo espacio disponible
        max_width = int(columns * DEFAULT_WIDTH_SCALE)
        max_height = rows - 4  # Reservar espacio para información
        
        # Si la imagen es muy pequeña, no la hagamos más grande que su tamaño original
        img_width, img_height = image.size
        if img_width < max_width and img_height < max_height:
            # Usar tamaño de imagen pero ajustado al ratio de aspecto correcto
            aspect_ratio = img_height / img_width
            new_height = int(img_width * aspect_ratio * ASPECT_RATIO_CORRECTION)
            if new_height <= max_height:
                return img_width, new_height
        
        # Usar el tamaño máximo disponible
        return max_width, max_height
    
    def image_to_ascii_fast(self, image, color_intensity="medium"):
        """
        Conversión ULTRA-RÁPIDA de imagen a ASCII con colores
        Optimizada al máximo sin perder funcionalidad
        """
        # Conversión más eficiente
        grayscale_image = image.convert("L")
        
        # Obtener datos como listas para acceso directo por índice
        color_pixels = list(image.getdata())
        gray_pixels = list(grayscale_image.getdata())
        width, height = image.size
        
        # Pre-calcular todos los valores necesarios
        chars_len = len(self.ascii_chars)
        gray_factor = (chars_len - 1) / 255
        reset_code = "\033[0m"
        chars_len_minus_1 = chars_len - 1  # Pre-calcular para evitar resta repetida
        
        # Crear lista de líneas con capacidad pre-asignada
        ascii_lines = []
        ascii_lines_append = ascii_lines.append  # Cache del método
        
        # Cache de funciones y valores para evitar lookups
        ascii_chars = self.ascii_chars
        color_mode = self.color_mode
        get_cached_color_code = self.get_cached_color_code  # Cache del método
        
        # Pre-calcular tabla de conversión gris->ASCII para máxima velocidad
        gray_to_ascii = []
        for i in range(256):
            ascii_index = int(i * gray_factor)
            if ascii_index > chars_len_minus_1:
                ascii_index = chars_len_minus_1
            gray_to_ascii.append(ascii_chars[ascii_index])
        
        # Optimización adicional: usar operador de acceso directo
        gray_to_ascii_get = gray_to_ascii.__getitem__
        
        # Procesamiento optimizado por filas
        for y in range(height):
            # Pre-asignar lista con tamaño conocido
            line_chars = [''] * width
            row_start = y * width
            
            # Bucle interno ultra-optimizado
            for x in range(width):
                pixel_idx = row_start + x
                
                # Acceso directo por índice (más rápido que next())
                r, g, b = color_pixels[pixel_idx]
                gray_value = gray_pixels[pixel_idx]
                
                # Cálculo de carácter ULTRA-optimizado usando tabla pre-calculada
                char = gray_to_ascii_get(gray_value)
                
                # Procesamiento de color con cache ultra-optimizado
                if color_mode == "grayscale":
                    line_chars[x] = char
                else:
                    # Usar cache de colores para máxima velocidad
                    color_code = get_cached_color_code(r, g, b)
                    line_chars[x] = color_code + char + reset_code
            
            # Unir caracteres de la línea
            ascii_lines_append("".join(line_chars))
        
        return "\n".join(ascii_lines)
    
    def get_cached_color_code(self, r, g, b):
        """Cache ultra-rápido para códigos de color"""
        # Crear clave de cache más eficiente
        color_key = (r, g, b, self.color_mode)
        
        # Verificar cache
        if color_key in self._color_cache:
            self._cache_hits += 1
            return self._color_cache[color_key]
        
        # Calcular código de color
        if self.color_mode == "truecolor":
            color_code = "\033[38;2;" + str(r) + ";" + str(g) + ";" + str(b) + "m"
        elif self.color_mode == "extended":
            color_code = self.color_converter.rgb_to_ansi_256(r, g, b)
        else:  # basic
            color_code = self.color_converter.rgb_to_ansi_basic(r, g, b)
        
        # Guardar en cache (limitar tamaño del cache)
        if len(self._color_cache) < 1000:  # Límite de 1000 colores en cache
            self._color_cache[color_key] = color_code
        
        self._cache_misses += 1
        return color_code
    
    def image_to_ascii_blocks(self, image, color_intensity="medium"):
        """
        Conversión usando bloques de color de fondo (alternativa visual)
        
        Args:
            image: PIL.Image a convertir
            color_intensity: intensidad del color
        
        Returns:
            str: ASCII art usando colores de fondo
        """
        color_image = image.convert("RGB")
        width, height = image.size
        
        ascii_lines = []
        
        for y in range(height):
            line = ""
            for x in range(width):
                r, g, b = color_image.getpixel((x, y))
                
                # Usar espacio con color de fondo para crear "bloques"
                if self.color_mode != "grayscale":
                    enhanced_r, enhanced_g, enhanced_b = self.color_converter.enhance_color(
                        r, g, b, color_intensity
                    )
                    
                    if self.color_mode == "basic":
                        bg_color = self.color_converter.get_background_color(
                            enhanced_r, enhanced_g, enhanced_b, "basic"
                        )
                    elif self.color_mode == "extended":
                        bg_color = self.color_converter.get_background_color(
                            enhanced_r, enhanced_g, enhanced_b, "extended"
                        )
                    else:  # truecolor
                        bg_color = self.color_converter.get_background_color(
                            enhanced_r, enhanced_g, enhanced_b, "truecolor"
                        )
                    
                    line += f"{bg_color} \033[0m"
                else:
                    # Escala de grises usando caracteres
                    brightness = int((r + g + b) / 3)
                    char_index = min(int(brightness / 255 * (len(self.ascii_chars) - 1)), 
                                   len(self.ascii_chars) - 1)
                    line += self.ascii_chars[char_index]
            
            ascii_lines.append(line)
        
        return "\n".join(ascii_lines)
    
    def clear_screen_fast(self):
        """Limpieza rápida de pantalla sin parpadeo usando códigos ANSI"""
        # Mover cursor al inicio y limpiar desde ahí
        print('\033[H\033[J', end='', flush=True)
    
    def hide_cursor(self):
        """Ocultar el cursor para reducir parpadeo"""
        print('\033[?25l', end='', flush=True)
    
    def show_cursor(self):
        """Mostrar el cursor al finalizar"""
        print('\033[?25h', end='', flush=True)
    
    def calculate_fps(self):
        """Calcula FPS actual"""
        current_time = time.time()
        if self.start_time is None:
            self.start_time = current_time
            self.last_fps_update = current_time
            return 0
        
        self.frame_count += 1
        
        if current_time - self.last_fps_update >= 1.0:
            elapsed = current_time - self.last_fps_update
            self.current_fps = (self.frame_count - 
                              (self.frame_count - int(self.frame_count * elapsed / 
                               (current_time - self.start_time)))) / elapsed
            self.last_fps_update = current_time
        
        return self.current_fps
    
    def run_live_ascii_color(self, fps=DEFAULT_FPS, region=None, show_info=True, 
                            color_intensity="medium", use_blocks=False):
        """
        Versión con colores del convertidor en tiempo real
        
        Args:
            fps: Fotogramas por segundo
            region: Región específica a capturar
            show_info: Mostrar información en tiempo real
            color_intensity: Intensidad del color ("low", "medium", "high")
            use_blocks: Usar bloques de color en lugar de caracteres
        """
        frame_delay = 1.0 / fps
        
        print(MESSAGES["starting"])
        if show_info:
            print(MESSAGES["stop_instruction"])
            print(MESSAGES["fps_info"].format(fps))
            print(MESSAGES["color_mode"].format(COLOR_MODES.get(self.color_mode, self.color_mode)))
            print(f"🎨 Intensidad: {color_intensity}")
            print(f"🔲 Modo bloques: {'Activado' if use_blocks else 'Desactivado'}")
            if region:
                print(f"📏 Región: {region}")
        
        for i in range(3, 0, -1):
            print(MESSAGES["countdown"].format(i))
            time.sleep(1)
        
        # Ocultar cursor para reducir parpadeo
        self.hide_cursor()
        
        self.frame_count = 0
        self.start_time = time.time()
        
        try:
            while True:
                frame_start = time.time()
                
                # Capturar pantalla
                screenshot = self.capture_screen_fast(region)
                if screenshot is None:
                    continue
                
                # Redimensionar imagen (versión rápida)
                resized_image = self.resize_image_fast(screenshot)
                
                # Convertir a ASCII con colores (versión ultra-rápida)
                if use_blocks:
                    ascii_art = self.image_to_ascii_blocks(resized_image, color_intensity)
                else:
                    ascii_art = self.image_to_ascii_fast(resized_image, color_intensity)
                
                # Preparar contenido completo ULTRA-optimizado
                if show_info:
                    current_fps = self.calculate_fps()
                    # Construcción optimizada sin f-strings para mayor velocidad
                    info_parts = [
                        Fore.CYAN,
                        "📊 FPS: ",
                        str(round(current_fps, 1)),
                        " | Frames: ",
                        str(self.frame_count),
                        " | Tamaño: ",
                        str(resized_image.size),
                        " | Modo: ",
                        self.color_mode,
                        Style.RESET_ALL,
                        "\n",
                        "-" * 60,  # Longitud fija para mayor velocidad
                        "\n",
                        ascii_art
                    ]
                    full_content = "".join(info_parts)
                else:
                    full_content = ascii_art
                
                # Limpiar pantalla y mostrar todo de una vez (optimizado)
                self.clear_screen_fast()
                print(full_content, end='', flush=True)
                
                # Control de FPS
                elapsed = time.time() - frame_start
                sleep_time = max(0, frame_delay - elapsed)
                if sleep_time > 0:
                    time.sleep(sleep_time)
                    
        except KeyboardInterrupt:
            # Restaurar cursor
            self.show_cursor()
            print(MESSAGES["stopping"])
            total_time = time.time() - self.start_time
            avg_fps = self.frame_count / total_time if total_time > 0 else 0
            print(f"📈 Estadísticas finales:")
            print(f"   • Frames totales: {self.frame_count}")
            print(f"   • Tiempo total: {total_time:.2f}s")
            print(f"   • FPS promedio: {avg_fps:.2f}")
            print(f"   • Modo de color: {self.color_mode}")
            # Mostrar estadísticas de cache
            total_requests = self._cache_hits + self._cache_misses
            if total_requests > 0:
                cache_rate = (self._cache_hits / total_requests) * 100
                print(f"   • Cache de colores: {cache_rate:.1f}% efectividad ({self._cache_hits}/{total_requests})")
            print(MESSAGES["finished"])
        finally:
            # Asegurar que el cursor siempre se restaure
            self.show_cursor()


def show_color_preview():
    """Muestra una vista previa de los modos de color disponibles"""
    print("\n" + "="*60)
    print("🎨 VISTA PREVIA DE MODOS DE COLOR")
    print("="*60)
    
    converter = ColorConverter()
    
    # Colores de prueba
    test_colors = [
        (255, 0, 0, "Rojo"),
        (0, 255, 0, "Verde"), 
        (0, 0, 255, "Azul"),
        (255, 255, 0, "Amarillo"),
        (255, 0, 255, "Magenta"),
        (0, 255, 255, "Cian")
    ]
    
    print("\n1. 🔲 Colores básicos (8 colores):")
    for r, g, b, name in test_colors:
        color_code = converter.rgb_to_ansi_basic(r, g, b)
        print(f"   {color_code}████ {name}\033[0m")
    
    print("\n2. 🌈 Colores extendidos (256 colores):")
    for r, g, b, name in test_colors:
        color_code = converter.rgb_to_ansi_256(r, g, b)
        print(f"   {color_code}████ {name}\033[0m")
    
    print("\n3. ✨ Colores verdaderos (16.7M colores):")
    for r, g, b, name in test_colors:
        color_code = converter.rgb_to_ansi_truecolor(r, g, b)
        print(f"   {color_code}████ {name}\033[0m")
    
    print("\n4. 🎯 Degradado de ejemplo:")
    print("   ", end="")
    for i in range(50):
        r = int(255 * (i / 50))
        g = int(255 * (1 - i / 50))
        b = 128
        color_code = converter.rgb_to_ansi_truecolor(r, g, b)
        print(f"{color_code}█\033[0m", end="")
    print()


def interactive_region_selector():
    """Selector interactivo de región"""
    print("\n" + "="*50)
    print("📏 SELECTOR DE REGIÓN")
    print("="*50)
    print("Instrucciones:")
    print("1. Minimiza esta ventana")
    print("2. Posiciona el cursor en la esquina superior izquierda")
    print("3. Regresa aquí y presiona Enter")
    
    input("\nPresiona Enter cuando estés listo...")
    x1, y1 = pyautogui.position()
    print(f"✅ Esquina superior izquierda: ({x1}, {y1})")
    
    print("\nAhora:")
    print("1. Posiciona el cursor en la esquina inferior derecha")
    print("2. Presiona Enter")
    
    input("\nPresiona Enter para capturar segunda esquina...")
    x2, y2 = pyautogui.position()
    print(f"✅ Esquina inferior derecha: ({x2}, {y2})")
    
    region = (
        min(x1, x2),
        min(y1, y2),
        abs(x2 - x1),
        abs(y2 - y1)
    )
    
    print(f"\n🎯 " + MESSAGES["region_selected"].format(region))
    return region


def main():
    """Función principal con soporte para colores"""
    print("=" * 70)
    print("🌈 TRANSFORMADOR DE PANTALLA A ASCII CON COLORES")
    print("=" * 70)
    print()
    
    # Mostrar información del sistema
    columns, rows = shutil.get_terminal_size()
    print(f"💻 Terminal: {columns}x{rows}")
    print(f"🖼️  Resolución de pantalla: {pyautogui.size()}")
    print()
    
    print("📋 OPCIONES:")
    print("1. 🚀 Inicio rápido (colores verdaderos)")
    print("2. 🎨 Vista previa de colores")
    print("3. ⚙️  Configuración completa")
    print("4. 📏 Captura de región + colores")
    print("5. ❌ Salir")
    print()
    
    try:
        choice = input("Selecciona una opción (1-5): ").strip()
        
        if choice == "1":
            # Inicio rápido con colores verdaderos
            converter = ColorScreenToASCII(color_mode="truecolor")
            
            fps_input = input(f"FPS ({MIN_FPS}-{MAX_FPS}, default {DEFAULT_FPS}): ").strip()
            fps = DEFAULT_FPS
            if fps_input.isdigit() and MIN_FPS <= int(fps_input) <= MAX_FPS:
                fps = int(fps_input)
            
            converter.run_live_ascii_color(fps=fps)
            
        elif choice == "2":
            # Vista previa de colores
            show_color_preview()
            input("\nPresiona Enter para continuar...")
            main()  # Volver al menú
            
        elif choice == "3":
            # Configuración completa
            print("\n" + "="*50)
            print("⚙️ CONFIGURACIÓN COMPLETA")
            print("="*50)
            
            # Seleccionar modo de color
            print("\nModos de color disponibles:")
            for i, (key, desc) in enumerate(COLOR_MODES.items(), 1):
                print(f"{i}. {desc}")
            
            color_choice = input(f"Modo de color (1-{len(COLOR_MODES)}, default 4): ").strip()
            color_modes = list(COLOR_MODES.keys())
            color_mode = color_modes[int(color_choice)-1] if color_choice.isdigit() and 1 <= int(color_choice) <= len(COLOR_MODES) else "truecolor"
            
            # Seleccionar estilo ASCII
            print("\nEstilos ASCII:")
            print("1. detailed - Caracteres detallados")
            print("2. simple - Bloques simples")
            print("3. gradient - Gradiente suave")
            
            style_choice = input("Estilo (1-3, default 1): ").strip()
            style_map = {"1": "detailed", "2": "simple", "3": "gradient"}
            ascii_style = style_map.get(style_choice, "detailed")
            
            # Intensidad de color
            print("\nIntensidad de color:")
            print("1. low - Colores suaves")
            print("2. medium - Colores normales")
            print("3. high - Colores vivos")
            
            intensity_choice = input("Intensidad (1-3, default 2): ").strip()
            intensity_map = {"1": "low", "2": "medium", "3": "high"}
            color_intensity = intensity_map.get(intensity_choice, "medium")
            
            # Modo de renderizado
            use_blocks = input("¿Usar bloques de color? (s/N): ").strip().lower() == 's'
            
            # Mostrar información
            show_info = input("¿Mostrar información en tiempo real? (S/n): ").strip().lower() != 'n'
            
            # FPS
            fps_input = input(f"FPS ({MIN_FPS}-{MAX_FPS}, default {DEFAULT_FPS}): ").strip()
            fps = DEFAULT_FPS
            if fps_input.isdigit() and MIN_FPS <= int(fps_input) <= MAX_FPS:
                fps = int(fps_input)
            
            # Ejecutar
            converter = ColorScreenToASCII(ascii_style=ascii_style, color_mode=color_mode)
            converter.run_live_ascii_color(
                fps=fps,
                show_info=show_info,
                color_intensity=color_intensity,
                use_blocks=use_blocks
            )
            
        elif choice == "4":
            # Captura de región con colores
            region = interactive_region_selector()
            
            print(f"\nModo de color (default: colores verdaderos):")
            for i, (key, desc) in enumerate(COLOR_MODES.items(), 1):
                print(f"{i}. {desc}")
            
            color_choice = input(f"Seleccionar (1-{len(COLOR_MODES)}, default 4): ").strip()
            color_modes = list(COLOR_MODES.keys())
            color_mode = color_modes[int(color_choice)-1] if color_choice.isdigit() and 1 <= int(color_choice) <= len(COLOR_MODES) else "truecolor"
            
            fps_input = input(f"FPS ({MIN_FPS}-{MAX_FPS}, default {DEFAULT_FPS}): ").strip()
            fps = DEFAULT_FPS
            if fps_input.isdigit() and MIN_FPS <= int(fps_input) <= MAX_FPS:
                fps = int(fps_input)
            
            converter = ColorScreenToASCII(color_mode=color_mode)
            converter.run_live_ascii_color(fps=fps, region=region)
            
        elif choice == "5":
            print(MESSAGES["goodbye"])
            
        else:
            print(MESSAGES["invalid_option"])
            
    except KeyboardInterrupt:
        print("\n" + MESSAGES["goodbye"])
    except Exception as e:
        print(MESSAGES["error"].format(e))


if __name__ == "__main__":
    main()