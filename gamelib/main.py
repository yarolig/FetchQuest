'''Game main module.

Contains the entry point used by the run_game.py script.

Feel free to put all your game code here, or in other modules in this "gamelib"
package.
'''
import pygame
import pygame.time
import pygame.display
import pygame.event
import os
import math
import moderngl
import array
import numpy

from gamelib.terrain import Terrain
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
from .vbo import *
from .myshader import *
from . import guns
from . import terrain
import random

import time
import glm
DPF = 0


def mat2list(m):
    return numpy.array([i
                        for v in m
                        for i in v
                        ], 'f')

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
    gun = None
    def __init__(self):
        self.inputs = {}
        self.guns = []
    def calc_dir(self):
        self.dir = glm.vec3(glm.cos(self.yaw) * glm.cos(self.pitch),
                 glm.sin(self.yaw) * glm.cos(self.pitch),
                 glm.sin(self.pitch))


class Ray:
    start = glm.vec3()
    end = glm.vec3()
    vel = glm.vec3()
    color = glm.vec3()
    ttl = 0 # frames
    size = 0.05

class Rays:
    def __init__(self):
        self.rays = []

    def process(self):
        for r in self.rays:
            r.start += r.vel
            r.end += r.vel

        for r in self.rays[:]:
            if r.ttl - 1 == 0:
                self.rays.remove(r)
            else:
                r.ttl -= 1

    def draw(self, game):
        Texture.set(data.filepath('fruit.png'))
        if not self.rays:
            return
        arr = []
        parr = [arr]

        def add_with_offset(r, off, c):
            s = r + off
            parr[0] += [s.x, s.y, s.z,
                        0, 0,
                        c.x, c.y, c.z]
        for r in self.rays:
            add_with_offset(r.start, glm.vec3(0,0,-r.size), r.color)
            add_with_offset(r.end, glm.vec3(0,0,-r.size), r.color)
            add_with_offset(r.end, glm.vec3(0,0,r.size), r.color)

            add_with_offset(r.start, glm.vec3(0, 0, -r.size), r.color)
            add_with_offset(r.start, glm.vec3(0, 0, r.size), r.color)
            add_with_offset(r.end, glm.vec3(0, 0, r.size), r.color)

            add_with_offset(r.start, glm.vec3(0, -r.size, 0), r.color)
            add_with_offset(r.end, glm.vec3(0, -r.size, 0), r.color)
            add_with_offset(r.end, glm.vec3(0, r.size, 0), r.color)

            add_with_offset(r.start, glm.vec3(0, -r.size, 0), r.color)
            add_with_offset(r.start, glm.vec3(0, r.size, 0), r.color)
            add_with_offset(r.end, glm.vec3(0, r.size, 0), r.color)

        vb = Vbo.get(data=arr)

        glUniformMatrix4fv(
            glGetUniformLocation(game.planet_shader, 'u_proj'),
            1, False,
            mat2list(glm.perspective(glm.radians(game.fov),
                                     game.aspect,
                                     0.1,
                                     1000.0)))

        glUniformMatrix4fv(
            glGetUniformLocation(game.planet_shader, 'u_view'),
            1, False,
            mat2list(glm.lookAt(
                game.player.pos,
                game.player.pos + game.player.dir,
                glm.vec3(0, 0, 1))))

        glUniform1i(gul(game.planet_shader, 'sampler'), 0)
        glEnableVertexAttribArray(gal(game.planet_shader, 'in_vert'))
        with vb.vbo:
            glVertexAttribPointer(gal(game.planet_shader, 'in_vert'), 3, GL_FLOAT, False, 8*4, vb.vbo)
            glDrawArrays(GL_TRIANGLES, 0, vb.count)
            global DPF
            DPF += 1
        vb.vbo.delete()

class Model:
    models = {}
    name = ''
    texture_name = ''
    shader_name = ''
    data_name = ''


class Box:
    ix = 0
    iy = 0
    iz = 0
    # air, floor, crate, wall, stairup, stairdown==air, floor+enemy, floor+player
    t = ''
    zscale = 1.0
    xyscale = 1.0
    texture = 'road.png'

    def __init__(self):
        pass

    def draw(self, game,tower):
        def gal(s):
            return glGetAttribLocation(game.planet_shader, s)
        game.shell.texture.set(data.filepath(self.texture))


        mview = glm.lookAt(
                    game.player.pos,
                    game.player.pos + game.player.dir,
                    glm.vec3(0, 0, 1))
        mpos = glm.translate(mview,
                             glm.vec3(tower.pos.x+self.xyscale*self.ix,
                                      tower.pos.y+self.xyscale*self.iy,
                                      tower.pos.z+tower.hceil*self.iz))
        mscl = glm.scale(mpos, glm.vec3(self.xyscale, self.xyscale, self.zscale))

        #mfixbox1 = glm.translate(mscl, glm.vec3(1, 1, 0))
        #mfixbox2 = glm.scale(mfixbox1, glm.vec3(0.5, 0.5, 1))

        glUniformMatrix4fv(
            glGetUniformLocation(game.planet_shader, 'u_view'),
            1, False,
            mat2list(mscl))
        glDrawArrays(GL_TRIANGLES, 0, game.vbo_cube.count)
        global DPF
        DPF += 1

