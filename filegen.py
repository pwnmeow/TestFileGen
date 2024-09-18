import os
import argparse
import re
# Magic bytes dictionary for common file types
MAGIC_BYTES = {
    'jpg': b'\xFF\xD8\xFF',               # JPEG
    'png': b'\x89PNG\r\n\x1a\n',          # PNG
    'gif': b'GIF87a',                     # GIF87a
    'gif89a': b'GIF89a',                  # GIF89a
    'pdf': b'%PDF-',                      # PDF
    'zip': b'PK\x03\x04',                 # ZIP
    'mp3': b'\x49\x44\x33',               # MP3
    'mp4': b'\x00\x00\x00\x18ftypmp42',   # MP4
    'exe': b'MZ',                         # EXE
    'doc': b'\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1', # DOC (pre-2007)
    'docx': b'PK\x03\x04',                # DOCX (ZIP format)
    'xls': b'\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1', # XLS (pre-2007)
    'xlsx': b'PK\x03\x04',                # XLSX (ZIP format)
    'ppt': b'\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1', # PPT (pre-2007)
    'pptx': b'PK\x03\x04',                # PPTX (ZIP format)
}
def parse_size(size_str):
    """
    Parse a human-readable file size string (e.g., '1G', '500M') into bytes.
    Supported units: K (kilobytes), M (megabytes), G (gigabytes), T (terabytes)
    """
    size_str = size_str.upper()
    size_re = re.match(r'^(\d+)([KMGTP]?)$', size_str)
    if not size_re:
        raise ValueError(f"Invalid size format: {size_str}")
    size = int(size_re.group(1))
    unit = size_re.group(2)
    unit_multipliers = {
        '': 1,        # Bytes
        'K': 1024,    # Kilobytes
        'M': 1024**2, # Megabytes
        'G': 1024**3, # Gigabytes
        'T': 1024**4  # Terabytes
    }
    return size * unit_multipliers.get(unit, 1)
def generate_fake_file(file_name: str, extension: str, size: int):
    """Generates a fake file with the specified extension, size, and magic bytes."""
    file_path = f"{file_name}.{extension}"
    magic_bytes = MAGIC_BYTES.get(extension.lower(), b'')
    # Ensure the file has at least enough size for the magic bytes
    if size < len(magic_bytes):
        raise ValueError(f"File size {size} is too small for the required magic bytes for {extension} extension.")
    # Create the file with magic bytes and random data
    with open(file_path, 'wb') as f:
        f.write(magic_bytes)  # Write magic bytes
        remaining_size = size - len(magic_bytes)
        # Write random data to fill the remaining size
        if remaining_size > 0:
            f.write(os.urandom(remaining_size))
    print(f"Fake file {file_path} of size {size} bytes created successfully.")
def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Generate a fake file with specified extension, size, and magic bytes.")
    parser.add_argument('file_name', type=str, help="The base name of the file (without extension)")
    parser.add_argument('extension', type=str, help="The file extension (e.g., jpg, png, pdf)")
    parser.add_argument('size', type=str, help="The size of the file (e.g., '1G', '500M')")
    args = parser.parse_args()
    # Parse the size argument (in human-readable format) to bytes
    size_in_bytes = parse_size(args.size)
    # Generate the file with the provided arguments
    generate_fake_file(args.file_name, args.extension, size_in_bytes)
if __name__ == "__main__":
    main()
