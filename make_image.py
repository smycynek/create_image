#!/usr/bin/env python3

import math
import sys
import numpy as np
from PIL import Image as im
from PIL.ImageOps import scale

import ntpath

ALPHA_VALUE = 80
THUMBNAIL_DIMENSION = 15
THUMNAIL_THRESHHOLD = 100
UPSCALE_DIMENSION = 4000

def make_buffer(array_from_file, buffer_extra=0):
    file_length = len(array_from_file)
    enclosing_large_dimension = math.floor(math.sqrt(file_length))+buffer_extra
    extra = enclosing_large_dimension*enclosing_large_dimension - file_length
    new_buffer = np.append(array_from_file, np.empty(extra, np.uintc))
    new_buffer = np.reshape(new_buffer, (enclosing_large_dimension, enclosing_large_dimension))
    new_file = im.fromarray(new_buffer, mode="CMYK").convert('RGB')
    if buffer_extra:
        print(f"File length: {file_length} 32-bit words")
        print(f"Target image size: {enclosing_large_dimension} x {enclosing_large_dimension} pixels (32 bits per pixel)")
    return new_file, enclosing_large_dimension

def scale_and_save(data, scale_factor, name):
    new_file = f"./{name}.png"
    data = scale(data, scale_factor, im.BOX)
    # data.save(new_file, quality="maximum")
    return data

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage:  make_image.py <filename> no_upscale (optional)")
        exit(1)
    filename = sys.argv[1]
    upscale = True
    if len(sys.argv) > 2:
        upscale = False

    print(f"input: {filename}")
    filename_bare= ntpath.basename(filename)
    print("Reading input...")
    array_file = np.fromfile(filename, dtype=np.uintc)
    new_image, enclosing_large_dimension = make_buffer(array_file,1)
    print("Saving large image...")
    large_file = scale_and_save(new_image, 1, filename_bare)

    if enclosing_large_dimension >= THUMNAIL_THRESHHOLD: # Only make thumnail and composite for larger images
        print("Processing section...")
        scale_factor = enclosing_large_dimension/THUMBNAIL_DIMENSION
        start_index = math.floor(len(array_file)/3) # start smaller sub-array of data about 1/3 into the file
        section_array = array_file[start_index:THUMBNAIL_DIMENSION*THUMBNAIL_DIMENSION + start_index]
        section_image, _ = make_buffer(section_array)
        print("Saving section...")
        section_file = scale_and_save(section_image, scale_factor, filename_bare + "_section")
        print("Saving composite...")
        section_file.putalpha(ALPHA_VALUE)
        composite = large_file.convert('RGBA')

        composite.paste(section_file, (0,0), section_file.convert('RGBA'))
        if upscale:
            composite = scale(composite, UPSCALE_DIMENSION/enclosing_large_dimension, im.BOX)

        composite.save(f"./{filename_bare}_composite.png")