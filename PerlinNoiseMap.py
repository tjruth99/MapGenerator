import noise
import numpy
import random
from PIL import Image

deepWater = [0, 0, 150]
water = [0, 0, 225]
sand = [194, 178, 128]
grass = [0, 150, 0]
forest = [0, 100, 0]
mountain = [100, 100, 100]
snow = [225, 225, 225]

n = 1024
scale = 100.0
octaves = 5
persistence = 0.5
lacunarity = 2.0

def generateNoiseMap():
    print("Generate Perlin Noise Map")
    map = numpy.zeros((n,n))
    data = numpy.zeros( (n,n,3), dtype=numpy.uint8 )
    
    # TODO: Find a better way to do variability
    seed = int(input("seed: "))

    random.seed( seed )

    rand = random.randint(0, 1024)

    max = -1024
    min = 1024

    for i in range(n):
        for j in range(n):
            num = noise.pnoise2(    (i/scale), 
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

    colorMap(map,max,min)

    generateNoiseMap()
    pass

def colorMap(map, max, min):
    data = numpy.zeros( (n,n,3), dtype=numpy.uint8 )

    deepOceanLevel = (max-min)*0.4
    oceanLevel = (max-min)*0.5
    sandLevel = (max-min)*0.55
    landLevel = (max-min)*0.62
    forestLevel = (max-min)*0.7
    mountainLevel = (max-min)*0.85

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

