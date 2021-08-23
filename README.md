# make_image.py

Makes color image based on the byte values of any file.

Very primitive and silly, and not guaranteed to reveal
secret Bible-code-like data trends, but hey, that's sort of the point :).

Usage:  `make_image.py <filename>`

` ./make_image.py /bin/bash # creates a PNG file based on the bash executable. `

The script looks at bytes from the file in 32-bit word chunks and maps them to 32-bit CMYK encoded pixels.

Then, a section of 225 bytes from part-way into that file is taken and given the same process.  (Assuming the file is 50K or larger)

Finally, that section off 225 bytes is enlarged overlaid on the original with transparency to show
scale and detail.    The final image is then scaled to 4000x4000 pixels unless the `no_scale` argument is added.


