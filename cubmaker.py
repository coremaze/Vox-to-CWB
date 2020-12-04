from vox import Vox
import struct
import io
import numpy as np
import argparse


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('input', type=str, help='vox file to convert')
    parser.add_argument('output', type=str, help='cub file to create')
    args = parser.parse_args()

    v = Vox(args.input)
    blocks = v.ListVoxels()

    xMax = max(blocks, key=lambda x: x[0])[0] + 1
    xMin = min(blocks, key=lambda x: x[0])[0]

    yMax = max(blocks, key=lambda x: x[1])[1] + 1
    yMin = min(blocks, key=lambda x: x[1])[1]

    zMax = max(blocks, key=lambda x: x[2])[2] + 1
    zMin = min(blocks, key=lambda x: x[2])[2]

    xLen = xMax - xMin
    yLen = yMax - yMin
    zLen = zMax - zMin

    #print(xLen, yLen, zLen)
    header = struct.pack('<III', xLen, yLen, zLen)

    body = np.zeros((zLen, yLen, xLen, 3)).astype(np.ubyte)

    for block in blocks:
        x,y,z,r,g,b,a = block

        x -= xMin
        y -= yMin
        z -= zMin

        body[z][y][x][0] = r
        body[z][y][x][1] = g
        body[z][y][x][2] = b

    with open(args.output, 'wb') as f:
        f.write(header)
        f.write(body)
