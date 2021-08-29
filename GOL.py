import Pixel
import numpy as np
import math

class GAME():
    def __init__(self):
        self.startActives = {}
        self.curActives = {}
        self.watchedCells = {}
        self.drawnCells = []
        self.numDrawn = 0
        self.iterations = 0
        self.deleting = False


    def updateRecentPix(self):
        return self.drawnCells.pop()

    def resetRecentPix(self):
        self.numDrawn = 0
        self.drawnCells = []

    def isLive(self, screen, cell, mode):
        if mode == 0:
            if screen.get_at((cell.x * 10, cell.y * 10))[:3] != (0, 0, 0) and screen.get_at((cell.x * 10, cell.y * 10))[:3] != (5, 5, 5):
                return True
            else:
                return False
        if mode == 1:
            if screen.get_at((cell.x * 10, cell.y * 10))[:3] != (17, 36, 15) and screen.get_at((cell.x * 10, cell.y * 10))[:3] != (36, 22, 15):
                return True
            else:
                return False


    def game(self, screen, cells, frozen, pos, window, mode):
        # IF GAME IS PAUSED: DRAW MODE
        if frozen and self.iterations != 0:
            print("Completed in ", self.iterations, " generations.")
            self.iterations = 0
        if frozen and pos != None and window != None:
            if window.getInitted():
                window.cleanSlate()
                window.unInit()
            pix = window.pixAtLocation(pos[0] // 10, pos[1] // 10)
            self.curActives[pix] = pix
            if pix not in self.drawnCells:
                self.drawnCells.append(pix)
                self.numDrawn +=1

            if mode==0:
                pix.draw(((pix.y/190)*125+(np.sin((pix.x/70))*125), abs(round((((pix.x)/200)*100))+(np.cos((pix.y/30))*100)), round(abs((np.cos((pix.x/70))*60)+(np.sin((pix.y/30))*190)))), pix=pix)
            if mode==1:
                pix.draw((232, 52, 26), pix=pix)

        # IF GAME IS UNPAUSED: EVOLVE MODE
        if not frozen and window != None:
            self.iterations+=1
            newLive = {}
            newDead = {}

            for cell in self.curActives:
                self.watchedCells[cell] = cell
                for neighbor in cell.getNeighbors(cell, window):
                    if not self.isLive(screen, neighbor, mode):
                        self.watchedCells[neighbor] = neighbor

            for cell in self.watchedCells:
                live = self.isLive(screen, cell, mode)
                neighbors = cell.getNeighbors(cell, window)
                localPop = 0
                for neighbor in neighbors:
                    if self.isLive(screen, neighbor, mode):
                        localPop += 1

                if live and (localPop < 2 or localPop > 3):
                    newDead[Pixel.Pixel(screen, cell.x, cell.y)] = Pixel.Pixel(screen, cell.x, cell.y)
                if live and ((localPop == 2) or (localPop == 3)):
                    newLive[Pixel.Pixel(screen, cell.x, cell.y)] = Pixel.Pixel(screen, cell.x, cell.y)
                if (not live) and localPop == 3:
                    newLive[Pixel.Pixel(screen, cell.x, cell.y)] = Pixel.Pixel(screen, cell.x, cell.y)

            self.watchedCells.clear()
            self.curActives.clear()

            for cell in newLive:
                localPopAgain = 0
                self.curActives[cell] = cell
                for neighbor in cell.getNeighbors(cell, window):
                    if self.isLive(screen, neighbor, mode):
                        localPopAgain +=1
                if mode ==0:
                    #cell.draw((220+(localPopAgain*3)+6, 255//(localPopAgain+1) , 90+localPopAgain*8), pix=cell)
                    cell.draw(((cell.y/190)*125+(np.sin((cell.x/70))*125), abs(round((((cell.x)/200)*100))+(np.cos((cell.y/30))*100)), round(abs((np.cos((cell.x/70))*60)+(np.sin((cell.y/30))*190)))),  pix=cell)
                if mode == 1:
                    cell.draw((220+(localPopAgain*3)+6, 20+localPopAgain*16 , 10+localPopAgain*8), pix=cell)

            for cell in newDead:
                if mode == 0:
                    cell.draw((0, 0, 0), pix=cell)
                if mode == 1:
                    cell.draw((36, 22, 15), pix=cell)
