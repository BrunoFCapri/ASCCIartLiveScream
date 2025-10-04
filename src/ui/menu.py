"""
Sistema de menús para la aplicación ASCII
"""
from typing import Dict, Any
from utils.config import *

class MenuSystem:
    """Sistema de menús interactivos"""
    
    def show_main_menu(self) -> str:
        """Muestra el menú principal"""
        print("\n" + "="*60)
        print("🖥️  TRANSFORMADOR ASCII MULTIHILO")
        print("="*60)
        print("\n📋 OPCIONES:")
        print("1. 🚀 Captura rápida (recomendado)")
        print("2. ⚙️  Configuración completa")
        print("3. 📏 Captura de región específica")
        print("4. 🖥️  Seleccionar monitor")
        print("5. 🧪 Prueba de rendimiento")
        print("6. ❌ Salir")
        print("-"*60)
        
        while True:
            choice = input("Selecciona una opción (1-6): ").strip()
            if choice in ['1', '2', '3', '4', '5', '6']:
                return choice
            print("❌ Por favor, selecciona una opción válida (1-6)")
    
    def get_fps_input(self) -> int:
        """Obtiene la configuración de FPS del usuario"""
        print(f"\n⚡ Configuración de FPS (1-{MAX_FPS}, recomendado: {DEFAULT_FPS}):")
        
        while True:
            try:
                fps = input(f"FPS deseados [{DEFAULT_FPS}]: ").strip()
                if not fps:
                    return DEFAULT_FPS
                
                fps = int(fps)
                if 1 <= fps <= MAX_FPS:
                    return fps
                else:
                    print(f"❌ FPS debe estar entre 1 y {MAX_FPS}")
            except ValueError:
                print("❌ Por favor, ingresa un número válido")
    
    def get_ascii_style(self) -> str:
        """Permite seleccionar el estilo ASCII"""
        print("\n🎨 Estilos ASCII disponibles:")
        styles = list(ASCII_CHARS.keys())
        
        for i, style in enumerate(styles, 1):
            chars_preview = ''.join(ASCII_CHARS[style][:5]) + "..."
            print(f"{i}. {style.capitalize()}: {chars_preview}")
        
        while True:
            try:
                choice = input(f"Selecciona estilo (1-{len(styles)}) [1]: ").strip()
                if not choice:
                    return styles[0]
                
                choice = int(choice)
                if 1 <= choice <= len(styles):
                    return styles[choice - 1]
                else:
                    print(f"❌ Selección debe estar entre 1 y {len(styles)}")
            except ValueError:
                print("❌ Por favor, ingresa un número válido")
    
    def get_color_mode(self) -> int:
        """Permite seleccionar el modo de color"""
        print("\n🌈 Modos de color disponibles:")
        print("="*50)
        modes = [
            ("🔲 Escala de grises", "Clásico ASCII sin colores", "Compatible con todos los terminales"),
            ("🎨 Colores básicos (8)", "8 colores ANSI básicos", "Máxima compatibilidad"),
            ("🌈 Colores extendidos (16)", "16 colores ANSI", "Buena compatibilidad"),
            ("🎭 Colores 256", "256 colores", "Terminal moderno requerido"),
            ("✨ Truecolor (16M)", "16 millones de colores", "Terminal avanzado - mejor calidad")
        ]
        
        for i, (name, desc, compat) in enumerate(modes):
            print(f"{i}. {name}")
            print(f"   {desc} - {compat}")
            print()
        
        while True:
            try:
                choice = input(f"Selecciona modo (0-{len(modes)-1}) [4]: ").strip()
                if not choice:
                    return 4  # Truecolor por defecto
                
                choice = int(choice)
                if 0 <= choice < len(modes):
                    return choice
                else:
                    print(f"❌ Selección debe estar entre 0 y {len(modes)-1}")
            except ValueError:
                print("❌ Por favor, ingresa un número válido")
    
    def get_full_configuration(self) -> Dict[str, Any]:
        """Obtiene configuración completa del usuario"""
        config = {}
        
        config['fps'] = self.get_fps_input()
        config['ascii_style'] = self.get_ascii_style()
        config['color_mode'] = self.get_color_mode()
        config['region'] = None  # Sin región por defecto
        
        print(f"\n✅ Configuración seleccionada:")
        print(f"   📈 FPS: {config['fps']}")
        print(f"   🎨 Estilo: {config['ascii_style'].capitalize()}")
        
        color_names = ['Escala de grises', 'Colores básicos (8)', 'Colores extendidos (16)', 'Colores 256', 'Truecolor (16M)']
        if config['color_mode'] < len(color_names):
            print(f"   🌈 Colores: {color_names[config['color_mode']]}")
        
        return config