# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#       decode.py by kolino :)
#         thanks for using
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

import numpy as np
from PIL import Image

def image_to_bits(image_path):
    """Converts an image to a bit string."""
    image = Image.open(image_path)
    rgb_values = np.array(image)
    bits = ''

    height, width, _ = rgb_values.shape
    total_pixels = height * width

    # Define the progress bar length
    progress_bar_length = 30

    for y in range(height):
        for x in range(width):
            r, g, b = rgb_values[y, x]
            bit_chunk = f'{r:08b}{g:08b}{b:08b}'
            bits += bit_chunk

            # Calculate progress percentage and update progress bar
            current_pixel = y * width + x + 1
            progress = current_pixel / total_pixels
            bar_filled = int(progress * progress_bar_length)
            bar = '#' * bar_filled + '-' * (progress_bar_length - bar_filled)
            percent = progress * 100

            # Print the progress bar and percentage
            print(f'\rDecoding progress: [{bar}] {percent:.2f}%', end='', flush=True)

    # Ensure the final progress reaches 100%
    print(f'\rDecoding progress: [{"#" * progress_bar_length}] 100.00%')
    return bits

def extract_metadata(bits, metadata_length=8):
    """Extracts metadata from the bit string."""
    metadata_bits = bits[:metadata_length * 8]
    file_extension = ''.join(chr(int(metadata_bits[i:i+8], 2)) for i in range(0, len(metadata_bits), 8)).strip('\x00')
    return file_extension, bits[metadata_length * 8:]

def bits_to_file(bits, output_file):
    """Converts a bit string to binary data and writes to a file."""
    byte_array = bytearray(int(bits[i:i + 8], 2) for i in range(0, len(bits), 8))
    with open(output_file, 'wb') as file:
        file.write(byte_array)

def decode_image_to_file(input_image):
    """Decodes an image to the original binary file."""
    # Convert image to bit string
    bits = image_to_bits(input_image)

    # Extract metadata and file bits
    file_extension, file_bits = extract_metadata(bits)

    # Determine the output file name
    output_file = f'output.{file_extension}'

    # Convert bit string to file
    bits_to_file(file_bits, output_file)

# Example usage:
decode_image_to_file('output.png')
