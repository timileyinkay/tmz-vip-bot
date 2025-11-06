# imghdr.py – compatibility shim for Python 3.13+
# Simple re-implementation of the old stdlib imghdr module

def what(file, h=None):
    """Return the image type (e.g., 'jpeg', 'png', etc.) or None."""
    if h is None:
        if isinstance(file, (str, bytes)):
            with open(file, 'rb') as f:
                h = f.read(32)
        else:
            h = file.read(32)

    if h.startswith(b'\xff\xd8'):
        return 'jpeg'
    if h.startswith(b'\x89PNG\r\n\x1a\n'):
        return 'png'
    if h.startswith(b'GIF87a') or h.startswith(b'GIF89a'):
        return 'gif'
    if h.startswith(b'BM'):
        return 'bmp'
    if h[:4] == b'II*\x00' or h[:4] == b'MM\x00*':
        return 'tiff'
    if h.startswith(b'RIFF') and h[8:12] == b'WEBP':
        return 'webp'
    return None
