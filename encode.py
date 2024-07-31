# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#       encode.py by kolino :)
#         thanks for using
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

import numpy as np
from PIL import Image
import os
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


def encode_file_to_image(input_file, output_image):
    """Encodes a binary file into an image."""
    # Extract file extension
    _, file_extension = os.path.splitext(input_file)
    file_extension = file_extension.lstrip('.')

    # Convert file to bits
    bits = file_to_bits(input_file)

    # Add metadata to the bits
    bits_with_metadata = add_metadata(bits, file_extension)

    # Calculate image dimensions
    total_bits = len(bits_with_metadata)
    width, height = calculate_dimensions(total_bits)

    # Convert bits to RGB values
    rgb_values = bits_to_rgb(bits_with_metadata, width, height)

    # Create the image
    create_image(rgb_values, output_image)


def main():
    """Main function to handle user input and process the image encoding."""
    input_file = input("Enter the path of the file to encode: ")
    output_image = 'output.png'

    if not os.path.isfile(input_file):
        print(f"File {input_file} does not exist.")
        return

    encode_file_to_image(input_file, output_image)

    # Display image details
    if os.path.isfile(output_image):
        image = Image.open(output_image)
        width, height = image.size
        size = os.path.getsize(output_image)
        print(f"Image Path: {os.path.abspath(output_image)}")
        print(f"Resolution: {width}x{height}")
        print(f"Size: {size} bytes")
    else:
        print("Error: Output image was not created successfully.")


main()
