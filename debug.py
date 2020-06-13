from Dungeon import *
from PerlinNoiseMap import *
from RandomWalk import *

generateRandomWalkMap(100, 10000, 16, 61, 0, 2).resize((500,500)).show()

cells = int(input("Dungeon Size: "))
img = generateDungeon(cells)
img.resize((500,500)).show()

