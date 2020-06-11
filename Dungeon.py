import numpy
import math
import random
from PIL import Image

# Generate a random dungeon in the style of binding of issac / original legend of zelda
#   n - size of map
#   maxRooms - maximum number of rooms to draw
def generateClassicDungeon(n, maxRooms):
    # Check to make sure maxRooms isn't larger than map size 
    if(maxRooms < 2 or maxRooms >= n**2):
        return

    map = numpy.zeros((n,n), dtype=int)

    #  Arrays to hold values to make paths branch from each direction of the starting node
    ax = [1, -1, 0, 0]
    ay = [0, 0, 1, -1]

    x = int(n/2)
    y = int(n/2)

    map[x][y] = 1
    tunnelSize = n
    roomsDrawn = 1

    for i in range(4):
        if roomsDrawn == maxRooms:
                break

        # Have 4 different tunnels that start from each side of the starting node
        x = int(n/2) + ax[i]
        y = int(n/2) + ay[i]

        for j in range(tunnelSize):
            if roomsDrawn == maxRooms:
                break

            if(x > 0 and x < n and y > 0 and y < n):
                map[x][y] = 1
                roomsDrawn += 1

            # Random Walk Algorithm
            val = random.randint(1,4)
            if (val == 1 and x < n):
                x = x + 1
            elif (val == 2 and x > 0):
                x = x - 1
            elif (val == 3 and y < n):
                y = y + 1
            elif (val == 4 and y > 0):
                y = y - 1

    # print the map for debugging
    printColor(map)

    return map

# Generate a classic dungeon in a more simplistic way
#   n - size of map
#   numRooms - number of rooms to generate
def generateClassicDungeonSnake(n, numRooms):
    # Check to make sure the numRooms isn't larger than map size 
    if( numRooms < 0 or numRooms >= n**2):
        return

    map = numpy.zeros((n,n), dtype=int)

    x = int(n/2)
    y = int(n/2)

    while numRooms > 0:
        if(x > 0 and x < n and y > 0 and y < n):
            # If the current position hasn't been visited, add a room there and mark down how many rooms to draw
            if map[x][y] == 0:
                map[x][y] = 1
                numRooms = numRooms - 1
            
        # Random Walk
        val = random.randint(1,4)
        if (val == 1 and x < n):
            x = x + 1
        elif (val == 2 and x > 0):
            x = x - 1
        elif (val == 3 and y < n):
            y = y + 1
        elif (val == 4 and y > 0):
            y = y - 1

    printColor(map)

    return map


# TODO:
#   - add more paths between rooms
#   - make hallways more maze-like (?)
def generateDungeon(n, cells):
    maxRoomSizeDim = int(n/cells)-5
    minRoomSizeDim = 10
    
    # stores the start and end coordinates of each room
    rooms=[]

    # ignore some rooms to give dungeon a more varied look, not always a grid
    ignoreRoomPercent = 25

    map = numpy.zeros((n,n), dtype=int)

    for i in range(cells):
        for j in range(cells):
            lenX = random.randint(minRoomSizeDim, maxRoomSizeDim)
            lenY = random.randint(minRoomSizeDim, maxRoomSizeDim)

            startX = int(((n/cells) * i) + random.randint(0, int(n/cells) - lenX))
            startY = int(((n/cells) * j) + random.randint(0, int(n/cells) - lenY))

            # Decides to draw the room or not
            ignore = random.randint(0, 100)

            if(ignore > ignoreRoomPercent):
                rooms.append([startX, startY, lenX+startX, lenY+startY])
                for x in range(lenX):
                    for y in range(lenY):
                        map[int(x + startX)][int(y + startY)] = 1

    # add a linear path to each room
    for i in range(1, len(rooms)):
        fromRoom = rooms[i-1]
        toRoom = rooms[i]

        # get the starting coordinates for the hallway from somewhere in the from room
        startX = random.randint(fromRoom[0]+1, fromRoom[2]-1)
        startY = random.randint(fromRoom[1]+1, fromRoom[3]-1)

        # get the ending coordinates for the hallway from somewhere in the to room
        endX = random.randint(toRoom[0]+1, toRoom[2]-1)
        endY = random.randint(toRoom[1]+1, toRoom[3]-1)

        # draw the hallway on the x plane
        if(endX > startX):
            for j in range(startX, endX):
                map[j][startY] = 1
        else: 
            for j in range(endX, startX):
                map[j][startY] = 1

        # draw the hallway on the y plane
        if(endY > startY):
            for j in range(startY, endY):
                map[endX-1][j] = 1
        else: 
            for j in range(endY, startY):
                map[endX-1][j] = 1

    # draw a border on the edge to make the map look cleaner
    for i in range(n):
        map[0][i] = 0
        map[i][0] = 0
        map[n-1][i] = 0
        map[i][n-1] = 0

    printColor(map)

    return map

            
def printColor(map):
    n = int(map.size**(1/2.0))
    data = numpy.zeros( (n,n,3), dtype=numpy.uint8 )
    
    for i in range(n):
        for j in range(n):
            if map[i][j] == 0:
                data[i][j] = [0,0,0]
            else:
                data[i][j] = [255, 255, 255]

    scaleUp(map, 10)

def scaleUp(map, factor):
    n = int(map.size**(1/2.0))
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
    n = (map.size**(1/2.0))
    for i in range(n):
        for j in range(n):
            print(map[i][j], end=" ")
        print()

generateDungeon(90, 3)
#generateClassicDungeon(10, 10)
#generateClassicDungeonSnake(10, 10)