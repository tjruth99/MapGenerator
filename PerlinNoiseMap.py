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

# n is the size of the map
n = 1024
# Scale determines how zoomed in the map is
scale = 200
# Octaves, persistence, and lacunarity determine the level of detail in the map
octaves = 7
persistence = 0.5
lacunarity = 2.0

# Get the min and max value in the map
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

# Generate a map using perlin noise with a seed
def generateNoiseMap():
    map = numpy.zeros((n,n))

    # Get a random seed to generate a new map
    seed = random.randint(-1000000, 1000000)

    for i in range(n):
        for j in range(n):
            map[i][j] = noise.snoise2((i/scale), 
                                    (j/scale), 
                                    octaves, 
                                    persistence, 
                                    lacunarity, 
                                    repeatx=n, 
                                    repeaty=n, 
                                    base=seed)

    colorMap(map)
    return map

def generateNoiseMapWithInput():
    print("Generate Perlin Noise Map")
    map = numpy.zeros((n,n))
    
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
                                    base=seed)

    #colorMap(map)
    return map

# Draw the map with no color
def greyscale(map):
    data = numpy.zeros( (n,n,3), dtype=numpy.uint8 )

    for i in range(n):
        for j in range(n):
            num = map[i][j]
            data[i][j] = [num*225, num*225, num*225]

    Image.fromarray(data).show()

# Color the map with the actual min and max values of the map
def colorMap(map):
    mm = getMinMax(map)
    
    colorMapMM(map, mm[0], mm[1])

# Color the map with specified min and max values, used for extreme and flat maps
def colorMapMM(map, min, max):
    data = numpy.zeros( (n,n,3), dtype=numpy.uint8 )

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

# Generate a map with more extreme mountains and deep oceans
def extreme(factor):
    map = generateNoiseMap()

    for i in range(n):
        for j in range(n):
            map[i][j] *= factor

    colorMapMM(map, -1, 1)

# Generate a map with less hills and and deep oceans
def flat(factor):
    map = generateNoiseMap()

    for i in range(n):
        for j in range(n):
            map[i][j] /= factor

    colorMapMM(map, -1, 1)


generateNoiseMap()