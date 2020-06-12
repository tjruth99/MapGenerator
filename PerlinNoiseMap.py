import noise
import numpy
import random
from PIL import Image

# RGB Colors of map
deepWater = [0, 0, 150]
water = [0, 0, 225]
sand = [194, 178, 128]
grass = [0, 150, 0]
forest = [0, 100, 0]
mountain = [100, 100, 100]
snow = [225, 225, 225]

# Determines what color a point is based on its percent of 
colorLevels = [0.35, 0.4, 0.45, 0.6, 0.7, 0.85]

n = 1024
scale = 200
octaves = 7
persistence = 0.5
lacunarity = 2.0

def getMinMax(map):
    n = int(map.size**(1/2.0))
    max = -1024
    min = 1024

    for i in range(n):
        for j in range(n):
            num = map[i][j]

            if num > max:
                max = num

            if num < min:
                min = num

    return [min, max]


def generateNoiseMap():
    print("Generate Perlin Noise Map")
    map = numpy.zeros((n,n))
    
    # TODO: Find a better way to do variability
    seed = int(input("seed: "))

    for i in range(n):
        for j in range(n):
            map[i][j] = noise.snoise2((i/scale), 
                                    (j/scale), 
                                    octaves, 
                                    persistence, 
                                    lacunarity, 
                                    repeatx=n, 
                                    repeaty=n, 
                                    base=seed) + 0.5

    colorMap(map)

    return map

def greyscale(map):
    data = numpy.zeros( (n,n,3), dtype=numpy.uint8 )

    for i in range(n):
        for j in range(n):
            num = map[i][j]
            data[i][j] = [num*225, num*225, num*225]

    Image.fromarray(data).show()

def colorMap(map):
    data = numpy.zeros( (n,n,3), dtype=numpy.uint8 )

    mm = getMinMax(map)
    min = mm[0]
    max = mm[1]

    deepOceanLevel = (max-min)*colorLevels[0]+min
    oceanLevel = (max-min)*colorLevels[1]+min
    sandLevel = (max-min)*colorLevels[2]+min
    landLevel = (max-min)*colorLevels[3]+min
    forestLevel = (max-min)*colorLevels[4]+min
    mountainLevel = (max-min)*colorLevels[5]+min

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

# Combining two perlin noise maps tends to give maps with a lot of islands
def combine():
    map1 = generateNoiseMap()
    map2 = generateNoiseMap()
    map3 = numpy.zeros((n,n))

    for i in range(n):
        for j in range(n):
            num = map1[i][j] * map2[i][j]
            map3[i][j] = num

    colorMap(map3)
    
generateNoiseMap()