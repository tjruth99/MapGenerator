import random
import math
import numpy
from PIL import Image


# Variables:
#   seed: seed for generation (optional)
#   n: width/height of map
#   steps: number of steps to generate the map
#   numCities: number of cities to generate
#       default: math.ceil(n/10)
#   elevation: number of ranges to generate
#       default: math.ceil(n/10)
#   islandCoef: variable to determine how many times the brush jumps around to make islands
#   rangeLength: max length for each mountain range
#   brushSize: size of brush that paints the land/mountains (0 small, 1 medium, 2 large, 3 extra large)
#       default: 1

waterColor = [0, 0, 225]
landColor = [0, 150, 0]
cityColor = [0, 0, 0]
snowColor = [225, 225, 225]
sandColor = [194, 178, 128]

colors = {
    0: waterColor,
    1: landColor,
    2: cityColor,
    3: snowColor,
    4: sandColor
}

# output an image of
def getMap(map, n):
    data = numpy.zeros( (n,n,3), dtype=numpy.uint8 )

    for i in range(n):
        for j in range(n):
            # Get the color to draw from colors dictionary
            data[i][j] = colors[map[i][j]]

    return Image.fromarray(data)


def paint(map, n, x, y, num, val, brushSize):
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

#   Randomly add cities to the map proportional to the size of the map
def populate(map, n, numCities):
    cities = 0
    tries = 0

    while cities < numCities:
        # Prevents an infinite loop
        if tries > n:
            break

        tries = tries + 1
        x = random.randint(0,n-1)
        y = random.randint(0,n-1)

        if(map[x][y] == 1):
            cities = cities + 1
            map[x][y] = 2

    #TODO (?): Use Voronoi to make the cities capitals of nations
    pass

#   Function to tell if a node is adjacent to a water node
def nextToWater(map, n, x, y):
    if(x == 0 or x == n-1 or y == 0 or y == n-1):
        return True

    if(map[x + 1][y] == 0 or map[x - 1][y] == 0):
        return True
    elif(map[x][y + 1] == 0 or map[x][y - 1] == 0):
        return True
    elif(map[x + 1][y + 1] == 0 or map[x + 1][y - 1] == 0):
        return True
    elif(map[x - 1][y + 1] == 0 or map[x - 1][y - 1] == 0):
        return True

    return False

#   Adds mountain ranges to the map
def elevate(map, n, elevation, rangeLength, brushSize):
    for ranges in range(elevation):
        x = -1
        y = -1
        val = -1
        tries = 0

        # While loop finds an appropriate starting location for a range
        while (map[x][y] != 1 or nextToWater(map, n, x, y)):
            if(tries >= n):
                return

            x = random.randint(1,n-2)
            y = random.randint(1,n-2)
            tries = tries + 1

        # For loop paints the range onto the map
        for i in range(rangeLength):
            paint(map, n, x, y, 3, val, brushSize)

            val = random.randint(1,4)
            if val == 1:
                x = x + 1
            elif val == 2:
                x = x - 1
            elif val == 3:
                y = y + 1
            else:
                y = y - 1

            if ((x < -1) or (x > n-1) or (y < -1) or (y > n-1) or map[x][y] == 0):
                break

    pass

#   Generate map based on random walk
def generateRandomWalkMap(n, steps, elevation, rangeLength, islandCoef, brushSize):
    x = int(n/2)
    y = int(n/2)
    val = -1

    map = numpy.zeros((n,n), dtype=int)

    for i in range(steps):
        if (0 < x < n-1) and (0 < y < n-1):
            paint(map, n, x, y, 1, val, brushSize)
        else:
            x = random.randint(0,n-1)
            y = random.randint(0,n-1)

        newIsland = random.randint(0, 100)
        if(newIsland < islandCoef*100):
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

    elevate(map, n, elevation, rangeLength, brushSize)

    return getMap(map, n)

def randomWalk():
    print("Generate Random Walk Map")

    n = int(input("n: "))
    steps = int(input("enter steps: "))
    elevation = int(input("elevation: "))
    rangeLength = int(input("rangeLength: "))
    islandCoef = float(input("islandCoef: "))
    brushSize = int(input("brush_size: "))

    print("n: %d, steps: %d" %(n,steps))
    img = generateRandomWalkMap(n, steps, elevation, rangeLength, islandCoef, brushSize)
    img.resize((500, 500)).show()