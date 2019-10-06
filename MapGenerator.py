import random
from colorama import init, Back, Style
init()

def printmap():
    for i in range(n):
        for j in range(n):
            if map[i][j] == 0:
                print(Back.BLUE + "0", end = " ")
            else:
                print(Back.GREEN + "1", end = " ")
        print()
    print(Style.RESET_ALL)
    pass

def randomWalk():
    x = int(n/2)
    y = int(n/2)

    for i in range(steps):
        if (-1 < x < n) and (-1 < y < n):
            map[x][y] = 1
        else:
            x = random.randint(0,n)
            y = random.randint(0,n)

        val = random.randint(1,4)
        if val == 1:
            x = x + 1
        elif val == 2:
            x = x - 1
        elif val == 3:
            y = y + 1
        else:
            y = y - 1

    printmap()
    pass

while True:
    n = int(input("enter n: "))
    steps = int(input("enter steps: "))
    map = [[0 for i in range(n)] for j in range(n)] 
    randomWalk()