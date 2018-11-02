from vox import Vox
import struct

def GetZoneCoordinates(blockx, blocky):
    return (blockx//256, blocky//256)

def GetZoneFileName(blockx, blocky):
    x, y = GetZoneCoordinates(blockx, blocky)
    return f"{x}-{y}.cwb"

def MakeBlockData(x,y,z,r,g,b,t):
    bx = struct.pack("<I", x)
    by = struct.pack("<I", y)
    bz = struct.pack("<i", z)
    br = struct.pack("<B", r)
    bg = struct.pack("<B", g)
    bb = struct.pack("<B", b)
    bt = struct.pack("<B", t)
    return bx + by + bz + br + bg + bb + bt




if __name__ == "__main__":

    voxName = input("Enter vox file: ")
    startx = int(input("Enter x offset in blocks: "))
    starty = int(input("Enter y offset in blocks: "))
    startz = int(input("Enter z offset in blocks: "))

    v = Vox(voxName)
    blocks = v.ListVoxels()
    ##startx = 128110
    ##starty = 127988
    ##startz = -63

    zones = {}

    for block in blocks:
        x,y,z,r,g,b,a = block
        newx = x + startx
        newy = y + starty
        newz = z + startz

        fileName = GetZoneFileName(newx, newy)
        if fileName not in zones:
            print(f'Initializing {fileName}')
            zones[fileName] = b''

        if (r,g,b) == (0,0,255):
            zones[fileName] += MakeBlockData(newx, newy, newz, r, g, b, 2)
        else:
            zones[fileName] += MakeBlockData(newx, newy, newz, r, g, b, 1)

    for zone in zones:
        data = zones[zone]
        print(f"Saving {zone}.")
        with open(zone, 'wb') as f:
            f.write(data)
