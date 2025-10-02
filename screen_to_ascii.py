#!/usr/bin/env python3
"""
Transformador de pantalla a ASCII en tiempo real
Captura la pantalla y la convierte a caracteres ASCII para mostrar en terminal
"""

import pyautogui
import os
import time
import shutil
from PIL import Image
from colorama import init, Fore, Back, Style

# Inicializar colorama para Windows
init()

class ScreenToASCII:
    def __init__(self):
        # Caracteres ASCII ordenados por densidad visual (de más oscuro a más claro)
        self.ascii_chars = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]
        # Desactivar failsafe de pyautogui para evitar interrupciones
        pyautogui.FAILSAFE = False
        
    def capture_screen(self, region=None):
        """
        Captura la pantalla completa o una región específica
        
        Args:
            region: tupla (x, y, width, height) para capturar región específica
                   None para capturar pantalla completa
        
        Returns:
            PIL.Image: Imagen capturada
        """
        try:
            if region:
                screenshot = pyautogui.screenshot(region=region)
            else:
                screenshot = pyautogui.screenshot()
            return screenshot
        except Exception as e:
            print(f"Error capturando pantalla: {e}")
            return None
    
    def get_terminal_size(self):
        """
        Obtiene el tamaño de la terminal
        
        Returns:
            tuple: (columnas, filas) de la terminal
        """
        try:
            columns, rows = shutil.get_terminal_size()
            return columns, rows
        except:
            # Valores por defecto si no se puede obtener el tamaño
            return 80, 24
    
    def resize_image(self, image, new_width=None):
        """
        Redimensiona la imagen manteniendo la proporción
        
        Args:
            image: PIL.Image a redimensionar
            new_width: ancho deseado, si None usa el ancho de la terminal
        
        Returns:
            PIL.Image: Imagen redimensionada
        """
        if new_width is None:
            columns, _ = self.get_terminal_size()
            new_width = columns - 2  # Dejar margen
            
        width, height = image.size
        aspect_ratio = height / width
        
        # Ajustar por la proporción de caracteres ASCII (más altos que anchos)
        new_height = int(aspect_ratio * new_width * 0.55)
        
        return image.resize((new_width, new_height))
    
    def image_to_ascii(self, image):
        """
        Convierte una imagen PIL a texto ASCII
        
        Args:
            image: PIL.Image a convertir
        
        Returns:
            str: Representación ASCII de la imagen
        """
        # Convertir a escala de grises
        grayscale_image = image.convert("L")
        
        ascii_str = ""
        for y in range(grayscale_image.height):
            for x in range(grayscale_image.width):
                # Obtener el valor del pixel (0-255)
                pixel_value = grayscale_image.getpixel((x, y))
                
                # Mapear el valor del pixel a un caracter ASCII
                ascii_index = int(pixel_value / 255 * (len(self.ascii_chars) - 1))
                ascii_str += self.ascii_chars[ascii_index]
            
            ascii_str += "\n"
        
        return ascii_str
    
    def clear_screen(self):
        """Limpia la pantalla de la terminal"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def run_live_ascii(self, fps=10, region=None):
        """
        Ejecuta el transformador en tiempo real
        
        Args:
            fps: Fotogramas por segundo (mayor = más fluido pero más CPU)
            region: región específica a capturar (x, y, width, height)
        """
        frame_delay = 1.0 / fps
        
        print("🎥 Iniciando captura de pantalla a ASCII...")
        print("⚠️  Presiona Ctrl+C para detener")
        print(f"📺 FPS: {fps}")
        print("⏳ Iniciando en 3 segundos...")
        
        time.sleep(3)
        
        try:
            while True:
                start_time = time.time()
                
                # Capturar pantalla
                screenshot = self.capture_screen(region)
                if screenshot is None:
                    continue
                
                # Redimensionar imagen
                resized_image = self.resize_image(screenshot)
                
                # Convertir a ASCII
                ascii_art = self.image_to_ascii(resized_image)
                
                # Limpiar pantalla y mostrar ASCII
                self.clear_screen()
                print(ascii_art, end='')
                
                # Controlar FPS
                elapsed_time = time.time() - start_time
                sleep_time = max(0, frame_delay - elapsed_time)
                if sleep_time > 0:
                    time.sleep(sleep_time)
                    
        except KeyboardInterrupt:
            print("\n🛑 Deteniendo captura...")
            print("✅ ¡Programa terminado!")


def main():
    """Función principal"""
    converter = ScreenToASCII()
    
    print("=" * 50)
    print("🖥️  TRANSFORMADOR DE PANTALLA A ASCII")
    print("=" * 50)
    print()
    print("Opciones:")
    print("1. Captura completa de pantalla")
    print("2. Captura de región específica")
    print("3. Salir")
    print()
    
    try:
        choice = input("Selecciona una opción (1-3): ").strip()
        
        if choice == "1":
            # Configurar FPS
            fps_input = input("FPS (1-30, default 10): ").strip()
            fps = 10
            if fps_input.isdigit() and 1 <= int(fps_input) <= 30:
                fps = int(fps_input)
            
            converter.run_live_ascii(fps=fps)
            
        elif choice == "2":
            print("\n📏 Define la región a capturar:")
            print("Mueve el mouse a la esquina superior izquierda y presiona Enter...")
            input()
            x1, y1 = pyautogui.position()
            print(f"Esquina superior izquierda: ({x1}, {y1})")
            
            print("Mueve el mouse a la esquina inferior derecha y presiona Enter...")
            input()
            x2, y2 = pyautogui.position()
            print(f"Esquina inferior derecha: ({x2}, {y2})")
            
            # Calcular región
            region = (
                min(x1, x2),
                min(y1, y2),
                abs(x2 - x1),
                abs(y2 - y1)
            )
            
            print(f"Región seleccionada: {region}")
            
            # Configurar FPS
            fps_input = input("FPS (1-30, default 10): ").strip()
            fps = 10
            if fps_input.isdigit() and 1 <= int(fps_input) <= 30:
                fps = int(fps_input)
            
            converter.run_live_ascii(fps=fps, region=region)
            
        elif choice == "3":
            print("👋 ¡Hasta luego!")
            
        else:
            print("❌ Opción inválida")
            
    except KeyboardInterrupt:
        print("\n👋 ¡Hasta luego!")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()