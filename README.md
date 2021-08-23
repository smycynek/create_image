# make_image.py

Makes a set of color images based on the byte values of any file.

Very primitive and silly, and not guaranteed to reveal
secret Bible-code-like data trends, but hey, that's sort of the point :).

Usage:  `make_image.py <filename>`


` ./make_image.py /bin/bash # creates 3 PNG files based on the bash executable. `
`One represents all bytes, one represents the first 225 bytes,
(assuming the original file is larger than 90K), and one
is a composite of the two with transparency to show an enlargement
at scale.
