import pygame
import pygame.time
import pygame.display
import pygame.event
import os
import math
import moderngl
import array
import numpy

from . import data
import OpenGL
import OpenGL.arrays
import OpenGL.arrays.vbo
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL import shaders
#from OpenGL.arrays import vbo
from .draw_text import *
from .cube import *
import time
import glm



class Terrain:
    def __init__(self, name):
        self.terrain_surface = pygame.image.load(data.filepath(name))
        self.w = self.terrain_surface.get_width()
        self.h = self.terrain_surface.get_height()
        self.cell_w = 10.0


    def getiz(self, x, y):
        ii = (int(x)) % self.terrain_surface.get_width()
        jj = (int(y)) % self.terrain_surface.get_height()
        z = self.terrain_surface.get_at((jj, ii))[0]
        return z

    def getz(self, world_x, world_y):
        x = world_x / self.cell_w
        y = world_y / self.cell_w

        ix = math.floor(x)
        dx = x - ix
        rx = 1.0 - dx

        iy = math.floor(y)
        dy = y - iy
        ry = 1.0 - dy

        z00 = self.getiz(ix,   iy)
        z10 = self.getiz(ix+1, iy)
        z01 = self.getiz(ix,   iy+1)
        z11 = self.getiz(ix+1, iy+1)
        #print("{}".format([z00,z10,z01,z11,' ',dx,dy,rx,ry, ' ', ix, iy]))
        return (z00 * rx * ry +
                z10 * dx * ry +
                z01 * rx * dy +
                z11 * dx * dy)

    def make_data(self):
        arr = []
        parr = [arr]
        def addvert(i, j):
            vscale = self.cell_w
            nscale = 0.06
            noffset = 2019.0
            nhscale = 0.130
            tscale = 10.9
            parr[0] += [vscale * i,
                        vscale * j,
                        self.getz(vscale * i, vscale * j),
                        tscale * i, tscale * j,
                        1, 1, 1]

        for a in range(-10, 69):
            for b in range(-10, 69):
                addvert(a, b)
                addvert(a + 1, b)
                addvert(a, b + 1)

                addvert(a, b + 1)
                addvert(a + 1, b)
                addvert(a + 1, b + 1)
        return arr