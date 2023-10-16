# Handle LZMA compression

import lzma


def decompress_txt(path):
    # Read from txt files and return plain text
    # Check if the file is compressed
    if path.endswith(".xz"):
        with lzma.open(path, "rt") as f:
            return f.read()
    else:
        with open(path, "rt") as f:
            return f.read()


def compress_txt(path, txt):
    # Write plain text to txt files and compress it
    with lzma.open(path, "wt") as f:
        f.write(txt)


def compress_any(path, data):
    # Write any data to files and compress it
    with lzma.open(path, "wb") as f:
        f.write(data)


def decompress_any(path):
    # Read from any files and return data
    # Check if the file is compressed
    if path.endswith(".xz"):
        with lzma.open(path, "rb") as f:
            return f.read()
    else:
        with open(path, "rb") as f:
            return f.read()
