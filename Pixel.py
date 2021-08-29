# A class containing info on a particular pixel on the screen at some given time
# Location, color, direction...
import GUI
from numba import jit, cuda
import pygame


class Pixel:

    # inits a matrix of all pixels, each pixel 10x10 real pixels (subject to change)
    # EDGES: Left, top: 0,0  --  bottom,right: 104, 192
    def __init__(self, screen, x, y):
        self.screenWidth, self.screenHeight = screen.get_size()
        self.screenWidth = self.screenWidth / 10
        self.screenHeight = self.screenHeight / 10
        self.x = x
        self.y = y
        self.screen = screen
        self.neighbors = []

    def setNeighbors(self, pixel, window):
        self.neighbors = self.getNeighbors(pixel, window)

    # RGB color
    def draw(self, color, x=0, y=0, pix=None):
        if pix is not None:
            pygame.draw.rect(self.screen, color, (pix.x * 10, pix.y * 10, 10, 10))
        else:
            pygame.draw.rect(self.screen, color, (x * 10, y * 10, 10, 10))

    # if pixel is touching the border, which border
    def isOnEdge(self, pixel):
        if pixel.x == 0 and pixel.y == 0: return "tlc"
        if pixel.x == 0 and pixel.y + 1 == self.screenHeight: return "blc"
        if pixel.x + 1 == self.screenWidth and pixel.y == 0: return "trc"
        if pixel.x + 1 == self.screenWidth and pixel.y + 1 == self.screenHeight: return "brc"
        if pixel.x == 0: return "left"
        if pixel.y == 0: return "top"
        if pixel.x + 1 == self.screenWidth: return "right"
        if pixel.y + 1 == self.screenHeight: return "bottom"
        return None

    # returns all neighboring pixels of any pixel in an image
    def getNeighbors(self, pixel, window):
        if self.isOnEdge(pixel) is None: return [window.pixAtLocation(pixel.x - 1, pixel.y - 1),
                                                 window.pixAtLocation(pixel.x - 1, pixel.y),
                                                 window.pixAtLocation(pixel.x - 1, pixel.y + 1),
                                                 window.pixAtLocation(pixel.x, pixel.y - 1),
                                                 window.pixAtLocation(pixel.x, pixel.y + 1),
                                                 window.pixAtLocation(pixel.x + 1, pixel.y - 1),
                                                 window.pixAtLocation(pixel.x + 1, pixel.y),
                                                 window.pixAtLocation(pixel.x + 1, pixel.y + 1)]

        if self.isOnEdge(pixel) == "left": return [window.pixAtLocation(pixel.x, pixel.y - 1),
                                                   window.pixAtLocation(pixel.x, pixel.y + 1),
                                                   window.pixAtLocation(pixel.x + 1, pixel.y - 1),
                                                   window.pixAtLocation(pixel.x + 1, pixel.y),
                                                   window.pixAtLocation(pixel.x + 1, pixel.y + 1)]

        if self.isOnEdge(pixel) == "right": return [window.pixAtLocation(pixel.x - 1, pixel.y - 1),
                                                    window.pixAtLocation(pixel.x - 1, pixel.y),
                                                    window.pixAtLocation(pixel.x - 1, pixel.y + 1),
                                                    window.pixAtLocation(pixel.x, pixel.y - 1),
                                                    window.pixAtLocation(pixel.x, pixel.y + 1)]

        if self.isOnEdge(pixel) == "top": return [window.pixAtLocation(pixel.x - 1, pixel.y + 1),
                                                  window.pixAtLocation(pixel.x - 1, pixel.y),
                                                  window.pixAtLocation(pixel.x, pixel.y + 1),
                                                  window.pixAtLocation(pixel.x + 1, pixel.y + 1),
                                                  window.pixAtLocation(pixel.x + 1, pixel.y)]

        if self.isOnEdge(pixel) == "bottom": return [window.pixAtLocation(pixel.x - 1, pixel.y),
                                                     window.pixAtLocation(pixel.x - 1, pixel.y - 1),
                                                     window.pixAtLocation(pixel.x, pixel.y - 1),
                                                     window.pixAtLocation(pixel.x + 1, pixel.y),
                                                     window.pixAtLocation(pixel.x + 1, pixel.y - 1)]

        if self.isOnEdge(pixel) == "tlc": return [window.pixAtLocation(pixel.x, pixel.y + 1),
                                                  window.pixAtLocation(pixel.x + 1, pixel.y),
                                                  window.pixAtLocation(pixel.x + 1, pixel.y + 1)]

        if self.isOnEdge(pixel) == "blc": return [window.pixAtLocation(pixel.x, pixel.y - 1),
                                                  window.pixAtLocation(pixel.x + 1, pixel.y),
                                                  window.pixAtLocation(pixel.x + 1, pixel.y - 1)]

        if self.isOnEdge(pixel) == "trc": return [window.pixAtLocation(pixel.x - 1, pixel.y),
                                                  window.pixAtLocation(pixel.x, pixel.y + 1),
                                                  window.pixAtLocation(pixel.x - 1, pixel.y + 1)]

        if self.isOnEdge(pixel) == "brc": return [window.pixAtLocation(pixel.x, pixel.y - 1),
                                                  window.pixAtLocation(pixel.x - 1, pixel.y),
                                                  window.pixAtLocation(pixel.x - 1, pixel.y - 1)]
