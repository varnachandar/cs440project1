import tkinter as tk
from tkinter import messagebox
import math
from tkinter.ttk import*
from tkinter import*

# global variables
blocked = [] # 0 if unblocked, 1 if blocked
gval = [] # holds the g(n)
parent = [] # holds the parents of a vertex
fringe = [] # open list
closed = set() # closed list
makeButton = [] # holds the vertices that need buttons


# create the Tkinter window
window = tk.Tk()
canvas = tk.Canvas(window, bg='white', height=1700, width=1700) #using the 1000 1000 gives a height of 50 and width of 100 tbh idk why
canvas.pack(fill=tk.BOTH, expand=True)

# make the grid from a given file and extract the blocked/unblocked data and set up gval and parent to initiall be set to infinity and (0,0) respectively 
def makeGrid(filename):
    f = open(filename, "r")

    coordinates = set() # used to keep track of the blocked areas
    place = 0
    
    #read the file and extract the necessary parts
    for line in f:
        if place == 1:
            endx, endy = line.split()
            endx = int(endx)
            endy = int(endy)
            place = place+1
        elif place == 0:
            startx,starty = line.split()
            startx = int(startx)
            starty = int(starty)
            place = place+1
        elif place == 2:
            dim1, dim2 = line.split()
            place = place+1
        else:
            x,y,b = line.split() 
            b = int(b)
            x = int(x)
            y = int(y)
            if (b == 1):
                coordinates.add((x*17,y*17)) # this is for making the grid
            
            blocked.append(b) # getting the info abt blocked vs unblocked
            gval.append(float('inf')) # all the g vals are initialy infinity
            parent.append([0,0]) # all of the parents are just (0,0) initially
        

    # make a grid using what the file detailed, x goes from 1 to 100, y goes from 1 to 50, (1,1) is the top left corner   
    for i in range (17,1700,17): # the for loop makes the squares with size 10 across the entire canvas
        for j in range(17,850,17): # also in a sense we have coordinates now but in increments of 10 instead of 1, can't do one by one bcs then you just end up with a big black block since it is rly just the outlines smushed together
            if (i,j) in coordinates: # if the square is supposed to blocked it is filled gray, otherwise it is white
            #create rectangle has parameters x1,y1,x2,y2 where x1 y1 is the start coordinate and x2,y2 is the end coordinate
                canvas.create_rectangle(i, j, i+17, j+17, outline = 'black', fill='gray')
            else:
                canvas.create_rectangle(i, j, i+17, j+17, outline = 'black',fill = 'white')

    # use red circle for start and green for the end
    canvas.create_oval((startx*17)-7, (starty*17)-7, (startx*17)+7, (starty*17)+7, outline = 'black', fill='red') 
    canvas.create_oval((endx*17)-7, (endy*17)-7, (endx*17)+7, (endy*17)+7, outline = 'black', fill='green')

    f.close()
    return [startx,starty,endx,endy,blocked,gval,parent]

# general array method:
def findIndex (x,y): # gives the index for the arrays for gval,blocked and parent
    return ((x-1)*50) + y -1

# closed list method:
def cElementOf(x, y): # using closed set with the elements in the format (x,y)and want to know if a certain coordinate is already in the set, now runs in O(1) time where previously closed was a list and ran in O(n) time
    if (x,y) not in closed:
        return 0
    else:
        return 1

# fringe methods: elements of the array (priority queue) are in the format [x,y],val
def elementOf(x, y): # want to know if a certain coordinate is already in the fringe
    if (len(fringe) == 0):
        return 0

    for i in (0,len(fringe)-1):
        xval = fringe[i][0][0] 
        yval = fringe[i][0][1]
        if x == xval and y == yval:
            return 1 
    return 0

def remove(x,y): # want to remove a certain coordinate from the fringe
    if (len(fringe) == 0):
        return

    for i in (0,len(fringe)-1):
        xval = fringe[i][0][0]
        yval = fringe[i][0][1]
        if x == xval and y == yval:
            fringe.pop(i)
            return

def insert(x, y, val): # want to insert a certain coordinate and value into the fringe
    if(len(fringe) == 0): # if the array has ntg in it, just add it
        fringe.append([[x,y],val])
        return 

    for i in (0,len(fringe)-1): # if the array has values, to make it a priority queue, insert it a certain way
        value = fringe[i][1]
        if (val>value):
            fringe.insert(i,[[x,y],val]) # insert in a way that the first element will be largest -> go in decreasing order and the last is the smallest val (this gets popped first)
            return
    fringe.append([[x,y],val]) # if it gets through the for loop without adding, add to the end if it has the smallest val

