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
import glm





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

class Monster:
    pos = glm.vec3()
    vel = glm.vec3()
    dir = glm.vec3()
    yaw = 0
    pitch = 0
    hp = 100
    def __init__(self):
        self.inputs = {}
    def calc_dir(self):
        self.dir = glm.vec3(glm.cos(self.yaw) * glm.cos(self.pitch),
                 glm.sin(self.yaw) * glm.cos(self.pitch),
                 glm.sin(self.pitch))

class Game:
    def __init__(self, shell):
        self.key_names = KeyNames()
        self.shell = shell
        self.player = Monster()
        self.player.pos = glm.vec3(10,10,10)
        self.planet_shader = shaders.compileProgram(
            shaders.compileShader(data.load_text('planet.vert'), GL_VERTEX_SHADER),
            shaders.compileShader(data.load_text('planet.frag'), GL_FRAGMENT_SHADER),
        )

        arr = []
        parr = [arr]

        def addvert(i, j):
            vscale = 10.0
            nscale = 0.06
            noffset = 2019.0
            nhscale = 130.0
            z = glm.simplex(glm.vec3(noffset + nscale * i, noffset + nscale * j, 09.23))*nhscale
            print("n={}".format(z))

            parr[0] += [vscale * i,
                        vscale * j,
                        z,
                        0.2*i, 0.2*j,
                        1, 1, 1]

        for a in range(-32,32):
            for b in range(-32,32):
                addvert(a,b)
                addvert(a+1,b)
                addvert(a,b+1)

                addvert(a,b+1)
                addvert(a+1,b)
                addvert(a+1,b+1)


        #print(arr)
        self.planet_vbo = OpenGL.arrays.vbo.VBO(numpy.array(arr, dtype='f'))
        self.planet_vbo_count = len(arr) // 9
        pass


    def on_key(self, key, is_down):
        print("key {} is {}".format(self.key_names.get(key), 'down' if is_down else 'up'))
        self.player.inputs[key] = is_down

    def process_monster(self, m):
        assert isinstance(m, Monster)
        if m.inputs.get(pygame.K_w):
            m.pos += m.dir * 0.1
        if m.inputs.get(pygame.K_s):
            m.pos -= m.dir * 0.1
        if m.inputs.get(pygame.K_a):
            side = glm.cross(m.dir, glm.vec3(0,0,1))
            m.pos -= side * 0.1
        if m.inputs.get(pygame.K_d):
            side = glm.cross(m.dir, glm.vec3(0, 0, 1))
            m.pos += side * 0.1
    prev_pos = None
    def on_move(self, position):
        print(position)
        if self.prev_pos is None:
            self.prev_pos = glm.vec2(position)
        pos = glm.vec2(position)
        dpos = self.prev_pos - pos
        #print(dpos)
        self.player.yaw -= 0.01 * position[0]
        self.player.pitch -= 0.01 * position[1]
        if self.player.pitch < -1.2: self.player.pitch = -1.2
        if self.player.pitch > 1.2: self.player.pitch = 1.2
        self.prev_pos = pos
        self.player.calc_dir()

    def draw(self):
        self.process_monster(self.player)

        self.shell.texture.set(data.filepath('planet.jpg'))
        glUseProgram(self.planet_shader)

        def gul(s):
            return glGetUniformLocation(self.planet_shader, s)

        def gal(s):
            return glGetAttribLocation(self.planet_shader, s)

        def mat2list(m):
            return numpy.array([i
                    for v in m
                    for i in v
                    ], 'f')
        glUniformMatrix4fv(
            glGetUniformLocation(self.planet_shader, 'u_proj'),
            1, False,
            mat2list(glm.perspective(glm.radians(90), 4. / 3., 0.1, 1000.0)))

        glUniformMatrix4fv(
            glGetUniformLocation(self.planet_shader, 'u_view'),
            1, False,
            mat2list(glm.lookAt(
                self.player.pos,
                self.player.pos + self.player.dir,
                glm.vec3(0, 0, 1))))

        glUniform1i(gul('sampler'), 0)

        glEnableVertexAttribArray(gal('in_vert'))
        with self.planet_vbo:
            glVertexAttribPointer(gal('in_vert'), 3, GL_FLOAT, False, 8*4, self.planet_vbo)
            glDrawArrays(GL_TRIANGLES, 0, self.planet_vbo_count)
        glUseProgram(0)


class Shell:
    def __init__(self):
        self.text = TextDrawer()
        self.texture = Texture()
        pygame.init()
        pygame.display.init()
        pygame.display.set_mode([800, 600],
                                pygame.OPENGL    | pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()
        self.text.init()
        self.game = Game(self)
        # workaround for
        pygame.mixer.quit()

    def resize(self, w, h):
        glViewport(0, 0, w, h)

    def draw(self):
        glClearColor(0.3, 0.4, 0.5, 1.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glEnable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)
        fps = self.clock.get_fps()
        s = "FPS: {:.1f}".format(fps)
        self.text.draw((700, 570), s, 30)

        self.game.draw()
        glFinish()
        glFlush()
        pygame.display.flip()

    def start(self):

        while True:
            dt=self.clock.tick(60)

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
