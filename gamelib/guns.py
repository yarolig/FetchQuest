

import copy
import glm










class Gun:
    name = 'gun'

    # state:
    charges = 10000.0
    spreadx = 1.0
    spready = 1.0
    offsetx = 0.0
    offsety = 0.0
    temperature = 0.0
    state_shot = 0  # no of frame when shooting initiated
    state_reload = 0  # no of frame when reloading initiated

    def str(self):
        return  "{} {:.1f} s{:.1f}s{:.1f} {:.1f}o{:.1f} t{:.1f} sh={}".format(
            self.name, self.charges, self.spreadx, self.spready,
            self.offsetx, self.offsety, self.temperature,
            self.state_shot
        )
    # constants
    #clip_size = 8
    max_charge = 64.5
    charge_rate = 0.01 # charges per frame

    dt_per_shot = 1
    fail_temperature = 100
    recover_temperature = 50
    temperature_decay = 0.99

    preshot_time = 1 # frames, min=1
    shot_time = 30 # frames
    auto_shot_time = 90 # frames # single-shot gun will fire again if LM is hold
    reload_time = 60 # frames
    draw_time = 60 # frames

    normal_spread = 0.1 # degrees
    spreadx_per_shot = 0.2 # degrees
    spready_per_shot = 0.1  # degrees
    offsetx_per_shot = -0.01
    offsety_per_shot = 0.01
    spread_decay = 0.9

    movement_spread = 0.5  # degrees
    standing_spread = 0.01  # degrees
    flying_spread = 1.5 # degrees
    maxzoom = 60
    zoom_emcay = 0.999
    zoom_decay = 0.9

    hands = 1
    accurate_angular_speed = 2 # degrees per frame
    max_angular_speed = 4 # degrees per frame

    damage = 5
    rays_per_shot = 1
    full_damage_range = 30 # units, one cell is xyscale=1.0 unit


class Pistol(Gun):
    name = 'pistol'
    normal_spread = 1.0  # degrees
    spreadx_per_shot = 1.0  # degrees
    spready_per_shot = 1.0  # degrees
    offsetx_per_shot = -0.01
    offsety_per_shot = 0.01
    spread_decay = 0.9
    rays_per_shot = 1
    shot_time = 20


class Shotgun(Gun):
    name = 'shotgun'
    normal_spread = 7.0  # degrees
    spreadx_per_shot = 5.0  # degrees
    spready_per_shot = 5.0  # degrees
    offsetx_per_shot = -0.01
    offsety_per_shot = 0.01
    spread_decay = 0.9
    rays_per_shot = 5
    shot_time = 40


class SMG(Gun):
    name = 'SMG'
    normal_spread = 1.0  # degrees
    spreadx_per_shot = 0.8  # degrees
    spready_per_shot = 0.8  # degrees
    offsetx_per_shot = 0.5
    offsety_per_shot = 2.5
    spread_decay = 0.9
    rays_per_shot = 1
    shot_time = 3


class Rifle(Gun):
    name = 'rifle'
    normal_spread = 0.5  # degrees
    spreadx_per_shot = 0.8  # degrees
    spready_per_shot = 0.8  # degrees
    offsetx_per_shot = 0.5
    offsety_per_shot = 2.5
    spread_decay = 0.9
    rays_per_shot = 1
    shot_time = 6

class SniperRifle(Gun):
    name = 'sniper rifle'
    normal_spread = 0.01  # degrees
    spreadx_per_shot = 1.  # degrees
    spready_per_shot = 1.  # degrees
    offsetx_per_shot = 0.1
    offsety_per_shot = 0.1
    spread_decay = 0.95
    rays_per_shot = 1
    shot_time = 30

class MachineGun(Gun):
    name = 'machinegun'
    normal_spread = 0.5  # degrees
    spreadx_per_shot = 0.8  # degrees
    spready_per_shot = 0.8  # degrees
    offsetx_per_shot = 0.5
    offsety_per_shot = 2.5
    spread_decay = 0.9
    rays_per_shot = 1
    shot_time = 10
