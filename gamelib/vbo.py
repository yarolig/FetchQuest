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

class Vbo:
    vbos = {}
    def __init__(self):
        self.vbo = 0
        self.count = 0

    @classmethod
    def get(cls, name='', data=None):
        if name in cls.vbos:
            return cls.vbos[name]
        assert data
        v = Vbo()
        v.vbo = OpenGL.arrays.vbo.VBO(numpy.array(data, dtype='f'))
        v.count = len(data) // 8
        if name:
            cls.vbos[name] = v
        return v
