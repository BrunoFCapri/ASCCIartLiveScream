#!/usr/bin/env python3
"""
Transformador de pantalla a ASCII MEJORADO
Versión optimizada con mejor rendimiento y características adicionales
"""

import pyautogui
import os
import time
import shutil
import threading
from PIL import Image
from colorama import init, Fore, Back, Style
from config import *

# Inicializar colorama para Windows
init()

class AdvancedScreenToASCII:
    def __init__(self, ascii_style="detailed"):
        """
        Inicializa el convertidor con diferentes estilos de ASCII
        
        Args:
            ascii_style: "detailed", "simple", o "gradient"
        """
        self.ascii_styles = {
            "detailed": ASCII_CHARS_DETAILED,
            "simple": ASCII_CHARS_SIMPLE,
            "gradient": ASCII_CHARS_GRADIENT
        }
        
        self.ascii_chars = self.ascii_styles.get(ascii_style, ASCII_CHARS_DETAILED)
        pyautogui.FAILSAFE = False
        
        # Variables para estadísticas
        self.frame_count = 0
        self.start_time = None
        self.last_fps_update = 0
        self.current_fps = 0
        
    def capture_screen_threaded(self, region=None):
        """
        Captura optimizada de pantalla usando threading
        """
        try:
            if region:
                screenshot = pyautogui.screenshot(region=region)
            else:
                # Captura optimizada para pantalla completa
                screenshot = pyautogui.screenshot()
            return screenshot
        except Exception as e:
            return None
    
    def get_terminal_size(self):
        """Obtiene el tamaño actual de la terminal"""
        try:
            columns, rows = shutil.get_terminal_size()
            return columns, rows
        except:
            return DEFAULT_TERMINAL_WIDTH, DEFAULT_TERMINAL_HEIGHT
    
    def resize_image_optimized(self, image, max_width=None, max_height=None):
        """
        Redimensiona la imagen de forma optimizada
        """
        if max_width is None or max_height is None:
            columns, rows = self.get_terminal_size()
            max_width = int(columns * DEFAULT_WIDTH_SCALE)
            max_height = rows - 5  # Dejar espacio para información adicional
            
        width, height = image.size
        aspect_ratio = height / width
        
        # Calcular nuevas dimensiones
        new_width = min(max_width, width)
        new_height = int(aspect_ratio * new_width * ASPECT_RATIO_CORRECTION)
        
        # Ajustar si la altura es demasiado grande
        if new_height > max_height:
            new_height = max_height
            new_width = int(new_height / aspect_ratio / ASPECT_RATIO_CORRECTION)
        
        # Usar resampling más rápido para tiempo real
        return image.resize((new_width, new_height), Image.Resampling.NEAREST)
    
    def image_to_ascii_optimized(self, image):
        """
        Conversión optimizada de imagen a ASCII
        """
        # Convertir a escala de grises
        grayscale_image = image.convert("L")
        
        # Obtener datos de pixels de una vez
        pixels = list(grayscale_image.getdata())
        width, height = grayscale_image.size
        
        ascii_lines = []
        chars_len = len(self.ascii_chars)
        
        for y in range(height):
            line = ""
            for x in range(width):
                pixel_value = pixels[y * width + x]
                ascii_index = min(int(pixel_value / 255 * (chars_len - 1)), chars_len - 1)
                line += self.ascii_chars[ascii_index]
            ascii_lines.append(line)
        
        return "\n".join(ascii_lines)
    
    def clear_screen_fast(self):
        """Limpieza rápida de pantalla"""
        if os.name == 'nt':  # Windows
            os.system('cls')
        else:  # Unix/Linux/MacOS
            os.system('clear')
    
    def calculate_fps(self):
        """Calcula FPS actual"""
        current_time = time.time()
        if self.start_time is None:
            self.start_time = current_time
            self.last_fps_update = current_time
            return 0
        
        self.frame_count += 1
        
        # Actualizar FPS cada segundo
        if current_time - self.last_fps_update >= 1.0:
            elapsed = current_time - self.last_fps_update
            self.current_fps = (self.frame_count - 
                              (self.frame_count - int(self.frame_count * elapsed / 
                               (current_time - self.start_time)))) / elapsed
            self.last_fps_update = current_time
        
        return self.current_fps
    
    def run_live_ascii_advanced(self, fps=DEFAULT_FPS, region=None, show_info=True, 
                               ascii_style="detailed"):
        """
        Versión avanzada del convertidor en tiempo real
        """
        # Cambiar estilo si es necesario
        if ascii_style in self.ascii_styles:
            self.ascii_chars = self.ascii_styles[ascii_style]
        
        frame_delay = 1.0 / fps
        
        print(MESSAGES["starting"])
        if show_info:
            print(MESSAGES["stop_instruction"])
            print(MESSAGES["fps_info"].format(fps))
            print(f"🎨 Estilo ASCII: {ascii_style}")
            if region:
                print(f"📏 Región: {region}")
        
        for i in range(3, 0, -1):
            print(MESSAGES["countdown"].format(i))
            time.sleep(1)
        
        self.frame_count = 0
        self.start_time = time.time()
        
        try:
            while True:
                frame_start = time.time()
                
                # Capturar pantalla
                screenshot = self.capture_screen_threaded(region)
                if screenshot is None:
                    continue
                
                # Redimensionar imagen
                resized_image = self.resize_image_optimized(screenshot)
                
                # Convertir a ASCII
                ascii_art = self.image_to_ascii_optimized(resized_image)
                
                # Limpiar pantalla y mostrar
                self.clear_screen_fast()
                
                if show_info:
                    current_fps = self.calculate_fps()
                    info_line = f"📊 FPS: {current_fps:.1f} | Frames: {self.frame_count} | Tamaño: {resized_image.size}"
                    print(Fore.CYAN + info_line + Style.RESET_ALL)
                    print("-" * len(info_line))
                
                print(ascii_art)
                
                # Control de FPS
                elapsed = time.time() - frame_start
                sleep_time = max(0, frame_delay - elapsed)
                if sleep_time > 0:
                    time.sleep(sleep_time)
                    
        except KeyboardInterrupt:
            print(MESSAGES["stopping"])
            total_time = time.time() - self.start_time
            avg_fps = self.frame_count / total_time if total_time > 0 else 0
            print(f"📈 Estadísticas finales:")
            print(f"   • Frames totales: {self.frame_count}")
            print(f"   • Tiempo total: {total_time:.2f}s")
            print(f"   • FPS promedio: {avg_fps:.2f}")
            print(MESSAGES["finished"])


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
    
    # Calcular región
    region = (
        min(x1, x2),
        min(y1, y2),
        abs(x2 - x1),
        abs(y2 - y1)
    )
    
    print(f"\n🎯 " + MESSAGES["region_selected"].format(region))
    return region


