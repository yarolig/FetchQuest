'''Game main module.

Contains the entry point used by the run_game.py script.

Feel free to put all your game code here, or in other modules in this "gamelib"
package.
'''
import pygame
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


class Game:
    def __init__(self):
        self.text_textures = {}

    def drawText(self, position, textString, size=32):
        if (textString, size) in self.text_textures:
            tex, w, h = self.text_textures[(textString, size)]
        else:
            font=pygame.font.Font(None, size)
            textSurface=font.render(textString,True,(255,255,255,255),(0,0,0,255))
            textData=pygame.image.tostring(textSurface,"RGBA",True)
            w, h = textSurface.get_width(), textSurface.get_height()

            tex = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, tex)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA,
                         GL_UNSIGNED_BYTE, textData)

            self.text_textures[(textString, size)] = (tex, w, h)

        glBindTexture(GL_TEXTURE_2D, tex)

        vertex_array_vbo = OpenGL.arrays.vbo.VBO(numpy.array(
           [0,0, 0,0, 1,0,0,
            1,0, 1,0, 1,0,0,
            0,1, 0,1, 1,0,0,

            0,1, 0,1, 1,0,0,
            1,0, 1,0, 1,0,0,
            1,1, 1,1, 1,0,0,
           ], dtype='f'))

        x, y = position
        x = (x - 400.0) / 400.0
        y = (y - 300.0) / 300.0

        def gul(s):
            n = glGetUniformLocation(self.ui_shader, s)
            #print("gul({})={}".format(s,n))
            return n

        def gal(s):
            n = glGetAttribLocation(self.ui_shader, s)
            #print("gal({})={}".format(s,n))
            return n
        glUseProgram(self.ui_shader)
        vertex_array_vbo.bind()

        glUniform2f(glGetUniformLocation(self.ui_shader, 'u_pos'), x, y)
        glUniform2f(glGetUniformLocation(self.ui_shader, 'u_size'),
                    w / 400.0, h / 300.0)

        glUniform1i(gul('sampler'), 0)
        glEnableVertexAttribArray(gal('in_vert'))
        glEnableVertexAttribArray(gal('in_tex'))
        glEnableVertexAttribArray(gal('in_color'))

        glVertexAttribPointer(gal('in_vert'), 2, GL_FLOAT, False, 7*4, vertex_array_vbo)
        glVertexAttribPointer(gal('in_tex'),  2, GL_FLOAT, False, 7*4, vertex_array_vbo+2*4)
        glVertexAttribPointer(gal('in_color'), 3, GL_FLOAT, False, 7*4, vertex_array_vbo+4*4)
        glDrawArrays(GL_TRIANGLES, 0, 6)
        vertex_array_vbo.unbind()
        glUseProgram(0)

        #vertex_array.render(moderngl.TRIANGLES)

    def draw(self):
        glClearColor(0.3, 0.4, 0.5, 1.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        self.drawText((100, 400), "Please do not use ModernGL", 60)
        self.drawText((100, 100), "There is no documentation that is allowed to use.", 40)
        pygame.display.flip()

    def start(self):
        pygame.init()
        pygame.display.init()
        pygame.display.set_mode([800,600], pygame.OPENGL | pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.RESIZABLE)
        clock = pygame.time.Clock()

        print(data.load('ui.vert').read())
        self.ui_shader = shaders.compileProgram(
            shaders.compileShader(data.load_text('ui.vert'), GL_VERTEX_SHADER),
            shaders.compileShader(data.load_text('ui.frag'), GL_FRAGMENT_SHADER),
        )

        while True:
            clock.tick(59)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    return
                elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    return
                else:
                    print(e)
            self.draw()


def main():
    g = Game()
    g.start()
    print("Thank you for playing.")
