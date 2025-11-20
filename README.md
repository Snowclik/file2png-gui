# 🔐 file2png v4 - Conversor de Archivos ↔ PNG Cifrado

Herramienta ultra-rápida para convertir cualquier archivo a una imagen PNG cifrada con AES-256 y viceversa. Incluye interfaz gráfica moderna con tema oscuro.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

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
pip install numpy pillow cryptography customtkinter
```

O usando el archivo de requisitos:

```bash
pip install -r requirements.txt
```

## 🚀 Uso

### Interfaz Gráfica (Recomendado)

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

### Línea de Comandos

#### Codificar (Archivo → PNG)

```bash
python file2png.py documento.pdf salida.png --password miSecreto123
```

#### Decodificar (PNG → Archivo)

```bash
python file2png.py salida.png ./recuperados --password miSecreto123
```

## 📊 Niveles de Compresión

| Nivel | Velocidad | Tamaño PNG | Tiempo (100 MB) |
|-------|-----------|------------|-----------------|
| 1-3   | ⚡ Rápido | ~2x archivo | ~15-20 seg |
| 4-6   | ⚠️ Medio  | ~1.7x archivo | ~1-2 min |
| 7-9   | 🐌 Lento  | ~1.5x archivo | ~3-5 min |

**Recomendación**: Usa nivel 1 para máxima velocidad. La diferencia de tamaño es mínima comparada con el tiempo ahorrado.

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
# Contraseña: miVideoSecreto123
# Nivel: 1 (rápido)
# Resultado: video_encrypted.png
```

### Decodificar un Documento

```bash
python file2png-gui.py
# Modo: Decodificar
# Selecciona: documento_encrypted.png
# Contraseña: miDocumentoSecreto456
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
