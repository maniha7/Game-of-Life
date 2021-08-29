import GUI
import pygame
import time
from Pixel import Pixel

window = GUI.window()
running = True
pushed = False
updateSpeed = .04
window.update(window=window)
tempResetState = []
resetState = []

while running:
    frameStart = time.perf_counter()
    for event in window.getEvent():
        #Close button control
        if event.type == pygame.QUIT:
            running = False


        if event.type == pygame.KEYDOWN:
            #PLAY/PAUSE CONTROL
            if event.key == pygame.K_SPACE:
                if window.frozen:
                    for cell in window.game.drawnCells:
                        resetState.append(cell)

                else:
                    window.timeToReset = True
                window.freeze()

            #SPEED CONTROLS
            if event.key == pygame.K_RIGHT and updateSpeed >.01:
                updateSpeed-=.01
            if event.key == pygame.K_LEFT and updateSpeed <.15:
                updateSpeed+=.01

            #EXIT CONTROL
            if event.key == pygame.K_ESCAPE:
                running = False

            #PASTE CONTROLS
            #Glider
            if event.key == pygame.K_1:
                pos = pygame.mouse.get_pos()
                if window.initted == True:
                    window.cleanSlate()
                window.pasteGlider(pos)
                window.update(window=window)
                if window.timeToReset:
                    resetState = []
                    for cell in tempResetState:
                        resetState.append(cell)
                    window.timeToReset = False


            #GliderGun
            if event.key == pygame.K_2:
                pos = pygame.mouse.get_pos()
                if window.initted == True:
                    window.cleanSlate()
                window.pasteGliderGun(pos)
                window.update(window=window)
                if window.timeToReset:
                    resetState = []
                    for cell in tempResetState:
                        resetState.append(cell)
                    window.timeToReset = False


            #DELETE CONTROLS
            if event.key == pygame.K_c and window.frozen:
                window.textSlate()
                tempResetState = []
                window.timeToReset = True
                window.update(window=window)
            if event.key == pygame.K_BACKSPACE and window.frozen:
                window.undrawLast()
                window.update(window=window)

            #RESET CONTROL
            if event.key == pygame.K_r and window.frozen:
                for cell in window.game.drawnCells:
                    resetState.append(cell)
                window.cleanSlate()
                for cell in resetState:
                    color = window.modeActiveColor(cell)
                    cell.draw(color, pix = cell)
                    window.game.curActives[cell]=cell
                    window.update(window=window)
                window.timeToReset = False

        #HELD LEFT CLICK MIRRORED CONTROLS (PLUS CONSTANT UPDATE FOR SMOOTH DRAWING LINES)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and window.frozen:
            if window.timeToReset:
                resetState = []
                for cell in tempResetState:
                    resetState.append(cell)
                window.timeToReset = False

            pushed = True
            while pushed:
                pos = pygame.mouse.get_pos()
                window.update(pos=pos, window=window)
                for event in window.getEvent():
                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        pushed = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False
                        if event.key == pygame.K_c:
                            window.textSlate()
                            tempResetState = []
                            window.update(window=window)
                        if event.key == pygame.K_SPACE:
                            pushed = False
                            if window.frozen:
                                for cell in window.game.drawnCells:
                                    resetState.append(cell)

                            else:
                                window.timeToReset = True
                            window.freeze()

        #CHANGE COLOR CONTROLS
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and window.frozen:
            window.changeColor()
            window.update(window=window)


    if not window.frozen:
        window.update(window=window)
        frameEnd = time.perf_counter()
        frameTime = frameEnd - frameStart
        if updateSpeed - frameTime > 0:
            time.sleep(updateSpeed-frameTime)
        frameFinal = time.perf_counter()
        frameFinalTime = frameFinal - frameStart
        tempResetState = window.game.curActives
        #print("FPS: ", updateSpeed)
        #print("Frame time ", frameFinalTime)

