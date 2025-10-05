# 🖥️ ASCII Screen Capture with Multithreading

Un proyecto en Python que captura la pantalla en tiempo real y la convierte a arte ASCII utilizando procesamiento en paralelo para mejorar la tasa de fotogramas. Este enfoque permite dividir la pantalla en matrices, donde cada matriz es procesada por un hilo separado, optimizando así el rendimiento de la aplicación.

## 🚀 Características

- 🎥 **Captura en tiempo real**: Convierte tu pantalla a ASCII mientras trabajas.
- ⚡ **Procesamiento en paralelo**: Utiliza hilos para procesar matrices de la pantalla simultáneamente.
- 📏 **Captura selectiva**: Permite seleccionar una región específica de la pantalla para capturar.
 - 📏 **Captura selectiva**: Permite seleccionar una región específica de la pantalla para capturar (arrastrando un rectángulo sobre la pantalla).
- 🎨 **Múltiples estilos ASCII**: Ofrece diferentes estilos de conversión de píxeles a caracteres ASCII.
- 📊 **Estadísticas de rendimiento**: Monitorea FPS y otros métricas en tiempo real.
- 🎯 **Interfaz intuitiva**: Fácil de usar con menús interactivos y salida en terminal.

## 🛠️ Requisitos

- Python 3.7+
- Dependencias necesarias (ver `requirements.txt`)

## 📦 Dependencias

Consulta el archivo `requirements.txt` para obtener la lista completa de dependencias necesarias para ejecutar el proyecto.

## 🚀 Uso

### Ejecución del Proyecto

Para ejecutar la aplicación, utiliza el siguiente comando en la terminal:

```bash
python src/main.py
```

### Seleccionar una región de la pantalla

1. En el menú principal, elige la opción "📏 Captura de región específica".
2. Se abrirá una superposición semitransparente en el monitor seleccionado.
3. Arrastra con el mouse para dibujar el rectángulo de captura y suelta para confirmar.
4. Presiona ESC o clic derecho para cancelar.

Consejo: Si la superposición no está disponible en tu entorno, el sistema usará un método alternativo en el que posicione el mouse en dos esquinas y confirmes con Enter.

## 📋 Estructura del Proyecto

```
ascii-screen-capture-threaded/
├── src
│   ├── main.py                  # Punto de entrada de la aplicación
│   ├── core
│   │   ├── __init__.py
│   │   ├── screen_capture.py     # Captura de pantalla y división en matrices
│   │   ├── ascii_converter.py    # Conversión de píxeles a ASCII
│   │   └── matrix_processor.py    # Procesamiento de matrices en paralelo
│   ├── threading
│   │   ├── __init__.py
│   │   ├── thread_manager.py     # Gestión de hilos
│   │   ├── matrix_worker.py      # Trabajo de cada hilo en una matriz
│   │   └── thread_pool.py        # Gestión de un grupo de hilos
│   ├── utils
│   │   ├── __init__.py
│   │   ├── config.py             # Configuración del proyecto
│   │   ├── performance.py        # Monitoreo de rendimiento
│   │   └── display.py            # Manejo de la salida en terminal
│   └── ui
│       ├── __init__.py
│       ├── menu.py               # Menú interactivo
│       └── terminal_ui.py        # Interfaz de usuario en terminal
├── tests
│   ├── __init__.py
│   ├── test_matrix_processor.py   # Pruebas para MatrixProcessor
│   ├── test_thread_manager.py     # Pruebas para ThreadManager
│   └── test_performance.py        # Pruebas para funciones de rendimiento
├── requirements.txt               # Dependencias del proyecto
├── setup.py                       # Script de configuración del proyecto
└── README.md                      # Documentación del proyecto
```

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Si tienes ideas para mejorar el proyecto, no dudes en abrir un issue o enviar un pull request.

## 📜 Licencia

Este proyecto está bajo licencia MIT. Puedes usarlo libremente para proyectos personales y comerciales.

## 🎉 ¡Disfruta!

¡Diviértete convirtiendo tu pantalla en arte ASCII y experimenta con diferentes configuraciones para encontrar la combinación perfecta para tu caso de uso!