# c function
def cfunc(a, b, c, d): # finds the distance btwn two points
    xd = c-a
    xd = math.pow(xd,2)
    yd = d-b
    yd = math.pow(yd,2)
    dist = math.sqrt(xd+yd)
    return dist

# finding successors 
def findSuccessor (x,y,blocked,successor): 
    if (x+1 < 101): # checking the right side
        if (y == 1): 
            if not(blocked[findIndex(x,y)] == 1): # making sure it isn't on the top edge and has a blocked square below
                successor.append([x+1,y])
        elif(y == 50):
            if not(blocked[findIndex(x,y-1)] == 1): # making sure it isn't on the bottom edge and has a blocked square above
                successor.append([x+1,y])
        elif not ((blocked[findIndex(x,y-1)] == 1) and (blocked[findIndex(x,y)]==1)): # making sure both above and below aren't blocked
                successor.append([x+1,y])

        if ((y-1 > 0) and (blocked[findIndex(x,y-1)] == 0)): # making sure it doesn't go diagonally up through a blocked square
            successor.append([x+1,y-1]) 

        if((y+1<51) and (blocked[findIndex(x,y)] == 0)): # making sure it doesn't go diagonally down through a blocked square
            successor.append([x+1,y+1])

    if (x-1 > 0): # checking the left side
        if y == 1:
            if not(blocked[findIndex(x-1,y)] == 1): # making sure it isn't on the top edge and has a blocked square below
                successor.append([x-1,y])
        elif y == 50:
            if not(blocked[findIndex(x-1,y-1)] == 1): # making sure it isn't on the bottom edge and has a blocked square above
                successor.append([x-1,y])
        elif not((blocked[findIndex(x-1,y)] == 1) and (blocked[findIndex(x-1,y-1)] == 1)): # making sure both above and below aren't blocked
            successor.append([x-1,y])
        
        if((y-1 > 0) and (blocked[findIndex(x-1,y-1)] == 0)): # making sure it doesn't go diagonally up through a blocked square
            successor.append([x-1,y-1]) 
        if((y+1 < 51) and (blocked[findIndex(x-1,y)] == 0)): # making sure it doesn't go diagonally down through a blocked square
            successor.append([x-1,y+1])

    if(y+1 < 51): # checking below
        if x==1:
            if not (blocked[findIndex(x,y)] == 1): # making sure it isn't on the left edge and has a blocked square to the right
                successor.append([x,y+1])
        elif x == 100:
            if not(blocked[findIndex(x-1,y)] == 1): # making sure it isn't on the right edge and has a blocked square to the left
                successor.append([x,y+1])
        elif not ((blocked[findIndex(x,y)] == 1) and (blocked[findIndex(x-1,y)] == 1)): # making sure both the left and right aren't blocked
            successor.append([x,y+1])

    if(y-1 > 0): # checking above
        if x == 1: 
            if not(blocked[findIndex(x,y-1)] == 1): # making sure it isn't on the left edge and has a blocked square to the right
                successor.append([x,y-1])
        elif x == 100:
            if not(blocked[findIndex(x-1,y-1)] == 1): # making sure it isn't on the right edge and has a blocked square to the left
                successor.append([x,y-1])
        elif not((blocked[findIndex(x,y-1)] == 1) and (blocked[findIndex(x-1,y-1)] == 1)): # making sure both the left and right aren't blocked
            successor.append([x,y-1])
    return successor

# finding the path used
def createPath(parent,startx,starty,endx,endy,path):
    index = findIndex(endx,endy)
    [px,py] = parent[index]
    path.append([endx,endy])
    counter = 0
    while counter != 2: 
        path.append(parent[index])
        index = findIndex(px,py)
        [px,py] = parent[index]
        if px == startx and py == starty:
            counter = counter+1   
    return path

# trace the path used for both A* and theta
def traceBack(path,startx,starty,endx,endy): # used to trace the path from the start vertex to the end vertex
    [px,py] = path.pop()
    while len(path)!= 0:
        [xi,yi] = path.pop()
        canvas.create_line(px*17,py*17,xi*17,yi*17, fill = 'blue', width = 2)
        px = xi
        py = yi
    
    # plot the start and end again so that it is above all of the shading - just for clarity purpose
    canvas.create_oval((startx*17)-7, (starty*17)-7, (startx*17)+7, (starty*17)+7, outline = 'black', fill='red') 
    canvas.create_oval((endx*17)-7, (endy*17)-7, (endx*17)+7, (endy*17)+7, outline = 'black', fill='green')

