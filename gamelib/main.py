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
    def draw(self):
        self.ctx.clear()
        self.vertex_array.render(moderngl.TRIANGLES)
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
        [0,0,0, 1,0,0,
         1,0,0, 1,0,0,
         0,1,0, 1,0,0,]).tobytes())
        
        self.vertex_array = self.ctx.simple_vertex_array(self.ui_shader, self.vertex_buffer, 'in_vert', 'in_color')
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
