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
    getColor(map).show()

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

    getColor(map).show()

    return map


# TODO:
#   - add more paths between rooms
#   - make hallways more maze-like (?)
def generateDungeon(cells):
    n = cells * 30
    maxRoomSizeDim = int(n/cells)-5
    minRoomSizeDim = 10
    
    # stores the start and end coordinates of each room
    rooms = []

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

    # Draw a path connecting each room
    drawPath(map, rooms)

    # draw a border on the edge to make the map look cleaner
    for i in range(n):
        map[0][i] = 0
        map[i][0] = 0
        map[n-1][i] = 0
        map[i][n-1] = 0

    # Get the dungeon with color data
    data = getColor(map)

    # Return a Pillow Image
    return Image.fromarray(data)

# Draw the path to each room using minimum spanning tree
def drawPath(map, rooms):
    connectedRooms = [0]
    listOfEdges = []

    distances = getDistanceToEachRoom(0, rooms)
    for j in distances:
        listOfEdges.append(j)

    # Use Primm's Algorithm to draw a connected path to each room
    for i in range(len(rooms)-1):
        minNode = []
        minValue = 999999

        # Go through each edge to find the minimum 
        for j in listOfEdges:
            # Check to make sure the node does not connect two rooms already inside the list
            if(not (j[1] in connectedRooms and j[2] in connectedRooms)):
                # Get the minimum value
                if(j[0] < minValue):
                    minValue = j[0]
                    minNode = j

        # If the indexes are not already in connected rooms, add it to the connected room lists and add edges to list
        if(not minNode[1] in connectedRooms):
            connectedRooms.append(minNode[1])
            distances = getDistanceToEachRoom(minNode[1], rooms)
            for j in distances:
                listOfEdges.append(j)
            
        if(not minNode[2] in connectedRooms):
            connectedRooms.append(minNode[2])
            distances = getDistanceToEachRoom(minNode[2], rooms)
            for j in distances:
                listOfEdges.append(j)

        # Draw the hallway between the rooms
        drawHallway(map, rooms[minNode[1]], rooms[minNode[2]])
    pass

# Take the index of a room and give a list of the distances to each of the other rooms in the dungeon
def getDistanceToEachRoom(index, rooms):
    curRoom = rooms[index]

    # Use the center of the current room to measure the distance
    curX = int((curRoom[0] + curRoom[2]) / 2)
    curY = int((curRoom[1] + curRoom[3]) / 2)

    distances = []

    for i in range(len(rooms)):
        targetRoom = rooms[i]

        # Use the center of the targer room to measure the distance
        targetX = int((targetRoom[0] + targetRoom[2]) / 2)
        targetY = int((targetRoom[1] + targetRoom[3]) / 2)

        # Get the distance
        d= int(math.sqrt((targetX - curX)**2 + (targetY - curY)**2))

        # Ignore distances of 0
        if(i != index):
            # Append an array of the distance, the current room index, and the targer room index
            distances.append([d, index, i])

    return distances

# Draw a hallway between two rooms
def drawHallway(map, fromRoom, toRoom):
    # get the starting coordinates for the hallway from the middle of the room
    startX = int((fromRoom[0] + fromRoom[2]) / 2)
    startY = int((fromRoom[1] + fromRoom[3]) / 2)

    # get the ending coordinates for the hallway from the middle of the room
    endX = int((toRoom[0] + toRoom[2]) / 2)
    endY = int((toRoom[1] + toRoom[3]) / 2)

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

            
def getColor(map):
    n = int(map.size**(1/2.0))
    data = numpy.zeros( (n,n,3), dtype=numpy.uint8 )
    
    for i in range(n):
        for j in range(n):
            if map[i][j] == 0:
                data[i][j] = [0,0,0]
            else:
                data[i][j] = [255, 255, 255]

    return data

def printArray(map):
    n = (map.size**(1/2.0))
    for i in range(n):
        for j in range(n):
            print(map[i][j], end=" ")
        print()

