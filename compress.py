import cv2
import numpy as np
from random import randint
import sys, os
from time import sleep, perf_counter as pc

# ======================== SETTINGS ======================
# ========================================================
INPUT = 'in.png'
OUTPUT = 'result.jpg'
COMPRESSED_FILE_OUTPUT = 'compressed.txt'
# ========================================================
# ========================================================

class Compressor():
    def __init__(self, H, W, img):
        self.W = W
        self.H = H
        self.img = img
        self.hexed = []
        self.compressed = []

    def _rgb_to_hex(self, r, g, b):
        return '#{:02x}{:02x}{:02x}'.format(r, g, b)

    # length encode
    def _rle(self, a):
        r = []
        last = a[0]
        c = 0
        for i in a:
            if last == i:
                c += 1
            else:
                r.append((last, c))
                last = i
                c = 1
        r.append((last, c))
        return r

    def _hexify(self):
        for i in range(self.H):
            t = []
            for j in range(self.W):
                t.append(self._rgb_to_hex(
                    self.img[i, j, 0], self.img[i, j, 1], self.img[i, j, 2]))
            self.hexed.append(t)

    def compress(self):
        self._hexify()
        for row in self.hexed:
            self.compressed.append(self._rle(row))

    def writeTo(self, file):
        with open(file, 'w') as f:
            for row in self.compressed:
                for tup in row:
                    s, rep = tup
                    f.write(f'{rep}{s} ')
                f.write('\n')


class Reader():
    def __init__(self):
        self.H = None
        self.W = None
        self.hexed = []
        self.res = []
        self.img = None

    def _hex_to_rgb(self, hex):
        rgb = []
        for i in (0, 2, 4):
            decimal = int(hex[i:i+2], 16)
            rgb.append(decimal)

        return rgb

    def readFrom(self, file):
        with open(file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                r = []
                splittedLine = line.split(' ')[:-1]
                for block in splittedLine:
                    rep, color = block.split("#")
                    for _ in range(int(rep)):
                        r.append(self._hex_to_rgb(color))
                self.res.append(r)

        W = len(self.res[0]); H = len(self.res)
        self.img = np.zeros((H, W, 3), np.uint8)
        for i in range(len(self.res)):
            for j in range(len(self.res[i])):
                self.img[i, j] = self.res[i][j]

    def saveFile(self, file):
        cv2.imwrite(file, self.img)

# Read image
img = cv2.imread(INPUT)
height, width, depth = img.shape

# Compress
c = Compressor(height, width, img)

t_encode = pc()
c.compress()
print("[+]Time to encode:", pc()-t_encode)
c.writeTo(COMPRESSED_FILE_OUTPUT)

print("Size of OG in memory:", sys.getsizeof(c.img)//1024, "KB")
print("Size of OG file:", os.path.getsize(INPUT) // 1024, "KB")
print("Size of compressed in memory:", sys.getsizeof(c.compressed)//1024, "KB")
print("Size of compressed file:", os.path.getsize(COMPRESSED_FILE_OUTPUT) // 1024, "KB")

# Decompress
r = Reader()
t_decode = pc()
r.readFrom(COMPRESSED_FILE_OUTPUT)
print("[+]Time to decode:", pc() - t_decode)
r.saveFile(OUTPUT)
