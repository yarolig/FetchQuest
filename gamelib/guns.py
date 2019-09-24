

import copy
import glm










class Gun:
    name = 'gun'

    # state:
    charges = 10.0
    spread = 1.0
    offsetx = 0.0
    offsety = 0.0
    temperature = 0.0
    state_shot = 0  # no of frame when shooting initiated
    state_reload = 0  # no of frame when reloading initiated

    # constants
    #clip_size = 8
    max_charge = 64.5
    charge_rate = 0.01 # charges per frame

    dt_per_shot = 1
    fail_temperature = 100
    recover_temperature = 50
    temperature_decay = 0.999

    preshot_time = 0 # frames
    shot_time = 10 # frames
    auto_shot_time = 30 # frames # single-shot gun will fire again if LM is hold
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