tower1 = '''
--------
XX.#....
XX......
XXX..X..
X^...XX.
X^....X.
XXXX..X@
XXXX....
XX.@....
--------
.../////
.../////
.../////
.v//////
.v//////
..////^^
........
.XX.....
--------
........
.X......
.X..//..
.XX.//..
@@X.//vv
..@.XXXX
....XXXX
'''


def yxrange(h, w):
    for y in range(h):
        for x in range(w):
            yield y, x

class Tower:
    def __init__(self):
        self.boxes = []
        self.w = 8
        self.h = 8
        self.hceil = 4.0
        self.pos = glm.vec3(0,0,100)
        for c in range(3):
            for b, a in yxrange(self.h, self.w):
                box = Box()
                box.ix = a
                box.iy = b
                box.iz = c
                if b in (0,7):
                    box.zscale = self.hceil
                else:
                    box.zscale = 0.1 if 1 < a < 7 else 1
                self.boxes.append(box)

    def draw(self, game):
        with game.vbo_cube.vbo:
            glVertexAttribPointer(0, 3, GL_FLOAT, False, 8 * 4,
                                  game.vbo_cube.vbo)
            for i in self.boxes:
                i.draw(game, self)


class Game:
    def __init__(self, shell):
        self.key_names = KeyNames()
        self.shell = shell
        self.aim = False
        self.player = Monster()
        self.player.guns.append(guns.Pistol())
        self.player.guns.append(guns.Shotgun())
        self.player.guns.append(guns.SMG())
        self.player.guns.append(guns.Rifle())
        self.player.guns.append(guns.SniperRifle())
        self.player.guns.append(guns.MachineGun())
        self.player.gun = self.player.guns[0]


        self.fov = 90
        self.tgt_fov = 90
        self.aspect = 4.0/3.0
        self.player.pos = glm.vec3(300,80,130)
        self.planet_shader = shaders.compileProgram(
            shaders.compileShader(data.load_text('planet.vert'), GL_VERTEX_SHADER),
            shaders.compileShader(data.load_text('planet.frag'), GL_FRAGMENT_SHADER),
        )
        self.towers = []
        t = Tower()
        t.pos = glm.vec3(300, 80, 100)
        self.towers.append(t)
        self.terrain = terrain.Terrain('terrain.png')
        self.vbo_planet = Vbo.get('planet', self.terrain.make_data())
        self.vbo_cube = Vbo.get('cube', make_cube())
        self.rays = Rays()
        r = Ray()
        r.start = glm.vec3(0, 0, 0)
        r.end = glm.vec3(100, 100, 100)
        self.rays.rays.append(r)

        r = Ray()
        r.start = glm.vec3(300, 80, 108)
        r.end = glm.vec3(400, 80, 108)
        self.rays.rays.append(r)


    def on_key(self, key, is_down):
        print("key {} is {}".format(self.key_names.get(key), 'down' if is_down else 'up'))
        self.player.inputs[key] = is_down
        if key == 3:
            self.aim = is_down
            if self.aim:
                self.tgt_fov = 5
            else:
                self.tgt_fov = 90


    def fire_weapon(self, m, g):
        if g.charges < 1.0:
            return  False

        if g.temperature >= g.fail_temperature:
            return False

        # create rays
        for i in range(g.rays_per_shot):
            r = Ray()
            up = glm.vec3(0, 0, 1)
            side = glm.normalize(glm.cross(m.dir, glm.vec3(0, 0, 1)))

            identity = glm.identity(glm.mat4)

            xspread = random.randint(-100, 100) + random.randint(-100, 100)
            yspread = random.randint(-100, 100) + random.randint(-100, 100)

            xspread = (0.01 * xspread) * g.spreadx + g.offsetx
            yspread = (0.01 * yspread) * g.spready + g.offsety

            spreaded_dir = (
                glm.rotate(identity, glm.radians(xspread), up) * glm.vec4(
                m.dir, 0.0)).xyz
            spreaded_dir = (
                glm.rotate(identity, glm.radians(yspread), side) * glm.vec4(
                spreaded_dir, 0.0)).xyz

            gun_offset = 0.1
            r.start = m.pos + spreaded_dir * 0.5 + glm.vec3(0, 0,
                                                             -gun_offset) + side * gun_offset
            r.end = m.pos + spreaded_dir * 300 + glm.vec3(0, 0, 0)

            r.vel = spreaded_dir * 0.3
            r.ttl = 30
            self.rays.rays.append(r)
            print('{}'.format(r.start))
        # add spread, temp and decrease charges
        g.spreadx += g.spreadx_per_shot
        g.spready += g.spready_per_shot

        g.offsetx += g.offsetx_per_shot
        g.offsety += g.offsety_per_shot

        g.charges -= 1.0
        g.temperature += g.dt_per_shot
        return True

    def process_weapon(self, m):
        if not m.gun:
            return
        assert  isinstance(m.gun, guns.Gun)
        g = m.gun
        '''
    # state:
    charges = 10.0
    spread = 1.0
    offsetx = 0.0
    offsety = 0.0
    temperature = 0.0
    state_shot = 0  # no of frame when shooting initiated
    state_reload = 0  # no of frame when reloading initiated
'''
        initiate_fire = False
        if m.inputs.get(1):
            if g.state_reload:
                pass
            elif g.state_shot:
                if g.state_shot == g.auto_shot_time:
                    initiate_fire = True
            else:
                initiate_fire = True

        if initiate_fire:
            g.state_shot = 1

        # decay spread, temp
        g.spreadx = g.spreadx * g.spread_decay + g.normal_spread * (1.0 - g.spread_decay)
        g.spready = g.spready * g.spread_decay + g.normal_spread * (1.0 - g.spread_decay)

        g.offsetx = g.offsetx * g.spread_decay
        g.offsety = g.offsety * g.spread_decay

        g.temperature *= g.temperature_decay

        if g.state_shot == g.preshot_time:
            if not self.fire_weapon(m, g):
                g.state_shot = 0

        elif g.state_shot >= g.shot_time:
            g.state_shot = 0
        if g.state_shot: g.state_shot += 1
        if g.state_reload: g.state_reload += 1

    def process_monster(self, m):
        assert isinstance(m, Monster)
        mvel = 0.1
        if m.inputs.get(pygame.K_w):
            m.pos += m.dir * mvel

        if m.inputs.get(pygame.K_s):
            m.pos -= m.dir * mvel

        if m.inputs.get(pygame.K_a):
            side = glm.normalize(glm.cross(m.dir, glm.vec3(0,0,1)))
            m.pos -= side * mvel

        if m.inputs.get(pygame.K_d):
            side = glm.normalize(glm.cross(m.dir, glm.vec3(0, 0, 1)))
            m.pos += side * mvel

        if m.inputs.get(pygame.K_SPACE):
            m.pos.z += mvel

        if m.inputs.get(pygame.K_c):
            m.pos.z -= mvel

        for i in range(1,9):
            if m.inputs.get(pygame.K_1 - 1 + i):
                if i-1 < len(m.guns):
                    m.gun = m.guns[i-1]

        self.process_weapon(m)
        zr = 0.5
        terrainz = max([self.terrain.getz(m.pos.x, m.pos.y),
                        self.terrain.getz(m.pos.x+zr, m.pos.y),
                        self.terrain.getz(m.pos.x-zr, m.pos.y),
                        self.terrain.getz(m.pos.x, m.pos.y+zr),
                        self.terrain.getz(m.pos.x, m.pos.y-zr)])
        #m.pos.z = terrainz + 1.7
        #print('{:.2f} {:.2f}'.format(terrainz, self.terrain.getz(m.pos.x, m.pos.y)))

        if m.pos.z > terrainz + 1.7:
            # in air
            m.vel.z -= 0.01
        elif m.pos.z > terrainz - 1.7:
            # hit ground
            desiredz = terrainz + 1.7
            delta = desiredz - m.pos.z
            m.pos.z = m.pos.z * 0.7 + desiredz * 0.3
            if m.vel.z < 0:
                m.vel.z = 0
        else:
            pass

        m.pos += m.vel
        m.vel *= 0.99


    prev_pos = None
    def on_move(self, position):
        #print(position)
        if self.prev_pos is None:
            self.prev_pos = glm.vec2(position)
        pos = glm.vec2(position)
        dpos = self.prev_pos - pos
        #print(dpos)

        sens = 0.0001 * self.fov
        #if self.aim:
        #    sens = 0.001
        self.player.yaw -= sens * position[0]
        self.player.pitch -= sens * position[1]
        if self.player.pitch < -1.57: self.player.pitch = -1.57
        if self.player.pitch > 1.57: self.player.pitch = 1.57
        self.prev_pos = pos
        self.player.calc_dir()

    def draw(self):
        self.process_monster(self.player)
        self.fov = self.fov * 0.92 + self.tgt_fov * 0.08
        Texture.set(data.filepath('planet.png'))
        glUseProgram(self.planet_shader)

        def gul(s):
            return glGetUniformLocation(self.planet_shader, s)

        def gal(s):
            return glGetAttribLocation(self.planet_shader, s)


        glUniformMatrix4fv(
            glGetUniformLocation(self.planet_shader, 'u_proj'),
            1, False,
            mat2list(glm.perspective(glm.radians(self.fov),
                                     self.aspect,
                                     0.1,
                                     1000.0)))

        glUniformMatrix4fv(
            glGetUniformLocation(self.planet_shader, 'u_view'),
            1, False,
            mat2list(glm.lookAt(
                self.player.pos,
                self.player.pos + self.player.dir,
                glm.vec3(0, 0, 1))))

        glUniform1i(gul('sampler'), 0)

        glEnableVertexAttribArray(gal('in_vert'))
        with self.vbo_planet.vbo:
            glVertexAttribPointer(gal('in_vert'), 3, GL_FLOAT, False, 8*4, self.vbo_planet.vbo)
            glDrawArrays(GL_TRIANGLES, 0, self.vbo_planet.count)
            global DPF
            DPF += 1

        Texture.set(data.filepath('water.png'))
        glUniformMatrix4fv(
            glGetUniformLocation(self.planet_shader, 'u_view'),
            1, False,
            mat2list(
                glm.scale(
                    glm.translate(
                        glm.lookAt(
                            self.player.pos,
                            self.player.pos + self.player.dir,
                            glm.vec3(0, 0, 1)),
                        glm.vec3(0, 0, 100.0)),
                    glm.vec3(1, 1, 0))))
        with self.vbo_planet.vbo:
            glVertexAttribPointer(gal('in_vert'), 3, GL_FLOAT, False, 8*4, self.vbo_planet.vbo)
            glDrawArrays(GL_TRIANGLES, 0, self.vbo_planet.count)
            global DPF
            DPF += 1
        self.rays.process()
        self.rays.draw(self)
        #for t in self.towers:
        #    t.draw(self)
        glUseProgram(0)




