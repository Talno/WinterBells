import pygame
import os
import random

#bpm 115
#transparent ball background

res_x = 1600
res_y = 900
#basic initialization of screen and game stuff
pygame.init()
screen = pygame.display.set_mode((res_x, res_y))
done = False
touchable = False

char_x = 800
char_y = 100
char_vel_x = 0
char_vel_y = 0
char_pos = (char_x, char_y)
char_vel = (char_vel_x, char_vel_y)
char_size = (60, 60)
MAXVEL = 20
JUMPVEL = 19
TIMESTEP = 60
GRAV = 2
bells = []
bell_vel = [0, GRAV]
bell_size = (52, 59)
bell_interval = 262
camera_pos = 900
MAXHEIGHT = 650
bouncy = 0
#fps cap
clock = pygame.time.Clock()

#images
images = {}

def get_image(path):
	global images
	image = images.get(path)
	if image == None:
		os_ind_path = path.replace('/', os.sep).replace('\\', os.sep).lower()
		image = pygame.image.load(os_ind_path)
		images[path] = image
	return image
#spawns bell on top of screen at random location
def spawn_bell():
	global res_x
	global res_y
	global bells
	bell_x_pos = random.randint(80, res_x - 80)
	bell_y_pos = camera_pos + 100
	bells.insert(0, [bell_x_pos, bell_y_pos])
#updates their position so that they fall
#also checks if they are offscreen to remove
def update_bell_pos():
	global bells
	global bell_size
	
	for bell in bells:
		for i in range(len(bell)):
			bell[i] -= bell_vel[i]
		#update bell removal when camera is implemented
		if screen_pos(bell[1]) > res_y:
			bells.remove(bell)
		#screen.blit(get_image("bell.png"), bell)
		
def draw_bells():
	global bells
	
	for bell in bells:
		blit_obj('bell.png', bell)
#checks if ball overlaps with bell
#square hitboxes because i dont get paid
#returns the position of the bell hit
def hit_bell():
	global bell_size
	global char_size
	global bells
	global char_pos
	hit = None
	
	char_pos_end = list(map(lambda x, y: x + y, char_pos, char_size))
	for bell in bells:
		bell_end = list(map(lambda x, y: x + y, bell, bell_size))
		if overlap((bell, bell_end), (char_pos, char_pos_end)):
			hit = bell
			break
	
	return hit

def jump(vel):
	global char_vel_y
	global char_vel_x
	global char_vel
	
	char_vel_y = vel
	char_vel = (char_vel_x, char_vel_y)
def overlap(a, b):
	ylap = False
	xlap = False
	if (a[0][1] < b[0][1] and a[1][1] > b[0][1]) or (a[0][1] > b[0][1] and a[0][1] < b[1][1]):
		ylap = True
	if (a[0][0] < b[0][0] and a[1][0] > b[0][0]) or (a[0][0] > b[0][0] and a[0][0] < b[1][0]):
		xlap = True
		
	return ylap and xlap
#determines movement of the character, updates the global position variable
def char_move(pressed):
	global char_vel_x
	global char_vel_y
	global char_y
	global char_x
	global char_pos
	global touchable
	moved = False
	#user controlled left and right movement
	if pressed[pygame.K_LEFT]: 
		char_vel_x = max(MAXVEL * -1, char_vel_x - MAXVEL/TIMESTEP)
		moved = True
	if pressed[pygame.K_RIGHT]: 
		char_vel_x = min(MAXVEL, char_vel_x + MAXVEL/TIMESTEP)
		moved = True
	if pressed[pygame.K_SPACE] and not touchable:
		touchable = True
		jump(JUMPVEL)
	#friction
	if not moved:
		if char_vel_x < 0 :
			char_vel_x = min(0, char_vel_x + MAXVEL/TIMESTEP/2)
		elif char_vel_x > 0:
			char_vel_x = max(0, char_vel_x - MAXVEL/TIMESTEP/2)
	char_x = min(max(0, char_x + char_vel_x), res_x - char_size[0])
		
	if char_x == 0 or char_x == (res_x - char_size[0]):
		char_vel_x = 0
	#gravity affects them each time step
	char_vel_y = min(MAXVEL, char_vel_y - MAXVEL/60)  
	char_y = max(char_size[1], char_y + char_vel_y)
	
	char_pos = (char_x, char_y)

def blit_obj(file, pos):
	global camera_pos
	screen.blit(get_image(file), (pos[0],  camera_pos - pos[1]))
	
def update_camera_pos():
	global char_pos
	global camera_pos
	global MAXHEIGHT
	
	#following upwards
	if camera_pos - char_pos[1] < (res_y - MAXHEIGHT):
		camera_pos = char_pos[1] + (res_y - MAXHEIGHT)
	if camera_pos - char_pos[1]  > res_y - char_size[1]:
		camera_pos = char_pos[1] + res_y - char_size[1]
#gets position on screen relative to camera given y position
def screen_pos(pos):
	global camera_pos
	return camera_pos - pos
	
def on_ground():
	return char_y == char_size[1]
	
pygame.mixer.music.load('WinterBells.mp3')
pygame.mixer.music.play(-1)

spawn_bell() #still error prone, if all bells disappear there will be problems? I think?
while not done:
	#event handling
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
			
	screen.fill((250,250,250))
	
	#movement control and display main char
	pressed = pygame.key.get_pressed()
	char_move(pressed)
	update_camera_pos()
	update_bell_pos()
	
	blit_obj('ball.png', char_pos)
	#spawning bells for game
	if screen_pos(bells[0][1]) > bell_interval - 100:
		spawn_bell()
	
	bell = hit_bell()
	if bell and touchable:
		jump(JUMPVEL)
		bells.remove(bell)
	draw_bells()
	
	if touchable and on_ground() and not bouncy:
		bouncy = 2
	
	if bouncy > 0 and on_ground():
		jump(bouncy * 2)
		bouncy -= 1
		if bouncy == 0:
			touchable = False
		
	pygame.display.flip()
	clock.tick(TIMESTEP)