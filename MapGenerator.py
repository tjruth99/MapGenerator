import random
import math
from colorama import init, Back, Style
init()

# 0 is water, 1 is land, 2 is a city TODO: Brown is mountain
def printmap():
    for i in range(n):
        for j in range(n):
            if map[i][j] == 0:
                print(Back.BLUE + "0", end = " ")
            elif map[i][j] == 1:
                print(Back.GREEN + "1", end = " ")
            elif map[i][j] == 2:
                print(Back.BLACK + "2", end = " ")
        print()
    print(Style.RESET_ALL)
    pass

def populate():
    cities = 0
    while cities < math.ceil(n/10):
        x = random.randint(0,n-1)
        y = random.randint(0,n-1)

        if(map[x][y] == 1):
            cities = cities + 1
            map[x][y] = 2

    #TODO: Use Voronoi to make the cities capitals of nations
    pass

def elevate():
    #TODO: Make mountains and mountain ranges
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
    genrateMap()