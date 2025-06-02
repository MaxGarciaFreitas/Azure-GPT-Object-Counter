"""
Last Updated: May 12, 2025
Author: Max Freitas
File Purpose: Fix image orientation
"""
from PIL import Image, ImageOps, ExifTags



def get_orientation_tag():
    """Safely get orientation tag ID"""
    try:
        return next(k for k, v in ExifTags.TAGS.items() if v == 'Orientation')
    except StopIteration:
        return None


ORIENTATION_TAG = get_orientation_tag()

def correct_orientation(image):
    """
    Corrects image orientation based on EXIF data.
    Handles all 8 possible orientation cases.
    Returns image with corrected orientation.
    """
    if ORIENTATION_TAG is None:
        print("ORIENTATION_TAG is missing")
        return image
        
    try:
        if not hasattr(image, 'getexif'):
            print("Image has no EXIF support")
            return image
            
        exif = image.getexif()
        if not exif:
            print("Image has no EXIF data")
            return image
            
        orientation = exif.get(ORIENTATION_TAG)
        if orientation is None:
            print("No orientation tag found")
            return image
            
        if orientation == 1:
            return image
        elif orientation == 2:
            image = ImageOps.mirror(image)
        elif orientation == 3:
            image = image.rotate(180, expand=True)
        elif orientation == 4:
            image = ImageOps.flip(image)
        elif orientation == 5:
            image = ImageOps.mirror(image.rotate(90, expand=True))
        elif orientation == 6:
            image = image.rotate(270, expand=True)
        elif orientation == 7:
            image = ImageOps.mirror(image.rotate(270, expand=True))
        elif orientation == 8:
            image = image.rotate(90, expand=True)
        
        return image
        
    except Exception as e:
        print(f"Orientation correction failed: {e}")
        return image
