"""
Capturador de pantalla optimizado para multithreading con soporte multi-monitor
"""
import pyautogui
import numpy as np
from PIL import Image
import os
import time
import tkinter as tk
from typing import Tuple, Optional, List, Dict

class ScreenCapture:
    """Capturador de pantalla optimizado"""
    
    def __init__(self):
        # Desactivar fail-safe de pyautogui para mejor rendimiento
        pyautogui.FAILSAFE = False
        self._last_screenshot = None
        self._terminal_size_cache = None
        self._cache_time = 0
        self.monitors = self.detect_monitors()
        self.selected_monitor = 0  # Monitor principal por defecto
        
    def get_terminal_size(self) -> Tuple[int, int]:
        """Obtiene el tamaño de terminal con cache"""
        current_time = time.time()
        if (self._terminal_size_cache is None or 
            current_time - self._cache_time > 1.0):  # Cache por 1 segundo
            
            try:
                size = os.get_terminal_size()
                self._terminal_size_cache = (size.columns - 1, size.lines - 4)
                self._cache_time = current_time
            except:
                self._terminal_size_cache = (80, 20)  # Fallback
                
        return self._terminal_size_cache
    
    def detect_monitors(self) -> List[Dict]:
        """Detecta todos los monitores disponibles usando tkinter"""
        monitors = []
        try:
            # Crear ventana temporal para obtener información de monitores
            root = tk.Tk()
            root.withdraw()  # Ocultar ventana
            
            # Monitor principal
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            
            monitors.append({
                'id': 0,
                'name': 'Monitor Principal',
                'x': 0,
                'y': 0,
                'width': screen_width,
                'height': screen_height,
                'region': (0, 0, screen_width, screen_height)
            })
            
            # Intentar detectar monitores adicionales usando pyautogui
            try:
                # Obtener el tamaño total del área virtual (todos los monitores)
                virtual_screen = pyautogui.screenshot()
                virtual_width, virtual_height = virtual_screen.size
                
                # Si es más grande que el monitor principal, hay monitores adicionales
                if virtual_width > screen_width:
                    # Monitor secundario (asumiendo configuración horizontal)
                    monitor2_width = virtual_width - screen_width
                    monitors.append({
                        'id': 1,
                        'name': 'Monitor Secundario',
                        'x': screen_width,
                        'y': 0,
                        'width': monitor2_width,
                        'height': screen_height,
                        'region': (screen_width, 0, monitor2_width, screen_height)
                    })
                
                if virtual_height > screen_height:
                    # Monitor adicional vertical
                    monitor3_height = virtual_height - screen_height
                    monitors.append({
                        'id': 2,
                        'name': 'Monitor Vertical',
                        'x': 0,
                        'y': screen_height,
                        'width': screen_width,
                        'height': monitor3_height,
                        'region': (0, screen_height, screen_width, monitor3_height)
                    })
                    
            except Exception as e:
                print(f"⚠️  No se pudieron detectar monitores adicionales: {e}")
            
            root.destroy()
            
        except Exception as e:
            print(f"⚠️  Error detectando monitores: {e}")
            # Monitor por defecto
            monitors = [{
                'id': 0,
                'name': 'Monitor Por Defecto',
                'x': 0,
                'y': 0,
                'width': 1920,
                'height': 1080,
                'region': (0, 0, 1920, 1080)
            }]
        
        return monitors
    
    def list_monitors(self) -> None:
        """Lista todos los monitores detectados"""
        print("\n🖥️  Monitores detectados:")
        print("="*50)
        for monitor in self.monitors:
            marker = "👈 ACTUAL" if monitor['id'] == self.selected_monitor else ""
            print(f"{monitor['id']}. {monitor['name']} {marker}")
            print(f"   📐 Resolución: {monitor['width']}x{monitor['height']}")
            print(f"   📍 Posición: ({monitor['x']}, {monitor['y']})")
            print()
    
    def select_monitor(self, monitor_id: int = None) -> bool:
        """Selecciona un monitor específico"""
        if monitor_id is None:
            self.list_monitors()
            while True:
                try:
                    choice = input(f"Selecciona monitor (0-{len(self.monitors)-1}) [0]: ").strip()
                    if not choice:
                        monitor_id = 0
                        break
                    
                    monitor_id = int(choice)
                    if 0 <= monitor_id < len(self.monitors):
                        break
                    else:
                        print(f"❌ Selección debe estar entre 0 y {len(self.monitors)-1}")
                except ValueError:
                    print("❌ Por favor, ingresa un número válido")
        
        if 0 <= monitor_id < len(self.monitors):
            self.selected_monitor = monitor_id
            monitor = self.monitors[monitor_id]
            print(f"✅ Monitor seleccionado: {monitor['name']} ({monitor['width']}x{monitor['height']})")
            return True
        
        print(f"❌ Monitor {monitor_id} no encontrado")
        return False
    
    def get_monitor_region(self, monitor_id: int = None) -> Tuple[int, int, int, int]:
        """Obtiene la región del monitor especificado"""
        if monitor_id is None:
            monitor_id = self.selected_monitor
            
        if 0 <= monitor_id < len(self.monitors):
            return self.monitors[monitor_id]['region']
        
        # Fallback al monitor principal
        return (0, 0, 1920, 1080)
    
    def capture_screen(self, region: Optional[Tuple[int, int, int, int]] = None, 
                      monitor_id: Optional[int] = None) -> np.ndarray:
        """Captura la pantalla y retorna como numpy array"""
        try:
            # Usar región especificada o la del monitor seleccionado
            if region:
                screenshot = pyautogui.screenshot(region=region)
            elif monitor_id is not None or self.selected_monitor != 0:
                # Capturar desde monitor específico
                monitor_region = self.get_monitor_region(monitor_id)
                screenshot = pyautogui.screenshot(region=monitor_region)
            else:
                # Captura completa (todos los monitores)
                screenshot = pyautogui.screenshot()
            
            # Convertir directamente a numpy array
            return np.array(screenshot)
            
        except Exception as e:
            print(f"Error capturando pantalla: {e}")
            # Retornar imagen negra como fallback
            return np.zeros((100, 100, 3), dtype=np.uint8)
    
    def resize_for_terminal(self, image_array: np.ndarray, 
                          width_scale: float = 0.95) -> np.ndarray:
        """Redimensiona la imagen para ajustarse al terminal - OPTIMIZADO"""
        terminal_width, terminal_height = self.get_terminal_size()
        
        # Calcular nuevo tamaño usando operaciones enteras más rápidas
        new_width = int(terminal_width * width_scale)
        new_height = (new_width * 55) >> 7  # Equivale a * 0.55 pero más rápido
        
        # Limitar altura al terminal
        if new_height > terminal_height:
            new_height = terminal_height
            new_width = (new_height << 7) // 55  # Más rápido que / 0.55
        
        # Optimización: usar algoritmo más rápido según el factor de escala
        current_height, current_width = image_array.shape[:2]
        scale_factor = new_width / current_width
        
        if scale_factor > 0.5:
            # Para escalas grandes, usar LANCZOS (mejor calidad)
            image = Image.fromarray(image_array)
            resized = image.resize((new_width, new_height), Image.LANCZOS)
            return np.array(resized)
        else:
            # Para escalas pequeñas, usar NEAREST (más rápido)
            image = Image.fromarray(image_array)
            resized = image.resize((new_width, new_height), Image.NEAREST)
            return np.array(resized)
    
    def capture_and_resize(self, region: Optional[Tuple[int, int, int, int]] = None,
                          width_scale: float = 0.95, monitor_id: Optional[int] = None) -> np.ndarray:
        """Captura y redimensiona en una sola operación"""
        screen_array = self.capture_screen(region, monitor_id)
        return self.resize_for_terminal(screen_array, width_scale)
    
    def get_region_interactive(self) -> Tuple[int, int, int, int]:
        """Permite al usuario seleccionar una región interactivamente"""
        print("📍 Selección de región:")
        print("1. Mueve el mouse a la esquina SUPERIOR IZQUIERDA")
        input("   Presiona Enter cuando esté en posición...")
        
        x1, y1 = pyautogui.position()
        print(f"   ✅ Esquina superior izquierda: ({x1}, {y1})")
        
        print("2. Mueve el mouse a la esquina INFERIOR DERECHA")
        input("   Presiona Enter cuando esté en posición...")
        
        x2, y2 = pyautogui.position()
        print(f"   ✅ Esquina inferior derecha: ({x2}, {y2})")
        
        # Calcular región (x, y, width, height)
        region = (min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
        print(f"   📏 Región seleccionada: {region}")
        
        return region

    def start_capture(self):
        self.divide_into_matrices()
        return self.matrices  # Return the list of matrices for processing