from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk, Image
import time
import os

from Dungeon import generateDungeon
from PerlinNoiseMap import generateNoiseMap
from RandomWalk import generateRandomWalkMap

imgSize = 500,500
cells = 3
map = generateDungeon(cells)

def saveImage():
    t = time.localtime()
    cur_time = time.strftime("%Y-%d-%m-%H-%M-%S", t)

    file_name = os.getcwd() + "\\images\\" + cur_time + ".png"
    print(file_name)

    map.save(file_name, "PNG")
    pass

def getDungeon(): 
    try:
        cells = int(dungeonSize.get())
    except:
        messagebox.showwarning("NaN", "Enter a number into the box!")
        return

    if(cells >= 2 and cells <= 15):
        global map
        map = generateDungeon(cells)
        img = ImageTk.PhotoImage(map.resize(imgSize))
        canvas.create_image(0,0, anchor=NW, image=img)
        canvas.image = img
    else: 
        messagebox.showinfo("Invalid Range", "Please enter a number between 2 and 15")

def getPerlinMap():
    global map
    map = generateNoiseMap()
    img = ImageTk.PhotoImage(map.resize(imgSize))
    canvas.create_image(0,0, anchor=NW, image=img)
    canvas.image = img

def getRandomWalkMap():
    global map
    map = generateRandomWalkMap(250, 50000, 0, 0, 0, 2)
    img = ImageTk.PhotoImage(map.resize(imgSize))
    canvas.create_image(0,0, anchor=NW, image=img)
    canvas.image = img


if __name__ == "__main__":
    root = Tk()
    root.title("Map Generator")
    root.resizable(False, False)
    root.grid_columnconfigure(0, weight=1)

    notebook = ttk.Notebook(root, width=500)

    dungeonFrame = Frame(notebook)
    dungeonFrame.grid(row=0, column=0, sticky="N")
    dungeonFrame.columnconfigure(0, weight=1)

    perlinFrame = Frame(notebook)
    perlinFrame.grid(row=0, column=1, sticky="N")
    perlinFrame.columnconfigure(0, weight=1)

    walkFrame = Frame(notebook)
    walkFrame.grid(row=0, column=1, sticky="N")
    walkFrame.columnconfigure(0, weight=1)

    notebook.add(dungeonFrame, text="Dungeon")
    notebook.add(perlinFrame, text="Perlin Map")
    notebook.add(walkFrame, text="Random Walk")
    notebook.grid(row=0, column=0)
    
    Label(dungeonFrame, text="Dungeon Generator").grid(row=0,column=0)
    Label(dungeonFrame, text="Size of dungeon (2-15)").grid(row=1, column=0)
    dungeonSize = Entry(dungeonFrame, width=10)
    dungeonSize.insert(0, "3")
    dungeonSize.grid(row=2, column=0)
    Button(dungeonFrame, text="Generate Dungeon", command=getDungeon).grid(row=3,column=0)

    Label(perlinFrame, text="Perlin Noise Map Generator").grid(row=0,column=0)
    Button(perlinFrame, text="Generate Map", command=getPerlinMap).grid(row=1,column=0)

    Label(walkFrame, text="Random Walk Map Generator").grid(row=0,column=0)
    Button(walkFrame, text="Generate Map", command=getRandomWalkMap).grid(row=1,column=0)

    canvas = Canvas(root, width=500, height=500)
    canvas.grid(row=4, column=0)

    Button(root, text="Save Image", command=saveImage).grid(row = 5, column=0)

    root.mainloop()