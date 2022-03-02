import pygame
import random
import time
from utility import *
pygame.init()

#screen variables
WIDTH , HEIGHT = (280 , 500)
GROUNDY = HEIGHT * 0.8
WIN = pygame.display.set_mode((WIDTH , HEIGHT))
pygame.display.set_caption("FLAPPY BIRD GAME USING PYGAME MODULE !")
FPS = 35

#game pictures
GAME_SOUNDS = {}
NUMBERS = (
	pygame.image.load("gallery/sprites/0.png"),
	pygame.image.load("gallery/sprites/1.png"),
	pygame.image.load("gallery/sprites/2.png"),
	pygame.image.load("gallery/sprites/3.png"),
	pygame.image.load("gallery/sprites/4.png"),
	pygame.image.load("gallery/sprites/5.png"),
	pygame.image.load("gallery/sprites/6.png"),
	pygame.image.load("gallery/sprites/7.png"),
	pygame.image.load("gallery/sprites/8.png"),
	pygame.image.load("gallery/sprites/9.png")
)

MESSAGE1 = pygame.image.load("gallery/sprites/message1.png")
MESSAGE2 = pygame.image.load("gallery/sprites/message2.png")
BACKGROUND = pygame.image.load("gallery/sprites/background.png")
PLAYER = pygame.image.load("gallery/sprites/bird.png")
BASE = pygame.image.load("gallery/sprites/base.png")
PIPE = (pygame.transform.rotate(pygame.image.load("gallery/sprites/pipe.png") , 180) , pygame.image.load("gallery/sprites/pipe.png"))

#GAME SOUNDS
GAME_SOUNDS['die'] = pygame.mixer.Sound("gallery/audio/die.wav")
GAME_SOUNDS['hit'] = pygame.mixer.Sound("gallery/audio/hit.wav")
GAME_SOUNDS['point'] = pygame.mixer.Sound("gallery/audio/point.wav")
GAME_SOUNDS['swoosh'] = pygame.mixer.Sound("gallery/audio/swoosh.wav")
GAME_SOUNDS['wing'] = pygame.mixer.Sound("gallery/audio/wing.wav")

#FONT VARIABLES
FONT = pygame.font.SysFont("Arial Black" , 30)

# gameInfo class created for tracking the levels increasing the difficulty according to level 
class GameInfo :
	LEVELS = 10
	def __init__(self , level = 1):
		self.level = level
		self.started = False
	def start_level(self):
		self.started = True
	def next_level(self) :
		self.level += 1
		self.started = False
	def reset(self):
		self.level = 1
		self.started = False
	def finished(self):
		return self.level > self.LEVELS

class Abstract :
	def __init__(self , x ,y):
		self.x = x 
		self.y = y 
		self.bird_img = None
		self.upper_pipe_img = None
		self.lower_pipe_img = None

	def draw(self , window) :
		window.blit(self.bird_img , (self.x , self.y))
		

class Bird(Abstract) :
	def __init__(self , x , y):
		super().__init__(x , y)
		self.bird_img = PLAYER
		self.angle = 0 
		self.mask = pygame.mask.from_surface(pygame.transform.rotate(self.bird_img , self.angle))

	def move(self , vel):
		self.y += vel 

	def offscreen(self , height):
		return not (self.y + self.bird_img.get_height() != GROUNDY and self.y  >= 0)

	def collide(self, obj):
		return collide(self, obj)
	
	def rotate(self , vel = 0) :
		self.angle += vel
		blit_rotate_center(WIN , self.bird_img , (self.x , self.y ), self.angle)
		
class UpperPipe(Abstract) :
	def __init__(self , x, y , upper_pipe_img ):
		super().__init__(x, y)
		self.upper_pipe_img = upper_pipe_img
		self.mask = pygame.mask.from_surface(self.upper_pipe_img)

	def move(self , vel):
		self.x += vel

	def offscreen(self , width):
		return not (self.x >= -PIPE[0].get_width())

