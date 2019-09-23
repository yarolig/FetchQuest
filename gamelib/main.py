'''Game main module.

Contains the entry point used by the run_game.py script.

Feel free to put all your game code here, or in other modules in this "gamelib"
package.
'''
import pygame
import pygame.time
import pygame.display
import os

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
import time

def dprint(x):
    s=''
    for i in dir(x):
        if i.startswith('_'):
            continue
        try:
            s+='{}:{} \n'.format(i, getattr(x,i))
        except:
            s+='{}:{} \n'.format(i, 'error')
    print(s)


class KeyNames:
    def __init__(self):
        self.names = {
            1 : 'M_LEFT',
            2 : 'M_CENTER',
            3 : 'M_RIGHT',
        }
        for k in dir(pygame):
            if k.startswith('K_'):
                n = getattr(pygame, k)
                self.names[n] = k
    def get(self, n):
        return self.names.get(n) or "{}".format(n)


class Game:
    def __init__(self):
        self.key_names = KeyNames()
        pass

    def on_key(self, key, is_down):
        print("key {} is {}".format(self.key_names.get(key), 'down' if is_down else 'up'))

    def on_move(self, pos):
        pass


class Shell:
    def __init__(self):
        self.text = TextDrawer()
        pygame.init()
        pygame.display.init()
        pygame.display.set_mode([800, 600],
                                pygame.OPENGL | pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()
        self.text.init()
        self.game = Game()
        # workaround for
        pygame.mixer.quit()

    def resize(self, w, h):
        glViewport(0, 0, w, h)

    def draw(self):
        glClearColor(0.3, 0.4, 0.5, 1.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        fps = self.clock.get_fps()
        s = "FPS: {:.1f}".format(fps)
        self.text.draw((700, 570), s, 30)

        glFinish()
        glFlush()
        pygame.display.flip()

    def start(self):

        while True:
            dt=self.clock.tick(45)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    return
                elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    return
                elif e.type == pygame.KEYDOWN:
                    self.game.on_key(e.key, is_down=True)
                elif e.type == pygame.KEYUP:
                    self.game.on_key(e.key, is_down=False)
                elif e.type == pygame.MOUSEMOTION:
                    self.game.on_move(e.rel)
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    self.game.on_key(e.button, is_down=True)
                elif e.type == pygame.MOUSEBUTTONUP:
                    self.game.on_key(e.button, is_down=False)

                #elif e.type == pygame.VIDEORESIZE:
                #    self.resize(e.w, e.h)
                else:
                    print(e)
            self.draw()

def main():
    g = Shell()
    g.start()
    print("Thank you for playing.")
