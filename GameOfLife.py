#!/usr/bin/env python

    # # # # # # # # # # # # # # # # # # # # # # #
    #                                           #
    #   Conway's Game of Life                   #
    #                                           #
    #   Simulation of a two-dimensional         #
    #   Cellular Automaton.                     #
    #   Several properties like window size     #
    #   and world variation can be changed      #
    #   in the config.txt file.                 #
    #                                           #
    #   For more information read the           #
    #   readme.txt!                             #
    #                                           #
    # # # # # # # # # # # # # # # # # # # # # # #


import pygame
import sys, os
from pygame.locals import *


class Cell() :

    def __init__(self, alive, row, column) :
        self.alive = alive
        self.pos = (row, column)

    def getNeighbors(self) :
        self.neighbors = 0
        for i in (-1, 0, 1) :
            for j in (-1, 0, 1) :
                if cell[(self.pos[0]+i)%height][(self.pos[1]+j)%width].alive and (not (i == 0 and j == 0)) :
                    self.neighbors += 1

    def updateLife(self, prop) :
        if (str(self.neighbors) in prop[1]) and (self.alive == False) :
            self.alive = True
        elif str(self.neighbors) not in prop[0] :
            self.alive = False
        return self.alive

    def edit(self) :
        self.alive = not self.alive
        if self.alive :
            pygame.draw.rect(window, color[1], (10*self.pos[1], 10*self.pos[0], 10, 10))
        else :
            pygame.draw.rect(window, color[0], (10*self.pos[1], 10*self.pos[0], 10, 10))


def load(config) :

    for line in config :
        pos = line.split()
        cell[int(pos[1])][int(pos[0])].edit()


def save(config) :

    config.truncate()
    for i in range(height) :
        for j in range(width) :
            if cell[i][j].alive :
                config.write(str(j) + " " + str(i) + "\n")


def nextCycle(prop) :

    window.fill(color[0])

    for i in range(height) :
        for j in range(width) :
            cell[i][j].getNeighbors()

    for i in range(height) :
        for j in range(width) :
            if cell[i][j].updateLife(prop) :
                pygame.draw.rect(window, color[1], (10*j, 10*i, 10, 10))


def main() :

    pygame.init()

    config = open(os.path.join("data", "config.txt"))

    global width
    global height
    width = int(config.readline()[6:])
    height = int(config.readline()[7:])
    
    r = int(config.readline()[4:])
    g = int(config.readline()[6:])
    b = int(config.readline()[5:])
    fps = int(config.readline()[14:])
    survival = config.readline()[15:].split()
    birth = config.readline()[12:].split()
    config.close()

    global color
    color = ((255, 255, 255), (r, g, b))
    
    fpsClock = pygame.time.Clock()

    world_properties = (survival, birth)

    global window
    window = pygame.display.set_mode((10*width, 10*height), 0, 32)
    pygame.display.set_caption("Game of Life")

    window.fill(color[0])
    
    global cell
    cell = [[Cell(False, j, i) for i in range(width)] for j in range(height)]

    run = True
    pause = True

    while run :

        if not pause :
            nextCycle(world_properties)
            pygame.draw.polygon(window, color[1], ((10*width/2-10, 10*height-20), (10*width/2-10, 10*height-40), (10*width/2+10, 10*height-30)))
        else :
            pygame.draw.rect(window, color[1], (10*width/2-12, 10*height-40, 10, 20))
            pygame.draw.rect(window, color[1], (10*width/2+2, 10*height-40, 10, 20))

        for event in pygame.event.get() :
            if event.type == QUIT :
                run = False
            elif event.type == KEYUP :
                if event.key == K_SPACE :
                    pause = not pause
                    pygame.draw.polygon(window, color[0], ((10*width/2-10, 10*height-20), (10*width/2-10, 10*height-40), (10*width/2+10, 10*height-30)))
                elif event.key == K_c :
                    pause = True
                    for i in range(height) :
                        for j in range(width) :
                            cell[i][j].alive = False
                    window.fill(color[0])
                elif event.key  == K_o :
                    savefile = open(os.path.join("data", "savefile.txt"))
                    load(savefile)
                    savefile.close()
                elif event.key  == K_s :
                    savefile = open(os.path.join("data", "savefile.txt"), "w")
                    save(savefile)
                    savefile.close()
            elif event.type == MOUSEBUTTONUP :
                m = pygame.mouse.get_pos()
                m = [m[0]//10, m[1]//10]
                cell[m[1]][m[0]].edit()

        if run :
            pygame.display.update()
            fpsClock.tick(fps)

    pygame.quit()
    sys.exit()


if __name__ == "__main__" :
    main()
