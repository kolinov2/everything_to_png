# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#       decode.py by kolino :)
#         thanks for using
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# new commit: using pools because old code was f* slow

import numpy as np
from PIL import Image
from multiprocessing import Pool, cpu_count
import tkinter as tk
from tkinter import filedialog
import os
import sys

PROGRESS_BAR_LENGTH = 30

def row_to_bits(row):
    return ''.join(f'{r:08b}{g:08b}{b:08b}' for r, g, b in row)

def image_to_bits_parallel(image_path):
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(f"[!] Failed to open image: {e}")
        pause_and_exit()

    rgb_values = np.array(image)
    height, _, _ = rgb_values.shape
    rows = [rgb_values[y] for y in range(height)]
    bits_list = []

    with Pool(cpu_count()) as pool:
        for i, bit_row in enumerate(pool.imap(row_to_bits, rows), 1):
            bits_list.append(bit_row)
            progress = i / height
            filled = int(progress * PROGRESS_BAR_LENGTH)
            bar = '#' * filled + '-' * (PROGRESS_BAR_LENGTH - filled)
            percent = progress * 100
            sys.stdout.write(f"\rDecoding progress: [{bar}] {percent:.2f}%")
            sys.stdout.flush()

    sys.stdout.write(f"\rDecoding progress: [{'#' * PROGRESS_BAR_LENGTH}] 100.00%\n")
    sys.stdout.flush()

    return ''.join(bits_list)

def extract_metadata(bits, metadata_length=8):
    if len(bits) < metadata_length * 8:
        raise ValueError("Bit string too short to contain metadata.")
    metadata_bits = bits[:metadata_length * 8]
    file_extension = ''.join(
        chr(int(metadata_bits[i:i+8], 2))
        for i in range(0, len(metadata_bits), 8)
    ).strip('\x00')
    if not file_extension:
        raise ValueError("No file extension metadata found.")
    return file_extension, bits[metadata_length * 8:]

def generate_unique_filename(base_name, extension):
    counter = 1
    candidate = f"{base_name}.{extension}"
    while os.path.exists(candidate):
        candidate = f"{base_name}_{counter}.{extension}"
        counter += 1
    return candidate

def bits_to_file(bits, output_file):
    try:
        byte_array = bytearray(
            int(bits[i:i + 8], 2)
            for i in range(0, len(bits), 8)
        )
    except Exception as e:
        print(f"[!] Failed to convert bits to bytes: {e}")
        pause_and_exit()

    try:
        with open(output_file, 'wb') as file:
            file.write(byte_array)
    except Exception as e:
        print(f"[!] Failed to write output file: {e}")
        pause_and_exit()

def choose_image_file():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(
        title="Select an image to decode",
        filetypes=[("Image Files", "*.png;*.bmp;*.jpg;*.jpeg")]
    )

def pause_and_exit():
    try:
        input("Press Enter to exit...")
    except Exception:
        pass
    sys.exit(1)

def decode_image_to_file():
    input_image = choose_image_file()
    if not input_image:
        print("[!] No file selected.")
        pause_and_exit()

    try:
        print(f"[*] Decoding '{os.path.basename(input_image)}' using {cpu_count()} cores...")
        bits = image_to_bits_parallel(input_image)
        file_extension, file_bits = extract_metadata(bits)
        output_file = generate_unique_filename('output', file_extension)
        bits_to_file(file_bits, output_file)
        print(f"[✓] Done! File saved as '{output_file}'")
        input("Press Enter to exit...")
    except Exception as e:
        print(f"[!] An unexpected error occurred: {e}")
        pause_and_exit()

if __name__ == "__main__":
    decode_image_to_file()
