from PerlinNoiseMap import generateNoiseMap
from RandomWalk import randomWalk

print("Generate a map (0 for Perlin Noise / 1 for Random Walk)")
type = int(input(">"))

if type == 0:
    generateNoiseMap()
else:
    randomWalk()