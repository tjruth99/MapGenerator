import noise
import numpy
import random
from PIL import Image

deepWater = [0, 0, 150]
water = [0, 0, 225]
sand = [194, 178, 128]
grass = [0, 150, 0]
mountain = [100, 100, 100]
snow = [225, 225, 225]

n = 1024
scale = 100.0
octaves = 5
persistence = 0.5
lacunarity = 2.0

def generateNoiseMap():
    print("Generate Perlin Noise Map")
    #help(noise)
    map = numpy.zeros((n,n))
    data = numpy.zeros( (n,n,3), dtype=numpy.uint8 )
    
    seed = int(input("seed: "))

    random.seed( seed )

    rand = random.randint(0, 1024)

    max = -1
    min = 1

    for i in range(n):
        for j in range(n):
            num = noise.pnoise2(    (i/scale), 
                                    (j/scale), 
                                    octaves, 
                                    persistence, 
                                    lacunarity, 
                                    repeatx=n, 
                                    repeaty=n, 
                                    base=rand) * 10
            map[i][j] = num

            if num > max:
                max = num

            if num < min:
                min = num
                
            if( num < -1 ):                 # deep ocean
                data[i][j] = deepWater
            elif ( num < 0 ):               # ocean
                data[i][j] = water
            elif ( num < 0.5 ):             # sand
                data[i][j] = sand
            elif ( num < 1.5 ):             # land
                data[i][j] = grass
            elif( num < 2.0 ):              # mountains
                data[i][j] = mountain
            else:                           #snow
                data[i][j] = snow

    Image.fromarray(data).show()
    print(max,min)

    generateNoiseMap()
    pass