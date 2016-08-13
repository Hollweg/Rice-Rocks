
#Implementation of Rice Rocks - Used Program template for RiceRocks
#Developed by Guilherme Hollweg
#An Introduction to Interactive Programming with Python
#Rice University
#Final Assignment

''' Explicacao
O objetivo do jogo e conseguir a maior pontuacao possivel

Jogabilidade: Utilizando as flechas direcionais do teclado.

- Comeca o jogo com 3 vidas
- Destruindo 1 asteroide voce recebe um ponto
- A cada 250 pontos, o jogador recebe uma vida extra
- Existe um botao para resetar o jogo
- Existe um campo para o usuario inserir seu nome e se desejado,
mudar a velocidade dos motores da nave - de 0 a 1.
- Existem 4 dificuldades diferentes
    Nota: So pode mudar a dificuldade quando o jogo estiver pausado

Divirta-se :D

Explanation:
The games objective is to get the high possilbe Score and try to survive.

How to play: Use the directional keys in the keyboard.

- You start with 3 lives
- Destroy one asteroid give you 1 point.
- Every 250 score you'll receive an extra life
- There is a button to Reset the game
- There is a field to put your name and a field to change (if desired) the ship
thrust velocity (0.1 to 1)
- There are 4 different difficulties

Note: You only can change the games dificulty if the game is reseted.

Have fun :D'''

import simplegui
import math
import random

# globals for user interface
Width = 800
Height = 600

# limits
Max_Rocks = 13
Missile_Age = 45
Propulsion = 0.1
Vel_Rocks = 0.4

# Screen Variables
Player = 'Player'
Start_Score = 0
Score = Start_Score
Start_Lives = 3
Lives = Start_Lives
Random_Explosion = 0
Random_Explosion_Info = 0

Time = 0
Started = False

# don't create new rocks too close to the ship
Min_Ship_To_New_Rock_Dist = 100
Explosion_Age = 79

class ImageInfo:
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

# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim

# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris3_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2013.png")

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

asteroid_brown_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_brown_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_brown.png")

asteroid_blend_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_blend_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blend.png")

# unlimited lifespan and True for animated. Notice: animated rocks are bigger
animated_asteroid_info = ImageInfo([64, 64], [128, 128], 64, None, True)
animated_asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/asteroid1.opengameart.warspawn.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

explosion_orange_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_orange_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_orange.png")

explosion_blue_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_blue_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_blue.png")

big_explosion_info = ImageInfo([50, 50], [100, 100], 50, 81, True)
big_explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/explosion.hasgraphics.png")
BIG_EXPLOSION_DIM = [9, 9]

# sound assets purchased from sounddogs.com, please do not redistribute
# .ogg versions of sounds are also available, just replace .mp3 by .ogg
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0]-q[0])**2+(p[1]-q[1])**2)

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()

    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]] , self.image_size,
                              self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)
        # canvas.draw_circle(self.pos, self.radius, 1, "White", "White")

    def update(self):
        global Propulsion
    
        # update angle
        self.angle += self.angle_vel
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % Width
        self.pos[1] = (self.pos[1] + self.vel[1]) % Height
        # update velocity
        if self.thrust:
            acc = angle_to_vector(self.angle)
            self.vel[0] += acc[0] * float(Propulsion)
            self.vel[1] += acc[1] * float(Propulsion)
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
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + 6 * forward[0], self.vel[1] + 6 * forward[1]]
        a_missile = Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)

    def get_position(self):
        return self.pos

    def set_position(self, new_pos):
        self.pos = [new_pos[0], new_pos[1]]

    def set_vel(self, new_vel):
        self.vel = [new_vel[0],new_vel[1]]

    def get_radius(self):
        return self.radius

# Sprite class
class Sprite:
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

    def draw(self, canvas):
        # time used for animation of rocks
        global rock_timer, Random_Explosion
        # animate rocks. Use angle to obtain number of the current image. Angle is updated in the update method.
        if self.animated:
            #the below was for animated rocks. Dropped.
            #print self.angle
            #current_rock_index = (self.angle % self.image_center[0]) // 1
            #self.angle += self.angle_vel
            #current_rock_center = [self.image_center[0] + current_rock_index * self.image_size[0], self.image_center[1]]
            #print current_rock_index
            #print current_rock_center
            # animated rocks don't have angle set (0)
            # animated explosions: pick images from the sprite
            # images is tiles in nine rows and nine columns
            # aging is done in the update handler
            #print explosion_index, self.age
            EXPLOSION_DIM = [9, 9]
            explosion_index = [self.age % EXPLOSION_DIM[0], (self.age // EXPLOSION_DIM[0]) % EXPLOSION_DIM[1]]
            canvas.draw_image(Random_Explosion, [self.image_center[0] + explosion_index[0] * self.image_size[0],
                     self.image_center[1] + explosion_index[1] * self.image_size[1]],
                     self.image_size, self.pos, self.image_size)
            #canvas.draw_image(self.image, current_sprite_center, self.image_size,
            #              self.pos, self.image_size, 0)
            # for not animated objects just draw them
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                          self.pos, self.image_size, self.angle)

    def update(self):
        # update angle
        self.angle += self.angle_vel
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % Width
        self.pos[1] = (self.pos[1] + self.vel[1]) % Height
        # increment age on every update
        self.age += 1

    def get_position(self):
        return self.pos

    def get_radius(self):
        return self.radius

    def get_age(self):
        return self.age

    def collide(self, other_object):
        ''' detect and handle collisions. '''
        # how far from both objects' centers
        distance = dist(self.get_position(), other_object.get_position())
        if distance <= self.radius + other_object.get_radius():
            # there was a collision
            return True
        return False

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
    # this is important: check what key was released, so that you adjust only the things that that key controlled.
    if key == simplegui.KEY_MAP['left']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(False)

# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global Started, Score, Lives, Start_Score, Start_Lives
    center = [Width / 2, Height / 2]
    size = splash_info.get_size()
    inWidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inHeight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not Started) and inWidth and inHeight:
        Started = True
    # reset counters
    Score = Start_Score
    Lives = Start_Lives
    soundtrack.rewind()
    soundtrack.play()

