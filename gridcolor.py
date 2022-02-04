import tkinter as tk
import random # to generate a random no. for the index to block
import os
#from os.path import exists



f = open("grid.txt", "w")

window = tk.Tk()

canvas = tk.Canvas(window, bg='white', height=1000, width=1000) #using the 1000 1000 gives a height of 50 and width of 100 tbh idk why
canvas.pack(fill=tk.BOTH, expand=True)

coordinates = set() # set makes sure there are no doublesPap
while len(coordinates) < 500: # 500 is 10% of the grid coordinates
    x, y = random.randint(0, 100)*10, random.randint(0, 50)*10 # multiply by 10 bcs our index goes by 10
    coordinates.add((x,y))

b = 0

startx = random.randint(0,100)
starty = random.randint(0,50)

endx = random.randint(0,100)
endy = random.randint(0,50)

string = str(startx) + " " + str(starty) + "\n"
f.write(string)

string = str(endx) + " " + str(endy) + "\n"
f.write(string)

for i in range (0,1000,10): # the for loop lets us make the squares with size 10 across the entire canvas
  for j in range(0,500,10): # also in a sense we have coordinates now but in increments of 10 instead of 1, can't do one by one bcs then you just end up with a big black block since it is rly just the outlines smushed together
        if (i,j) in coordinates: # this is the part that we will have to randomize
            #create rectangle has parameters x1,y1,x2,y2 where x1 y1 is the start coordinate and x2,y2 is the end coordinate
            #outline is the outline color and fill is the fill color
           canvas.create_rectangle(i, j, i+10, j+10, outline = 'black', fill='gray')
           b = 1
        else:
           canvas.create_rectangle(i, j, i+10, j+10, outline = 'black',fill = 'white')
           b = 0
        x = int(i/10)
        y = int(j/10)
        xs = str(x + 1)
        ys = str(y + 1)
        bs = str(b)

        string = xs + " " + ys + " " + bs + "\n"
        
        f.write(string)

window.mainloop()
