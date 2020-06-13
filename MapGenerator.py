from tkinter import *
from PIL import ImageTk, Image

#from PerlinNoiseMap import generateNoiseMap
#from RandomWalk import randomWalk
from Dungeon import generateDungeon

global img
root = Tk()

def getDungeon(): 
    img = ImageTk.PhotoImage(generateDungeon(3))
    canvas.create_image(0,0, anchor=NW, image=img)
    canvas.image = img

Label(root, text="Dungeon Generator").pack()
Button(root, text="Generate Dungeon", command=getDungeon).pack()
canvas = Canvas(root, width=500, height=500)
canvas.pack()
img = ImageTk.PhotoImage(generateDungeon(3))
canvas.create_image(0,0, anchor=NW, image= img)

root.mainloop()