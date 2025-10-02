#!/usr/bin/env python3
"""
Script de prueba para el transformador ASCII con colores
Verifica que el soporte de colores funcione correctamente
"""

import sys
import os
from colorama import init

# Inicializar colorama
init()

def test_color_support():
    """Prueba el soporte de colores del terminal"""
    print("🎨 PRUEBA DE SOPORTE DE COLORES")
    print("=" * 50)
    
    # Prueba básica de colores ANSI
    print("\n1. 🔴 Colores básicos ANSI:")
    colors = [
        ("\033[31m", "Rojo", "\033[0m"),
        ("\033[32m", "Verde", "\033[0m"),
        ("\033[34m", "Azul", "\033[0m"),
        ("\033[33m", "Amarillo", "\033[0m"),
        ("\033[35m", "Magenta", "\033[0m"),
        ("\033[36m", "Cian", "\033[0m"),
    ]
    
    for color_code, name, reset in colors:
        print(f"   {color_code}████ {name}{reset}")
    
    # Prueba de 256 colores
    print("\n2. 🌈 Colores extendidos (256):")
    print("   ", end="")
    for i in range(16, 232, 8):
        print(f"\033[38;5;{i}m██\033[0m", end="")
    print()
    
    # Prueba de colores RGB verdaderos
    print("\n3. ✨ Colores RGB verdaderos:")
    print("   ", end="")
    for i in range(0, 256, 8):
        r = i
        g = 255 - i
        b = 128
        print(f"\033[38;2;{r};{g};{b}m█\033[0m", end="")
    print()
    
    # Prueba de colores de fondo
    print("\n4. 🔲 Colores de fondo:")
    bg_colors = [41, 42, 43, 44, 45, 46]  # Fondos básicos
    for bg in bg_colors:
        print(f"\033[{bg}m  \033[0m", end="")
    print()
    
    return True

def test_color_imports():
    """Prueba las importaciones de módulos de color"""
    print("\n🧪 Probando importaciones de color...")
    
    try:
        from color_utils import ColorConverter
        print("✅ color_utils.ColorConverter")
        
        converter = ColorConverter()
        print("✅ Inicialización de ColorConverter")
        
        # Probar conversión básica
        color_code = converter.rgb_to_ansi_basic(255, 0, 0)
        print(f"✅ Conversión RGB a ANSI básico: {color_code}ROJO\033[0m")
        
        color_code = converter.rgb_to_ansi_256(0, 255, 0)
        print(f"✅ Conversión RGB a 256 colores: {color_code}VERDE\033[0m")
        
        color_code = converter.rgb_to_ansi_truecolor(0, 0, 255)
        print(f"✅ Conversión RGB a color verdadero: {color_code}AZUL\033[0m")
        
        return True
        
    except ImportError as e:
        print(f"❌ Error importando módulos de color: {e}")
        return False
    except Exception as e:
        print(f"❌ Error en pruebas de color: {e}")
        return False

def test_color_ascii_conversion():
    """Prueba la conversión ASCII con colores"""
    print("\n🎨 Probando conversión ASCII con colores...")
    
    try:
        from PIL import Image
        from color_utils import ColorConverter
        
        # Crear imagen de prueba colorida
        test_image = Image.new('RGB', (20, 10))
        pixels = []
        
        # Crear gradiente de colores
        for y in range(10):
            for x in range(20):
                r = int(255 * (x / 20))
                g = int(255 * (y / 10))
                b = 128
                pixels.append((r, g, b))
        
        test_image.putdata(pixels)
        
        # Convertir usando diferentes modos
        converter = ColorConverter()
        
        print("✅ Imagen de prueba creada")
        
        # Probar conversión con colores básicos
        ascii_result = ""
        for y in range(test_image.height):
            for x in range(test_image.width):
                r, g, b = test_image.getpixel((x, y))
                color_code = converter.rgb_to_ansi_basic(r, g, b)
                ascii_result += f"{color_code}█\033[0m"
            ascii_result += "\n"
        
        print("✅ Conversión con colores básicos:")
        print(ascii_result[:200] + "..." if len(ascii_result) > 200 else ascii_result)
        
        return True
        
    except Exception as e:
        print(f"❌ Error en conversión ASCII con colores: {e}")
        return False

