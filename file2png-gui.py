"""
file2png GUI v4 - Interfaz Gráfica INDEPENDIENTE
Conversor de Archivos ↔ PNG Cifrado con AES-256
Versión standalone - No requiere otros archivos Python

Basado en el proyecto original de mmoroca:
https://github.com/mmoroca/file2png

INSTALACIÓN DE DEPENDENCIAS:
pip install numpy pillow cryptography customtkinter

CARACTERÍSTICAS:
- Cifrado AES-256 con protección por contraseña
- Procesamiento ultra-rápido con NumPy + Multiprocessing
- Interfaz gráfica moderna con tema oscuro
- Selector de nivel de compresión PNG
- Barras de progreso y logging detallado
- Salt aleatorio para máxima seguridad
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import os
import sys
from pathlib import Path

# Importaciones para el procesamiento
from PIL import Image
import zipfile
import io
import numpy as np
from multiprocessing import Pool, cpu_count
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

WHITE = 255
BLACK = 0
GRAY_PADDING = 127
SALT_SIZE = 16
KEY_SIZE = 32
CHUNK_SIZE = 10 * 1024 * 1024

# ============================================================================
# FUNCIONES DE CIFRADO/DESCIFRADO
# ============================================================================

def derive_key(password: str, salt: bytes) -> bytes:
    """Derive a 256-bit key from password using PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_SIZE,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode('utf-8'))

def encrypt_data(data: bytes, password: str) -> tuple:
    """Encrypt data with AES-256-CBC."""
    salt = os.urandom(SALT_SIZE)
    key = derive_key(password, salt)
    iv = os.urandom(16)
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    padding_length = 16 - (len(data) % 16)
    padded_data = data + bytes([padding_length]) * padding_length
    encrypted = encryptor.update(padded_data) + encryptor.finalize()
    
    return iv + encrypted, salt

def decrypt_data(encrypted_data: bytes, password: str, salt: bytes) -> bytes:
    """Decrypt AES-256-CBC encrypted data."""
    key = derive_key(password, salt)
    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    
    padding_length = padded_data[-1]
    return padded_data[:-padding_length]

def process_chunk(args):
    """Process a chunk of bytes to bits."""
    chunk_data, start_idx = args
    byte_array = np.frombuffer(chunk_data, dtype=np.uint8)
    bits = np.unpackbits(byte_array)
    return start_idx, bits

# ============================================================================
# FUNCIONES DE CODIFICACIÓN/DECODIFICACIÓN
# ============================================================================