def main():
    """Función principal mejorada"""
    print("=" * 60)
    print("🖥️  TRANSFORMADOR AVANZADO DE PANTALLA A ASCII")
    print("=" * 60)
    print()
    
    # Mostrar información del sistema
    columns, rows = shutil.get_terminal_size()
    print(f"💻 Terminal: {columns}x{rows}")
    print(f"🖼️  Resolución de pantalla: {pyautogui.size()}")
    print()
    
    print("📋 OPCIONES:")
    print("1. 🖥️  Captura completa de pantalla")
    print("2. 📏 Captura de región específica")
    print("3. 🎨 Configuración avanzada")
    print("4. ❌ Salir")
    print()
    
    try:
        choice = input("Selecciona una opción (1-4): ").strip()
        
        if choice == "1":
            # Captura completa
            converter = AdvancedScreenToASCII()
            
            fps_input = input(f"FPS ({MIN_FPS}-{MAX_FPS}, default {DEFAULT_FPS}): ").strip()
            fps = DEFAULT_FPS
            if fps_input.isdigit() and MIN_FPS <= int(fps_input) <= MAX_FPS:
                fps = int(fps_input)
            
            converter.run_live_ascii_advanced(fps=fps)
            
        elif choice == "2":
            # Captura de región
            region = interactive_region_selector()
            converter = AdvancedScreenToASCII()
            
            fps_input = input(f"FPS ({MIN_FPS}-{MAX_FPS}, default {DEFAULT_FPS}): ").strip()
            fps = DEFAULT_FPS
            if fps_input.isdigit() and MIN_FPS <= int(fps_input) <= MAX_FPS:
                fps = int(fps_input)
            
            converter.run_live_ascii_advanced(fps=fps, region=region)
            
        elif choice == "3":
            # Configuración avanzada
            print("\n" + "="*40)
            print("🎨 CONFIGURACIÓN AVANZADA")
            print("="*40)
            
            print("Estilos de ASCII disponibles:")
            print("1. detailed - Caracteres detallados: @#S%?*+;:,.")
            print("2. simple - Bloques: █▓▒░ ")
            print("3. gradient - Gradiente: .:-=+*#%@")
            
            style_choice = input("Estilo (1-3, default 1): ").strip()
            style_map = {"1": "detailed", "2": "simple", "3": "gradient"}
            ascii_style = style_map.get(style_choice, "detailed")
            
            show_info = input("Mostrar información en tiempo real? (s/N): ").strip().lower() == 's'
            
            region_choice = input("¿Capturar región específica? (s/N): ").strip().lower()
            region = None
            if region_choice == 's':
                region = interactive_region_selector()
            
            fps_input = input(f"FPS ({MIN_FPS}-{MAX_FPS}, default {DEFAULT_FPS}): ").strip()
            fps = DEFAULT_FPS
            if fps_input.isdigit() and MIN_FPS <= int(fps_input) <= MAX_FPS:
                fps = int(fps_input)
            
            converter = AdvancedScreenToASCII(ascii_style=ascii_style)
            converter.run_live_ascii_advanced(
                fps=fps, 
                region=region, 
                show_info=show_info, 
                ascii_style=ascii_style
            )
            
        elif choice == "4":
            print(MESSAGES["goodbye"])
            
        else:
            print(MESSAGES["invalid_option"])
            
    except KeyboardInterrupt:
        print("\n" + MESSAGES["goodbye"])
    except Exception as e:
        print(MESSAGES["error"].format(e))


if __name__ == "__main__":
    main()