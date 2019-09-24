

class Enemy:
    #state
    player_seen_at_tower = None # tower coordinates (x, y, z)
    player_seen = None          # world coordinates vec3


    # constants
    speed = 1
    jump_speed = 5
    jump_angle = 30
    maxhp = 100

    disappear_on_sight = False
    use_ranged_weapons = True
    use_grenades = False
    melee_weapon = None # should be some kind of Gun
    inventory_choices = [] # [[gun2, gun2], [gun3,None], [grenade1, grenade2,None,None]]
