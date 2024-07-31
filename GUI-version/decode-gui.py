import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import numpy as np
from PIL import Image
import os
import subprocess


def image_to_bits(image_path):
    """Converts an image to a bit string."""
    image = Image.open(image_path)
    rgb_values = np.array(image)
    bits = ''

    height, width, _ = rgb_values.shape
    total_pixels = height * width

    for y in range(height):
        for x in range(width):
            r, g, b = rgb_values[y, x]
            bit_chunk = f'{r:08b}{g:08b}{b:08b}'
            bits += bit_chunk

    return bits


def extract_metadata(bits, metadata_length=8):
    """Extracts metadata from the bit string."""
    metadata_bits = bits[:metadata_length * 8]
    file_extension = ''.join(chr(int(metadata_bits[i:i + 8], 2)) for i in range(0, len(metadata_bits), 8)).strip('\x00')
    return file_extension, bits[metadata_length * 8:]


def bits_to_file(bits, output_file):
    """Converts a bit string to binary data and writes to a file."""
    byte_array = bytearray(int(bits[i:i + 8], 2) for i in range(0, len(bits), 8))
    with open(output_file, 'wb') as file:
        file.write(byte_array)


def decode_image_to_file(input_image):
    """Decodes an image to the original binary file."""
    bits = image_to_bits(input_image)
    file_extension, file_bits = extract_metadata(bits)

    output_folder = "decoded"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_file = os.path.join(output_folder, f'decoded.{file_extension}')
    bits_to_file(file_bits, output_file)

    if os.name == 'nt':  # Windows
        os.startfile(output_folder)
    elif os.name == 'posix':  # macOS or Linux
        subprocess.run(['open' if os.uname().sysname == 'Darwin' else 'xdg-open', output_folder])

    messagebox.showinfo("Success", f"File decoded successfully as {output_file}")


# Function to handle the drag and drop event
def on_drop(event):
    file_path = event.data.strip('{}')
    if os.path.isfile(file_path):
        decode_image_to_file(file_path)


# GUI Setup
root = TkinterDnD.Tk()
root.title("Image to File Decoder")

frame = tk.Frame(root)
frame.pack(pady=40, padx=30)

label = tk.Label(frame, text="Drag and drop an image to decode or ")
label.pack()

button_decode = tk.Button(frame, text="Select Image to Decode", command=lambda: decode_image_to_file(
    filedialog.askopenfilename(filetypes=[("PNG files", "*.png")], title="Select encoded image file")))
button_decode.pack(pady=10)

root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', on_drop)

root.mainloop()
