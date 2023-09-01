from cv2 import imread, imwrite
import numpy as np
import random
import argparse

class Encoder():

    def __init__(self, in_file, out_file):
        img = imread(in_file)
        height, width, _ = img.shape
        
        self.out_file = out_file
        self.img = img
        self.height = height
        self.width = width
        
        self.hexed = np.empty((height, width), dtype='S6')
        self.compressed = []
        

    def _rgb_to_hex(self, r, g, b):
        return '{:02x}{:02x}{:02x}'.format(r, g, b)


    def _rle(self, a):
        result = []
        last = a[0]
        count = 0
        for i in a:
            if last == i:
                count += 1
            else:
                result.append((last, count))
                last = i
                count = 1
        result.append((last, count))
        return result


    def _hexify(self):
        for i in range(self.height):
            for j in range(self.width):
                hex = self._rgb_to_hex(self.img[i, j, 0], self.img[i, j, 1], self.img[i, j, 2])
                self.hexed[i, j] = hex


    def write_compressed(self):
        s = f'{self.height}x{self.width}\n'
        for row in self.compressed:
            for cell in row:
                color, count = cell
                s += f'{count}#{color.decode()}'
            s += '\n'
            
        open(self.out_file, 'w+', encoding='utf8').write(s)


    def compress(self):
        self._hexify()
        for row in self.hexed:
            self.compressed.append(self._rle(row))
        self.write_compressed()

class Decoder():
    
    def __init__(self, in_file, out_file):
        self.in_file = in_file
        self.out_file = out_file
        
        self.file_content = open(in_file, 'r', encoding='utf8').read()
        self.file_lines = self.file_content.splitlines()
        
        self.color_to_rgb = lambda color: [int(color[i:i+2], 16) for i in (0, 2, 4)]
    

    def _create_img_array(self):
        height, width = [int(data) for data in self.file_lines[0].split('x')]
        
        self.height = height
        self.width = width
        self.img = np.empty((height, width, 3), dtype=np.uint8)
        
    def _unpack_line(self, line: str):
        result = []
        curr = ''
        skips = 0
        
        for i, ch in enumerate(line):
            if skips > 0:
                skips -= 1
                continue
            if ch == '#':
                color = line[i+1:i+7]
                result.append((color, int(curr)))
                
                curr = ''
                skips = 6
            else:
                curr += ch

        return result

    def decompress(self):
        self._create_img_array()
        
        i, j = 0, 0
        
        for line in self.file_lines:
            if i >= self.height:
                continue
            
            data = self._unpack_line(line)
            # for each rle encoded pair
            for color, count in data:
                for k in range(count):
                    r, g, b = self.color_to_rgb(color)
                    self.img[i, k + j, 0] = r
                    self.img[i, k + j, 1] = g
                    self.img[i, k + j, 2] = b
                j += count
                
            j = 0
            i += 1
        
        self.write_img()
            
    def write_img(self):
        imwrite(self.out_file, self.img)
            


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--decode', dest='decode', type=bool, help='decode mode', default=False, action=argparse.BooleanOptionalAction)
    parser.add_argument('-i', '--input', dest='in_file', type=str, help='Input file', required=True)
    parser.add_argument('-o', '--ouput', dest='out_file', type=str, help='Output file', default='out')
    
    args = parser.parse_args()
    
    # add file extension
    args.out_file += '.jpeg' if args.decode else '.txt'
    
    return args

def main(args):
    print('Writing to:', args.out_file)
    
    if args.decode:
        decoder = Decoder(in_file=args.in_file, out_file=args.out_file)
        decoder.decompress()
    else:
        encoder = Encoder(in_file=args.in_file, out_file=args.out_file)
        encoder.compress()
        


if __name__ == '__main__':
    args = get_args()
    main(args)