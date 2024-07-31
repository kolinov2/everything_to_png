import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import os
import numpy as np
from PIL import Image
import math


def file_to_bits(file_path):
    """Converts a binary file to a bit string."""
    with open(file_path, 'rb') as file:
        byte_data = file.read()
    bits = ''.join(f'{byte:08b}' for byte in byte_data)
    return bits


def calculate_dimensions(total_bits, bits_per_pixel=24):
    """Calculates the dimensions of an image based on the number of bits."""
    num_pixels = total_bits // bits_per_pixel
    width = int(math.ceil(math.sqrt(num_pixels)))
    height = int(math.ceil(num_pixels / width))

    while width * height < num_pixels:
        width += 1
        height = int(math.ceil(num_pixels / width))

    return width, height


def add_metadata(bits, file_extension, metadata_length=8):
    """Adds metadata to the bit string indicating the file extension."""
    # Convert file extension to bits, each character takes up 8 bits
    metadata_bits = ''.join(f'{ord(char):08b}' for char in file_extension)
    metadata_bits = metadata_bits.ljust(metadata_length * 8, '0')
    return metadata_bits + bits


def bits_to_rgb(bits, width, height):
    """Converts a bit string to an RGB array with dimensions width x height."""
    num_pixels = width * height
    rgb_values = np.zeros((height, width, 3), dtype=np.uint8)

    bits = bits.ljust(num_pixels * 24, '0')

    for i in range(num_pixels):
        start = i * 24
        end = start + 24
        bit_chunk = bits[start:end]

        r = int(bit_chunk[:8], 2)
        g = int(bit_chunk[8:16], 2)
        b = int(bit_chunk[16:], 2)

        y, x = divmod(i, width)
        rgb_values[y, x] = [r, g, b]

    return rgb_values


def create_image(rgb_values, output_file):
    """Creates an image from an RGB array."""
    image = Image.fromarray(rgb_values, 'RGB')
    image.save(output_file)


# Function to handle the drag and drop event
def on_drop(event):
    file_path = event.data.strip('{}')
    if os.path.isfile(file_path):
        entry_file_path.delete(0, tk.END)
        entry_file_path.insert(0, file_path)


# Function to encode the file into an image
def encode_file():
    input_file = entry_file_path.get()
    if not input_file:
        messagebox.showwarning("No File", "Please select a file to encode.")
        return

    output_image = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png")],
        title="Save encoded image as"
    )

    if not output_image:
        return

    try:
        file_extension = os.path.splitext(input_file)[1].lstrip('.')
        bits = file_to_bits(input_file)
        bits_with_metadata = add_metadata(bits, file_extension)
        total_bits = len(bits_with_metadata)
        width, height = calculate_dimensions(total_bits)
        rgb_values = bits_to_rgb(bits_with_metadata, width, height)
        create_image(rgb_values, output_image)
        messagebox.showinfo("Success", f"File encoded successfully as {output_image}")
    except Exception as e:
        messagebox.showerror("Error", str(e))


# GUI Setup
root = TkinterDnD.Tk()
root.title("File to Image Encoder")

frame = tk.Frame(root)
frame.pack(pady=20, padx=20)

label = tk.Label(frame, text="Drag and drop a file to encode:")
label.pack()

entry_file_path = tk.Entry(frame, width=50)
entry_file_path.pack(padx=10, pady=10)

button_encode = tk.Button(frame, text="Encode", command=encode_file)
button_encode.pack(pady=10)

root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', on_drop)

root.mainloop()