def encode_file_gui(file_path, png_dest_path, password, compression_level=1, log_callback=None):
    """Encode file to PNG with GUI logging."""
    def log(msg):
        if log_callback:
            log_callback(msg)
        print(msg)
    
    ext = os.path.splitext(file_path)[1].lower()
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    log(f"📂 Procesando: {os.path.basename(file_path)} ({file_size_mb:.2f} MB)")
    
    try:
        # Step 1: Compress to ZIP
        if ext == '.zip':
            log("ℹ️  Archivo ya es ZIP. Leyendo bytes...")
            with open(file_path, 'rb') as f:
                binary_data = f.read()
        else:
            log("ℹ️  Comprimiendo a ZIP...")
            buffer_zip = io.BytesIO()
            with zipfile.ZipFile(buffer_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
                clean_name = os.path.basename(file_path)
                zf.write(file_path, arcname=clean_name)
            binary_data = buffer_zip.getvalue()
            log(f"   ✓ Comprimido: {len(binary_data):,} bytes")
        
        # Step 2: Encrypt
        log("🔐 Cifrando con AES-256...")
        encrypted_data, salt = encrypt_data(binary_data, password)
        log(f"   ✓ Cifrado: {len(encrypted_data):,} bytes")
        
        # Step 3: Convert to bits
        log("🎨 Convirtiendo a bitmap...")
        salt_array = np.frombuffer(salt, dtype=np.uint8)
        salt_bits = np.unpackbits(salt_array)
        
        data_size = len(encrypted_data)
        num_processes = min(cpu_count(), 8)
        
        if data_size > CHUNK_SIZE * 2:
            log(f"   Usando {num_processes} núcleos de CPU...")
            chunks = []
            for i in range(0, data_size, CHUNK_SIZE):
                chunk = encrypted_data[i:i + CHUNK_SIZE]
                chunks.append((chunk, i))
            
            with Pool(num_processes) as pool:
                results = pool.map(process_chunk, chunks)
            
            results.sort(key=lambda x: x[0])
            data_bits = np.concatenate([bits for _, bits in results])
        else:
            byte_array = np.frombuffer(encrypted_data, dtype=np.uint8)
            data_bits = np.unpackbits(byte_array)
        
        all_bits = np.concatenate([salt_bits, data_bits])
        
        # Step 4: Create image
        num_bits = len(all_bits)
        side = int(np.ceil(np.sqrt(num_bits)))
        total_pixels = side * side
        log(f"   Dimensiones: {side}x{side} = {total_pixels:,} píxeles")
        
        padded = np.pad(all_bits, (0, total_pixels - num_bits), constant_values=2)
        pixel_map = np.array([BLACK, WHITE, GRAY_PADDING], dtype=np.uint8)
        pixels = pixel_map[padded]
        img_array = pixels.reshape(side, side)
        
        # Step 5: Save PNG
        log(f"💾 Guardando PNG (compresión nivel {compression_level})...")
        img = Image.fromarray(img_array, mode='L')
        
        if not png_dest_path.lower().endswith('.png'):
            png_dest_path += '.png'
        
        img.save(png_dest_path, compress_level=compression_level)
        
        file_size_mb = os.path.getsize(png_dest_path) / (1024 * 1024)
        log(f"✅ Imagen cifrada guardada: {os.path.basename(png_dest_path)}")
        log(f"   📊 Tamaño PNG: {file_size_mb:.2f} MB")
        log(f"   🔒 ¡Recuerda tu contraseña!")
        
        return True
    except Exception as e:
        log(f"❌ Error de codificación: {e}")
        return False

def decode_png_gui(png_path, dest_folder, password, log_callback=None):
    """Decode PNG to file with GUI logging."""
    def log(msg):
        if log_callback:
            log_callback(msg)
        print(msg)
    
    log(f"🔍 Leyendo imagen cifrada: {os.path.basename(png_path)}")
    
    try:
        Image.MAX_IMAGE_PIXELS = None
        
        # Step 1: Load image
        img = Image.open(png_path).convert('L')
        width, height = img.size
        log(f"   Tamaño: {width}x{height} = {width*height:,} píxeles")
        
        img_array = np.array(img, dtype=np.uint8)
        
        # Step 2: Extract bits
        log("🔓 Extrayendo bits...")
        flat_pixels = img_array.flatten()
        
        black_mask = (flat_pixels == BLACK)
        white_mask = (flat_pixels == WHITE)
        valid_mask = black_mask | white_mask
        num_valid = np.sum(valid_mask)
        
        log(f"   Encontrados {num_valid:,} bits de datos")
        
        bits = white_mask[valid_mask].astype(np.uint8)
        
        # Step 3: Extract salt
        salt_bits_count = SALT_SIZE * 8
        salt_bits = bits[:salt_bits_count]
        data_bits = bits[salt_bits_count:]
        
        salt = np.packbits(salt_bits).tobytes()
        log(f"   Salt extraído: {len(salt)} bytes")
        
        # Step 4: Reconstruct bytes
        log("🔄 Reconstruyendo datos cifrados...")
        remainder = len(data_bits) % 8
        if remainder != 0:
            data_bits = np.pad(data_bits, (0, 8 - remainder), constant_values=0)
        
        encrypted_bytes = np.packbits(data_bits).tobytes()
        log(f"   Datos cifrados: {len(encrypted_bytes):,} bytes")
        
        # Step 5: Decrypt
        log("🔐 Descifrando con AES-256...")
        try:
            decrypted_data = decrypt_data(encrypted_bytes, password, salt)
            log(f"   Tamaño descifrado: {len(decrypted_data):,} bytes")
        except Exception as e:
            log(f"❌ Descifrado fallido: Contraseña incorrecta o datos corruptos")
            return False
        
        # Step 6: Extract ZIP
        log("📦 Extrayendo archivos del ZIP...")
        
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)
        
        memory_buffer = io.BytesIO(decrypted_data)
        
        try:
            with zipfile.ZipFile(memory_buffer, 'r') as zf:
                zf.extractall(path=dest_folder)
                names = zf.namelist()
                log(f"✅ Archivos recuperados en '{dest_folder}':")
                for name in names:
                    file_path = os.path.join(dest_folder, name)
                    file_size = os.path.getsize(file_path)
                    log(f"   - {name} ({file_size:,} bytes)")
            return True
        except zipfile.BadZipFile:
            log("❌ Error: Los datos descifrados no forman un ZIP válido")
            return False
            
    except Exception as e:
        log(f"❌ Error de decodificación: {e}")
        return False