#Button Methods
# method for when it is clicked
def onClick(gval,i,j,endx,endy,A_t):
    index = findIndex(i,j)
    g = gval[index]
    if (A_t == 0):
        h = heuristic(i,j,endx,endy)
    else:
        h = thetaHeuristic(i,j,endx,endy)
    f = g+h
    tk.messagebox.showinfo("coordinate: ({x}, {y})".format(x = i, y = j), "g: {gval} \n h: {hval} \n  f: {fval}".format(gval = g, hval = h, fval = f))
# button formatting
def createbutton(i,j, gval,endx,endy,A_t,path):
    f = Frame(window, height = 8, width = 8, bg = 'orange')
    f.pack_propagate(0)
    f.place(x = i*17-4, y = j*17-4)

    if (path == 1):
        button = Button(f, width=8, height=8, command = lambda:onClick(gval,i,j,endx,endy,A_t) , compound="center", padx=0, pady=0, borderwidth = 1, bg = 'blue')

    else: 
        button = Button(f, width=8, height=8, command = lambda:onClick(gval,i,j,endx,endy,A_t) , compound="center", padx=0, pady=0, borderwidth = 1, bg = 'orange')
    
    button.pack(fill = BOTH, expand = 1)
# creating all the buttons
def buttons(makeButton,gval,A_t,endx,endy,path):
    while (len(makeButton) != 0):
        [x,y] = makeButton.pop()
        if [x,y] in path:
            createbutton(x,y,gval,endx,endy,A_t,1)
        else:
            createbutton(x,y,gval,endx,endy,A_t,0)
    while(len(fringe) != 0):
        [x,y],v = fringe.pop()
        if [x,y] in path:
            createbutton(x,y,gval,endx,endy,A_t,1)
        else:
            createbutton(x,y,gval,endx,endy,A_t,0)


# A* specific methods
# heuristic: 
def heuristic(x,y,endx,endy):
   a = math.sqrt(2)
   e = min(abs(x-endx), abs(y-endy))
   i = max(abs(x-endx), abs(y-endy))
   o = min(abs(x-endx), abs(y-endy))
   u = (a*e) + i - o
   return u

# update vertex:
def UpdateVertex(a,b, c, d, gval,endx,endy): 
    index_s = findIndex(a,b)
    index_sprime = findIndex(c,d)
    cval = cfunc(a,b,c,d)

    if gval[index_s] + cval < gval[index_sprime]:
        gval[index_sprime] = gval[index_s] +cval
        parent[index_sprime] = [a,b]
        if elementOf(c,d):
            remove(c,d)
        
        val = gval[index_sprime] + heuristic(c,d,endx,endy)
        insert(c, d, val)

# A*
def A_star(a,b,c,d,blocked,gval,parent):
    startx = a
    starty = b
    endx = c
    endy = d
    indexS = findIndex(startx,starty)
    gval[indexS] = 0
    parent[indexS] = [startx,starty]
    val = gval[indexS] +heuristic(startx,starty,endx,endy)
    insert(startx,starty,val)
   
    while len(fringe) != 0:
        [[x,y],v] = fringe.pop()
        makeButton.append([x,y])
        if x == endx and y == endy:
            print("path found")
            path = []
            path = createPath(parent,startx,starty,endx,endy,path)
            buttons(makeButton,gval,0,endx,endy,path)
            traceBack(path,startx,starty,endx,endy)
            return
            
        closed.add((x,y))
        
        successor = []
        successor = findSuccessor(x,y,blocked,successor) 
       
        while len(successor) != 0:
            [sx,sy] = successor.pop()
            if not cElementOf(sx, sy):
                if not elementOf(sx,sy):
                    si = findIndex(sx,sy)
                    gval[si] = float('inf')
                    parent[si] = None 
                UpdateVertex(x,y,sx,sy,gval,endx,endy)
        
    print("no path found")
    return 

# theta specific methods:
# heuristic 
def thetaHeuristic(x,y,endx,endy):
   cval = cfunc(x,y,endx,endy)
   return cval

