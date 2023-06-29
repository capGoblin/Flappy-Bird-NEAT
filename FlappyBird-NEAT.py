import pygame
import neat
import time
import math
import os
import random
import pickle
import configparser

pygame.font.init()
pygame.init()


WIN_WIDTH = 500
WIN_HEIGHT = 640
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

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

		# win.blit(self.imgs, (self.x, self.y))

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
        # self.top_pipe_height = self.height - self.GAP

        self.bottom_pipe_height = self.height + self.GAP
        # print(self.bottom_pipe_height)
        # # print(self.top_pipe_height)
        # print(self.top_pipe_height + self.top_pipe.get_height())
        # print((self.bottom_pipe_height) - (self.top_pipe_height + self.top_pipe.get_height()))
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


def draw_window(win, birds, pipes, base, score):
	win.blit(BG_IMG, (0,0))

	for pipe in pipes:
		pipe.draw(win)

	text = STAT_FONT.render(str(score), 1, (255,255,255))
	# win.blit(text, (WIN_WIDTH - text.get_width() - 10, -10))
	win.blit(text, (WIN_WIDTH / 2 - 5, 0))

	base.draw(win)
	for bird in birds:
		bird.draw(win)
	base.move()
	pygame.display.update()


def main(genomes, config):
	config_parser = configparser.ConfigParser()
	config_parser.read(config_path)

	fitness_threshold = float(config_parser['NEAT']['fitness_threshold'])

	nets = []
	ge = []
	birds = []

	for _, g in genomes:
		g.fitness = 0
		net = neat.nn.FeedForwardNetwork.create(g, config)
		nets.append(net)
		birds.append(Bird(200, 200))
		# birds.append(Bird(100, random.randint(200, 300)))
		ge.append(g)


	clock = pygame.time.Clock()
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
				pygame.quit()
				quit()

			# elif event.type == pygame.KEYDOWN:
			# 	if event.key == pygame.K_SPACE:
			# 		bird.jump()
		pipe_ind = 0
		if len(birds) > 0:
			if len(pipes) > 1 and birds[0].x > pipes[0].x + PIPE_IMG.get_width():
				pipe_ind = 1

		else:
			run = False
			break

		for x, bird in enumerate(birds):
			bird.move()
			# ge[x].fitness += 0.1

			output = nets[x].activate((bird.y, bird.y - pipes[pipe_ind].top_pipe_height, bird.y - pipes[pipe_ind].bottom_pipe_height))

			if output[0] >= 0.5:
				bird.jump()

		add_pipe = False
		rem = []
		for pipe in pipes:
			for x, bird in enumerate(birds):
				if pipe.collide(bird):
					ge[x].fitness -= 1
					birds.pop(x)
					nets.pop(x)
					ge.pop(x)
				# if not pipe.collide(bird):
				# 	ge[x].fitness += 5


				if pipe.x <= bird.x + BIRD_IMGS[0].get_width():
					pipe.passed = True
					add_pipe = True

			if pipe.x + PIPE_IMG.get_width() <= 0:
				rem.append(pipe)

			pipe.move()

		if add_pipe and pipe.passed:
			score += 1
			for g in ge:
				g.fitness += 5
			pipes.append(Pipe(600))

			# for random horizontal gap between pipes

			# pipe_x = pipes[-1].x + random.randint(200, 300)
			# pipes.append(Pipe(pipe_x))

		for r in rem:
			pipes.remove(r)

		for x, bird in enumerate(birds):
			if bird.y + BIRD_IMGS[0].get_height() >= 600 or bird.y < 0:
				ge[x].fitness -= 1
				birds.pop(x)
				nets.pop(x)
				ge.pop(x)


		# bird.move()
		draw_window(win, birds, pipes, base, score)


		for g in ge:
			if g.fitness >= fitness_threshold:
				winner = g
				run = False


def save_bird(bird, filename):
    with open(filename, 'wb') as file:
        pickle.dump(bird, file)

def run(config_path):


	config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, 
		neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
	p = neat.Population(config)

	p.add_reporter(neat.StdOutReporter(True))
	p.add_reporter(neat.StatisticsReporter())

	winner = p.run(main, 50)

	save_bird(winner, 'winner.pkl')

	return winner


if __name__ == "__main__":
	local_dir = os.path.dirname(__file__)
	config_path = os.path.join(local_dir,  "config.txt")
	winner = run(config_path)

