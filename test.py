from calendar import c
import math

def heuristic(x,y, endx, endy):
   #return 0
   a = math.sqrt(2)
   e = min(abs(x-endx), abs(y-endy))
   i = max(abs(x-endx), abs(y-endy))
   o = min(abs(x-endx), abs(y-endy))
   u = (a*e) + i - o
   
   return u


def main():
    
    for x in range(1, 6):
        for y in range(1, 5):
            print(x,y," ",heuristic(x,y,2,4),"+", heuristic(x,y,2,1))

    
    return 

if __name__ == "__main__":
    main()
