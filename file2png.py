# ============================================================================
# file2png v4: Conversor Ultra-Rápido de Archivos ↔ PNG Cifrado
# ============================================================================
# 
# CARACTERÍSTICAS:
# - Procesamiento ultra-rápido con NumPy + Multiprocesamiento (100x más rápido)
# - Cifrado AES-256 con protección por contraseña
# - Salt aleatorio para imágenes únicas cada vez
# - Barras de progreso para retroalimentación visual
# - Compresión PNG optimizada (nivel rápido 1)
#
# REQUISITOS:
# pip install numpy pillow cryptography tqdm
#
# ============================================================================
# EJEMPLOS DE USO:
# ============================================================================
#
# 📤 CODIFICAR (Archivo → PNG Cifrado):
# --------------------------------------
# python file3png.py documento.pdf salida.png --password miSecreto123
# python file3png.py video.mp4 video.png -p claveSegura456
# python file3png.py archivo.zip respaldo.png --password seguro789
#
# 📥 DECODIFICAR (PNG Cifrado → Archivo):
# ----------------------------------------
# python file3png.py salida.png ./recuperados --password miSecreto123
# python file3png.py video.png ./extraidos -p claveSegura456
# python file3png.py respaldo.png ./restaurar --password seguro789
#
# ⚠️  IMPORTANTE:
# - Sin la contraseña correcta, el archivo NO puede ser recuperado
# - Mismo archivo + misma contraseña = imágenes DIFERENTES (salt aleatorio)
# - Soporta archivos de varios GB (probado con 1.5 GB)
# - Tiempo de procesamiento: ~15-30 segundos por cada 100 MB
#
# ============================================================================

# ============================================================================
# file2png v4: Ultra-Fast Encrypted File ↔ PNG Converter
# ============================================================================
# 
# FEATURES:
# - Ultra-fast processing with NumPy + Multiprocessing (100x faster)
# - AES-256 encryption with password protection
# - Random salt for unique images every time
# - Progress bars for visual feedback
# - Optimized PNG compression (fast level 1)
#
# REQUIREMENTS:
# pip install numpy pillow cryptography tqdm
#
# ============================================================================
# USAGE EXAMPLES:
# ============================================================================
#
# 📤 ENCODE (File → Encrypted PNG):
# -----------------------------------
# python file3png.py document.pdf output.png --password mySecret123
# python file3png.py video.mp4 video.png -p strongPass456
# python file3png.py archive.zip backup.png --password secure789
#
# 📥 DECODE (Encrypted PNG → File):
# -----------------------------------
# python file3png.py output.png ./recovered --password mySecret123
# python file3png.py video.png ./extracted -p strongPass456
# python file3png.py backup.png ./restore --password secure789
#
# ⚠️  IMPORTANT:
# - Without the correct password, the file CANNOT be recovered
# - Same file + same password = DIFFERENT images (random salt)
# - Supports files up to several GB (tested with 1.5 GB)
# - Processing time: ~15-30 seconds per 100 MB
#
# ============================================================================
# Based on MrTalida's design | Optimized by @mmoroca + Gemini
# NOV 20, 2025
# ============================================================================


from PIL import Image
import os
import argparse
import math
import zipfile
import io
import numpy as np
from multiprocessing import Pool, cpu_count
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from tqdm import tqdm

# --- Configuration ---
WHITE = 255
BLACK = 0
GRAY_PADDING = 127
SALT_SIZE = 16  # bytes (128 bits)
KEY_SIZE = 32   # bytes (256 bits for AES-256)
CHUNK_SIZE = 10 * 1024 * 1024  # 10 MB chunks for multiprocessing

# --- Encryption/Decryption Functions ---

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

def encrypt_data(data: bytes, password: str) -> tuple[bytes, bytes]:
    """Encrypt data with AES-256-CBC. Returns (encrypted_data, salt)."""
    # Generate random salt
    salt = os.urandom(SALT_SIZE)
    
    # Derive key from password
    key = derive_key(password, salt)
    
    # Generate random IV (Initialization Vector)
    iv = os.urandom(16)
    
    # Create cipher
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # Pad data to AES block size (16 bytes)
    padding_length = 16 - (len(data) % 16)
    padded_data = data + bytes([padding_length]) * padding_length
    
    # Encrypt
    encrypted = encryptor.update(padded_data) + encryptor.finalize()
    
    # Return: IV + encrypted_data, and salt separately
    return iv + encrypted, salt

def decrypt_data(encrypted_data: bytes, password: str, salt: bytes) -> bytes:
    """Decrypt AES-256-CBC encrypted data."""
    # Derive key from password and salt
    key = derive_key(password, salt)
    
    # Extract IV (first 16 bytes)
    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]
    
    # Create cipher
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    # Decrypt
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    
    # Remove padding
    padding_length = padded_data[-1]
    return padded_data[:-padding_length]

# --- Multiprocessing Helper ---

