import pygame
import neat
import time
import math
import os
import pickle
import random
pygame.font.init()
pygame.init()

WIN_WIDTH = 500
WIN_HEIGHT = 640
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

win_surface = pygame.display.get_surface()
win_surface_width = win_surface.get_width()
win_surface_height = win_surface.get_height()

STAT_FONT = pygame.font.SysFont('comicsans', 50)

class Bird:
	MAX_ROTATION = 25
	ROT_VEL = 20
	ANIMATION_SPEED = 5
	GRAVITY = 0.5


	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.vel = 0
		self.tilt = 0
		self.img_count = 0
		self.tick_count = 0
		self.height = self.y
		self.imgs = BIRD_IMGS[0]
		self.animation_index = 0


	def jump(self):
		self.vel = -5
		self.tick_count = 0
		self.height = self.y




	def move(self):
		self.tick_count += 1
		displacement = self.vel * self.tick_count + 0.5 * self.tick_count ** 2

		if displacement >= 15:
			displacement = 15

		self.y = self.y + displacement


		if displacement < 0:
			if self.tilt < self.MAX_ROTATION:
				self.tilt = self.MAX_ROTATION
		else:
			if self.tilt > -90:
				self.tilt -= self.ROT_VEL

	# def draw(self, win):
	# 	self.img_count += 1
	# 	if self.img_count < len(BIRD_IMGS) * self.ANIMATION_SPEED:
	# 	    self.imgs = BIRD_IMGS[self.img_count // self.ANIMATION_SPEED]
	# 	else:
	# 	    self.img_count = 0
	# 	    self.imgs = BIRD_IMGS[0]
	# 	# if self.img_count < len(BIRD_IMGS) * self.ANIMATION_SPEED:
	# 	# 	self.imgs = BIRD_IMGS[self.img_count // self.ANIMATION_SPEED]
	# 	# elif self.img_count > len(BIRD_IMGS) * self.ANIMATION_SPEED:
	# 	# 	self.img_count = 0
	# 	# 	self.imgs = BIRD_IMGS[0]

	# 	win.blit(self.imgs, (self.x, self.y))


	def draw(self, win):
		self.img_count += 1

		if self.img_count % self.ANIMATION_SPEED == 0:
			self.animation_index += 1
			if self.animation_index >= len(BIRD_IMGS):
				self.animation_index = 0
		self.imgs = BIRD_IMGS[self.animation_index]

		if self.tilt <= -80:
			self.imgs = BIRD_IMGS[1]

		rotated_image = pygame.transform.rotate(self.imgs, self.tilt)
		new_rect = rotated_image.get_rect(center=self.imgs.get_rect(topleft=(self.x, self.y)).center)
		win.blit(rotated_image, new_rect.topleft)

	def get_mask(self):
		return pygame.mask.from_surface(self.imgs)



class Pipe:
    GAP = 200
    VELOCITY = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top_pipe = pygame.transform.flip(PIPE_IMG, False, True)
        self.bottom_pipe = PIPE_IMG
        self.passed = False
        self.set_height()

    def set_height(self):
        # self.heightt = random.randint(50, 250)
        self.height = random.randint(100, 275)

        self.top_pipe_height = self.height - self.top_pipe.get_height()

        self.bottom_pipe_height = self.height + self.GAP

    def move(self):
        self.x -= self.VELOCITY

    def draw(self, win):
        win.blit(self.top_pipe, (self.x, self.top_pipe_height))
        win.blit(self.bottom_pipe, (self.x, self.bottom_pipe_height))

    def collide(self, bird):
    	bird_mask = bird.get_mask()
    	top_mask = pygame.mask.from_surface(self.top_pipe)
    	bottom_mask = pygame.mask.from_surface(self.bottom_pipe)

    	top_offset = (self.x - bird.x, self.top_pipe_height - round(bird.y))
    	bottom_offset = (self.x - bird.x, self.bottom_pipe_height - round(bird.y))

    	t_point = bird_mask.overlap(top_mask, top_offset)
    	b_point = bird_mask.overlap(bottom_mask, bottom_offset)

    	if t_point != None or b_point != None:
    		return True
    	return False


class Base:
	VELOCITY = 5
	WIDTH = BASE_IMG.get_width()
	IMG = BASE_IMG

	def __init__(self, y): 
		self.y = y
		self.x1 = 0
		self.x2 = self.WIDTH

	def move(self):
		self.x1 -= self.VELOCITY
		self.x2 -= self.VELOCITY

		if self.x1 + self.WIDTH <= 0:
			self.x1 = self.x2 + self.WIDTH

		if self.x2 + self.WIDTH <= 0:
			self.x2 = self.x1 + self.WIDTH


	def draw(self, win):
		win.blit(self.IMG, (self.x1, self.y))
		win.blit(self.IMG, (self.x2, self.y))


def draw_window(win, bird, pipes, base, score):
	win.blit(BG_IMG, (0,0))

	for pipe in pipes:
		pipe.draw(win)

	text = STAT_FONT.render(str(score), 1, (255,255,255))
	win.blit(text, (WIN_WIDTH / 2 - 5, 0))

	bird.draw(win)
	base.draw(win)
	base.move()
	pygame.display.update()


def load_bird(filename):
    with open(filename, 'rb') as file:
        genome = pickle.load(file)
    return genome

def main():
	clock = pygame.time.Clock()

	local_dir = os.path.dirname(__file__)
	config_path = os.path.join(local_dir,  "config.txt")

	config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
	genome = load_bird('winner.pkl')
	net = neat.nn.FeedForwardNetwork.create(genome, config)

	bird = Bird(200, 200)
	pipes = [Pipe(400)]
	base = Base(600)

	score = 0

	run = True 
	while run:
		clock.tick(30)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		pipe_ind = 0
		if len(pipes) > 1 and bird.x > pipes[0].x + PIPE_IMG.get_width():
			pipe_ind = 1

		inputs = (bird.y, bird.y - pipes[pipe_ind].top_pipe_height, bird.y - pipes[pipe_ind].bottom_pipe_height)
		output = net.activate(inputs)

		if output[0] >= 0.5:
			bird.jump()

		add_pipe = False
		rem = []
		for pipe in pipes:
			

			if pipe.collide(bird):
				pass
				# genome.fitness -= 1
				# run = False

			if pipe.x + PIPE_IMG.get_width() <= 0:
				rem.append(pipe)

			if pipe.x <= bird.x + BIRD_IMGS[0].get_width():
				pipe.passed = True
				add_pipe = True

			pipe.move()

		if add_pipe and pipe.passed:
			score += 1
			# genome.fitness += 5
			# pipes.append(Pipe(500))

			# for random horizontal gap between pipes to test harder
			# (dec range for more closer gaps)
			pipe_x = pipes[-1].x + random.randint(200, 300)
			pipes.append(Pipe(pipe_x))

		for r in rem:
			pipes.remove(r)

		if bird.y + BIRD_IMGS[0].get_height() >= 600:
			# genome.fitness -= 1
			run = False


		bird.move()
		draw_window(win, bird, pipes, base, score)
	pygame.quit()
	quit()


main()