# ============================================================================
# INTERFAZ GRÁFICA
# ============================================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class File2PngGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("🔐 file2png v4 - Conversor Cifrado")
        self.geometry("750x750")  # Tamaño inicial más compacto
        self.resizable(True, True)
        self.minsize(700, 600)  # Tamaño mínimo más pequeño
        
        # Configurar grid para que se adapte
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.selected_file = None
        self.output_name = ctk.StringVar(value="")
        self.mode = ctk.StringVar(value="encode")
        self.compression_level = ctk.IntVar(value=1)
        
        self.create_widgets()
        
    def create_widgets(self):
        # Crear un canvas con scrollbar para scroll vertical
        canvas = ctk.CTkCanvas(self, bg="#2b2b2b", highlightthickness=0)
        scrollbar = ctk.CTkScrollbar(self, orientation="vertical", command=canvas.yview)
        
        # Frame scrollable dentro del canvas
        scrollable_frame = ctk.CTkFrame(canvas)
        
        # Configurar el canvas
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        # Crear ventana en el canvas y guardar ID
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        # Hacer que el frame se expanda al ancho del canvas
        def _configure_canvas(event):
            canvas.itemconfig(canvas_window, width=event.width)
        
        canvas.bind("<Configure>", _configure_canvas)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Empacar canvas y scrollbar
        canvas.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)
        
        # Guardar referencia al contenedor scrollable
        self.main_container = scrollable_frame
        
        # Habilitar scroll con rueda del mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Header (más compacto)
        header_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        header_frame.pack(pady=10, padx=10, fill="x")
        
        title_label = ctk.CTkLabel(header_frame, text="🔐 file2png v4",
                                   font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack()
        
        subtitle_label = ctk.CTkLabel(header_frame, 
                                      text="Conversor Ultra-Rápido con Cifrado AES-256",
                                      font=ctk.CTkFont(size=12), text_color="gray")
        subtitle_label.pack()
        
        # Mode selector
        mode_frame = ctk.CTkFrame(self.main_container)
        mode_frame.pack(pady=8, padx=10, fill="x")
        
        ctk.CTkLabel(mode_frame, text="Modo:", font=ctk.CTkFont(size=13, weight="bold")).pack(side="left", padx=10)
        
        ctk.CTkRadioButton(mode_frame, text="📤 Codificar",
                          variable=self.mode, value="encode",
                          command=self.update_ui_for_mode).pack(side="left", padx=5)
        
        ctk.CTkRadioButton(mode_frame, text="📥 Decodificar",
                          variable=self.mode, value="decode",
                          command=self.update_ui_for_mode).pack(side="left", padx=5)
        
        # File selection
        file_frame = ctk.CTkFrame(self.main_container)
        file_frame.pack(pady=8, padx=10, fill="x")
        
        ctk.CTkLabel(file_frame, text="Archivo de entrada:", 
                    font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=10, pady=(8, 3))
        
        file_select_frame = ctk.CTkFrame(file_frame, fg_color="transparent")
        file_select_frame.pack(fill="x", padx=10, pady=(0, 8))
        
        self.file_entry = ctk.CTkEntry(file_select_frame, placeholder_text="Selecciona un archivo...",
                                       height=35, font=ctk.CTkFont(size=11))
        self.file_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        
        ctk.CTkButton(file_select_frame, text="📁", command=self.select_file,
                     width=35, height=35, font=ctk.CTkFont(size=16)).pack(side="right")
        
        # Output name (NUEVO)
        self.output_frame = ctk.CTkFrame(self.main_container)
        self.output_frame.pack(pady=8, padx=10, fill="x")
        
        ctk.CTkLabel(self.output_frame, text="Nombre de salida:", 
                    font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=10, pady=(8, 3))
        
        self.output_entry = ctk.CTkEntry(self.output_frame, 
                                        textvariable=self.output_name,
                                        placeholder_text="archivo_cifrado.png",
                                        height=35, font=ctk.CTkFont(size=11))
        self.output_entry.pack(fill="x", padx=10, pady=(0, 8))
        
        
        # Password
        password_frame = ctk.CTkFrame(self.main_container)
        password_frame.pack(pady=8, padx=10, fill="x")
        
        # Guardar referencia para update_ui_for_mode
        self.password_frame = password_frame
        
        ctk.CTkLabel(password_frame, text="Contraseña:", 
                    font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=10, pady=(8, 3))
        
        password_input_frame = ctk.CTkFrame(password_frame, fg_color="transparent")
        password_input_frame.pack(fill="x", padx=10, pady=(0, 8))
        
        self.password_entry = ctk.CTkEntry(password_input_frame, placeholder_text="Ingresa una contraseña segura...",
                                          show="●", height=35, font=ctk.CTkFont(size=11))
        self.password_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        
        self.password_visible = False
        self.toggle_password_btn = ctk.CTkButton(password_input_frame, text="👁️", width=35, height=35,
                                                 command=self.toggle_password_visibility,
                                                 font=ctk.CTkFont(size=14))
        self.toggle_password_btn.pack(side="right")
        
        # Compression level
        self.compression_frame = ctk.CTkFrame(self.main_container)
        self.compression_frame.pack(pady=8, padx=10, fill="x")
        
        ctk.CTkLabel(self.compression_frame, text="Nivel de Compresión PNG:",
                    font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=10, pady=(8, 3))
        
        slider_frame = ctk.CTkFrame(self.compression_frame, fg_color="transparent")
        slider_frame.pack(fill="x", padx=10, pady=(0, 3))
        
        self.compression_slider = ctk.CTkSlider(slider_frame, from_=1, to=9, number_of_steps=8,
                                               variable=self.compression_level,
                                               command=self.update_compression_info)
        self.compression_slider.pack(side="left", fill="x", expand=True, padx=(0, 8))
        
        self.compression_value_label = ctk.CTkLabel(slider_frame, text="1",
                                                    font=ctk.CTkFont(size=13, weight="bold"), width=25)
        self.compression_value_label.pack(side="right")
        
        self.compression_alert = ctk.CTkLabel(self.compression_frame,
                                             text="⚡ Rápido: ~15-20 seg por 100 MB",
                                             font=ctk.CTkFont(size=11), text_color="#4CAF50", anchor="w")
        self.compression_alert.pack(anchor="w", padx=10, pady=(0, 8))
        
        # Progress
        progress_frame = ctk.CTkFrame(self.main_container)
        progress_frame.pack(pady=8, padx=10, fill="x")
        
        self.progress_bar = ctk.CTkProgressBar(progress_frame, height=15)
        self.progress_bar.pack(fill="x", padx=10, pady=8)
        self.progress_bar.set(0)
        
        self.status_label = ctk.CTkLabel(progress_frame, text="Listo para procesar",
                                         font=ctk.CTkFont(size=11), text_color="gray")
        self.status_label.pack(padx=10, pady=(0, 8))
        
        # Log (más compacto)
        log_frame = ctk.CTkFrame(self.main_container)
        log_frame.pack(pady=8, padx=10, fill="both", expand=True)
        
        ctk.CTkLabel(log_frame, text="Registro:", 
                    font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=10, pady=(8, 3))
        
        self.log_text = ctk.CTkTextbox(log_frame, height=100, font=ctk.CTkFont(size=10))
        self.log_text.pack(fill="both", expand=True, padx=10, pady=(0, 8))
        
        # Action button (SIEMPRE VISIBLE)
        button_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        button_frame.pack(pady=5, padx=10, fill="x")
        
        self.process_button = ctk.CTkButton(button_frame, text="🚀 Procesar",
                                           command=self.process_file, height=45,
                                           font=ctk.CTkFont(size=15, weight="bold"),
                                           fg_color="#2196F3", hover_color="#1976D2")
        self.process_button.pack(fill="x")
        
    def toggle_password_visibility(self):
        """Toggle password visibility"""
        self.password_visible = not self.password_visible
        if self.password_visible:
            self.password_entry.configure(show="")
            self.toggle_password_btn.configure(text="🙈")
        else:
            self.password_entry.configure(show="●")
            self.toggle_password_btn.configure(text="👁️")
    
    def update_ui_for_mode(self):
        """Update UI based on selected mode - show/hide widgets"""
        if self.mode.get() == "decode":
            # Ocultar campos específicos de codificación
            self.output_frame.pack_forget()
            self.compression_frame.pack_forget()
        else:
            # Mostrar campos de codificación
            # Asegurarse de que estén en el orden correcto
            # Primero desempacar
            self.output_frame.pack_forget()
            self.compression_frame.pack_forget()
            
            # Luego empacar en el orden correcto
            # output_frame debe ir después de file_frame (antes de password_frame)
            # Encontrar el password_frame y empacar antes de él
            all_children = list(self.main_container.winfo_children())
            
            # Buscar índice del password_frame
            password_idx = None
            for i, child in enumerate(all_children):
                if child == self.password_frame:
                    password_idx = i
                    break
            
            if password_idx is not None and password_idx > 0:
                # Empacar output_frame antes de password_frame
                self.output_frame.pack(pady=8, padx=10, fill="x", before=self.password_frame)
                # Empacar compression_frame después de password_frame
                self.compression_frame.pack(pady=8, padx=10, fill="x", after=self.password_frame)
            else:
                # Fallback: empacar al final
                self.output_frame.pack(pady=8, padx=10, fill="x")
                self.compression_frame.pack(pady=8, padx=10, fill="x")
    
    def _get_widget_by_label(self, container, label_text):
        """Helper to find a widget by its label text"""
        for child in container.winfo_children():
            try:
                for widget in child.winfo_children():
                    if isinstance(widget, ctk.CTkLabel):
                        if label_text in widget.cget("text"):
                            return child
            except:
                pass
        return None
    
    def select_file(self):
        """Select input file and auto-populate output name"""
        if self.mode.get() == "encode":
            file_path = filedialog.askopenfilename(
                title="Selecciona un archivo para codificar",
                filetypes=[("Todos los archivos", "*.*")])
            
            # Auto-generar nombre de salida
            if file_path:
                base_name = Path(file_path).stem
                self.output_name.set(f"{base_name}_encrypted.png")
        else:
            file_path = filedialog.askopenfilename(
                title="Selecciona una imagen PNG para decodificar",
                filetypes=[("Imágenes PNG", "*.png"), ("Todos los archivos", "*.*")])
        
        if file_path:
            self.selected_file = file_path
            self.file_entry.delete(0, "end")
            self.file_entry.insert(0, file_path)
            self.log(f"✓ Archivo seleccionado: {os.path.basename(file_path)}")
    
    
    def update_compression_info(self, value):
        """Update compression level info"""
        level = int(value)
        self.compression_value_label.configure(text=str(level))
        
        if level <= 3:
            self.compression_alert.configure(
                text="⚡ Rápido: ~15-20 seg por 100 MB | Tamaño: ~2x archivo original",
                text_color="#4CAF50")
        elif level <= 6:
            self.compression_alert.configure(
                text="⚠️ Medio: ~1-2 min por 100 MB | Tamaño: ~1.7x archivo original",
                text_color="#FF9800")
        else:
            self.compression_alert.configure(
                text="🐌 Lento: ~3-5 min por 100 MB | Tamaño: ~1.5x archivo original",
                text_color="#F44336")
    
    def log(self, message):
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.update()
    
    def update_status(self, message, progress=None):
        self.status_label.configure(text=message)
        if progress is not None:
            self.progress_bar.set(progress)
        self.update()
    
    def process_file(self):
        if not self.selected_file:
            messagebox.showerror("Error", "Por favor selecciona un archivo")
            return
        
        password = self.password_entry.get()
        if not password:
            messagebox.showerror("Error", "Por favor ingresa una contraseña")
            return
        
        # Solo sugerir contraseña larga al codificar
        if self.mode.get() == "encode" and len(password) < 6:
            messagebox.showwarning("Advertencia", "Se recomienda una contraseña de al menos 6 caracteres")
        
        self.process_button.configure(state="disabled", text="⏳ Procesando...")
        self.log_text.delete("1.0", "end")
        
        thread = threading.Thread(target=self.process_thread, args=(password,))
        thread.daemon = True
        thread.start()
    
    def process_thread(self, password):
        try:
            if self.mode.get() == "encode":
                self.encode_process(password)
            else:
                self.decode_process(password)
        except Exception as e:
            self.log(f"❌ Error: {str(e)}")
            self.update_status("Error en el procesamiento", 0)
            messagebox.showerror("Error", f"Ocurrió un error:\n{str(e)}")
        finally:
            self.process_button.configure(state="normal", text="🚀 Procesar")
    
    def encode_process(self, password):
        self.update_status("Iniciando codificación...", 0.1)
        self.log("=" * 60)
        self.log("📤 CODIFICACIÓN INICIADA")
        self.log("=" * 60)
        
        # Usar el nombre de salida del campo de texto
        output_name = self.output_name.get().strip()
        if not output_name:
            output_name = Path(self.selected_file).stem + "_encrypted.png"
        
        # Asegurar extensión .png
        if not output_name.lower().endswith('.png'):
            output_name += '.png'
        
        # Pedir solo la carpeta de destino
        output_dir = filedialog.askdirectory(
            title="Selecciona carpeta para guardar el PNG cifrado")
        
        if not output_dir:
            self.log("❌ Operación cancelada")
            self.update_status("Cancelado", 0)
            return
        
        output_path = os.path.join(output_dir, output_name)
        
        self.update_status("Procesando archivo...", 0.3)
        
        success = encode_file_gui(self.selected_file, output_path, password,
                                 self.compression_level.get(), self.log)
        
        if success:
            self.update_status("✅ Codificación completada", 1.0)
            self.log("=" * 60)
            self.log("✨ PROCESO COMPLETADO")
            self.log("=" * 60)
            messagebox.showinfo("Éxito",
                              f"Archivo codificado exitosamente:\n{output_path}\n\n¡Guarda tu contraseña de forma segura!")
        else:
            self.update_status("Error en codificación", 0)
    
    def decode_process(self, password):
        self.update_status("Iniciando decodificación...", 0.1)
        self.log("=" * 60)
        self.log("📥 DECODIFICACIÓN INICIADA")
        self.log("=" * 60)
        
        output_folder = filedialog.askdirectory(
            title="Selecciona carpeta para guardar archivos recuperados")
        
        if not output_folder:
            self.log("❌ Operación cancelada")
            self.update_status("Cancelado", 0)
            return
        
        self.update_status("Descifrando archivo...", 0.3)
        
        success = decode_png_gui(self.selected_file, output_folder, password, self.log)
        
        if success:
            self.update_status("✅ Decodificación completada", 1.0)
            self.log("=" * 60)
            self.log("✨ PROCESO COMPLETADO")
            self.log("=" * 60)
            messagebox.showinfo("Éxito",
                              f"Archivos recuperados exitosamente en:\n{output_folder}")
        else:
            self.update_status("Error en decodificación", 0)

def main():
    app = File2PngGUI()
    app.mainloop()

if __name__ == "__main__":
    main()
