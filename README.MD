# Terrible image RLE Encoder

A simple and (currently) bad image compressor, that uses the RLE algorithm.

## Encoded output

It iterates over every row in an image, and convert to color blocks with the repeatition and the color, exmaple: `3#fefefe` this means that there are 3 pixels with color `#fefefe`.

```
...

50#ffffff10#00000040#dedede

...
```

It writes this output to a `.txt` file.

## Getting started

### Install the required dependencies

```
$ pip install -r requirements.txt
```

### CLI Arguments

```
usage: rlencode.py [-h] [-d | --decode | --no-decode] -i IN_FILE [-o OUT_FILE]

options:
  -h, --help            show this help message and exit
  -d, --decode, --no-decode
                        decode mode (default: False)
  -i IN_FILE, --input IN_FILE
                        Input file
  -o OUT_FILE, --ouput OUT_FILE
                        Output file (defualt: 'out')
```

### Examples

```
# Compress an image
$ rlencode.py -i /path/to/my/img.png -o /path/to/desired/output.txt

# Decompress
$ rlencode.py -d -i /path/to/compressed/file.txt -o img.jpeg
```

