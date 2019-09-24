

class Grenade:
    # state
    ttl = 0 # frames, it is armed if ttl!=0

    # constants
    subgrenades = 0 # if >0 make another grenades when explode
    subgrenade_angle = (30, 60)
    subgrenade_speed = 3
    subgrenade_type = None # Grenade instance
    damage = 50
    fire_effect = False  # obstruct vision
    smoke_effect = False # obstruct lasers!
    em_effect = False
    oil_effect = False
    stun_effect = False
    poison_gas_effect = False
    freeze_effect = False
    foam_effect = False


    mine = False # initial ttl = -1
    speed = 5
    sticky = True # stop moving when hit a wall/floor
    breaks = False  # explode on hit

    radius = 10
    initial_ttl = 120





