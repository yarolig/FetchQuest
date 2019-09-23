
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



class Texture:
    textures = {}
    @classmethod
    def set(self, name):
        if name in self.textures:
            tex = self.textures[name]
        else:
            surface = pygame.image.load(name)
            data = pygame.image.tostring(surface, "RGBA", True)
            w, h = surface.get_width(), surface.get_height()

            tex = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, tex)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA,
                         GL_UNSIGNED_BYTE, data)
            self.textures[name] = tex
            glGenerateMipmap(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, tex)



class TextDrawer:
    def __init__(self):
        self.text_textures = {}

    def init(self):
        self.ui_shader = shaders.compileProgram(
            shaders.compileShader(data.load_text('ui.vert'), GL_VERTEX_SHADER),
            shaders.compileShader(data.load_text('ui.frag'),
                                  GL_FRAGMENT_SHADER),
        )
        self.vertex_array_vbo = OpenGL.arrays.vbo.VBO(numpy.array(
            [0, 0, 0, 0, 0, 0.1, 0,
             1, 0, 1, 0, 0, 0.2, 0,
             0, 1, 0, 1, 0, 0.2, 0,

             0, 1, 0, 1, 0, 0.2, 0,
             1, 0, 1, 0, 0, 0.2, 0,
             1, 1, 1, 1, 0, 0.3, 0,
             ], dtype='f'))

    def draw(self, pos, text, size):
        if (text, size) in self.text_textures:
            tex, w, h = self.text_textures[(text, size)]
        else:
            font=pygame.font.Font(None, size)
            textSurface=font.render(text,True,(255,255,255,255),(0,0,0,255))
            textData=pygame.image.tostring(textSurface,"RGBA",True)
            w, h = textSurface.get_width(), textSurface.get_height()

            tex = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, tex)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA,
                         GL_UNSIGNED_BYTE, textData)

            self.text_textures[(text, size)] = (tex, w, h)

        glBindTexture(GL_TEXTURE_2D, tex)


        x, y = pos
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
        self.vertex_array_vbo.bind()

        glUniform2f(glGetUniformLocation(self.ui_shader, 'u_pos'), x, y)
        glUniform2f(glGetUniformLocation(self.ui_shader, 'u_size'),
                    w / 400.0, h / 300.0)

        glUniform1i(gul('sampler'), 0)
        glEnableVertexAttribArray(gal('in_vert'))
        glEnableVertexAttribArray(gal('in_tex'))
        glEnableVertexAttribArray(gal('in_color'))

        glVertexAttribPointer(gal('in_vert'), 2, GL_FLOAT, False, 7*4, self.vertex_array_vbo)
        glVertexAttribPointer(gal('in_tex'),  2, GL_FLOAT, False, 7*4, self.vertex_array_vbo+2*4)
        glVertexAttribPointer(gal('in_color'), 3, GL_FLOAT, False, 7*4, self.vertex_array_vbo+4*4)
        glDrawArrays(GL_TRIANGLES, 0, 6)
        self.vertex_array_vbo.unbind()
        glUseProgram(0)


class CrosshairDrawer:
    def __init__(self):
        self.text_textures = {}

    def init(self):
        self.ui_shader = shaders.compileProgram(
            shaders.compileShader(data.load_text('ui.vert'), GL_VERTEX_SHADER),
            shaders.compileShader(data.load_text('ui.frag'),
                                  GL_FRAGMENT_SHADER),
        )
        self.vertex_array_vbo = OpenGL.arrays.vbo.VBO(numpy.array(
            [0, 0, 0, 0, 0, 0.1, 0,
             1, 0, 1, 0, 0, 0.2, 0,
             0, 1, 0, 1, 0, 0.2, 0,

             0, 1, 0, 1, 0, 0.2, 0,
             1, 0, 1, 0, 0, 0.2, 0,
             1, 1, 1, 1, 0, 0.3, 0,
             ], dtype='f'))

    def draw(self, size, name,aspect):
        Texture.set(name)
        def gul(s):
            n = glGetUniformLocation(self.ui_shader, s)
            #print("gul({})={}".format(s,n))
            return n

        def gal(s):
            n = glGetAttribLocation(self.ui_shader, s)
            #print("gal({})={}".format(s,n))
            return n
        glUseProgram(self.ui_shader)
        self.vertex_array_vbo.bind()
        glUniform2f(glGetUniformLocation(self.ui_shader, 'u_pos'), -0.05*aspect, -0.05)
        glUniform2f(glGetUniformLocation(self.ui_shader, 'u_size'), 0.10*aspect, 0.10)

        glUniform1i(gul('sampler'), 0)
        glEnableVertexAttribArray(gal('in_vert'))
        glEnableVertexAttribArray(gal('in_tex'))
        glEnableVertexAttribArray(gal('in_color'))

        glVertexAttribPointer(gal('in_vert'), 2, GL_FLOAT, False, 7*4, self.vertex_array_vbo)
        glVertexAttribPointer(gal('in_tex'),  2, GL_FLOAT, False, 7*4, self.vertex_array_vbo+2*4)
        glVertexAttribPointer(gal('in_color'), 3, GL_FLOAT, False, 7*4, self.vertex_array_vbo+4*4)
        glDrawArrays(GL_TRIANGLES, 0, 6)
        self.vertex_array_vbo.unbind()
        glUseProgram(0)
