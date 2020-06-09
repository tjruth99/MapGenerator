import numpy
import math
import random
from PIL import Image

n = 25

# Generate a random dungeon in the style of binding of issac / original legend of zelda
#   - No Hallways
#   - Rooms are exactly one grid tile
def generateClassicDungeon():
    map = numpy.zeros((n,n), dtype=int)

    ax = [1, -1, 0, 0]
    ay = [0, 0, 1, -1]

    x = int(n/2)
    y = int(n/2)

    map[x][y] = 1
    tunnelSize = n

    for i in range(4):
        x = int(n/2) + ax[i]
        y = int(n/2) + ay[i]

        for j in range(tunnelSize):
            if(x > 0 and x < n and y > 0 and y < n):
                map[x][y] = 1
            val = random.randint(1,4)
            if val == 1:
                x = x + 1
            elif val == 2:
                x = x - 1
            elif val == 3:
                y = y + 1
            else:
                y = y - 1

    printColor(map)

    return map

def printColor(map):
    data = numpy.zeros( (n,n,3), dtype=numpy.uint8 )
    
    for i in range(n):
        for j in range(n):
            if map[i][j] == 0:
                data[i][j] = [0,0,0]
            else:
                data[i][j] = [255, 255, 255]

    scaleUp(map, n, 10)

def scaleUp(map, n, factor):
    data = numpy.zeros( (n*factor,n*factor,3), dtype=numpy.uint8 )

    for i in range(n):
        for j in range(n):
            for k in range(factor):
                for l in range(factor):
                    val = map[i][j]
                    if val == 0:
                        data[(i*factor)+k][(j*factor)+l] = [0,0,0]
                    elif val == 1:
                        data[(i*factor)+k][(j*factor)+l] = [255, 255, 255]

    Image.fromarray(data).show()

def printArray(map):
    for i in range(n):
        for j in range(n):
            print(map[i][j], end=" ")
        print()

generateClassicDungeon()