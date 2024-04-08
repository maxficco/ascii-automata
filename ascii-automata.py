import os
import time
import random

ascii_weight_index = ["█","█","█","█","█","█","█","█","█"]
class Cell:
    def __init__(self, x, y, isalive):
        self.x = x
        self.y = y
        self.isalive = isalive
        self.neighbors = 0

    def printcell(self, s):
        if self.isalive == True:
            if self.x == GRID_W-1:
                s += ascii_weight_index[self.neighbors] + "\n"
            else:
                s += ascii_weight_index[self.neighbors]
        else:
            if self.x == GRID_W-1:
                s += " " + "\n"
            else:
                s += " "
        return s
    def countneighbors(self, xindex, yindex):
        neighbors = 0
        try:
            if cells[yindex][xindex+1].isalive == True:
                neighbors += 1
        except IndexError:
            pass
        try:
            if cells[yindex-1][xindex+1].isalive == True and yindex != 0:
                neighbors += 1
        except IndexError:
            pass
        try:
            if cells[yindex-1][xindex].isalive == True and yindex != 0:
                neighbors += 1
        except IndexError:
            pass
        try:
            if cells[yindex-1][xindex-1].isalive == True and yindex != 0 and xindex != 0:
                neighbors += 1
        except IndexError:
            pass
        try:
            if cells[yindex][xindex-1].isalive == True and xindex != 0:
                neighbors += 1
        except IndexError:
            pass
        try:
            if cells[yindex+1][xindex-1].isalive == True and xindex != 0:
                neighbors += 1
        except IndexError:
            pass
        try:
            if cells[yindex+1][xindex].isalive == True:
                neighbors += 1
        except IndexError:
            pass
        try:
            if cells[yindex+1][xindex+1].isalive == True: 
                neighbors += 1
        except IndexError:
            pass
    
        return neighbors
    
    def dolife(self, neighbors, born, survive):
        if self.isalive == False:
            if str(neighbors) in born:
                self.isalive = True
        else:
            self.isalive = False
            if str(neighbors) in survive:
                self.isalive = True
        return self

os.system("clear")
GRID_W = os.get_terminal_size().columns
GRID_H = os.get_terminal_size().lines

printguide = False
while True:
    os.system("clear")
    print("""Enter the rule for the cellular automaton.

Use B/S notation, where the digits after B specify the counts of live neighbors necessary for a cell to be born in the next generation,
and the digits after S specify the counts of live neighbors necessary for a cell to survive to the next generation.
    
Enter "help" for examples.
""")
    if printguide:
        print("""
    B3/S23 [Life]
    John Conway's rule is by far the best known and most explored CA.

    B36/S23 [HighLife]
    Very similar to Conway's Life but with an interesting replicator.

    B3678/S34678 [Day & Night]
    Dead cells in a sea of live cells behave the same as live cells in a sea of dead cells.

    B35678/S5678 [Diamoeba]
    Creates diamond-shaped blobs with unpredictable behavior.

    B2/S [Seeds]
    Every living cell dies every generation, but most patterns still explode.

    B234/S [Serviettes or Persian Rug]
    A single 2x2 block turns into a set of Persian rugs.

    B345/S5 [LongLife]
    Oscillators with extremely long periods can occur quite naturally.

    B4678/S35678 [Anneal]
    Creates blobs that tend to reduce their edges' curvature

    B5678/S45678 [Vote]
    An automaton that generates stable blobs/"caves"
                """) 
    try:
        rule = input() 
        if rule.lower() == "help":
            printguide = True
            time.sleep(0.25)
            continue
        born, survive = rule.split("/")
        born = set(list(born))
        survive = set(list(survive))
        time.sleep(0.25)
        break
    except:
        print("Try again.")
        time.sleep(1)
        continue

cells = []
for y in range(GRID_H):
    row = []
    for x in range(GRID_W):
        row.append(Cell(x, y, False))
    cells.append(row)

while True:
    os.system("clear")
    old_s = ""
    
    for r in cells:
        for c in r:
            c.neighbors = c.countneighbors(r.index(c), cells.index(r))

    for r in cells:
        for c in r:
            old_s = c.printcell(old_s)
    print(old_s)
    print("Enter space separated (x y) coordinates")
    print("""
Commands:
- "go" - run program with current grid
- "random" - create a random grid
- "horizontal" - create horizonal lines
- "vertical" - create vertical lines
- "diagonal" - create diagonal lines
- "fill" - fill entire grid
- "clear" - clear grid
            """)
    inp = input()
    if inp.lower() == "go":
        break
    elif inp.lower() == "random":
        for r in cells:
            for c in r:
                c.isalive = random.choice([True, False])
        continue
    elif inp.lower() == "horizontal":
        for r in cells:
            for c in r:
                if c.y%2 == 1:
                    c.isalive = True
        continue
    elif inp.lower() == "vertical":
        for r in cells:
            for c in r:
                if c.x%2 == 1:
                    c.isalive = True
        continue
    elif inp.lower() == "diagonal":
        for r in cells:
            for c in r:
                if (c.x%2 == 0 and c.y%2 == 1) or (c.x%2 == 1 and c.y%2 == 0):
                    c.isalive = True
        continue
    elif inp.lower() == "fill":
        for r in cells:
            for c in r:
                c.isalive = True
        continue
    elif inp.lower() == "clear":
        for r in cells:
            for c in r:
                c.isalive = False
        continue
    try:
        newlife = list(inp.split())
        cells[int(newlife[1])][int(newlife[0])].isalive = True
    except:
        print("Try again.")
        time.sleep(1)


old_old_s = old_s
while True:
    s = ""
    for r in cells:
        for c in r:
            c.dolife(c.neighbors, born, survive)
    for r in cells:
        for c in r:
            c.neighbors = c.countneighbors(r.index(c), cells.index(r)) 
            s = c.printcell(s)
    
    os.system("clear")
    print(s)
    
    if old_s == s or old_old_s == s:
        break
    else:
        old_old_s = old_s
        old_s = s
    time.sleep(0.05)

