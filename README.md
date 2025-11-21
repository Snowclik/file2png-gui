# 🔐 file2png v4 - Encrypted File ↔ PNG Converter

> Ultra-fast tool to convert any file to an AES-256 encrypted PNG image and vice versa. Includes modern GUI with dark theme.

> Herramienta ultra-rápida para convertir cualquier archivo a una imagen PNG cifrada con AES-256 y viceversa. Incluye interfaz gráfica moderna con tema oscuro.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## 📖 Documentation / Documentación

<details>
<summary>🇬🇧 <b>English Documentation</b></summary>

## ✨ Features

- 🔒 **AES-256 Encryption**: Military-grade file protection
- ⚡ **Ultra-Fast**: Processing with NumPy + Multiprocessing (100x faster)
- 🎨 **Graphical Interface**: Modern GUI with CustomTkinter and dark theme
- 🔀 **Random Salt**: Each conversion generates a unique image
- 📊 **Compression Levels**: Choose between speed or size
- 📈 **Progress Bars**: Real-time visual feedback
- 👁️ **Show/Hide Password**: Eye button to verify your password
- 📜 **Auto Scroll**: Interface adapts to any window size

## 📦 Installation

### Requirements

- Python 3.8 or higher
- pip (Python package manager)

### Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install numpy pillow cryptography customtkinter
```

## 🐧 Available Versions / Versiones Disponibles

This project includes **two versions** to suit different needs:

Este proyecto incluye **dos versiones** para diferentes necesidades:

### 🖥️ GUI Version (Graphical Interface)
**File:** `file2png-gui.py`

- ✅ Modern dark theme interface
- ✅ Interactive compression level selector (1-9)
- ✅ Real-time progress bars
- ✅ Show/hide password button
- ✅ Auto-scroll support
- ✅ Beginner-friendly

### ⌨️ CLI Version (Command Line)
**File:** `file2png.py`

- ✅ Fast and lightweight
- ✅ Scriptable and automatable
- ✅ Server-friendly (no GUI required)
- ⚠️ Compression level fixed in code (default: level 1)
- ✅ Advanced users

### 📊 Comparison Table / Tabla Comparativa

| Feature / Característica | GUI (`file2png-gui.py`) | CLI (`file2png.py`) |
|--------------------------|-------------------------|---------------------|
| **Ease of Use / Facilidad** | ⭐⭐⭐⭐⭐ Beginner-friendly | ⭐⭐⭐ Requires command line knowledge |
| **Compression Level / Nivel de Compresión** | ✅ Adjustable via slider (1-9) | ⚠️ Fixed in code (requires editing) |
| **Progress Feedback / Retroalimentación** | ✅ Visual progress bars | ⚠️ Text output only |
| **Password Visibility / Ver Contraseña** | ✅ Toggle button (👁️) | ❌ Hidden in terminal |
| **Automation / Automatización** | ❌ Manual operation | ✅ Scriptable |
| **Server Use / Uso en Servidor** | ❌ Requires display | ✅ Works headless |
| **Speed / Velocidad** | Fast / Rápido | Slightly faster / Ligeramente más rápido |

**Recommendation / Recomendación:**
- 🎨 **Use GUI** if you want ease of use and visual feedback
- ⚡ **Use CLI** if you need automation or server deployment

---

## 🚀 Usage / Uso

### 🖥️ GUI Version (Recommended for Beginners)

```bash
python file2png-gui.py
```

The interface will guide you step by step:

1. **Select mode**: Encode or Decode
2. **Choose file**: Click 📁 to select
3. **Output name** (encode only): Auto-completes, but you can edit it
4. **Enter password**: Use 👁️ button to show/hide
5. **Compression level** (encode only): Adjust according to your needs
6. **Process**: Click 🚀 Process

### ⌨️ CLI Version (For Advanced Users & Automation)

> **Note:** The CLI version uses a fixed compression level (default: 1). To change it, edit the `compress_level` parameter in the code.

#### Encode (File → PNG)

**Syntax:**
```bash
python file2png.py <source-file> <output.png> --password <your-password>
```

**Example:**
```bash
python file2png.py document.pdf encrypted.png --password MySecurePass123
```

#### Decode (PNG → File)

**Syntax:**
```bash
python file2png.py <encrypted.png> <output-folder> --password <your-password>
```

**Example:**
```bash
python file2png.py encrypted.png ./recovered --password MySecurePass123
```

## 📊 Compression Levels (GUI Only)

The GUI version allows you to choose the compression level. Higher levels = smaller file, but slower processing.

| Level | Speed | PNG Size | Seconds per 100 MB |
|-------|-------|----------|-------------------|
| 1-3   | ⚡ Fast | ~2.0x original | 15-20 sec |
| 4-6   | ⚠️ Medium | ~1.7x original | 60-120 sec |
| 7-9   | 🐌 Slow | ~1.5x original | 180-300 sec |

**Examples:**
- 100 MB file at level 1: ~15-20 seconds
- 500 MB file at level 1: ~75-100 seconds
- 1 GB file at level 1: ~150-200 seconds

**Recommendation**: Use level 1 for maximum speed. The size difference is minimal compared to time saved.

> **CLI Note:** The CLI version uses level 1 by default. To change it, edit `compress_level=1` in the code.

## 🔒 Security

- **Encryption**: AES-256-CBC (military standard)
- **Key Derivation**: PBKDF2-HMAC-SHA256 with 100,000 iterations
- **Random Salt**: 128 bits (16 bytes) unique per conversion
- **Random IV**: 128 bits for each encryption operation

> ⚠️ **IMPORTANT**: Without the correct password, the file CANNOT be recovered. Keep your password safe.

## 📁 Project Structure

```
.
├── file2png-gui.py     # Modern graphical interface (recommended)
├── file2png.py         # Original CLI version
├── README.md           # This file
├── requirements.txt    # Dependencies
└── LICENSE             # MIT License
```

## 🎯 Use Cases

- **Secure Backup**: Convert sensitive files to encrypted images
- **Discreet Transfer**: Send files as innocent-looking "images"
- **Cloud Storage**: Upload encrypted files to image services
- **Steganography**: Hide data in image format

## 🛠️ Technologies Used

- **Python 3.8+**: Programming language
- **NumPy**: Ultra-fast vectorized operations
- **Pillow (PIL)**: Image manipulation
- **cryptography**: AES-256 encryption
- **CustomTkinter**: Modern graphical interface
- **multiprocessing**: Parallel processing

## 📝 Examples

### Encode a Video

```bash
python file2png-gui.py
# Select: video.mp4
# Password: MyVideoSecret123
# Level: 1 (fast)
# Result: video_encrypted.png
```

### Decode a Document

```bash
python file2png-gui.py
# Mode: Decode
# Select: document_encrypted.png
# Password: MyDocSecret456
# Folder: ./recovered
# Result: document.pdf in ./recovered
```

## ⚡ Performance

Tested with **117 MB** file:

- **Encoding**: ~15-20 seconds (level 1)
- **Decoding**: ~10-15 seconds
- **CPU Usage**: Multicore (up to 8 cores)
- **PNG Size**: ~234 MB (2x original file)

## 🤝 Credits

This project is based on the original work by **mmoroca**:
- GitHub: [https://github.com/mmoroca/file2png](https://github.com/mmoroca/file2png)

### Implemented Improvements

- ✅ Modern GUI with CustomTkinter
- ✅ NumPy optimization (100x faster)
- ✅ Parallel processing with multiprocessing
- ✅ AES-256 encryption with random salt
- ✅ Compression level selector
- ✅ Progress bars and detailed logging
- ✅ Responsive design with auto-scroll
- ✅ Bilingual documentation (Spanish/English)

## 📄 License

This project is distributed under the MIT License. See the original file for more details.

## ⚠️ Warnings

- PNG size will be approximately **2x the original file size** (with level 1)
- Very large files (>1 GB) may take several minutes to process
- **Keep your password safe**: There is no way to recover the file without it
- Encryption is secure, but strength depends on your password

## 🐛 Known Issues

- On Windows, mouse wheel scrolling may affect other controls
- Extremely large files (>2 GB) may cause memory issues

## 📞 Support

If you find any issues or have suggestions, please open an issue in mmoroca's original repository.

---

**Developed with ❤️ by the Python community**

Based on [file2png](https://github.com/mmoroca/file2png) by mmoroca

</details>

<details>
<summary>🇪🇸 <b>Documentación en Español</b></summary>

## ✨ Características

- 🔒 **Cifrado AES-256**: Protección militar de tus archivos
- ⚡ **Ultra-Rápido**: Procesamiento con NumPy + Multiprocessing (100x más rápido)
- 🎨 **Interfaz Gráfica**: GUI moderna con CustomTkinter y tema oscuro
- 🔀 **Salt Aleatorio**: Cada conversión genera una imagen única
- 📊 **Niveles de Compresión**: Elige entre velocidad o tamaño
- 📈 **Barras de Progreso**: Retroalimentación visual en tiempo real
- 👁️ **Mostrar/Ocultar Contraseña**: Botón de ojo para verificar tu contraseña
- 📜 **Scroll Automático**: Interfaz adaptable a cualquier tamaño de ventana

## 📦 Instalación

### Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalar Dependencias

```bash
pip install -r requirements.txt
```

O manualmente:

```bash
pip install numpy pillow cryptography customtkinter
```

## 🐧 Versiones Disponibles

Este proyecto incluye **dos versiones** para diferentes necesidades:

### 🖥️ Versión GUI (Interfaz Gráfica)
**Archivo:** `file2png-gui.py`

- ✅ Interfaz moderna con tema oscuro
- ✅ Selector interactivo de nivel de compresión (1-9)
- ✅ Barras de progreso en tiempo real
- ✅ Botón para mostrar/ocultar contraseña
- ✅ Soporte de scroll automático
- ✅ Amigable para principiantes

### ⌨️ Versión CLI (Línea de Comandos)
**Archivo:** `file2png.py`

- ✅ Rápida y ligera
- ✅ Scriptable y automatizable
- ✅ Funciona en servidores (sin GUI)
- ⚠️ Nivel de compresión fijo en el código (predeterminado: nivel 1)
- ✅ Para usuarios avanzados

### 📊 Tabla Comparativa

| Característica | GUI (`file2png-gui.py`) | CLI (`file2png.py`) |
|----------------|-------------------------|---------------------|
| **Facilidad de Uso** | ⭐⭐⭐⭐⭐ Amigable para principiantes | ⭐⭐⭐ Requiere conocimientos de línea de comandos |
| **Nivel de Compresión** | ✅ Ajustable con slider (1-9) | ⚠️ Fijo en código (requiere edición) |
| **Retroalimentación de Progreso** | ✅ Barras de progreso visuales | ⚠️ Solo salida de texto |
| **Visibilidad de Contraseña** | ✅ Botón de alternar (👁️) | ❌ Oculta en terminal |
| **Automatización** | ❌ Operación manual | ✅ Scriptable |
| **Uso en Servidor** | ❌ Requiere pantalla | ✅ Funciona sin GUI |
| **Velocidad** | Rápido | Ligeramente más rápido |

**Recomendación:**
- 🎨 **Usa GUI** si quieres facilidad de uso y retroalimentación visual
- ⚡ **Usa CLI** si necesitas automatización o despliegue en servidor

---

## 🚀 Uso

### 🖥️ Versión GUI (Recomendada para Principiantes)

```bash
python file2png-gui.py
```

La interfaz te guiará paso a paso:

1. **Selecciona el modo**: Codificar o Decodificar
2. **Elige el archivo**: Haz clic en 📁 para seleccionar
3. **Nombre de salida** (solo codificar): Se auto-completa, pero puedes editarlo
4. **Ingresa contraseña**: Usa el botón 👁️ para mostrar/ocultar
5. **Nivel de compresión** (solo codificar): Ajusta según tus necesidades
6. **Procesar**: Haz clic en 🚀 Procesar

### ⌨️ Versión CLI (Para Usuarios Avanzados y Automatización)

> **Nota:** La versión CLI usa un nivel de compresión fijo (predeterminado: 1). Para cambiarlo, edita el parámetro `compress_level` en el código.

#### Codificar (Archivo → PNG)

**Sintaxis:**
```bash
python file2png.py <archivo-origen> <salida.png> --password <tu-contraseña>
```

**Ejemplo:**
```bash
python file2png.py documento.pdf cifrado.png --password MiClaveSegura123
```

#### Decodificar (PNG → Archivo)

**Sintaxis:**
```bash
python file2png.py <cifrado.png> <carpeta-salida> --password <tu-contraseña>
```

**Ejemplo:**
```bash
python file2png.py cifrado.png ./recuperados --password MiClaveSegura123
```

## 📊 Niveles de Compresión (Solo GUI)

La versión GUI te permite elegir el nivel de compresión. Niveles más altos = archivo más pequeño, pero procesamiento más lento.

| Nivel | Velocidad | Tamaño PNG | Segundos por 100 MB |
|-------|-----------|------------|---------------------|
| 1-3   | ⚡ Rápido | ~2.0x original | 15-20 seg |
| 4-6   | ⚠️ Medio  | ~1.7x original | 60-120 seg |
| 7-9   | 🐌 Lento  | ~1.5x original | 180-300 seg |

**Ejemplos:**
- Archivo de 100 MB en nivel 1: ~15-20 segundos
- Archivo de 500 MB en nivel 1: ~75-100 segundos
- Archivo de 1 GB en nivel 1: ~150-200 segundos

**Recomendación**: Usa nivel 1 para máxima velocidad. La diferencia de tamaño es mínima comparada con el tiempo ahorrado.

> **Nota CLI:** La versión CLI usa nivel 1 por defecto. Para cambiarlo, edita `compress_level=1` en el código.

## 🔒 Seguridad

- **Cifrado**: AES-256-CBC (estándar militar)
- **Derivación de Clave**: PBKDF2-HMAC-SHA256 con 100,000 iteraciones
- **Salt Aleatorio**: 128 bits (16 bytes) único por conversión
- **IV Aleatorio**: 128 bits para cada operación de cifrado

> ⚠️ **IMPORTANTE**: Sin la contraseña correcta, el archivo NO puede ser recuperado. Guarda tu contraseña de forma segura.

## 📁 Estructura del Proyecto

```
.
├── file2png-gui.py     # Interfaz gráfica moderna (recomendado)
├── file2png.py         # Versión CLI original
├── README.md           # Este archivo
├── requirements.txt    # Dependencias
└── LICENSE             # Licencia MIT
```

## 🎯 Casos de Uso

- **Backup Seguro**: Convierte archivos sensibles a imágenes cifradas
- **Transferencia Discreta**: Envía archivos como "imágenes" inocentes
- **Almacenamiento en la Nube**: Sube archivos cifrados a servicios de imágenes
- **Esteganografía**: Oculta datos en formato de imagen

## 🛠️ Tecnologías Utilizadas

- **Python 3.8+**: Lenguaje de programación
- **NumPy**: Operaciones vectorizadas ultra-rápidas
- **Pillow (PIL)**: Manipulación de imágenes
- **cryptography**: Cifrado AES-256
- **CustomTkinter**: Interfaz gráfica moderna
- **multiprocessing**: Procesamiento paralelo

## 📝 Ejemplos

### Codificar un Video

```bash
python file2png-gui.py
# Selecciona: video.mp4
# Contraseña: MiVideoSecreto123
# Nivel: 1 (rápido)
# Resultado: video_encrypted.png
```

### Decodificar un Documento

```bash
python file2png-gui.py
# Modo: Decodificar
# Selecciona: documento_encrypted.png
# Contraseña: MiDocSecreto456
# Carpeta: ./recuperados
# Resultado: documento.pdf en ./recuperados
```

## ⚡ Rendimiento

Probado con archivo de **117 MB**:

- **Codificación**: ~15-20 segundos (nivel 1)
- **Decodificación**: ~10-15 segundos
- **Uso de CPU**: Multicore (hasta 8 núcleos)
- **Tamaño PNG**: ~234 MB (2x archivo original)

## 🤝 Créditos

Este proyecto está basado en el trabajo original de **mmoroca**:
- GitHub: [https://github.com/mmoroca/file2png](https://github.com/mmoroca/file2png)

### Mejoras Implementadas

- ✅ Interfaz gráfica moderna con CustomTkinter
- ✅ Optimización con NumPy (100x más rápido)
- ✅ Procesamiento paralelo con multiprocessing
- ✅ Cifrado AES-256 con salt aleatorio
- ✅ Selector de nivel de compresión
- ✅ Barras de progreso y logging detallado
- ✅ Diseño responsive con scroll automático
- ✅ Documentación bilingüe (español/inglés)

## 📄 Licencia

Este proyecto se distribuye bajo la licencia MIT. Ver el archivo original para más detalles.

## ⚠️ Advertencias

- El tamaño del PNG será aproximadamente **2x el tamaño del archivo original** (con nivel 1)
- Archivos muy grandes (>1 GB) pueden tardar varios minutos en procesarse
- **Guarda tu contraseña de forma segura**: No hay forma de recuperar el archivo sin ella
- El cifrado es seguro, pero la fortaleza depende de tu contraseña

## 🐛 Problemas Conocidos

- En Windows, el scroll con rueda del mouse puede afectar otros controles
- Archivos extremadamente grandes (>2 GB) pueden causar problemas de memoria

## 📞 Soporte

Si encuentras algún problema o tienes sugerencias, por favor abre un issue en el repositorio original de mmoroca.

---

**Desarrollado con ❤️ por la comunidad de Python**

Basado en [file2png](https://github.com/mmoroca/file2png) de mmoroca

</details>

---

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run GUI
python file2png-gui.py

# Or use CLI
python file2png.py <source> <destination> --password <your-password>
```
