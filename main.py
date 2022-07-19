import pygame
import random

#CONSTANTS
windowWidth = 1000
windowHeight = 563
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (211, 211, 211)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIGHT_GREY = (105, 105, 105)

#PYGAME DECLARING REQUIREMENTS
pygame.init()
pygame.font.init()
window = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption('Minesweeper')

class Box:
  def __init__(self, xInList, yInList, x, y, width, height):
    self.xInList = xInList
    self.yInList = yInList
    self.x = x
    self.y = y
    self.isBomb = False
    self.width = width
    self.height = height
    self.defaultBoxColor = GREY
    self.hoverOver = False
    self.hoverOverBoxColor = LIGHT_GREY
    self.canIBeClicked = False
    self.outLineColor = BLACK
    self.safeBoxColor = GREEN
    self.bombBoxColor = RED
    self.numOfBombs = 0
    self.mineBoxColor = RED
    self.found = False
    self.textSize = 20
    self.arialFont = pygame.font.SysFont('arial', self.textSize)
    self.textColor = BLACK
    self.isItCheckedForSurroundingZeros = False
  
  def draw(self):
    if (self.found) and (self.isBomb):
      self.drawExposedMine()
    elif (self.found) and not (self.isBomb):
      self.drawNumberMine()
    else:
      self.drawHiddenMine()


  def drawHiddenMine(self):
    self.drawBox()
    self.drawOutLine()

  def drawExposedMine(self):
    self.drawBox()
    self.drawOutLine()
    # self.drawMine()

  def drawNumberMine(self):
    self.drawBox()
    self.drawOutLine()
    self.drawNumber()

  def drawNumber(self):
    number = str(self.numOfBombs)
    numberWidth = self.getNumberWidth(number)
    numberHeight = self.getNumberHeight(number)
    textRenderer = self.arialFont.render(number, False, self.textColor)
    window.blit(textRenderer, (self.x + (self.width // 2) - (numberWidth // 2), self.y + (self.height // 2) - (numberHeight // 2)))

  def getNumberWidth(self, number):
    textRenderer = self.arialFont.render(number, False, self.textColor)
    return textRenderer.get_width()

  def getNumberHeight(self, number):
    textRenderer = self.arialFont.render(number, False, self.textColor)
    return textRenderer.get_height()

  def drawOutLine(self):
    # TOP LINE
    pygame.draw.line(window, self.outLineColor, [self.x, self.y], [self.x + self.width, self.y])
    # RIGHT LINE
    pygame.draw.line(window, self.outLineColor, [self.x + self.width, self.y], [self.x + self.width, self.y + self.height])
    # BOTTOM LINE
    pygame.draw.line(window, self.outLineColor, [self.x + self.width, self.y + self.height], [self.x, self.y + self.height])
    # LEFT LINE
    pygame.draw.line(window, self.outLineColor, [self.x, self.y + self.height], [self.x, self.y])

  def drawBox(self):
    # MIDDLE BOX

    if (self.found) and (self.isBomb):
      color = self.mineBoxColor
    elif (self.found) and not (self.isBomb):
      color = self.safeBoxColor
    elif (self.hoverOver):
      color = self.hoverOverBoxColor
    else:
      color = self.defaultBoxColor
  
    pygame.draw.rect(window, (color), (self.x, self.y, self.width, self.height))

  def calculateNumOfBombs(self, listOfMines):
    numOfMines = 0
    # Check the mines in every direction from this line
    for i in range(-1, 2): 
      # print(f"{(self.xInList+i)=}")
      for j in range(-1, 2):
        # print(f"{(self.yInList+j)=}")
        # If there is no object in this index (because the bomb could be on the edge of map)
        # DONT CHECK ITSELF
        if not ((i == 0) and (j == 0)):
          # DONT CHECK OUTSIDE THE BOX (this is done because list[-1] goes to back of list instead of giving index error)
          if not (((self.xInList+i) == -1) or ((self.yInList+j) == -1)):
            try:
              if listOfMines[self.xInList + i][self.yInList + j].isBomb == True:
                # print("checking: ",i,", ",j, " BOMB FOUND")
                numOfMines += 1
            except IndexError as error:
              pass

    self.numOfBombs = numOfMines

  def gotClicked(self, listOfBoxes):
    self.found = True

  # def drawMine(self):
  #   pygame.draw.rect(window, (self.mineColor), (self.x + (self.width // 4), self.y + (self.height // 4), self.width - (2*(self.width // 4)), self.height - (2*(self.height // 4))))

class DrawingBoxes():

  def __init__(self, x, y, width, height, color):
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.color = color

  def draw(self):
    # print("drew")
    pygame.draw.rect(window, (self.color), (self.x, self.y, self.width, self.height))

class ClickingMine():
  def __init__(self, boxHoveredColor):
    self.boxHoveredColor = boxHoveredColor
    self.leftClickPressed = False
    self.mouseHoveredOver = False
    self.stayEnabledColor = GREEN

  def isLeftClickPressed(self):
    if pygame.mouse.get_pressed()[0] == True:
      return True
    if pygame.mouse.get_pressed()[0] == False:
      return False

  def isMouseHoveringOverMe(self):
    Mouse = pygame.mouse.get_pos()
    if (Mouse[0] > self.x) and (Mouse[0] < self.x + self.width):
      if (Mouse[1] > self.y) and (Mouse[1] < self.y + self.height):
        self.mouseHoveredOver = True
        return True
      else:
        self.mouseHoveredOver = False
        return False
    else:
      self.mouseHoveredOver = False
      return False

  def isMineClicked(self):
    if (self.leftClickIsAvailable == True and self.isLeftClickPressed() == True):
      self.leftClickPressed = True
      self.leftClickIsAvailable = False
      return True

    if (self.isMouseHoveringOverMe() == True and self.isLeftClickPressed() == False):
      self.leftClickIsAvailable = True
    else:
      self.leftClickIsAvailable = False

def createBoxes():
  topLeftX = 125
  topLeftY = 50
  sizeOfBoxX = 25
  sizeOfBoxY = 25
  numOfXBoxes = 10
  numOfYBoxes = 10
  listOfBoxes = []
  # MAKES THE ARRAY
  for y in range(0, numOfXBoxes):
    listOfBoxesX = []
    for x in range(0, numOfYBoxes):
      box = Box(y, x, topLeftX + (sizeOfBoxX * x), topLeftY + (sizeOfBoxY * y), sizeOfBoxX, sizeOfBoxY)
      listOfBoxesX.append(box)
    listOfBoxes.append(listOfBoxesX)
  # PUT BOMBS IN MINES
  setRandomBombs(listOfBoxes)
  setBoxesNumOfBombs(listOfBoxes)
  return listOfBoxes

def putBombsInBoxes(listOfBoxes):
  setRandomBombs(listOfBoxes)
  setBoxesNumOfBombs(listOfBoxes)

def drawBoxes(listOfBoxes):
  for list in listOfBoxes:
    for mine in list:
      mine.draw()

def setRandomBombs(listOfBoxes):
  numOfBombs = 10
  bombsPlaced = 0
  while bombsPlaced < numOfBombs:
    randX = random.randint(0, len(listOfBoxes[0]) -1)
    randY = random.randint(0, len(listOfBoxes) -1)
    # print(listOfBoxes[randX][randY])
    if listOfBoxes[randX][randY].isBomb == False:
      listOfBoxes[randX][randY].isBomb = True
      bombsPlaced +=1

def printListOfLines(listOfBoxes):
  print("      0    1    2    3    4    5    6    7    8    9")
  i = 0
  for list in listOfBoxes:
    textList = []
    for box in list:
      if box.isBomb == True:
        textList.append("X")
      else:
        textList.append("-")
    print(i, " ",textList)
    i += 1

def setBoxesNumOfBombs(listOfBoxes):
  for list in listOfBoxes:
    for box in list:
      box.calculateNumOfBombs(listOfBoxes)

def isMouseHoveringOverMe(box):
    Mouse = pygame.mouse.get_pos()
    if (Mouse[0] > box.x) and (Mouse[0] < box.x + box.width):
      if (Mouse[1] > box.y) and (Mouse[1] < box.y + box.height):
        box.hoverOver = True
      else:
        box.hoverOver = False
    else:
      box.hoverOver = False

def didMouseClickOnBox(box, listOfBoxes):
  if box.found == False:
    isMouseHoveringOverMe(box)
    if (box.canIBeClicked) and (isLeftClickPressed()):
      box.gotClicked(listOfBoxes)

    if (box.hoverOver == True and isLeftClickPressed() == False):
      box.canIBeClicked = True
    else:
      box.canIBeClicked = False

def exposeSurroundingEmptyMines(listOfBoxes, box):
  if box.numOfBombs == 0:
    for i in range(-1, 2): 
        for j in range(-1, 2):
          if not ((i == 0) and (j == 0)):
            if not (((box.xInList+i) == -1) or ((box.yInList+j) == -1)):
              try:
                listOfBoxes[box.xInList + i][box.yInList + j].gotClicked(listOfBoxes)
              except IndexError as error:
                pass

def isLeftClickPressed():
    if pygame.mouse.get_pressed()[0] == True:
      return True
    if pygame.mouse.get_pressed()[0] == False:
      return False

def howManyBoxesFound(listOfBoxes):
  numBoxes = 0
  for list in listOfBoxes:
    for box in list:
      if box.found == True:
        numBoxes += 1
  return numBoxes

def numOfBombs(listOfBoxes):
  numBombs = 0
  for list in listOfBoxes:
    for box in list:
      if box.isBomb == True:
        numBombs +=1
  return numBombs

def howManySafeBoxesRemaining(listOfBoxes):
  safeBoxesRemaining = 0
  # print("total Number Of Boxes:", totalNumberOfBoxesInList(listOfBoxes))
  try:
    safeBoxesRemaining = totalNumberOfBoxesInList(listOfBoxes) - (numOfBombs(listOfBoxes) + howManyBoxesFound(listOfBoxes))
  except TypeError as error:
    pass
  return safeBoxesRemaining

def totalNumberOfBoxesInList(listOfBoxes):
  numBoxes = 0
  for list in listOfBoxes:
    for box in list:
      numBoxes += 1
  return numBoxes

def textOnScreen(text, x, y, textColor, textSize):
  arialFont = pygame.font.SysFont('arial', textSize)
  textRenderer = arialFont.render(text, False, textColor)
  window.blit(textRenderer, (x, y))

backgroundColor = DrawingBoxes(0, 0, windowWidth, windowHeight, WHITE)

numOfBoxesGivenOnFirstClick = 10

listOfBoxes = createBoxes()

CoordsClicked = []

print(printListOfLines(listOfBoxes))

def running(listOfBoxes):
  run = True

  while run:
    for event in pygame.event.get():
      
      # QUITTING
      if event.type == pygame.QUIT:
        run = False
      # THE PROGRAM
      backgroundColor.draw()
      drawBoxes(listOfBoxes)
      textOnScreen("Boxes Left:", 10, 10, BLACK, 30)
      textOnScreen(str(howManySafeBoxesRemaining(listOfBoxes)), 170, 10, BLACK, 30)
      textOnScreen("Number of Bombs:", 250, 10, BLACK, 30)
      textOnScreen(str(numOfBombs(listOfBoxes)), 500, 10, BLACK, 30)
      



      for list in listOfBoxes:
        for box in list:
          didMouseClickOnBox(box, listOfBoxes)
          if (box.found == True) and (box.isItCheckedForSurroundingZeros == False):
            exposeSurroundingEmptyMines(listOfBoxes, box)
            box.isItCheckedForSurroundingZeros = True
          if (box.found == True) and not (box.yInList,box.xInList) in CoordsClicked:
            CoordsClicked.append((box.yInList,box.xInList))
          
          if (box.found == True) and (box.yInList,box.xInList) in CoordsClicked:
            if len(CoordsClicked) == 1:
              if (howManyBoxesFound(listOfBoxes) < numOfBoxesGivenOnFirstClick):
                listOfBoxes = createBoxes()
                printListOfLines(listOfBoxes)
                print("MADE A NEW listOfBoxes")
                

      #print(CoordsClicked)
      pygame.display.flip()


running(listOfBoxes)
