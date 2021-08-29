import pygame
import Pixel
import GOL
import numpy as np
import tkinter as tk

sysInfo = tk.Tk()

class window:
    def __init__(self):
        #init display settings
        pygame.init()
        pygame.display.set_caption('Game Of Life')
        self.width = sysInfo.winfo_screenwidth()
        self.height = sysInfo.winfo_screenheight()
        self.screen = pygame.display.set_mode((self.width,self.height))
        self.frozen = True
        self.mode = 0
        self.maxColors = 1
        self.colors = [(5, 5, 5),(17, 36, 15)]
        self.curColor = self.colors[0]
        self.timeToReset = True

        #init pixel matrix
        self.pixels = {}
        self.textSlate()
        for pixel in self.pixels:
            self.pixels[pixel].setNeighbors(self.pixels[pixel], self)

        #init helper text

        self.game = GOL.GAME()


    #blank pixel setup - mode 1 for rainbow - mode 2 for green&orange
    def cleanSlate(self):
        for x in range(self.width//10):
            for y in range(self.height//10):
                cPix = Pixel.Pixel(self.screen,x,y)
                self.pixels[(x,y)]=cPix
                cPix.draw(self.curColor, x=x, y=y)
        self.initted = False


    # default pixel setup with helper text - mode 1 for black&pink - mode 2 for green&orange
    def textSlate(self):
        for x in range(self.width // 10):
            for y in range(self.height // 10):
                cPix = Pixel.Pixel(self.screen, x, y)
                self.pixels[(x, y)] = cPix
                cPix.draw(self.curColor, x=x, y=y)
        pygame.font.init()
        font = pygame.font.SysFont('sourcecodeproblack', 30)
        draw = font.render('Left Click: Draw', False, (255, 255, 255))
        delete = font.render('Backspace: Undo', False, (255, 255, 255))
        clear = font.render('C: Clear Screen', False, (255, 255, 255))
        start = font.render('Spacebar: Start/Pause Simulation', False, (255, 255, 255))
        color = font.render('Right Click: Change Color Preset', False, (255, 255, 255))
        pasteInfo = font.render('Paste (at cursor):', False, (255, 255, 255))
        paste1 = font.render('1: Glider', False, (255, 255, 255))
        paste2 = font.render('2: Glider Gun', False, (255, 255, 255))
        self.screen.blit(draw, (10, 10))
        self.screen.blit(delete, (10, 60))
        self.screen.blit(clear, (10, 110))
        self.screen.blit(start, (10, 160))
        self.screen.blit(color, (10, 220))
        self.screen.blit(pasteInfo, (self.width-400, 10))
        self.screen.blit(paste1, (self.width - 350, 60))
        self.screen.blit(paste2, (self.width - 350, 110))

        self.initted = True


    def modeActiveColor(self,cell):
        if self.mode ==0:
            return ((cell.y/190)*125+(np.sin((cell.x/70))*125), abs(round((((cell.x)/200)*100))+(np.cos((cell.y/30))*100)), round(abs((np.cos((cell.x/70))*60)+(np.sin((cell.y/30))*190))))

        if self.mode ==1:
            return (232, 52, 26)

    #returns pixel object at (x,y) on the screen
    def pixAtLocation(self,x,y):
        pixel = self.pixels[(x,y)]
        return pixel

    #Gets whether or not the screen has JUST been opened with nothing drawn yet. Used for knowing when to erase helper text.
    def getInitted(self):
        return self.initted

    #Indicate the screen has been modified since launch: no longer clear screen of text when a pixel is drawn (since no text exists)
    def unInit(self):
        self.initted = False

    #remove most recently drawn pixel (undo function -- history stored in GOL.game.drawnCells)
    def undrawLast(self):
        if self.game.numDrawn >0:
            self.game.numDrawn -=1
            pix = self.game.updateRecentPix()
            pix.draw(self.curColor, pix=pix)

    #return current keyboard/mouse input
    def getEvent(self):
        return pygame.event.get()

    #update screen graphics
    def update(self,pos=None, window=None):
        self.game.game(self.screen,self.pixels,self.frozen,pos,window, self.mode)
        pygame.display.flip()

    #Start/Pause animation and reset Undo backlog (can't undo once animation has altered screen)
    def freeze(self):
        self.game.resetRecentPix()
        self.frozen = not self.frozen

    #Change screen color mode by cycling through array of color settings
    def changeColor(self):
        if self.mode==self.maxColors:
            self.mode=0
        else:
            self.mode +=1
        self.curColor = self.colors[self.mode]
        self.textSlate()

    #paste glider
    def pasteGlider(self, pos):
        i = pos[0]
        j = pos[1]
        counter = 0
        arrange = "010" \
                  "001" \
                  "111"
        for y in range(3):
            for x in range(3):
                if(((i//10)+x)<=self.width//10 and ((j//10)+y)<=self.height//10 and arrange[counter]=="1"):
                    pix = self.pixAtLocation((i//10)+x,(j//10)+y)
                    pix.draw(((pix.y/190)*125+(np.sin((pix.x/70))*125), abs(round((((pix.x)/200)*100))+(np.cos((pix.y/30))*100)), round(abs((np.cos((pix.x/70))*60)+(np.sin((pix.y/30))*190)))), pix=pix)
                    self.game.curActives[pix]=pix
                    self.game.drawnCells.append(pix)
                counter+=1

    #paste glider gun
    def pasteGliderGun(self, pos):
        i = pos[0]
        j = pos[1]
        counter = 0
        arrange = "000000000000000000000000100000000000" \
                  "000000000000000000000010100000000000" \
                  "000000000000110000001100000000000011" \
                  "000000000001000100001100000000000011" \
                  "110000000010000010001100000000000000" \
                  "110000000010001011000010100000000000" \
                  "000000000010000010000000100000000000" \
                  "000000000001000100000000000000000000" \
                  "000000000000110000000000000000000000"
        for y in range(9):
            for x in range(36):
                if(((i//10)+x)<=self.width//10 and ((j//10)+y)<=self.height//10 and arrange[counter]=="1"):
                    pix = self.pixAtLocation((i//10)+x,(j//10)+y)
                    pix.draw(((pix.y/190)*125+(np.sin((pix.x/70))*125), abs(round((((pix.x)/200)*100))+(np.cos((pix.y/30))*100)), round(abs((np.cos((pix.x/70))*60)+(np.sin((pix.y/30))*190)))), pix=pix)
                    self.game.curActives[pix]=pix
                    self.game.drawnCells.append(pix)
                counter+=1