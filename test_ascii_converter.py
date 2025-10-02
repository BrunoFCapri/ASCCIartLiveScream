#!/usr/bin/env python3
"""
Script de prueba para el transformador de pantalla a ASCII
Verifica que todas las dependencias estén instaladas y funcionando
"""

import sys
import importlib

def test_imports():
    """Prueba que todas las dependencias estén disponibles"""
    required_modules = [
        'PIL',
        'pyautogui', 
        'colorama',
        'os',
        'time',
        'shutil'
    ]
    
    print("🧪 Probando importaciones...")
    failed_imports = []
    
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            failed_imports.append(module)
    
    return failed_imports

def test_screen_capture():
    """Prueba la captura de pantalla"""
    print("\n📸 Probando captura de pantalla...")
    try:
        import pyautogui
        
        # Desactivar failsafe para la prueba
        pyautogui.FAILSAFE = False
        
        # Tomar screenshot de prueba
        screenshot = pyautogui.screenshot()
        print(f"✅ Captura exitosa: {screenshot.size}")
        
        # Probar conversión a escala de grises
        grayscale = screenshot.convert("L")
        print(f"✅ Conversión a escala de grises: {grayscale.size}")
        
        return True
    except Exception as e:
        print(f"❌ Error en captura: {e}")
        return False

def test_terminal_size():
    """Prueba la detección del tamaño de terminal"""
    print("\n📐 Probando detección de terminal...")
    try:
        import shutil
        columns, rows = shutil.get_terminal_size()
        print(f"✅ Tamaño de terminal: {columns}x{rows}")
        return True
    except Exception as e:
        print(f"❌ Error detectando terminal: {e}")
        return False

def test_ascii_conversion():
    """Prueba la conversión básica a ASCII"""
    print("\n🎨 Probando conversión ASCII...")
    try:
        from PIL import Image
        
        # Crear imagen de prueba simple
        test_image = Image.new('L', (10, 5), color=128)
        
        # Convertir a ASCII básico
        ascii_chars = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]
        ascii_art = ""
        
        for y in range(test_image.height):
            for x in range(test_image.width):
                pixel_value = test_image.getpixel((x, y))
                ascii_index = int(pixel_value / 255 * (len(ascii_chars) - 1))
                ascii_art += ascii_chars[ascii_index]
            ascii_art += "\n"
        
        print("✅ Conversión ASCII exitosa:")
        print(ascii_art)
        return True
    except Exception as e:
        print(f"❌ Error en conversión ASCII: {e}")
        return False

def main():
    """Ejecuta todas las pruebas"""
    print("=" * 50)
    print("🧪 PRUEBAS DEL TRANSFORMADOR ASCII")
    print("=" * 50)
    
    # Test 1: Importaciones
    failed_imports = test_imports()
    
    if failed_imports:
        print(f"\n❌ Faltan dependencias: {', '.join(failed_imports)}")
        print("💡 Instala con: pip install " + " ".join(failed_imports))
        return False
    
    # Test 2: Captura de pantalla
    if not test_screen_capture():
        print("\n❌ La captura de pantalla no funciona")
        return False
    
    # Test 3: Tamaño de terminal
    if not test_terminal_size():
        print("\n❌ No se puede detectar el tamaño de terminal")
        return False
    
    # Test 4: Conversión ASCII
    if not test_ascii_conversion():
        print("\n❌ La conversión ASCII no funciona")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 ¡TODAS LAS PRUEBAS PASARON!")
    print("✅ El transformador está listo para usar")
    print("🚀 Ejecuta: python advanced_screen_to_ascii.py")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n👋 Pruebas interrumpidas por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Error inesperado: {e}")
        sys.exit(1)