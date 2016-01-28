"""
    RiceRocks.py - Yevheniy Chuba - Spring 2014
    Implementation of RiceRocks game. 
    Enjoy: http://www.codeskulptor.org/#user33_6KEZdn2rEvmOGDF.py
    
    Although we used class-specific CodeSculptor for graphics, most of the methods
    and the rest of the concepts are similar if not the same in other Python librararies, 
    such as Pygame.
    Learned to:
        - implement complex graphics for moving objects: 
            - lasers, explosions, collisions, rotations, frames, counters
        - architect intermidiate OOP design
        - implement physics 101 with python:
            - accelaration, velocities, transformations (angle-to-vector) for multiple objects
        - keyboard interactions
"""

import simplegui
import math
import random

############### GLOBALS ##########################################################################################
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
started = False # whether the game started or not
rock_max = 11 # a number of rocks to start with
EXPLOSION_DIM = [9, 9] # the dimensions of animated explosion
#################################################################################################################


########### CLASS FOR CREATING A SINGLE IMAGE ####################################################################
class ImageInfo:
    ''' creates an image with attributes: center, size, radius, lifespan 
        and whether the image has multiple tiles(animation)
    '''
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated
###################################################################################################################


############### INSTANCES OF IMAGE CLASS + IMAGE URLS ################################################################
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.s2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
# .ogg versions of sounds are also available, just replace .mp3 by .ogg
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")
################################################################################################################################


############### HELPER FUNCTIONS #################################################################################################
# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)
##################################################################################################################################

############### SHIP CLASS #########################################################################################################
class Ship:
    ''' creates a ship instance with position in x,y; velocity in x,y; angle in radians, image_url, image_instance'''
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
    
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def draw(self,canvas):
        # if thrust is true - if excellarating with an "up" arrow
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]] , self.image_size,
                              self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)
        # canvas.draw_circle(self.pos, self.radius, 1, "White", "White")

    def update(self):
        # update angle
        self.angle += self.angle_vel
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

        # update velocity
        if self.thrust:
            acc = angle_to_vector(self.angle)
            self.vel[0] += acc[0] * .1
            self.vel[1] += acc[1] * .1
            
        self.vel[0] *= .99
        self.vel[1] *= .99

    def set_thrust(self, on):
        self.thrust = on
        if on:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
       
    def increment_angle_vel(self):
        self.angle_vel += .05
        
    def decrement_angle_vel(self):
        self.angle_vel -= .05
        
    def shoot(self):
        # when pressing "space" shoot a missile
        global missile_group
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + 6 * forward[0], self.vel[1] + 6 * forward[1]]
        missile_group.add(Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound))
############################################################################################################################################
    
    
############## SPRITE CLASS ###################################################################################################################
class Sprite:
    '''creates missile, rock, explosion instance with position in x,y; velocity in x,y; angle in radians, image_url, image_instance  '''
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
    
    def get_position(self):
        return self.pos
    
    def get_velocity(self):
        return self.vel
    
    def get_radius(self):
        return self.radius
    
    def collide(self, other_object):
        # when one object collides with another: if d < r1+r2
        self.pos = self.get_position()
        self.radius = self.get_radius()
        other_object.pos = other_object.get_position()
        other_object.radius = other_object.get_radius()
        d_x = self.pos[0] - other_object.pos[0]
        d_y = self.pos[1] - other_object.pos[1]
        d_r = self.radius + other_object.radius
        if abs(d_x) < d_r and abs(d_y) < d_r:
            return True
        else:
            return False
    
    def draw(self, canvas):
        # draws an image or an explosion
        if self.animated:
            explosion_index = [self.age % EXPLOSION_DIM[0], (self.age // EXPLOSION_DIM[0]) % EXPLOSION_DIM[1]]
            canvas.draw_image(self.image, 
                    [self.image_center[0] + explosion_index[0] * self.image_size[0], 
                     self.image_center[1] + explosion_index[1] * self.image_center[1]], 
                     self.image_size, self.pos, self.image_size)
            self.age += 1
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                             self.pos, self.image_size, self.angle)

    def update(self):
        # update angle
        self.angle += self.angle_vel
        self.age += 1
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        # determine the age of the sprite (missile)
        if self.age >= self.lifespan:
            return True
        else: 
            return False
##################################################################################################################################  


############### HANDLERS ############################################################################################################
# key handlers to control ship   
def keydown(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(True)
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
        
def keyup(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(False)
        
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, lives, score, rock_max
    lives = 3
    score = 0
    rock_max = 11
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True


# take a set and a canvas and call the update and draw methods for each sprite in the group
def process_sprite_group(group, canvas):
    for item in list(group):
        item.draw(canvas)
        item.update()
        if item.update():
            group.discard(item)

# collide a single object with each item in a group
def group_collide(group, other_object):
    for item in list(group): 
        if item.collide(other_object):
            explosion_group.add(Sprite(item.pos, item.vel, 0, 0, explosion_image, explosion_info, explosion_sound))
            group.discard(item)
            return True
    return False

# collide each item in one set with each item in another set
def group_group_collide(group_1, group_2):
    global score
    for item in list(group_1):
        if group_collide(group_2, item):
            group_1.discard(item)
            score += 1

# as score increases, increase the max number of rocks on the screen
def update_rock_max():
    global rock_max, score
    if score % 5 == 0:
        rock_max = 11+score/5

# the draw handler for the canvas
def draw(canvas):
    global time, started, rock_group, lives, missile_group, score, rock_max, explosion_group
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw UI
    if group_collide(rock_group, my_ship):
        lives -= 1
        canvas.draw_text("Lives: "+str(lives), [50, 50], 22, "White")
    else:
        canvas.draw_text("Lives: "+str(lives), [50, 50], 22, "White")
    
    canvas.draw_text("Score: "+str(score), [680, 50], 22, "White")

    # draw ship
    my_ship.draw(canvas)
    # update ship and sprites
    my_ship.update()
    # draw/update a set of missile sprites
    process_sprite_group(missile_group, canvas)
    # draw/update a set of rock sprites
    process_sprite_group(rock_group, canvas)
    # draw/update explosion
    process_sprite_group(explosion_group, canvas)
    
    # update group/group collisions
    group_group_collide(rock_group, missile_group)

    # if running out of lives, restart the game, reset the necessary sets
    if lives == 0:
        started = False
        rock_group = set([])
    
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
    # update the max number of rocks on the screen
    update_rock_max()
    
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group, started
    if started:
        soundtrack.play() # play the game soundtrack
        if len(list(rock_group)) <=rock_max:
            rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
            rock_vel = [random.random() * .6 - .3, random.random() * .6 - .3]
            rock_avel = random.random() * .2 - .1
            # make sure the rocks do not appear at the position+radius of the ship
            if rock_pos[0] > my_ship.pos[0]+my_ship.radius or rock_pos[0] < my_ship.pos[0]-my_ship.radius and rock_pos[1] > my_ship.pos[1]+my_ship.radius or rock_pos[1] < my_ship.pos[1]-my_ship.radius:
                rock_group.add(Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid_image, asteroid_info))
    else:
        # rewind the soundtrack for the next game
        soundtrack.rewind()
        soundtrack.pause()
###############################################################################################################################################################################


########### GAME INITIALIZERS ####################################################################################################################################################
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)
# initialize ship, rocks, missiles, explosions
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set([])
missile_group = set([])
explosion_group = set([])
# register handlers
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
