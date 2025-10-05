"""
Transformador de Pantalla a ASCII - Versión Multihilo
"""
import os
import sys
import time
import threading
from typing import Optional, Tuple

# Agregar el directorio src al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.screen_capture import ScreenCapture
from core.matrix_processor import ThreadedMatrixProcessor
from workers.thread_manager import ThreadManager
from utils.config import *
from ui.menu import MenuSystem
from ui.terminal_ui import TerminalUI

class ASCIIScreenCapture:
    """Aplicación principal de captura ASCII multihilo"""
    
    def __init__(self):
        self.screen_capture = ScreenCapture()
        self.thread_manager = ThreadManager(get_optimal_thread_count())
        self.matrix_processor = None
        self.terminal_ui = TerminalUI()
        self.menu = MenuSystem()
        self.running = False
        self.stats = {
            'frames_processed': 0,
            'total_time': 0.0,
            'avg_fps': 0.0
        }
    
    def initialize_processor(self, ascii_style: str = 'detailed'):
        """Inicializa el procesador de matrices"""
        chars = ASCII_CHARS.get(ascii_style, ASCII_CHARS['detailed'])
        thread_count = get_optimal_thread_count()
        self.matrix_processor = ThreadedMatrixProcessor(chars, thread_count)
        print(f"🔧 Procesador inicializado con {thread_count} hilos")
    
    def capture_loop(self, fps: int = 15, region: Optional[Tuple[int, int, int, int]] = None,
                    ascii_style: str = 'detailed', color_mode: int = 0):
        """Bucle principal de captura y conversión"""
        
        if not self.matrix_processor:
            self.initialize_processor(ascii_style)
        
        frame_time = 1.0 / fps
        self.running = True
        
        print(f"🚀 Iniciando captura a {fps} FPS")
        print("Presiona Ctrl+C para detener")
        
        try:
            self.terminal_ui.hide_cursor()
            start_time = time.time()
            
            while self.running:
                frame_start = time.time()
                
                # Capturar y redimensionar pantalla (usando monitor seleccionado)
                screen_array = self.screen_capture.capture_and_resize(region)
                
                # Procesar con multithreading
                ascii_lines, processing_stats = self.matrix_processor.process_matrix_threaded(
                    screen_array, color_mode
                )
                
                # Mostrar resultado
                self.terminal_ui.display_frame(ascii_lines, self._get_current_stats(processing_stats))
                
                # Control de FPS
                frame_time_used = time.time() - frame_start
                if frame_time_used < frame_time:
                    time.sleep(frame_time - frame_time_used)
                
                # Actualizar estadísticas
                self._update_stats(frame_time_used)
                
        except KeyboardInterrupt:
            print("\n🛑 Detenido por usuario")
        finally:
            self.running = False
            self.terminal_ui.show_cursor()
            self._show_final_stats()
    
    def _get_current_stats(self, processing_stats: dict) -> dict:
        """Obtiene estadísticas actuales"""
        return {
            'frames': self.stats['frames_processed'],
            'avg_fps': self.stats['avg_fps'],
            'processing_time': processing_stats.get('total_time', 0),
            'threads_used': processing_stats.get('threads_used', 0),
            'chunks_processed': processing_stats.get('chunks_processed', 0)
        }
    
    def _update_stats(self, frame_time: float):
        """Actualiza estadísticas de rendimiento"""
        self.stats['frames_processed'] += 1
        self.stats['total_time'] += frame_time
        
        if self.stats['total_time'] > 0:
            self.stats['avg_fps'] = self.stats['frames_processed'] / self.stats['total_time']
    
    def _show_final_stats(self):
        """Muestra estadísticas finales"""
        print(f"\n📊 ESTADÍSTICAS FINALES:")
        print(f"   Frames procesados: {self.stats['frames_processed']}")
        print(f"   Tiempo total: {self.stats['total_time']:.2f}s")
        print(f"   FPS promedio: {self.stats['avg_fps']:.2f}")
        print(f"   Hilos utilizados: {get_optimal_thread_count()}")
    
    def run(self):
        """Ejecuta la aplicación principal"""
        try:
            self.terminal_ui.show_header()
            
            # Mostrar información de monitores detectados
            print(f"\n🖥️  Monitores detectados: {len(self.screen_capture.monitors)}")
            if len(self.screen_capture.monitors) > 1:
                current_monitor = self.screen_capture.monitors[self.screen_capture.selected_monitor]
                print(f"📺 Monitor actual: {current_monitor['name']} ({current_monitor['width']}x{current_monitor['height']})")
                print("💡 Usa la opción 4 para cambiar de monitor")
            
            while True:
                choice = self.menu.show_main_menu()
                
                if choice == '1':  # Captura completa rápida
                    fps = self.menu.get_fps_input()
                    color_mode = self.menu.get_color_mode()
                    self.capture_loop(fps=fps, ascii_style='gradient', color_mode=color_mode)
                
                elif choice == '2':  # Captura con configuración completa
                    config = self.menu.get_full_configuration()
                    self.capture_loop(**config)
                
                elif choice == '3':  # Captura de región
                    region = self.screen_capture.get_region_interactive()
                    if not region:
                        print("❕ Selección cancelada. Volviendo al menú.")
                        time.sleep(0.8)
                        continue
                    fps = self.menu.get_fps_input()
                    color_mode = self.menu.get_color_mode()
                    self.capture_loop(fps=fps, region=region, ascii_style='detailed', color_mode=color_mode)
                
                elif choice == '4':  # Seleccionar monitor
                    self.screen_capture.select_monitor()
                    input("\nPresiona Enter para continuar...")
                
                elif choice == '5':  # Test de rendimiento
                    self._run_performance_test()
                
                elif choice == '6':  # Salir
                    break
                
                else:
                    print("❌ Opción inválida")
        
        except KeyboardInterrupt:
            print("\n👋 ¡Hasta luego!")
        finally:
            self.terminal_ui.cleanup()
    
    def _run_performance_test(self):
        """Ejecuta una prueba de rendimiento"""
        print("🧪 Ejecutando prueba de rendimiento...")
        
        # Test con diferentes números de hilos
        for thread_count in [1, 2, 4, 8]:
            if thread_count <= get_optimal_thread_count() * 2:
                print(f"\n⚡ Probando con {thread_count} hilos...")
                
                # Crear procesador temporal
                processor = ThreadedMatrixProcessor(ASCII_CHARS['simple'], thread_count)
                
                # Capturar frame de prueba
                screen_array = self.screen_capture.capture_and_resize()
                
                # Procesar 5 veces y promediar
                times = []
                for _ in range(5):
                    start = time.time()
                    _, stats = processor.process_matrix_threaded(screen_array)
                    times.append(time.time() - start)
                
                avg_time = sum(times) / len(times)
                fps_estimate = 1.0 / avg_time if avg_time > 0 else 0
                
                print(f"   Tiempo promedio: {avg_time:.4f}s")
                print(f"   FPS estimado: {fps_estimate:.1f}")

def main():
    """Función principal"""
    app = ASCIIScreenCapture()
    app.run()

if __name__ == "__main__":
    main()