def LineOfSight(a,b,c,d,blocked):
    x0 = a
    y0 = b
    x1 = c
    y1 = d
    f = 0
    dy = y1 - y0
    dx = x1-x0

    if dy<0:
        dy = -1*dy
        dod_y = -1 # direction of difference between y1 and y0
    else:
        dod_y = 1
    
    if dx <0:
        dx = -dx
        dod_x = -1 # direction of difference between x1 and x0
    else:
        dod_x = 1

     # sx = 1 return 0 else return -1
    if (dod_x == 1):
        s_x = 0
    else:   
        s_x = -1

    if (dod_y == 1):
        s_y = 0
    else:   
        s_y = -1
            
    if dx >= dy:
        while x0 != x1:
            f = f+dy
            if f >= dx:
                if blocked[findIndex(x0+ s_x, y0+s_y)] == 1:
                    return False
                y0 = y0 + dod_y
                f = f-dx
            if f != 0 and blocked[findIndex(x0+s_x, y0+s_y)] == 1:
                return False
            if dy == 0 and blocked[findIndex(x0+s_x, y0)] == 1 and gval[findIndex(x0+s_x, y0-1)] == 1:
                return False
            x0 = x0 + dod_x
    else:
        while y0 != y1:
            f = f+ dx
            if f >= dy:
                if blocked[findIndex(x0+s_x, y0+s_y)] == 1:
                    return False
                x0 = x0 + dod_x
                f = f-dy
            if f != 0 and blocked[findIndex(x0+s_x, y0+s_y)] == 1:
                return False
            if dy == 0 and blocked[findIndex(x0, y0+s_y)] == 1 and blocked[findIndex(x0-1, y0 +s_y)] == 1:
                return False
            y0 = y0 + dod_y
    return True

def thetaUpdateVertex(px,py,x,y,sx,sy,gval,parent,endx,endy,blocked): 
    index_p = findIndex(px,py)
    index_sprime = findIndex(sx,sy)
    cval = cfunc(px,py,sx,sy)
    index_s = findIndex(x,y)

    if LineOfSight(px,py,sx,sy,blocked):
        if((gval[index_p]+ cval) < gval[index_sprime]):
            gval[index_sprime] = gval[index_p]+ cval
            parent[index_sprime] = [px,py]
            if elementOf(sx,sy):
                remove(sx, sy)
            val = gval[index_sprime]+ thetaHeuristic(sx,sy,endx,endy)
            insert(sx, sy, val)
    else:
        cval = cfunc(x,y,sx,sy)
        if gval[index_s] + cval  < gval[index_sprime]:
            gval[index_sprime] = gval[index_s] + cval
            parent[index_sprime] = [x,y]
            if elementOf(sx,sy):
                remove(sx,sy)
            val = gval[index_sprime]+ thetaHeuristic(sx,sy,endx,endy)
            insert(sx,sy,val)

def theta(startx,starty,endx,endy,blocked,gval,parent):
    indexS = findIndex(startx,starty)
    gval[indexS] = 0
    parent[indexS] = [startx,starty]
    val = gval[indexS]+ thetaHeuristic(startx,starty,endx,endy)
    insert(startx,starty,val)

    while len(fringe) != 0:
        [[x,y],v] = fringe.pop()
        makeButton.append([x,y])
        if x == endx and y == endy:
            print("path found")
            path = []
            path = createPath(parent,startx,starty,endx,endy,path)
            buttons(makeButton,gval,1,endx,endy,path)
            traceBack(path,startx,starty,endx,endy)
            
            return 

        closed.add((x,y))

        successor = []
        successor = findSuccessor(x,y,blocked,successor)

        while len(successor) != 0:
            [sx,sy] = successor.pop()
            if (sx, sy) not in closed:
                if not elementOf(sx,sy):
                    si = findIndex(sx,sy)
                    gval[si] = float('inf')
                [px,py] = parent[findIndex(x,y)]
                thetaUpdateVertex(px,py,x,y,sx,sy,gval,parent,endx,endy,blocked)

    print("no path found")
    return 

# main method and keeping the window open:
def main():
    filename = input("Enter the file name in the format ___.txt: ")
    method = input("Enter A or Theta: ")
    [startx,starty,endx,endy,blocked,gval,parent] = makeGrid(filename)
    if (method == "A"):
        A_star(startx,starty,endx,endy,blocked,gval,parent)
    elif(method == "Theta"):
        theta(startx,starty,endx,endy,blocked,gval,parent)
    


if __name__ == "__main__":
    main()

window.mainloop()

    
    
