import random
import math
from colorama import init, Back, Style
init()

# 0 is water, 1 is land, 2 is a city TODO: 3 is mountain
def printmap():
    for i in range(n):
        for j in range(n):
            if map[i][j] == 0:
                print(Back.BLUE + "0", end = " ")
            elif map[i][j] == 1:
                print(Back.GREEN + "1", end = " ")
            elif map[i][j] == 2:
                print(Back.BLACK + "2", end = " ")
            elif map[i][j] == 3:
                print(Back.WHITE + "3", end = " ")
        print()
    print(Style.RESET_ALL)
    pass

#   Randomly add cities to the map proportional to the size of the map
def populate():
    cities = 0
    tries = 0

    while cities < math.ceil(n/10):
        # Prevents an infinite loop
        if tries > n:
            break

        tries = tries + 1
        x = random.randint(0,n-1)
        y = random.randint(0,n-1)

        if(map[x][y] == 1):
            cities = cities + 1
            map[x][y] = 2

    #TODO: Use Voronoi to make the cities capitals of nations
    pass

#   Function to tell if a node is adjacent to a water node
def nextToWater(x, y):
    if(map[x][y] == 0):
        return True
    elif(map[x + 1][y] == 0 or map[x - 1][y] == 0):
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
    for ranges in range(math.ceil(n/10)):
        x = -1
        y = -1
        val = -1
        tries = 0

        while (map[x][y] != 1 or nextToWater(x,y)):
            if(tries >= n):
                return

            x = random.randint(1,n-2)
            y = random.randint(1,n-2)
            tries = tries + 1

        for i in range(math.ceil(50)):
            map[x][y] = 3
            if (val == 1 or val == 2):
                map[x][y+1] = 3
                map[x][y-1] = 3
            elif(val == 3 or val == 4):
                map[x+1][y] = 3
                map[x-1][y] = 3

            val = random.randint(1,4)
            if val == 1:
                x = x + 1
            elif val == 2:
                x = x - 1
            elif val == 3:
                y = y + 1
            else:
                y = y - 1

            if ((x < -1) or (x > n) or (y < -1) or (x > n) or map[x][y] == 0):
                break

    pass

#   Generate map based on random walk
def generateMap():
    x = int(n/2)
    y = int(n/2)

    for i in range(steps):
        if (-1 < x < n) and (-1 < y < n):
            map[x][y] = 1
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

    elevate()
    populate()
    printmap()
    pass

while True:
    n = input("enter n: ")
    if n == "exit":
        break

    n = int(n)
    steps = int(input("enter steps: "))
    map = [[0 for i in range(n)] for j in range(n)] 
    generateMap()