def draw(canvas):
    global Time, Started, set_rocks, Lives, rock_timer

    # animiate background
    Time += 1
    wtime = (Time / 4) % Width
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [Width / 2, Height / 2], [Width, Height])
    canvas.draw_image(debris_image, center, size, (wtime - Width / 2, Height / 2), (Width, Height))
    canvas.draw_image(debris_image, center, size, (wtime + Height / 2, Height / 2), (Width, Height))

    # draw UI
    canvas.draw_text("Lives:", [50, 45], 18, "White", "sans-serif")
    canvas.draw_text("Score:", [680, 50], 18, "White", "sans-serif")
    canvas.draw_text(str(Lives), [100, 45], 18, "White", "sans-serif")
    canvas.draw_text(str(Score), [760, 50], 18, "White", "sans-serif")
    canvas.draw_text(str(Player), (50, 20), 18, "White", "sans-serif")

    # draw ship and sprites
    my_ship.draw(canvas)
    # draw and update sprites
    process_sprite_group(set_rocks, canvas)
    # draw and update missiles
    process_sprite_group(missile_group, canvas)
    # draw and update explosions
    process_sprite_group(explosion_group, canvas)

    # check for collisions between the ship and rocks
    # decrease the number of Lives by one, no matter how many rocks we collided with
    if group_collide(set_rocks, my_ship):
        Lives -= 1
        if Lives == 0:
            # stop the game
            # remove all rocks (new ones will not be added by the timer)
            # put the ship in the center
            Started = False
            set_rocks = set([])
            my_ship.set_position([Width / 2, Height / 2])
            my_ship.set_vel([0, 0])

    # collisons between missiles and rocks
    group_group_collide(set_rocks, missile_group)

    # update ship and sprites
    my_ship.update()

    # draw splash screen if not started
    if not Started:
        canvas.draw_image(splash_image, splash_info.get_center(),
                          splash_info.get_size(), [Width/2, Height/2],
                          splash_info.get_size())

# timer handler that spawns a rock
def rock_spawner():
    global set_rocks, Started, Vel_Rocks

    #global a_rock
    # keep creating rocks until limit reached
    # don't spawn too close to the ship
    # keep picking a new position until you find the right one
    #print "too close", rock_pos
    
    if len(set_rocks) < Max_Rocks and Started: 
        rock_pos = [random.randrange(0, Width), random.randrange(0, Height)]
        
        while dist(rock_pos, my_ship.get_position()) < Min_Ship_To_New_Rock_Dist:
            rock_pos = [random.randrange(0, Width), random.randrange(0, Height)]
        
        asteroid = random.choice([asteroid_image, asteroid_brown_image, asteroid_blend_image])
        rock_vel = [random.random() * Vel_Rocks, random.random() * Vel_Rocks]
        rock_avel = random.random() * 0.1
        a_rock = Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid, asteroid_info)
        set_rocks.add(a_rock)
        
        # animated rocks need a different speed
        #rock_avel = random.choice([-1, 1]) * .3 * random.random()
        #a_rock = Sprite(rock_pos, rock_vel, 0, rock_avel, animated_asteroid_image, animated_asteroid_info)
    
# processing a group of sprites
# removal before update() and draw() because aging done there. You want to check and age, not the other way around.
# handle removal of old missiles

def process_sprite_group(sprite_group, canvas):
    missile_remove = set([])
    for a_missile in missile_group:
        if a_missile.get_age() > Missile_Age:
            missile_remove.add(a_missile)
    #actual removal
    #for a_missile in missile_remove:
    #missile_group.remove(a_missile)
    missile_group.difference_update(missile_remove)

    # handle removal of old explosions
    explosion_remove = set([])
    for explosion in explosion_group:
        # image is tiles 9x9, so indexes starting from age 0-80 is a whole life cycle?
        if explosion.get_age() > Explosion_Age:
            explosion_remove.add(explosion)
        # actual removal
        explosion_group.difference_update(explosion_remove)
        #print explosion.get_age()

    #update and draw each sprite
    for a_sprite in sprite_group:
        a_sprite.update()
        a_sprite.draw(canvas)

