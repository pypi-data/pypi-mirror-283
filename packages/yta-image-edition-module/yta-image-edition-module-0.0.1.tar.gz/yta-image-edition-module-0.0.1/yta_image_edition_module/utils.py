from PIL import Image

def has_transparency(image: Image):
    """
    Checks if the provided image (read with pillow) has transparency.
    """
    if image.info.get("transparency", None) is not None:
        return True
    if image.mode == "P":
        transparent = image.info.get("transparency", -1)
        for _, index in image.getcolors():
            if index == transparent:
                return True
    elif image.mode == "RGBA":
        extrema = image.getextrema()
        if extrema[3][0] < 255:
            return True

    return False

def rgb_to_hex(r, g, b):
    """
    Returns the provided RGB color as a hex color.
    """
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

def is_valid(image_filename):
    """
    Tries to open the 'image_filename' provided to check if it is corrupt or it is valid. It 
    returns True if the provided image is valid, or False if is corrupt.
    """
    try:
        im = Image.open(image_filename)
        im.verify()
        im.close()
    except (IOError, OSError, Image.DecompressionBombError) as e:
        return False
    return True