class LowerPipe(Abstract) : 
	def __init__(self, x, y , lower_pipe_img):
		super().__init__(x, y)
		self.lower_pipe_img = lower_pipe_img
		self.mask = pygame.mask.from_surface(self.lower_pipe_img)

	def move(self , vel):
		self.x += vel 


## method used for checking perfect pixel collision
def collide(obj1 , obj2):
	offset_x = int(obj1.x - obj2.x )
	offset_y = int(obj1.y - obj2.y )
	return obj2.mask.overlap(obj1.mask , (offset_x , offset_y)) != None 

def add_pipes(number_of_pipes ,upper_pipes , lower_pipes , game_info , x):

	for i in range(number_of_pipes):
		offset = round(4 - game_info.level/10 )* PLAYER.get_height() 
		y2 = offset + random.randrange(0, int(HEIGHT - BASE.get_height() - offset))
		y1 = PIPE[0].get_height() - y2 + offset 

		if i > 0 :
			while abs(upper_pipes[-1].y + y1) > 150 :
				y2 = offset + random.randrange(0, int(HEIGHT - BASE.get_height() - offset))
				y1 = PIPE[0].get_height() - y2 + offset 			

		upper_pipe = UpperPipe(x + i*(PIPE[0].get_width() + 81 - game_info.level ) , -y1 , PIPE[0] )
		lower_pipe = LowerPipe(x + i*(PIPE[0].get_width() + 81 - game_info.level), y2 , PIPE[1])
			
		upper_pipes.append(upper_pipe)
		lower_pipes.append(lower_pipe)

def redraw(player , game_info , upper_pipes , lower_pipes , time1 , time2):
	global score, high_score
	WIN.blit(BACKGROUND , (0,0))
	for upper_pipe , lower_pipe in zip(upper_pipes , lower_pipes):
		WIN.blit(PIPE[0] , (upper_pipe.x , upper_pipe.y))
		WIN.blit(PIPE[1] , (lower_pipe.x , lower_pipe.y))
	WIN.blit(BASE , (0, GROUNDY))

	if -90 <= player.angle <= 45 and (time2 - time1) > 0.3:
		player.rotate(-5)
	else :
		player.rotate()

	# DISPLAYING SCORE 
	text = FONT.render("" , 1, (0,0,0))  # text may be entered according to the programmer's wish
	Digits = list(str(score))

	print_text(WIN , text, Digits , 0.1 )

def print_text(win , text , digits , factor) :
	width = 0 

	for digit in digits :
		width += NUMBERS[int(digit)].get_width()

	Xoffset = (WIDTH - width)//2

	for digit in digits :
		win.blit(NUMBERS[int(digit)] , (Xoffset , HEIGHT * factor))
		Xoffset += NUMBERS[int(digit)].get_width()