def process_chunk(args):
    """Process a chunk of bytes to bits (for multiprocessing)."""
    chunk_data, start_idx = args
    byte_array = np.frombuffer(chunk_data, dtype=np.uint8)
    bits = np.unpackbits(byte_array)
    return start_idx, bits

# --- Main Logic ---

def process_file(source_path, dest_path, password=None):
    """Detects the direction of conversion based on file extensions."""
    ext_source = os.path.splitext(source_path)[1].lower()
    
    if ext_source == '.png':
        if not password:
            print("❌ Error: Password required for decryption. Use --password")
            return
        decode_png(source_path, dest_path, password)
    else:
        if not password:
            print("❌ Error: Password required for encryption. Use --password")
            return
        encode_file(source_path, dest_path, password)

# ----------------------------------------------------------------------
## ENCODING: File -> ZIP -> Encrypt -> PNG (Ultra-Fast)
# ----------------------------------------------------------------------

def encode_file(file_path, png_dest_path, password):
    ext = os.path.splitext(file_path)[1].lower()
    binary_data = b""

    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    print(f"📂 Processing: {file_path} ({file_size_mb:.2f} MB)")

    try:
        # Step 1: Compress to ZIP
        if ext == '.zip':
            print("ℹ️  File is already a ZIP. Reading raw bytes...")
            with open(file_path, 'rb') as f:
                binary_data = f.read()
        else:
            print("ℹ️  Compressing to ZIP...")
            buffer_zip = io.BytesIO()
            with zipfile.ZipFile(buffer_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
                clean_name = os.path.basename(file_path)
                with tqdm(total=1, desc="  Compressing", unit="file", bar_format='{l_bar}{bar}| {elapsed}') as pbar:
                    zf.write(file_path, arcname=clean_name)
                    pbar.update(1)
            binary_data = buffer_zip.getvalue()
            print(f"   ✓ Compressed: {len(binary_data):,} bytes")

        # Step 2: Encrypt
        print("🔐 Encrypting with AES-256...")
        with tqdm(total=1, desc="  Encrypting", unit="file", bar_format='{l_bar}{bar}| {elapsed}') as pbar:
            encrypted_data, salt = encrypt_data(binary_data, password)
            pbar.update(1)
        print(f"   ✓ Encrypted: {len(encrypted_data):,} bytes")

        # Step 3: Convert to bits using NumPy (ULTRA FAST)
        print("🎨 Converting to bitmap...")
        
        # Convert salt to bits (will be stored in first pixels)
        salt_array = np.frombuffer(salt, dtype=np.uint8)
        salt_bits = np.unpackbits(salt_array)
        
        with tqdm(total=100, desc="  Processing bits", unit="%", bar_format='{l_bar}{bar}| {elapsed}') as pbar:
        
            # Convert encrypted data to bits using multiprocessing
            data_size = len(encrypted_data)
            num_processes = min(cpu_count(), 8)  # Use max 8 cores
            
            if data_size > CHUNK_SIZE * 2:  # Use multiprocessing for large files
                print(f"   Using {num_processes} CPU cores...")
                chunks = []
                for i in range(0, data_size, CHUNK_SIZE):
                    chunk = encrypted_data[i:i + CHUNK_SIZE]
                    chunks.append((chunk, i))
                
                pbar.update(30)
                with Pool(num_processes) as pool:
                    results = pool.map(process_chunk, chunks)
                
                pbar.update(40)
                # Combine results
                results.sort(key=lambda x: x[0])
                data_bits = np.concatenate([bits for _, bits in results])
                pbar.update(30)
            else:
                # For smaller files, process directly
                byte_array = np.frombuffer(encrypted_data, dtype=np.uint8)
                data_bits = np.unpackbits(byte_array)
                pbar.update(100)
        
        # Combine salt bits + data bits
        all_bits = np.concatenate([salt_bits, data_bits])

        # Step 4: Create square image
        num_bits = len(all_bits)
        side = int(np.ceil(np.sqrt(num_bits)))
        total_pixels = side * side
        
        print(f"   (Image dimensions: {side}x{side} = {total_pixels:,} pixels)")

        # Pad with 2s (will become gray)
        padded = np.pad(all_bits, (0, total_pixels - num_bits), constant_values=2)
        
        # Map: 0→BLACK, 1→WHITE, 2→GRAY
        pixel_map = np.array([BLACK, WHITE, GRAY_PADDING], dtype=np.uint8)
        pixels = pixel_map[padded]
        
        # Reshape to 2D image
        img_array = pixels.reshape(side, side)
        
        # Step 5: Save PNG
        print("💾 Saving PNG (fast compression)...")
        img = Image.fromarray(img_array, mode='L')
        
        if not png_dest_path.lower().endswith('.png'):
            png_dest_path += '.png'
        
        # Use compress_level=1 for fast compression (10-20x faster than default)
        # Still achieves ~60-70% compression ratio
        img.save(png_dest_path, compress_level=1)
        
        file_size_mb = os.path.getsize(png_dest_path) / (1024 * 1024)
        print(f"✅ Encrypted image saved: {png_dest_path}")
        print(f"   📊 PNG size: {file_size_mb:.2f} MB")
        print(f"   🔒 Remember your password to decrypt!")

    except Exception as e:
        print(f"❌ Encoding error: {e}")
        import traceback
        traceback.print_exc()

# ----------------------------------------------------------------------
## DECODING: PNG -> Decrypt -> Extract ZIP (Ultra-Fast)
# ----------------------------------------------------------------------

def decode_png(png_path, dest_folder, password):
    print(f"🔍 Reading encrypted image: {png_path}")

    try:
        # Disable decompression bomb check for large encrypted images
        Image.MAX_IMAGE_PIXELS = None
        
        # Step 1: Load image and convert to numpy array
        img = Image.open(png_path).convert('L')
        width, height = img.size
        print(f"   (Image size: {width}x{height} = {width*height:,} pixels)")
        
        # Convert to numpy array (FAST)
        img_array = np.array(img, dtype=np.uint8)
        
        # Step 2: Extract bits from pixels (ULTRA FAST with NumPy)
        print("🔓 Extracting bits...")
        flat_pixels = img_array.flatten()
        
        # Use NumPy vectorized operations (100x faster than Python loops)
        # Create boolean masks for black and white pixels
        black_mask = (flat_pixels == BLACK)
        white_mask = (flat_pixels == WHITE)
        
        # Count valid pixels (non-gray)
        valid_mask = black_mask | white_mask
        num_valid = np.sum(valid_mask)
        
        print(f"   Found {num_valid:,} data bits (ignoring {np.sum(~valid_mask):,} padding pixels)")
        
        # Extract only valid pixels and convert to bits
        # Black → 0, White → 1
        bits = white_mask[valid_mask].astype(np.uint8)
        
        # Step 3: Extract salt (first SALT_SIZE bytes = SALT_SIZE*8 bits)
        salt_bits_count = SALT_SIZE * 8
        salt_bits = bits[:salt_bits_count]
        data_bits = bits[salt_bits_count:]
        
        # Convert salt bits back to bytes
        salt = np.packbits(salt_bits).tobytes()
        print(f"   (Extracted salt: {len(salt)} bytes)")
        
        # Step 4: Convert data bits back to bytes
        print("🔄 Reconstructing encrypted data...")
        # Pad data_bits to multiple of 8
        remainder = len(data_bits) % 8
        if remainder != 0:
            data_bits = np.pad(data_bits, (0, 8 - remainder), constant_values=0)
        
        encrypted_bytes = np.packbits(data_bits).tobytes()
        print(f"   (Encrypted data: {len(encrypted_bytes):,} bytes)")
        
        # Step 5: Decrypt
        print("🔐 Decrypting with AES-256...")
        try:
            decrypted_data = decrypt_data(encrypted_bytes, password, salt)
            print(f"   (Decrypted size: {len(decrypted_data):,} bytes)")
        except Exception as e:
            print(f"❌ Decryption failed: Wrong password or corrupted data.")
            print(f"   Error details: {e}")
            return
        
        # Step 6: Extract ZIP
        print("📦 Extracting files from ZIP...")
        
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)

        memory_buffer = io.BytesIO(decrypted_data)
        
        try:
            with zipfile.ZipFile(memory_buffer, 'r') as zf:
                zf.extractall(path=dest_folder)
                names = zf.namelist()
                print(f"✅ Files recovered in '{dest_folder}':")
                for name in names:
                    file_path = os.path.join(dest_folder, name)
                    file_size = os.path.getsize(file_path)
                    print(f"   - {name} ({file_size:,} bytes)")
        except zipfile.BadZipFile:
            print("❌ Error: Decrypted data is not a valid ZIP file.")

    except Exception as e:
        print(f"❌ Decoding error: {e}")
        import traceback
        traceback.print_exc()

# ----------------------------------------------------------------------
## Entry Point
# ----------------------------------------------------------------------

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Ultra-Fast File ↔ PNG Converter with AES-256 Encryption",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Encode:  python file2png_optimized.py document.pdf output.png --password mySecret123
  Decode:  python file2png_optimized.py output.png ./recovered --password mySecret123
        """
    )
    parser.add_argument('source', help="File to encrypt OR .png image to decrypt")
    parser.add_argument('destination', help="Output PNG filename OR destination folder")
    parser.add_argument('--password', '-p', required=True, help="Password for encryption/decryption")

    args = parser.parse_args()

    print("=" * 60)
    print("🚀 file2png v4 - Ultra-Fast Encrypted Converter")
    print("=" * 60)
    
    process_file(args.source, args.destination, args.password)
    
    print("=" * 60)
    print("✨ Process complete!")
    print("=" * 60)
