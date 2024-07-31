# everything_to_png
[![python](https://img.shields.io/badge/Python-3.9-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org) ![version](https://img.shields.io/badge/version-1.0-green)

![evrybanner](https://github.com/user-attachments/assets/81f03466-d575-4d29-a254-46d7453a0e2e)

This project provides two Python scripts to encode and decode binary files into images and back. The encoding script takes a binary file (like .txt, .mp3, .zip, etc.) and encodes it into a PNG image. The decoding script extracts the original binary file from a PNG image.

## How to run
1. Use .py files 
   - you need python and ![Requirements](https://github.com/kolinov2/everything_to_png?tab=readme-ov-file#requirements) installed
   - then just run ```python3 encoder.py``` or ```python3 decoder.py```
2. Or use exe from release tab

## Requirements

To run this project, you need to have the following Python libraries installed:

- `numpy`
- `Pillow` (PIL fork)

You can install these libraries using pip:

```bash
pip install pip install -r requirements.txt
```


## How it works
### Encoding

1. **Convert File to Bits**:
   - The script reads the binary file and converts its contents into a string of bits. Each byte of the file is represented as an 8-bit binary sequence.

2. **Add Metadata**:
   - Metadata, including the file extension, is added to the bit string to help the decoder identify the original file type. This metadata is included at the beginning of the bit string.
     
     ![fileorganizaon](https://github.com/user-attachments/assets/baa5c130-e713-4284-9693-6fb28a4d239e)

     example:   
     ![fileorganizaon_example](https://github.com/user-attachments/assets/07b38f95-28a6-4810-a960-15c2c2164567)

3. **Create PNG Image**:
   - The bit string is transformed into RGB values, with each RGB pixel in the PNG image encoding 24 bits (8 bits per color channel). These RGB values are used to generate the PNG image.

4. **Save the Image**:
   - The PNG image, which contains the encoded data, is saved to the specified output location.
    
### Decoding

1. **Extract Bits from Image**:
   - The script reads the PNG image and extracts the pixel data, converting it back into a bit string.

2. **Retrieve Metadata**:
   - Metadata is extracted from the bit string to determine the original file extension. This helps in correctly reconstructing the file with the appropriate extension.

3. **Reconstruct the File**:
   - The bit string (excluding metadata) is converted back into binary data. This binary data is then saved as a file with the extension retrieved from the metadata

## Author
#### kolino :)