def test_terminal_compatibility():
    """Prueba la compatibilidad del terminal con diferentes modos de color"""
    print("\n💻 Probando compatibilidad del terminal...")
    
    # Verificar variable de entorno TERM
    term = os.environ.get('TERM', 'unknown')
    print(f"📺 Terminal: {term}")
    
    # Verificar COLORTERM
    colorterm = os.environ.get('COLORTERM', 'none')
    print(f"🎨 Soporte de color: {colorterm}")
    
    # Recomendar mejor modo según el terminal
    if colorterm == 'truecolor' or '24bit' in colorterm:
        print("✅ Recomendado: Usar modo 'truecolor' (16.7M colores)")
    elif term in ['xterm-256color', 'screen-256color']:
        print("✅ Recomendado: Usar modo 'extended' (256 colores)")
    else:
        print("⚠️  Recomendado: Usar modo 'basic' (8 colores)")
    
    return True

def run_color_demo():
    """Ejecuta una demostración interactiva de colores"""
    print("\n🎬 DEMOSTRACIÓN DE COLORES")
    print("=" * 40)
    
    try:
        from color_utils import ColorConverter
        converter = ColorConverter()
        
        # Crear un arcoíris ASCII
        print("\n🌈 Arcoíris ASCII:")
        rainbow_colors = [
            (255, 0, 0),    # Rojo
            (255, 165, 0),  # Naranja
            (255, 255, 0),  # Amarillo
            (0, 255, 0),    # Verde
            (0, 0, 255),    # Azul
            (75, 0, 130),   # Índigo
            (238, 130, 238) # Violeta
        ]
        
        for r, g, b in rainbow_colors:
            # Probar los tres modos
            basic = converter.rgb_to_ansi_basic(r, g, b)
            extended = converter.rgb_to_ansi_256(r, g, b)
            truecolor = converter.rgb_to_ansi_truecolor(r, g, b)
            
            print(f"{basic}██\033[0m{extended}██\033[0m{truecolor}██\033[0m  RGB({r},{g},{b})")
        
        print("\nLeyenda: [Básico][256][TrueColor]")
        
        # Crear degradado
        print("\n🎯 Degradado azul a rojo:")
        for i in range(50):
            progress = i / 49
            r = int(255 * progress)
            g = 0
            b = int(255 * (1 - progress))
            
            color_code = converter.rgb_to_ansi_truecolor(r, g, b)
            print(f"{color_code}█\033[0m", end="")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error en demostración: {e}")
        return False

def main():
    """Ejecuta todas las pruebas de color"""
    print("=" * 60)
    print("🌈 PRUEBAS COMPLETAS DEL SISTEMA DE COLORES")
    print("=" * 60)
    
    tests = [
        ("Soporte básico de colores", test_color_support),
        ("Importaciones de módulos", test_color_imports),
        ("Conversión ASCII con colores", test_color_ascii_conversion),
        ("Compatibilidad del terminal", test_terminal_compatibility),
        ("Demostración interactiva", run_color_demo)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n▶️  Ejecutando: {test_name}")
        print("-" * 40)
        
        try:
            if test_func():
                print(f"✅ {test_name}: PASÓ")
                passed += 1
            else:
                print(f"❌ {test_name}: FALLÓ")
        except Exception as e:
            print(f"💥 {test_name}: ERROR - {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 RESULTADOS: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡TODAS LAS PRUEBAS DE COLOR PASARON!")
        print("✅ El sistema de colores está listo para usar")
        print("🚀 Ejecuta: python color_screen_to_ascii.py")
    else:
        print("⚠️  Algunas pruebas fallaron")
        print("💡 Revisa los errores arriba para más información")
    
    print("=" * 60)
    
    return passed == total

if __name__ == "__main__":
    try:
        success = main()
        
        # Preguntar si ejecutar el programa principal
        if success:
            run_main = input("\n¿Quieres ejecutar el transformador con colores ahora? (s/N): ").strip().lower()
            if run_main == 's':
                print("\n🚀 Iniciando transformador con colores...")
                import color_screen_to_ascii
                color_screen_to_ascii.main()
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n👋 Pruebas interrumpidas por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Error inesperado: {e}")
        sys.exit(1)