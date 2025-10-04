"""
Interfaz de usuario para terminal
"""
import os
import sys
from typing import List, Dict, Any
from utils.config import *

class TerminalUI:
    """Interfaz de usuario para terminal"""
    
    def __init__(self):
        self.cursor_hidden = False
    
    def clear_screen(self):
        """Limpia la pantalla usando códigos ANSI"""
        sys.stdout.write(CLEAR_SCREEN)
        sys.stdout.flush()
    
    def hide_cursor(self):
        """Oculta el cursor"""
        if not self.cursor_hidden:
            sys.stdout.write(HIDE_CURSOR)
            sys.stdout.flush()
            self.cursor_hidden = True
    
    def show_cursor(self):
        """Muestra el cursor"""
        if self.cursor_hidden:
            sys.stdout.write(SHOW_CURSOR)
            sys.stdout.flush()
            self.cursor_hidden = False
    
    def show_header(self, color_mode: int = 0):
        """Muestra el header de la aplicación"""
        self.clear_screen()
        print("🎬" + "="*58 + "🎬")
        print("🖥️  TRANSFORMADOR DE PANTALLA A ASCII - MULTIHILO  🚀")
        print("🎬" + "="*58 + "🎬")
        print("⚡ Optimizado con procesamiento paralelo")
        
        # Mostrar modo de color actual
        color_modes = ["🔲 Escala de grises", "🎨 8 colores", "🌈 16 colores", "🎭 256 colores", "✨ Truecolor"]
        if color_mode < len(color_modes):
            print(f"{color_modes[color_mode]}")
        
        print("📊 Estadísticas en tiempo real")
    
    def display_frame(self, ascii_lines: List[str], stats: Dict[str, Any]):
        """Muestra un frame ASCII con estadísticas"""
        self.clear_screen()
        
        # Mostrar contenido ASCII
        for line in ascii_lines:
            print(line)
        
        # Mostrar estadísticas
        self._display_stats(stats)
    
    def _display_stats(self, stats: Dict[str, Any]):
        """Muestra estadísticas de rendimiento con threading dinámico"""
        frames = stats.get('frames', 0)
        fps = stats.get('avg_fps', 0.0)
        proc_time = stats.get('processing_time', 0.0) * 1000  # ms
        threads = stats.get('threads_used', 0)
        dynamic_threads = stats.get('dynamic_thread_count', threads)
        chunks = stats.get('chunks_processed', 0)
        cache_hits = stats.get('cache_hits', 0)
        cache_size = stats.get('cache_size', 0)
        
        # Línea principal de estadísticas
        main_stats = (
            f"📊 Frame: {frames} | "
            f"FPS: {fps:.1f} | "
            f"Proc: {proc_time:.1f}ms | "
            f"🧵 {threads}"
        )
        
        # Línea secundaria con threading dinámico y cache
        secondary_stats = (
            f"⚡ Dinámico: {dynamic_threads} hilos | "
            f"📦 Chunks: {chunks} | "
            f"💾 Cache: {cache_hits}/{cache_size} | "
            f"Ctrl+C: Salir"
        )
        
        # Mostrar estadísticas en dos líneas
        print("-" * 80)
        print(main_stats[:80])
        print(secondary_stats[:80])
    
    def cleanup(self):
        """Limpia la terminal al salir"""
        self.show_cursor()
        sys.stdout.write(RESET_COLOR)
        sys.stdout.flush()
        print("\n✨ Terminal restaurada")