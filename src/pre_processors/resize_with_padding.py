"""
Last Updated May 12, 2025
Author: Max Freitas
File Purpose: Resize image, and pad to maintain original aspect ratio.
"""

from PIL import Image


def resize_with_padding(img: str, target_size: tuple, padding_color: tuple):
    """
    Resize the input image to meet target size, and preserve aspect ratio and pad remaining pixels.

    Params:
    - img (PIL.Image): opened image object
    - output_path (str): path to store image
    - target_size (tuple): desired output size (width, height)
    - padding_color (tuple): Color for padding

    Returns:
    - new_img (PIL.Image): resized and padded image
    """
    # get original dims
    img_width, img_height = img.size
    print(f"Original size: {img.size}")

    # get new size
    img_ratio = img_width / img_height
    target_ratio = target_size[0] / target_size[1]

    # wider image
    if img_ratio > target_ratio:
        new_width = target_size[0]
        new_height = int(target_size[0] / img_ratio)

    # taller image
    else:
        new_height = target_size[1]
        new_width = int(target_size[1] * img_ratio)

    # resize image
    img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # create padding
    new_img = Image.new("RGB", target_size, padding_color)

    # Calculate padding to center the image
    padding_top = (target_size[1] - new_height) // 2
    padding_left = (target_size[0] - new_width) // 2

    # Paste the resized image into the center of the padded image
    new_img.paste(img_resized, (padding_left, padding_top))

    print(f"New size after resize and padding: {new_img.size}")

    # Return the new image (resized and padded)
    return new_img
