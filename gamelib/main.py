'''Game main module.

Contains the entry point used by the run_game.py script.

Feel free to put all your game code here, or in other modules in this "gamelib"
package.
'''
import pygame
import os

import moderngl
import array

from . import data



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
            tex = self.ctx.texture((w, h), 4, textData)
            self.text_textures[(textString, size)] = (tex, w, h)
        tex.use()
        vertex_buffer = self.ctx.buffer(array.array('f',
           [0,0, 0,0, 1,0,0,
            1,0, 1,0, 1,0,0,
            0,1, 0,1, 1,0,0,

            0,1, 0,1, 1,0,0,
            1,0, 1,0, 1,0,0,
            1,1, 1,1, 1,0,0,
           ]).tobytes())

        vertex_array = self.ctx.simple_vertex_array(
            self.ui_shader, vertex_buffer,
            'in_vert', 'in_tex', 'in_color')

        x, y = position
        x = (x - 400.0) / 400.0
        y = (y - 300.0) / 300.0

        self.ui_shader['sampler'].value = 0
        self.ui_shader['u_pos'].value = (x, y)
        self.ui_shader['u_size'].value = (w / 400.0, h / 300.0)

        vertex_array.render(moderngl.TRIANGLES)

    def draw(self):
        self.ctx.clear()
        self.drawText((100, 400), "Please do not use ModernGL", 60)
        self.drawText((100, 100), "There is no documentation that is allowed to use.", 40)
        pygame.display.flip()

    def start(self):
        pygame.init()
        pygame.display.init()
        pygame.display.set_mode([800,600], pygame.OPENGL | pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.RESIZABLE)
        self.ctx = moderngl.create_context()
        dprint(self.ctx)
        clock = pygame.time.Clock()
        print(data.load('ui.vert').read())
        self.ui_shader = self.ctx.program(vertex_shader=data.load_text('ui.vert'),
                                          fragment_shader=data.load_text('ui.frag'))
        self.vertex_buffer = self.ctx.buffer(array.array('f',
        [0,0,0, 0,0, 1,0,0,
         1,0,0, 1,0, 1,0,0,
         0,1,0, 0,1, 1,0,0,]).tobytes())

        #self.vertex_array = self.ctx.simple_vertex_array(
        #    self.ui_shader, self.vertex_buffer,
        #    'in_vert', 'in_tex', 'in_color')

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
