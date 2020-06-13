from Dungeon import *
from PerlinNoiseMap import *

cells = int(input("Dungeon Size: "))
img = generateDungeon(cells)
img.resize((500,500)).show()

