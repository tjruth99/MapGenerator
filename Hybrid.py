import noise
import numpy
import random
import math
from colorama import init, Back, Style
import numpy
import scipy.misc as smp
from PIL import Image
init()

# Perlin Noise 
n = 1024
scale = 100.0
octaves = 5
persistence = 0.5
lacunarity = 2.0

#Random Walk Variables
steps = 10000
num = 1
brushSize = 2

#Colors
deepWater = [0, 0, 150]
water = [0, 0, 225]
sand = [194, 178, 128]
grass = [0, 150, 0]
forest = [0, 100, 0]
mountain = [100, 100, 100]
snow = [225, 225, 225]

def generatePerlinNoiseMap():
    map = numpy.zeros((n,n))
    
    rand = random.randint(0,10000)

    max = -1024
    min = 1024

    for i in range(n):
        for j in range(n):
            num = noise.snoise2(    (i/scale), 
                                    (j/scale), 
                                    octaves, 
                                    persistence, 
                                    lacunarity, 
                                    repeatx=n, 
                                    repeaty=n, 
                                    base=rand) + 0.5
            map[i][j] = num

            if num > max:
                max = num

            if num < min:
                min = num

    print("\tshowing perlin map . . .")
    colorMap(map, max, min)
    return map

def paint(map, n, x, y, val):
    map[x][y] = num

    if(x == 0 or x == n-1 or y == 0 or y == n-1):
        return

    if(brushSize == 1):
        if (val == 1 or val == 2):
            map[x][y+1] = num
            map[x][y-1] = num
        elif(val == 3 or val == 4):
            map[x+1][y] = num
            map[x-1][y] = num

    if(brushSize >= 2):
        map[x+1][y] = num
        map[x-1][y] = num
        map[x][y+1] = num
        map[x][y-1] = num
        map[x+1][y+1] = num
        map[x+1][y-1] = num
        map[x-1][y+1] = num
        map[x-1][y-1] = num

    if(brushSize >=3):
        for i in range(-3, 3):
            for j in range(-3, 3):
                if((x+i > 0 and x+i < n) and (y+j > 0 and y+j <n)):
                    map[x+i][y+j] = num
    pass

def generateRandomWalkMap():
    map = numpy.zeros((n,n))

    x = int(n/2)
    y = int(n/2)
    val = -1

    for i in range(steps):
        if (0 < x < n-1) and (0 < y < n-1):
            paint(map, n, x, y, val)
        else:
            x = random.randint(0,n-1)
            y = random.randint(0,n-1)

        val = random.randint(1,4)
        if val == 1:
            x = x + 1
        elif val == 2:
            x = x - 1
        elif val == 3:
            y = y + 1
        else:
            y = y - 1

    print("\tshowing random map . . .")
    colorMap(map, 1, 0)
    return map

def colorMap(map, max, min):
    data = numpy.zeros( (n,n,3), dtype=numpy.uint8 )

    deepOceanLevel = (max-min)*0.35 + min
    oceanLevel = (max-min)*0.4 + min 
    sandLevel = (max-min)*0.45 + min
    landLevel = (max-min)*0.60 + min
    forestLevel = (max-min)*0.7 + min
    mountainLevel = (max-min)*0.85 + min

    for i in range(n):
        for j in range(n):
            num = map[i][j]
            if( num < deepOceanLevel ):     # deep ocean
                data[i][j] = deepWater
            elif ( num < oceanLevel ):      # ocean
                data[i][j] = water
            elif ( num < sandLevel ):       # sand
                data[i][j] = sand
            elif ( num < landLevel):        # land
                data[i][j] = grass
            elif ( num < forestLevel ):     # forest
                data[i][j] = forest
            elif( num < mountainLevel ):    # mountains
                data[i][j] = mountain
            else:                           #snow
                data[i][j] = snow

    Image.fromarray(data).show()

def generateHybridMap():
    print("Generate a hybrid map")

    noiseMap = generatePerlinNoiseMap()
    randomMap = generateRandomWalkMap()

    hybridMap = numpy.zeros((n,n))

    max = -1024
    min = 1024

    for i in range(n):
        for j in range(n):
            hybridMap[i][j] = noiseMap[i][j] * randomMap[i][j]

            if num > max:
                max = num

            if num < min:
                min = num
   
    print("\tshowing hybrid map . . .")
    print(hybridMap)
    colorMap(hybridMap, max, min)
    pass