# check for collisions between one object and a group
def group_collide(group, other_object):
    global explosion_group
    global Random_Explosion
    global Random_Explosion_Info
    
    collision_counter = 0
    tobremoved = set([])
    for a_sprite in group:
        if a_sprite.collide(other_object):
            # remove this rock from the group
            # create a new explosion
            # pos, vel, ang, ang_vel, image, info, sound = None
            #print "explosion created", explosion_group
            #print "collision!"
            tobremoved.add(a_sprite)
            collision_counter += 1
            explosion_pos = a_sprite.get_position()
            
            Random_Explosion = random.choice([explosion_image, explosion_orange_image, explosion_blue_image, big_explosion_image])
            if Random_Explosion == explosion_image:
                Random_Explosion_Info = explosion_info
            
            if Random_Explosion == explosion_orange_image:
                Random_Explosion_Info = explosion_orange_info
                
            if Random_Explosion == explosion_blue_image:
                Random_Explosion_Info = explosion_blue_info
                
            if Random_Explosion == big_explosion_image:
                Random_Explosion_Info = big_explosion_info
                
            new_explosion = Sprite(explosion_pos, [0,0], 0, 0, Random_Explosion, Random_Explosion_Info, explosion_sound)
           
            explosion_group.add(new_explosion)
    group.difference_update(tobremoved)
    return collision_counter
    # remove that sprite from the group
    #for a_sprite in tobremoved:
    #    group.remove(a_sprite)
    #	 print "removing collided sprite"
    
# check for collisions between two groups of objects
def group_group_collide(group1, group2):
    ''' group1 will happen to be rocks '''
    global Score, Lives
    
    number_collisions = 0
    tobremoved = set([])
    # iterate through the first group and check for collision with all elements in the other group
    for a_missile in group2:
        if group_collide(group1, a_missile):
            number_collisions += 1
            tobremoved.add(a_missile)
    #print "collision between two objects"
    # remove missiles that shot rocks
    group2.difference_update(tobremoved)
    #for a_missile in toberemoved:
    #    group2.remove(a_missile)
    # increase counter by how many rocks each missile collided with
    Score += number_collisions
    
    if (Score > 0 and (Score % 250 == 0)):
         Lives = Lives + 1  
         Score = Score + 1
         return
        
    return number_collisions

#Function to Variate the Player nama
def input_player_name(player_name):
   global Player
   Player = str(player_name)

#Function to Variate the Thrust Ship - Input    
def input_propulsion_variable (Prop_var):	
    global Propulsion
    Propulsion = Prop_var
 
#Set the game in Easy mode - More missile range and Max rocks 12
def Easy():
    global Max_Rocks, Missile_Age, Vel_Rocks
    
    if not Started:
        Max_Rocks = 12
        Missile_Age = 60
        Vel_Rocks = 0.3
    else:
        return

#Set the game in Normal mode - Less missile range and Max rocks 15
def Normal():
    global Max_Rocks, Missile_Age, Vel_Rocks
    
    if not Started:
        Max_Rocks = 15
        Missile_Age = 40
        Vel_Rocks = 0.7
    else:
        return

#Set the game in Normal mode - Almost unexisting missile range and Max rocks 18
def Hard():
    global Max_Rocks, Missile_Age, Vel_Rocks
    
    if not Started:
        Max_Rocks = 18
        Missile_Age = 25
        Vel_Rocks = 1
    else:
        return
    
#Set the game in Normal mode - Almost unexisting missile range and Max rocks 22
def Insane():
    global Max_Rocks, Missile_Age, Vel_Rocks
    
    if not Started:
        Max_Rocks = 22
        Missile_Age = 15
        Vel_Rocks = 1.4
    else:
        return
    
def Reset():
    global Started, set_rocks
    
    if Started == True:
        Started = False
        set_rocks = set([])
        my_ship.set_position([Width / 2, Height / 2])
        my_ship.set_vel([0, 0])
    
    return

# initialize Frame
frame = simplegui.create_frame("Asteroids", Width, Height)

# initialize ship and two sprites
my_ship = Ship([Width / 2, Height / 2], [0.2, 0.2], 0, ship_image, ship_info)

#a_rock = Sprite([width / 3, height / 3], [1, 1], 0, .1, asteroid_image, asteroid_info)
set_rocks = set([])
missile_group = set([])
explosion_group = set([])
#a_missile = Sprite([2 * width / 3, 2 * height / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)

#Text Inputs
frame.add_input ("Enter Your Name Here", input_player_name, 200)
frame.add_input ("Propulsion Variable (def. 0.1)", input_propulsion_variable, 200)

#create buttons and canvas callback
frame.add_button("Easy", Easy, 200)
frame.add_button("Normal",  Normal, 200)
frame.add_button("Hard", Hard, 200)
frame.add_button("Insane", Insane, 200)
frame.add_button("Reset", Reset, 200)


# register handlers
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
