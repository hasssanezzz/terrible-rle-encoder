# Terrible image RLE Encoder

A simple and (currently) bad image compressor, that uses the RLE (Run length encoding) algorithm.

## Encoded output

It iterates over every row in an image, and convert to color blocks with the repeatition and the color, exmaple: `3#fefefe` this means that there are 3 pixels with color `#fefefe`.

```
...

50#ffffff 10#000000 40#dedede

...
```

It writes this output to a .txt file.

## Getting started

You can change these variables to get the script started.

```py

# ======================== SETTINGS ======================
# ========================================================
INPUT = 'in.png' # input image
OUTPUT = 'result.jpg' # output image when decompressing
COMPRESSED_FILE_OUTPUT = 'compressed.txt' # output compressed file
# ========================================================
# ========================================================

```
