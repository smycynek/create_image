#!/usr/bin/env python3

import math
import sys
import numpy as np
from PIL import Image as im
import ntpath
if __name__ == "__main__":
    if len(sys.argv) !=2:
        print("usage:  make_image.py <filename>")
        exit(1)
    filename = sys.argv[1]
    print(f"input: {filename}")


new_file = f"./{ntpath.basename(filename)}_CMYK.jpg"
print(f"output: {new_file}")

array_file = np.fromfile(filename, dtype=np.uintc)
size = len(array_file)

dimension = math.floor(math.sqrt(size))+1
array = np.empty((dimension*dimension,1), np.uintc)

print(f"file length: {len(array_file)} 32-bit words")
print(f"image size: {dimension} x {dimension} pixels (32 bits per pixel)")

for idx, val in enumerate(array_file, start=0):
    array[idx]=val

array = np.reshape(array, (dimension, dimension))
data = im.fromarray(array, mode="CMYK")

data.save(new_file)




