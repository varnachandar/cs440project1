import tkinter as tk
import random # to generate a random no. for the index to block

window = tk.Tk()

canvas = tk.Canvas(window, bg='white', height=1000, width=1000) #using the 1000 1000 gives a height of 50 and width of 100 tbh idk why
canvas.pack(fill=tk.BOTH, expand=True)

x = random.randint(0,100)
x = x*10

y = random.randint(0,100)
y = y*10

#for some reason random doesn't always work, probably bcs j goes out of bounds

for i in range (0,1000,10): # the for loop lets us make the squares with size 10 across the entire canvas
  for j in range(0,1000,10): # also in a sense we have coordinates now but in increments of 10 instead of 1, can't do one by one bcs then you just end up with a big black block since it is rly just the outlines smushed together
        if i == x and j == y: # this is the part that we will have to randomize
            #create rectangle has parameters x1,y1,x2,y2 where x1 y1 is the start coordinate and x2,y2 is the end coordinate
            #outline is the outline color and fill is the fill color
           canvas.create_rectangle(i, j, i+10, j+10, outline = 'black', fill='gray')
        else:
           canvas.create_rectangle(i, j, i+10, j+10, outline = 'black',fill = 'white')

window.mainloop()
