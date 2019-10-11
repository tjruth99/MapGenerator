import noise
import numpy
import scipy
from PIL import Image

n = 1024
scale = 100.0
octaves = 6
persistence = 0.5
lacunarity = 2.0

def generateNoiseMap():
    print("Generate Perlin Noise Map")
    #help(noise)
    map = numpy.zeros((n,n))
    data = numpy.zeros( (n,n,3), dtype=numpy.uint8 )

    max = -1
    min = 1

    for i in range(n):
        for j in range(n):
            num = noise.pnoise2(    i/scale, 
                                    j/scale, 
                                    octaves=octaves, 
                                    persistence=persistence, 
                                    lacunarity=lacunarity, 
                                    repeatx=1024, 
                                    repeaty=1024, 
                                    base=0) * 10
            map[i][j] = num

            if num > max:
                max = num

            if num < min:
                min = num
                
            if( num < -1 ):                 # deep ocean
                data[i][j] = [0, 0, 150]
            elif ( num < 0 ):               # ocean
                data[i][j] = [0, 0, 225]
            elif ( num < 0.5 ):             # sand
                data[i][j] = [194, 178, 128]
            elif ( num < 1.5 ):             # land land
                data[i][j] = [0, 150, 0]
            elif( num < 2.5 ):              # mountains
                data[i][j] = [100, 100, 100]
            else:                           #snow
                data[i][j] = [225, 225, 225]

            #data[i][j] = [num*225, num*225, num*225]

    Image.fromarray(data).show()
    print(max,min)
    pass