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


def gul(shader, name):
    return glGetUniformLocation(shader, name)


def gal(shader, name):
    return glGetAttribLocation(shader, name)


class Shader:
    shaders = {}
    @classmethod
    def get(cls, name):
        if name in cls.shaders:
            return cls.shaders[name]
        s = shaders.compileProgram(
            shaders.compileShader(data.load_text(name + '.vert'), GL_VERTEX_SHADER),
            shaders.compileShader(data.load_text(name + '.frag'), GL_FRAGMENT_SHADER),
        )
        cls.shaders[name] = s
        return s

    @staticmethod
    def unset():
        glUseProgram(0)