def main():
	global score , high_score
	run = True
	clock = pygame.time.Clock()

	#game variables and objects
	game_info = GameInfo()
	player = Bird(WIDTH//5 , (HEIGHT - PLAYER.get_height())//2)
	message1x = int((WIDTH - MESSAGE1.get_width())/2)
	message1y = int(HEIGHT*0.13)
	message2x = int((WIDTH - MESSAGE2.get_width())/2)
	message2y = int(HEIGHT*0.26)
	score = 0

	pipeVelX = -4
	playerVelY = -15
	playerMaxVelY = 10	
	playerFlapped = False
	playerFlapAccY = -8

	upper_pipes = []
	lower_pipes = []

	time1 = 0
	played = False

    # main loop
	while run :
		clock.tick(FPS)

		time2 = time.time()
		redraw(player , game_info , upper_pipes , lower_pipes ,time1 , time2)
		while not game_info.started :
			pipeVelX = -4
			playerVelY = -15
			playerMaxVelY = 10	
			playerFlapped = False
			playerFlapAccY = -8

                        # displayed score when lost 
			if played :
				text = FONT.render("" , 1, (0,0,0))     
			
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					quit()
				if event.type == pygame.KEYDOWN :
					game_info.started = True
					played = True
					break
			player = Bird(WIDTH//5 , (HEIGHT - PLAYER.get_height())//2)
			WIN.blit(BACKGROUND , (0,0))
			WIN.blit(PLAYER, (player.x , player.y))
			WIN.blit(MESSAGE1 , (message1x , message1y))
			WIN.blit(MESSAGE2 , (message2x , message2y))
			pygame.display.update()

		for event in pygame.event.get():
			if event.type == pygame.QUIT :
				run = False
				pygame.quit()
				break
			if event.type == pygame.KEYDOWN and event.key == (pygame.K_UP or event.key == pygame.K_SPACE ):
				if player.y > 0 :
					playerVelY = playerFlapAccY
					player.angle = 40
					playerFlapped = True
					time1 = time.time()
					GAME_SOUNDS['wing'].play()

		if len(upper_pipes) == 0 :
			number_of_pipes = random.randint(2 + game_info.level , 5 + game_info.level)
			add_pipes(number_of_pipes  , upper_pipes , lower_pipes , game_info , WIDTH)


		if playerVelY < playerMaxVelY and not playerFlapped :
			playerVelY += 1
		if playerFlapped :
			playerFlapped = False

		player.move(min(playerVelY, GROUNDY -player.y - PLAYER.get_height()))

		for upper_pipe ,lower_pipe in zip(upper_pipes ,lower_pipes ):
			upper_pipe.move(pipeVelX)
			lower_pipe.move(pipeVelX)

			## checkig for collisions
			if player.collide(upper_pipe) or player.collide(lower_pipe):
				GAME_SOUNDS['hit'].play()
				game_info.started = False
				score = 0
				upper_pipes.clear()
				lower_pipes.clear()

		if game_info.started :
			if upper_pipes[0].offscreen(WIDTH) :
				upper_pipes.pop(0)
				lower_pipes.pop(0)
				
			number_of_pipes = random.randint(2 + game_info.level , 5 + game_info.level)
			if upper_pipes[-1].x < WIDTH * (2/3 + game_info.level/10):
				add_pipes(number_of_pipes , upper_pipes , lower_pipes , game_info , WIDTH + 100 )

		#checing for scores and level
		for pipe in upper_pipes :
			if pipe.x + PIPE[0].get_width()//2 <= player.x + PLAYER.get_width()//2 < pipe.x + PIPE[0].get_width()//2 + 4 :
				score += 1
				GAME_SOUNDS['point'].play()


		if player.offscreen(HEIGHT) :

			GAME_SOUNDS['hit'].play()
			
			game_info.started = False
			score = (game_info.level - 1) * 100
			upper_pipes.clear()
			lower_pipes.clear()	

		if score == game_info.level * 100  :
			game_info.next_level()

			GAME_SOUNDS['swoosh'].play()
			GAME_SOUNDS['die'].play()
			if game_info.level != 11 :
				text = FONT.render("LEVEL {}".format(game_info.level - 1), 1, (0,0,0))
				WIN.blit(text , (WIDTH//2 - text.get_width()//2 , HEIGHT//2 - text.get_height()//2 + 30))
				text = FONT.render("CLEARED !", 1, (0,0,0))
				WIN.blit(text , (WIDTH//2 - text.get_width()//2 , HEIGHT//2 - text.get_height()//2 + 60))
				
			pygame.display.update()
			pygame.time.delay(1500)
			game_info.started = True

		if game_info.finished():
			game_info.reset()
			score = 0
			text = FONT.render("YOU WON !", 1, (0,0,0))
			WIN.blit(text , (WIDTH//2 - text.get_width()//2 , HEIGHT//2 - text.get_height()//2 + 20))
			pygame.display.update()
			pygame.time.delay(1500)
			game_info.started = True

		pygame.display.update()
			

if __name__ == '__main__':
	main()
