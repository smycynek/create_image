#!/usr/bin/env python3

import math
import sys
import numpy as np
from PIL import Image as im
from PIL.ImageOps import scale

import ntpath

def make_buffer(array_from_file, buffer_extra=0):
    file_length = len(array_from_file)
    dimension = math.floor(math.sqrt(file_length))+buffer_extra
    extra = dimension*dimension - file_length
    new_buffer = np.append(array_from_file, np.empty(extra, np.uintc))
    new_buffer = np.reshape(new_buffer, (dimension, dimension))
    new_file = im.fromarray(new_buffer, mode="CMYK")
    print(f"file length: {file_length} 32-bit words")
    print(f"image size: {dimension} x {dimension} pixels (32 bits per pixel)")
    return new_file, dimension

def scale_and_save(data, scale_factor, name):
    new_file = f"./{name}_CMYK.jpg"
    data = scale(data, scale_factor, im.BOX)
    data.save(new_file, quality="maximum")

if __name__ == "__main__":
    if len(sys.argv) !=2:
        print("usage:  make_image.py <filename>")
        exit(1)
    filename = sys.argv[1]
    print(f"input: {filename}")

    array_file = np.fromfile(filename, dtype=np.uintc)
    new_image, dimension = make_buffer(array_file,1)
    scale_and_save(new_image, 1, ntpath.basename(filename))

    if dimension > 200:
        scale_factor = dimension/15
        thumb_array = array_file[:225]
        new_image, _ = make_buffer(thumb_array)
        scale_and_save(new_image, scale_factor, ntpath.basename(filename + "_thm"))


