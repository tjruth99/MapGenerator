from tkinter import *
from PIL import ImageTk, Image

#from PerlinNoiseMap import generateNoiseMap
#from RandomWalk import randomWalk
from Dungeon import generateDungeon

imgSize = 500,500
cells = 3

def getDungeon(): 
    cells = int(e.get())
    if(cells >= 2 and cells <= 15):
        img = ImageTk.PhotoImage(generateDungeon(cells).resize(imgSize))
        canvas.create_image(0,0, anchor=NW, image=img)
        canvas.image = img

if __name__ == "__main__":
    root = Tk()

    f = Frame(root, width=501, height=600)
    f.grid(row=0,column=0, sticky="NW")
    f.grid_propagate(0)
    f.update()

    Label(f, text="Dungeon Generator").grid(row=0,column=0)
    Label(f, text="Size of dungeon (2-15)").grid(row=1, column=0)
    e = Entry(f, width=10)
    e.insert(0, "3")
    e.grid(row=2,column=0)
    Button(f, text="Generate Dungeon", command=getDungeon).grid(row=3,column=0)
    canvas = Canvas(f, width=500, height=500)
    canvas.grid(row=4,column=0)

    root.mainloop()