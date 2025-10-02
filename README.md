# 🖥️ Transformador de Pantalla a ASCII

Un programa en Python que captura tu pantalla en tiempo real y la convierte a arte ASCII para mostrarla en la terminal.

## ✨ Características

- 🎥 **Captura en tiempo real**: Convierte tu pantalla a ASCII mientras trabajas
- 📏 **Captura selectiva**: Elige una región específica de la pantalla
- 🎨 **Múltiples estilos ASCII**: Desde detallado hasta bloques simples
- ⚡ **Optimizado para rendimiento**: Ajuste automático de FPS y resolución
- 📊 **Estadísticas en tiempo real**: Monitorea FPS y rendimiento
- 🎯 **Interfaz intuitiva**: Fácil de usar con menús interactivos

## 🛠️ Requisitos

- Python 3.7+
- Windows (o adaptar comandos de terminal para otros SO)

### 📦 Dependencias

```bash
pip install Pillow pyautogui colorama
```

## 🚀 Uso

### Versión Básica
```bash
python screen_to_ascii.py
```

### Versión Avanzada (Recomendada)
```bash
python advanced_screen_to_ascii.py
```

## 📋 Opciones Disponibles

### 1. 🖥️ Captura Completa
- Captura toda la pantalla
- Conversión automática a ASCII
- Ajuste automático al tamaño de terminal

### 2. 📏 Captura Selectiva
- Selecciona una región específica
- Ideal para enfocar en una aplicación
- Mejor rendimiento al capturar menos área

### 3. 🎨 Configuración Avanzada
- **Estilos ASCII**:
  - `detailed`: @#S%?*+;:,. (mayor detalle)
  - `simple`: █▓▒░  (bloques simples)
  - `gradient`: .:-=+*#%@ (gradiente suave)
- **FPS ajustable**: 1-30 fotogramas por segundo
- **Información en tiempo real**: Estadísticas de rendimiento

## ⚙️ Configuración

Edita `config.py` para personalizar:

```python
# Estilos de ASCII
ASCII_CHARS_DETAILED = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]
ASCII_CHARS_SIMPLE = ["█", "▓", "▒", "░", " "]

# Rendimiento
DEFAULT_FPS = 10
MAX_FPS = 30

# Ajustes de imagen
DEFAULT_WIDTH_SCALE = 0.9  # Usar 90% del ancho de terminal
ASPECT_RATIO_CORRECTION = 0.55  # Corrección altura/ancho
```

## 🎮 Controles

- **Iniciar**: Selecciona opción del menú
- **Detener**: `Ctrl+C` durante la captura
- **Salir**: Opción 4 en el menú principal

## 💡 Consejos de Uso

### Para Mejor Rendimiento:
- Usa FPS más bajos (5-10) para menos carga de CPU
- Captura regiones pequeñas en lugar de pantalla completa
- Cierra aplicaciones innecesarias mientras usas el programa

### Para Mejor Calidad Visual:
- Usa terminales con fuentes monoespaciadas
- Ajusta el tamaño de fuente de tu terminal
- Prueba diferentes estilos ASCII según el contenido

### Casos de Uso Interesantes:
- 📺 Ver videos en ASCII
- 🎮 Convertir juegos a ASCII art
- 👀 Monitorear aplicaciones de forma minimalista
- 🎨 Crear arte ASCII en tiempo real
- 📱 Demostrar aplicaciones de forma retro

## 🐛 Solución de Problemas

### El programa se ejecuta muy lento:
- Reduce el FPS (usa 5-8 FPS)
- Captura una región más pequeña
- Cierra otras aplicaciones

### La imagen se ve distorsionada:
- Ajusta `ASPECT_RATIO_CORRECTION` en config.py
- Cambia el tamaño de fuente de tu terminal
- Prueba diferentes estilos ASCII

### Error de captura de pantalla:
- Ejecuta como administrador si es necesario
- Verifica que pyautogui esté instalado correctamente
- En algunos sistemas, puede requerir permisos especiales

## 📁 Estructura del Proyecto

```
trasnform ascci/
│
├── screen_to_ascii.py          # Versión básica
├── advanced_screen_to_ascii.py # Versión avanzada (recomendada)
├── config.py                   # Configuración
└── README.md                   # Esta documentación
```

## 🔧 Personalización Avanzada

### Crear Tus Propios Caracteres ASCII:

```python
# En config.py, agrega tu propio estilo:
ASCII_CHARS_CUSTOM = ["🌑", "🌘", "🌗", "🌖", "🌕"]
```

### Modificar la Captura:

```python
# Capturar múltiples monitores
# Modificar capture_screen() en el código principal
```

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Ideas para mejorar:

- 🎨 Más estilos de ASCII
- 🖼️ Soporte para múltiples monitores
- 💾 Grabación a archivo
- 🌈 ASCII con colores
- 🔊 Sincronización con audio

## 📜 Licencia

Este proyecto está bajo licencia MIT. Úsalo libremente para proyectos personales y comerciales.

## 🎉 ¡Disfruta!

¡Diviértete convirtiendo tu pantalla en arte ASCII! Experimenta con diferentes configuraciones y encuentra la combinación perfecta para tu caso de uso.

---
*Hecho con ❤️ y Python*