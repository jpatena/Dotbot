# Jaron Patena
# CSE 512
# dotbot0.py

# by Kerstin Voigt, Sept 2014; inspired by Nils Nilsson, Introduction to
# Artificial Intelligence: A New Synthesis


from graphics import *
import random

# global vars
WORLD_MAX_X = 500
WORLD_MAX_Y = 500
GRID = 20
WALL = {}

# a piece of wall (one square)

class Wall:
    def __init__(self):
        global WALL
        prompt = Text(Point(8*GRID, WORLD_MAX_Y - 2*GRID),\
                      "Click one square per click, twice for the last")
        prompt.draw(win)
        prompt_on = True

        click = win.getMouse()
        click1x = click.x - click.x % GRID
        click1y = click.y - click.y % GRID

        while True:
            if prompt_on:
                prompt_on = False
                prompt.undraw()

            WALL[(click1x,click1y)] = Rectangle(Point(click1x,click1y),\
                                                Point(click1x + GRID,\
                                                      click1y + GRID))
            WALL[(click1x,click1y)].setFill("black")
            WALL[(click1x,click1y)].draw(win)

            click = win.getMouse()
            click2x = click.x - click.x % GRID
            click2y = click.y - click.y % GRID

            if (click1x,click1y) == (click2x,click2y):
                break
    
            click1x = click2x
            click1y = click2y

    def draw(self):
        for loc in WALL.keys():
            WALL[loc].draw(win)

    def undraw(self):
        for loc in WALL.keys():
            WALL[loc].undraw()
            


# the dotbot robot ...   
class DotBot:
    def __init__(self,loc = Point(5*GRID,5*GRID), col="red", pwr = 100):
        self.location = loc
        self.color = col
        self.the_dotbot = Oval(self.location,\
                               Point(self.location.x + GRID, self.location.y + GRID))
        self.the_dotbot.setFill(self.color)
        self.power = pwr
                               
    def __str__(self):
        return "%s dotbot at (%d,%d) with power %d" % (self.color,\
                                             self.location.x,\
                                             self.location.y,self.power)

    def update_dotbot(self):
        self.the_dotbot.move(self.location.x - self.the_dotbot.p1.x,\
                             self.location.y - self.the_dotbot.p1.y)
        
    def draw(self):
        self.update_dotbot()
        self.the_dotbot.draw(win)

    def undraw(self):
        self.the_dotbot.undraw()

    def go(self,where):
        if where == 1:
            self.move_up()
        elif where == 2:
            self.move_down()
        elif where == 3:
            self.move_left()
        elif where == 4:
            self.move_right()
        else:
            pass
        self.undraw()
        self.draw()
            
    def move_up(self):
        newloc = Point(self.location.x, self.location.y - GRID)
        if self.location.y >= GRID:
            self.location = newloc
      
    def move_down(self):
        newloc = Point(self.location.x, self.location.y + GRID)
        if self.location.y <= WORLD_MAX_Y - GRID:
            self.location = newloc
            
    def move_left(self):
        newloc = Point(self.location.x - GRID, self.location.y)        
        if self.location.x >= GRID:
            self.location = newloc

    def move_right(self):
        newloc = Point(self.location.x + GRID, self.location.y)
        if self.location.x <= WORLD_MAX_X - GRID:
            self.location = newloc
    def whereisit(self):
        return (self.location.x, self.location.y)
    
    # returns true or false if walls are present
    def sensor(self, wall):
        x1 = 0
        x2 = 0
        x3 = 0
        x4 = 0

        s1 = (self.location.x - GRID, self.location.y - GRID)
        s2 = (self.location.x, self.location.y - GRID)
        s3 = (self.location.x + GRID, self.location.y - GRID)
        s4 = (self.location.x + GRID, self.location.y)
        s5 = (self.location.x + GRID, self.location.y + GRID)
        s6 = (self.location.x, self.location.y + GRID)
        s7 = (self.location.x - GRID, self.location.y + GRID)
        s8 = (self.location.x - GRID, self.location.y)

        if((s2 in WALL) or (s3 in WALL)):
            x1 = 1
        if((s4 in WALL) or (s5 in WALL)):
            x2 = 1
        if((s6 in WALL) or (s7 in WALL)):
            x3 = 1
        if((s8 in WALL) or (s1 in WALL)):
            x4 = 1

        if(x1 == 1 and x2 == 0):
            self.move_right()
            self.undraw()
            self.draw()
            return True
        if(x2 == 1 and x3 == 0):
            self.move_down()
            self.undraw()
            self.draw()
            return True
        if(x3 == 1 and x4 == 0):
            self.move_left()
            self.undraw()
            self.draw()
            return True
        if(x4 == 1 and x1 == 0):
            self.move_up()
            self.undraw()
            self.draw()
            return True

        return False

    
# this could be a main function but doesn't have to be ...
# these lines will be executed as part of loading this file ...

win = GraphWin("Dotbot World", WORLD_MAX_X, WORLD_MAX_Y)

for i in range(GRID,WORLD_MAX_Y,GRID):
    hline = Line(Point(0,i),Point(WORLD_MAX_X,i))
    hline.draw(win)
    vline = Line(Point(i,0),Point(i,WORLD_MAX_Y))
    vline.draw(win)

mybot = DotBot()
mybot.draw()

mywall = Wall()

start = Text(Point(8*GRID, WORLD_MAX_Y-2*GRID), "Click to start the action -- twice to stop")
start.draw(win)

click = win.getMouse()
clickx1 = click.x - click.x % GRID
clicky1 = click.y - click.y % GRID

print "click at %d,%d" % (clickx1, clicky1)

start.undraw()

while True:
    
    click = win.getMouse()
    clickx2 = click.x - click.x % GRID
    clicky2 = click.y - click.y % GRID

    print "click at %d,%d" % (clickx2, clicky2)

    if(clickx1 == clickx2 and clicky1 == clicky2):
        #clicked same square twice --> quit
        enough = Text(Point(clickx1, clicky1), "Enough of that!")
        enough.draw(win)
        break


    print "bot moved ..."

    clickx1 = clickx2
    clicky1 = clicky2

    # if wall present, follow it forever
    if(mybot.sensor(mywall) == True):
        pass
    
    # if no walls, continue to wander at random
    else:
        mybot.go(random.randint(1,4))

win.getMouse()
win.getMouse()
win.close()
    
