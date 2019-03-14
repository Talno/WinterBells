import pygame
import os

#bpm 115

res_x = 1600
res_y = 900
#basic initialization of screen and game stuff
pygame.init()
screen = pygame.display.set_mode((res_x, res_y))
done = False

char_x = 800
char_y = 800
char_vel_x = 0
char_vel_y = 0
char_pos = (char_x, char_y)
char_vel = (char_vel_x, char_vel_y)
char_size = (60, 60)
MAXVEL = 20
TIMESTEP = 60
BELLSTEP = 31.3
step = 0
bells = {}

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
	
#determines movement of the character, updates the global position variable
def char_move(pressed):
	global char_vel_x
	global char_vel_y
	global char_y
	global char_x
	global char_pos
	moved = False
	#user controlled left and right movement
	if pressed[pygame.K_LEFT]: 
		char_vel_x = max(MAXVEL * -1, char_vel_x - MAXVEL/TIMESTEP)
		moved = True
	if pressed[pygame.K_RIGHT]: 
		char_vel_x = min(MAXVEL, char_vel_x + MAXVEL/TIMESTEP)
		moved = True
	#friction
	if not moved:
		if char_vel_x < 0 :
			char_vel_x = min(MAXVEL, char_vel_x + MAXVEL/TIMESTEP/2)
		elif char_vel_x > 0:
			char_vel_x = max(MAXVEL * -1, char_vel_x - MAXVEL/TIMESTEP/2)
	char_x = min(max(0, char_x + char_vel_x), res_x - char_size[0])
		
	if char_x == 0 or char_x == (res_x - char_size[0]):
		char_vel_x = 0
	#gravity affects them each time step
	char_vel_y = min(10, char_vel_y + MAXVEL/60)
	char_y = min(max(0, char_y + char_vel_y), res_y - char_size[1])
	
	char_pos = (char_x, char_y)


pygame.mixer.music.load('WinterBells.mp3')
pygame.mixer.music.play(-1)
while not done:
	#event handling
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
			
	screen.fill((250,250,250))

	#movement control and display main char
	pressed = pygame.key.get_pressed()
	char_move(pressed)
	screen.blit(get_image('ball.png'), char_pos)
	
	#spawning bells for game
	if step < BELLSTEP:
		step = step + 1
	else:
		step = step - BELLSTEP
		spawn_bell()
	
	pygame.display.flip()
	clock.tick(TIMESTEP)