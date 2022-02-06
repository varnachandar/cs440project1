import tkinter as tk
import random # to generate a random no. for the index to block
import os
#from os.path import exists



f = open("grid.txt", "r")

window = tk.Tk()

canvas = tk.Canvas(window, bg='white', height=1000, width=1000) #using the 1000 1000 gives a height of 50 and width of 100 tbh idk why
canvas.pack(fill=tk.BOTH, expand=True)

coordinates = set()
place = 0

for line in f:
    if place == 1:
        endx, endy = line.split()
        endx = int(endx) *10
        endy = int(endy) * 10
        place = place+1
    elif place == 0:
        startx,starty = line.split()
        startx = int(startx) *10
        starty = int(starty) *10
        place = place+1
    else:
        x,y,b = line.split() 
        b = int(b)
        x = int(x)
        y = int(y)
        if (b == 1):
            coordinates.add((x*10,y*10))

        



for i in range (0,1000,10): # the for loop lets us make the squares with size 10 across the entire canvas
  for j in range(0,500,10): # also in a sense we have coordinates now but in increments of 10 instead of 1, can't do one by one bcs then you just end up with a big black block since it is rly just the outlines smushed together
        if (i,j) in coordinates: # this is the part that we will have to randomize
            #create rectangle has parameters x1,y1,x2,y2 where x1 y1 is the start coordinate and x2,y2 is the end coordinate
            #outline is the outline color and fill is the fill color
           canvas.create_rectangle(i, j, i+10, j+10, outline = 'black', fill='gray')
        else:
           canvas.create_rectangle(i, j, i+10, j+10, outline = 'black',fill = 'white')

canvas.create_oval(startx-2, starty-2, startx+2, starty+2, outline = 'black', fill='red') 
canvas.create_oval(endx-2, endy-2, endx+2, endy+2, outline = 'black', fill='red')

f.close()

window.mainloop()
