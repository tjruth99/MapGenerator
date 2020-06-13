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

    try:
        scale = int(perlinScale.get())
        octaves = int(perlinOctaves.get())
    except:
        messagebox.showwarning("NaN", "Enter a number into the box!")
        return

    if(scale >= 1 and scale <= 200 and octaves >= 1 and octaves <= 10):
        map = generateNoiseMap(scale, octaves)
        img = ImageTk.PhotoImage(map.resize(imgSize))
        canvas.create_image(0,0, anchor=NW, image=img)
        canvas.image = img
    else: 
        messagebox.showinfo("Invalid Range", "Invalid Range, enter a scale between 1-200 and a level of detail between 1 and 10")

def getRandomWalkMap():
    global map

    try:
        n = int(walkN.get())
        steps = int(walkSteps.get())
        ranges = int(walkRanges.get())
        rangeLength = int(walkRangeLength.get())
        brush = int(walkBrush.get())
    except:
        messagebox.showwarning("NaN", "Enter a number into the box!")
        return

    if validWalkInputs(n, steps, ranges, rangeLength, brush):
        map = generateRandomWalkMap(n, steps, ranges, rangeLength, 0, brush)
        img = ImageTk.PhotoImage(map.resize(imgSize))
        canvas.create_image(0,0, anchor=NW, image=img)
        canvas.image = img

def validWalkInputs(n, steps, ranges, rangeLength, brush):
    if n < 10 or n > 500:
        messagebox.showinfo("Invalid Range", "Invalid Range, enter a size between 10 and 500!")
        return False
    elif steps < 0:
        messagebox.showinfo("Invalid Range", "Invalid Range, number of steps must be a positive number!")
        return False
    elif steps > 1000000:
        messagebox.showinfo("Invalid Range", "Invalid Range, number of steps is too large")
        return False
    elif ranges < 0:
        messagebox.showinfo("Invalid Range", "Invalid Range, number of ranges must be a positive number!")
        return False
    elif rangeLength < 0:
        messagebox.showinfo("Invalid Range", "Invalid Range, range length must be a positive number!")
        return False
    elif brush < 1 or brush > 3:
        messagebox.showinfo("Invalid Range", "Invalid Range, enter a brush size between 1 and 3!")
        return False
    
    # If all inputs are valid, return true
    return True


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
    
    # Frame for Random Dungeon Map
    Label(dungeonFrame, text="Dungeon Generator").grid(row=0,column=0)
    Label(dungeonFrame, text="Size of dungeon (2-15)").grid(row=1, column=0)
    dungeonSize = Entry(dungeonFrame, width=10)
    dungeonSize.insert(0, "3")
    dungeonSize.grid(row=2, column=0)
    Button(dungeonFrame, text="Generate Dungeon", command=getDungeon).grid(row=3,column=0)


    # Frame for Perlin Noise Map
    Label(perlinFrame, text="Perlin Noise Map Generator").grid(row=0,column=0)

    Label(perlinFrame, text="Scale: (1-200)").grid(row=1, column=0)
    perlinScale = Entry(perlinFrame, width=10)
    perlinScale.insert(0, "100")
    perlinScale.grid(row=2, column=0)

    Label(perlinFrame, text="Level of detail: (0-10)").grid(row=3, column=0)
    perlinOctaves = Entry(perlinFrame, width=10)
    perlinOctaves.insert(0, "5")
    perlinOctaves.grid(row=4, column=0)

    Button(perlinFrame, text="Generate Map", command=getPerlinMap).grid(row=5,column=0)


    # Frame for Random Walk Map
    Label(walkFrame, text="Random Walk Map Generator").grid(row=0,column=0,columnspan=2)

    Label(walkFrame, text="Enter size: (10-500)").grid(row=1,column=0)
    walkN = Entry(walkFrame, width=10)
    walkN.insert(0, "250")
    walkN.grid(row=2,column=0)

    Label(walkFrame, text="Number of steps: (0-1,000,000)").grid(row=1,column=1)
    walkSteps = Entry(walkFrame, width=10)
    walkSteps.insert(0, "50000")
    walkSteps.grid(row=2,column=1)

    Label(walkFrame, text="Number of Mountain Ranges: ").grid(row=3,column=0)
    walkRanges = Entry(walkFrame, width=10)
    walkRanges.insert(0, "10")
    walkRanges.grid(row=4,column=0)

    Label(walkFrame, text="Max Length of Mountain Range: ").grid(row=3,column=1)
    walkRangeLength = Entry(walkFrame, width=10)
    walkRangeLength.insert(0, "100")
    walkRangeLength.grid(row=4,column=1)

    Label(walkFrame, text="Size of brush (1-3): ").grid(row=5,column=1,columnspan=2)
    walkBrush = Entry(walkFrame, width=10)
    walkBrush.insert(0, "2")
    walkBrush.grid(row=6,column=1)

    Button(walkFrame, text="Generate Map", command=getRandomWalkMap).grid(row=10,column=0,columnspan=2)


    canvas = Canvas(root, width=500, height=500)
    canvas.grid(row=4, column=0)

    Button(root, text="Save Image", command=saveImage).grid(row = 5, column=0)

    root.mainloop()