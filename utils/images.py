import os
from typing import Union
import PIL.Image as ImageType

import bpy


def get_image(tex: bpy.types.Texture) -> bpy.types.Image:
    return tex.image if tex and hasattr(tex, 'image') and tex.image else None


def get_packed_file(image: Union[bpy.types.Image, None]) -> Union[bpy.types.PackedFile, None]:
    if image and not image.packed_file and _get_image_path(image):
        image.pack()
    return image.packed_file if image and image.packed_file else None


def _get_image_path(img: Union[bpy.types.Image, None]) -> Union[str, None]:
    path = os.path.abspath(bpy.path.abspath(img.filepath)) if img else ''
    return path if os.path.isfile(path) and not path.lower().endswith(('.spa', '.sph')) else None

def pil_to_blender_image(pil_image: ImageType) -> bpy.types.Image:
    width, height = pil_image.size
    image_pixels = np.array(pil_image) / 255  # Convert to [0, 1] range
    image_pixels = image_pixels.flatten().tolist()  # Flatten to 1D list

    blender_image = bpy.data.images.new("Image", width=width, height=height)
    blender_image.pixels = image_pixels

    return blender_image