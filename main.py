import random
import pygame
import numpy

class Shape:
    def __init__(self, shapeType, x=25, y=25):
        self.shapeType = shapeType
        self.x = x
        self.y = y
        self.moving = True
        self.shape = numpy.array([], dtype='O')
        self.w = 1
        self.h = 1
        for i in shapeType:
            self.w = 1
            for z in i:
                if z == 1:
                    self.shape= numpy.append(self.shape, Block(self.x*self.w, self.y*self.h, (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))))
                self.w += 1
            self.h += 1
        del self.w
        del self.h
    def move(self, valueX=0, valueY=25):
        self.updateGameArray(0)
        if self.canMove(valueX, valueY):
            self.x+=25
            self.y+=25
            for i in self.shape:

                i.move(valueX, valueY)
        else:
            for block in self.shape:
                block.moving = False
        self.updateGameArray(1)

    def updateGameArray(self, value):
        for block in self.shape:
            block.updateGameArray(value)
    def draw(self):
        for i in self.shape:
            i.draw()
    def checkMoving(self):
        for block in self.shape:
            if block.moving == False:

                self.moving = False
                return False
        return True
    def moveHor(self, valueX, valueY):
        self.updateGameArray(0)
        if self.canMove(valueX, valueY):

            for block in self.shape:
                block.moveHor(valueX, valueY)
        self.updateGameArray(1)
    def canMove(self, valueX, valueY):
        for i in self.shape:
            if i.check(i.x+valueX,i.y+valueY) == False:
                return False
        return True
    def rotate(self):
        self.updateGameArray(0)
        self.centre = self.grabCentre()
        if self.checkRotate(self.centre):
            for block in self.shape:
                block.rotate(self.centre)
            self.draw()

        self.updateGameArray(1)
    def checkRotate(self, centre):
        for block in self.shape:
            tx = block.x
            ty = block.y
            tx -= centre[0]
            ty -= centre[1]
            tx, ty = (0-ty)+centre[0], tx + centre[1]
            if block.check(tx, ty) == False:
                return False
        return True

    def grabCentre(self):
        self.findLowest()
        return [self.xvalues[len(self.xvalues)//2], self.yvalues[len(self.yvalues)//2]]

    def findLowest(self):
        self.xvalues = []
        self.yvalues = []
        for block in self.shape:


            self.xvalues.append(block.x)
            self.yvalues.append(block.y)


        self.xvalues.sort()
        self.yvalues.sort(reverse=True)
    def clearLine(self, ind):
        self.updateGameArray(0)
        shapesl = list(self.shape)
        for i in shapesl:
            if i.y == ind*25:
                self.shape = self.shape[self.shape != i]

        self.draw()
        self.updateGameArray(1)
    def fall(self, y):
        for block in self.shape:
            if block.y < y:
                block.moving = True
                while block.moving:
                    block.updateGameArray(0)
                    block.move(0, 25)
                    block.updateGameArray(1)






class Block:
    def __init__(self, x, y, colour):
        self.x = x
        self.y = y
        self.moving = True
        self.colour = colour
        self.draw()

    def draw(self):

        pygame.draw.rect(screen, self.colour, pygame.Rect(self.x, self.y, 25, 25))
    def updateGameArray(self, value):
        gameArray[self.y//25][self.x//25] = value
    def check(self, fx, fy):

        if fx >= 0 and fx < screenWidth and fy >= 0 and fy < screenHeight:

            if gameArray[fy//25][fx//25] == 1:

                return False

            return True
        else:

            return False
    def move(self, valueX, valueY):
        if self.check(self.x+valueX,self.y+valueY):
            self.x+=valueX
            self.y += valueY
            self.draw()
        else:

            self.moving = False
    def moveHor(self, valueX, valueY):

        if self.check(self.x+valueX, self.y+valueY):
            self.x += valueX
            self.y += valueY
            self.draw()
    def rotate(self, centre):

        self.x -= centre[0]
        self.y -= centre[1]
        self.x, self.y = (0-self.y)+centre[0], self.x + centre[1]






def newActive():

    return Shapes[random.randint(0,4)]

def drawGrid():
    screen.fill(background)
    i = 1
    for x in range(0, int(screenHeight/25)):
        pygame.draw.line(screen, lineColour, (25*i, 0), (25*i,screenHeight))
        i+=1
    i = 1
    for x in range(0, int(screenHeight/25)):
        pygame.draw.line(screen, lineColour, (0, 25*i), (screenWidth, 25*i))
        i+=1
def drawFallen():
    for shape in fallenShapes:
        shape.draw()
def checkLine(ind: int) -> bool:
    if numpy.nonzero(gameArray[ind])[0].size == screenWidth//25:
        return True
    return False

def clearLine():
    for i in range(0, screenHeight//25):
        if checkLine(i):
            for shape in fallenShapes:
                shape.clearLine(i)
            for shape in fallenShapes:
                shape.fall(i*25)






pygame.init()

fps = 120
frameCount = 0
fpsClock = pygame.time.Clock()

screenWidth = 500
screenHeight = 800
background = (0, 0,0)
lineColour = (255, 255, 255)
screen = pygame.display.set_mode((screenWidth, screenHeight))
gameArray = numpy.zeros([screenHeight//25, screenWidth//25])
Shapes = numpy.array([[[1,1,1,1], [0,0,0,0]], [[0,1,1,0], [0,1,1,0]], [[0,0,0,1],[1,1,1,1]], [[1,1,0,0],[0,1,1,0]], [[0,1,1,1], [0,0,1,0]]])

ActiveShape = Shape(newActive())
fallenShapes = numpy.array([])

val = 40



run = True

while run:
    drawGrid()
    drawFallen()

    if frameCount == val:
        frameCount = 0
        ActiveShape.move()
    else:
        ActiveShape.draw()

    if ActiveShape.checkMoving() == False:

        fallenShapes = numpy.append(fallenShapes, ActiveShape)
        clearLine()
        ActiveShape = Shape(newActive())
        if frameCount > 5:
            val -= 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:

                ActiveShape.moveHor(-25, 0)
            elif event.key == pygame.K_RIGHT:

                ActiveShape.moveHor(25, 0)
            elif event.key == pygame.K_DOWN:
                ActiveShape.move(0, 50)
            elif event.key == pygame.K_UP:
                ActiveShape.rotate()


    pygame.display.update()
    fpsClock.tick(fps)
    frameCount += 1