class Shell:
    def __init__(self):
        self.text = TextDrawer()
        self.crosshair = CrosshairDrawer()
        self.texture = Texture()
        self.grabbed = True
        self.overdraw = 1
        pygame.init()
        pygame.display.init()
        pygame.display.set_mode([1024, 768],
                                pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.text.init()
        self.crosshair.init()

        self.game = Game(self)

        # workaround for
        pygame.mixer.quit()
        pygame.event.set_grab(self.grabbed)
        pygame.mouse.set_visible(not self.grabbed)

    def resize(self, w, h):
        pygame.display.set_mode([w, h], pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE)
        glViewport(0, 0, w, h)
        self.aspect = float(w) / h

    def draw(self):
        glClearColor(0.3, 0.4, 0.5, 1.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        #glEnable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)
        fps = self.clock.get_fps()
        global DPF
        s = "FPS: {:.1f} * {} {}".format(
            fps,
            self.overdraw,
            self.game.player.gun.str()
        )
        DPF = 0

        self.text.draw((10, 570), s, 30)
        self.crosshair.draw(0, data.filepath('crosshair.png'), 1/self.game.aspect)

        for i in range(self.overdraw):
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
                    if e.key == pygame.K_g:
                        self.grabbed = not self.grabbed
                        pygame.event.set_grab(self.grabbed)
                        pygame.mouse.set_visible(not self.grabbed)
                    if e.key in (pygame.K_EQUALS, pygame.K_PLUS):
                        self.overdraw += 1
                    if e.key == pygame.K_MINUS:
                        self.overdraw = max(self.overdraw - 1, 1)

                elif e.type == pygame.KEYUP:
                    self.game.on_key(e.key, is_down=False)
                elif e.type == pygame.MOUSEMOTION:
                    self.game.on_move(e.rel)
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    self.game.on_key(e.button, is_down=True)
                elif e.type == pygame.MOUSEBUTTONUP:
                    self.game.on_key(e.button, is_down=False)

                elif e.type == pygame.VIDEORESIZE:
                    self.resize(e.w, e.h)
                else:
                    print(e)
            self.draw()

def main():
    g = Shell()
    g.start()
    print("Thank you for playing.")
