from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk, Image

from PerlinNoiseMap import generateNoiseMap
from Dungeon import generateDungeon

imgSize = 500,500
cells = 3

def getDungeon(): 
    try:
        cells = int(e.get())
    except:
        messagebox.showwarning("NaN", "Enter a number into the box!")
        return

    if(cells >= 2 and cells <= 15):
        map = generateDungeon(cells)
        img = ImageTk.PhotoImage(map.resize(imgSize))
        canvas.create_image(0,0, anchor=NW, image=img)
        canvas.image = img
    else: 
        messagebox.showinfo("Invalid Range", "Please enter a number between 2 and 15")

def getPerlinMap():
    map = generateNoiseMap()
    img = ImageTk.PhotoImage(map.resize(imgSize))
    canvas.create_image(0,0, anchor=NW, image=img)
    canvas.image = img

if __name__ == "__main__":
    root = Tk()
    root.title("Map Generator")
    root.resizable(False, False)

    notebook = ttk.Notebook(root)

    dungeonFrame = Frame(notebook, width=501, height=600)
    dungeonFrame.grid(row=0,column=0, sticky="N")

    perlinFrame = Frame(notebook, width=501, height=600)
    perlinFrame.grid(row=0,column=1, sticky="N")

    notebook.add(dungeonFrame, text="Dungeon")
    notebook.add(perlinFrame, text="Perlin Map")
    notebook.grid(row=0,column=0)
    
    Label(dungeonFrame, text="Dungeon Generator").grid(row=0,column=0)

    Label(dungeonFrame, text="Size of dungeon (2-15)").grid(row=1, column=0)
    e = Entry(dungeonFrame, width=10)
    e.insert(0, "3")
    e.grid(row=2,column=0)

    Button(dungeonFrame, text="Generate Dungeon", command=getDungeon).grid(row=3,column=0)

    Label(perlinFrame, text="Perlin Noise Map Generator").grid(row=0,column=0)

    Button(perlinFrame, text="Generate Map", command=getPerlinMap).grid(row=1,column=0)

    canvas = Canvas(root, width=500, height=500)
    canvas.grid(row=4,column=0)

    root.mainloop()