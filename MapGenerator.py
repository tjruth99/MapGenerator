import random
import math
from colorama import init, Back, Style
import numpy
import scipy.misc as smp
from PIL import Image
init()

#Variables:
#   seed: seed for generation (optional)
#   n: width/height of map
#   steps: number of steps to generate the map
#   numCities: number of cities to generate
#       default: math.ceil(n/10)
#   elevation: number of ranges to generate
#       default: math.ceil(n/10)
#   islandCoef: variable to determine how many times the brush jumps around to make islands
#   rangeLength: max length for each mountain range
#   brush_size: size of brush that paints the land/mountains (0 small, 1 medium, 2 large)
#       default: 1

# random.seed( 10 )
n = 100
steps = 10000
numCities = math.ceil(n/10)
elevation = math.ceil(n/10)
islandCoef = 0.00
rangeLength = n
brush_size = 1

# 0 is water, 1 is land, 2 is a city, 3 is mountain, 4 is beach
def printmap( printToConsole ):
    data = numpy.zeros( (n,n,3), dtype=numpy.uint8 )

    global area
    for i in range(n):
        for j in range(n):
            if map[i][j] == 0:
                if(printToConsole):
                    print(Back.BLUE + "0", end = " ")

                data[i][j] = [0,0,200]

            elif map[i][j] == 1:
                if(printToConsole):
                    print(Back.GREEN + "1", end = " ")

                data[i][j] = [0,200,0]
                area = area + 1

            elif map[i][j] == 2:
                if(printToConsole):
                    print(Back.BLACK + "2", end = " ")

                data[i][j] = [0,0,0]
                area = area + 1

            elif map[i][j] == 3:
                if(printToConsole):
                    print(Back.WHITE + "3", end = " ")

                data[i][j] = [225,225,225]
                area = area + 1

            elif map[i][j] == 4:
                if(printToConsole):
                    print(Back.LIGHTYELLOW_EX + "4", end = " ")

                data[i][j] = [225,225,0]
        if(printToConsole):
            print()
            print(Back.RESET)

    Image.fromarray(data).show()

def paint(x,y,num,val):
    map[x][y] = num

    if(x == 0 or x == n-1 or y == 0 or y == n-1):
        return

    if(brush_size == 1):
        if (val == 1 or val == 2):
            map[x][y+1] = num
            map[x][y-1] = num
        elif(val == 3 or val == 4):
            map[x+1][y] = num
            map[x-1][y] = num

    if(brush_size == 2):
        map[x+1][y] = num
        map[x-1][y] = num
        map[x][y+1] = num
        map[x][y-1] = num
        map[x+1][y+1] = num
        map[x+1][y-1] = num
        map[x-1][y+1] = num
        map[x-1][y-1] = num

    pass

#   Randomly add cities to the map proportional to the size of the map
def populate():
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
def nextToWater(x, y):
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
def elevate():
    for ranges in range(elevation):
        x = -1
        y = -1
        val = -1
        tries = 0

        # While loop finds an appropriate starting location for a range
        while (map[x][y] != 1 or nextToWater(x,y)):
            if(tries >= n):
                return

            x = random.randint(1,n-2)
            y = random.randint(1,n-2)
            tries = tries + 1

        # For loop paints the range onto the map
        for i in range(rangeLength):
            paint(x,y,3,val)

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

def beach():
    for x in range(n):
        for y in range(n):
            if(map[x][y] == 1 and nextToWater(x,y)):
                map[x][y] = 4
    pass

#   Generate map based on random walk
def generateMap():
    x = int(n/2)
    y = int(n/2)
    val = -1

    for i in range(steps):
        if (0 < x < n-1) and (0 < y < n-1):
            paint(x,y,1,val)
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

    elevate()
    populate()
#   beach()
    printmap(False)
    pass

while True:
    n = int(input("n: "))
    steps = int(input("enter steps: "))
    elevation = int(input("elevation: "))
    rangeLength = int(input("rangeLength: "))
    numCities = math.ceil(n/10)
    islandCoef = float(input("islandCoef: "))
    brush_size = int(input("brush_size: "))

    map = [[0 for i in range(n)] for j in range(n)]
    area = 0

    print("n: %d, steps: %d" %(n,steps))
    generateMap()
    print("Land Area: %d, Total Area: %d (%.2f%%)" %(area, n*n, (area/(n*n))*100))
