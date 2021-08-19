import random
import pygame
import json
pygame.init()

win = pygame.display.set_mode((330, 550))
pygame.display.set_caption("Dodge the Cars!!")
game_start = True
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
purple = (255, 0, 180)
yellow = (255, 255, 0)
white = (255, 255, 255)
score = 0
highscore = ""


class Player_car:
	def __init__(self):
		self.vel = 11
		self.x = 155
		self.y = 270
		self.move_right = False
		self.move_left = False
		self.current_pos = ""
		self.not_moving = True

	def draw_car(self):
		pygame.draw.rect(win, blue, (self.x, self.y, 20, 10))
		pygame.draw.rect(win, blue, (self.x + 5, self.y + 10, 10, 10))
		pygame.draw.rect(win, blue, (self.x, self.y + 20, 20, 10))
		pygame.draw.rect(win, blue, (self.x, self.y, 20, 30), 1)

	def move_car(self):
		if self.move_right == False and self.move_left == False:
			self.not_moving = True
		else:
			self.not_moving = False
		
		if self.move_right:
			if self.current_pos in range(45, 156):
				if self.x < 155:
					self.x += self.vel
			if self.current_pos in range(155, 266):
				if self.x < 265:
					self.x += self.vel

		if self.move_left:
			if self.current_pos in range(45, 156):
				if self.x > 45:
					self.x -= self.vel
			if self.current_pos in range(155, 266):
				if self.x > 155:
					self.x -= self.vel

class Cars_To_Be_Dodged:
	def __init__(self):
		# The third item in each list inside the overall list is for checking whether a computer_car has reached..
		# the point where it can crash into the player's car
		self.possible_pos = [[45, -10, False], [155, -10, False], [265, -10, False]]
		self.car_colours = [green, red, purple, yellow]
		self.cars_list = []
		self.spawn = True
		self.colour = ""
		self.vel = 10

	#creates a random position and colour for a car
	def random_car_pos(self):
		if self.spawn:
			car_pos = random.choice(self.possible_pos)
			car_properties = car_pos.copy()
			colour = random.choice(self.car_colours)
			car_properties.append(colour)
			if len(self.cars_list) < 2:
				self.cars_list.append(car_properties)
				self.spawn = False
			if len(self.cars_list) >= 2:
				same_pos = car_properties[0]
				# checks if the last two cars are the same position with the new car that's about to be added..
				# ..to the cars_list to avoid too many cars appearing on the same lane, leaving the other lanes barren
				if self.cars_list[-1][0] == same_pos: 
					if self.cars_list[-2][0] == same_pos:
						pass
				else:
					self.cars_list.append(car_properties)
					self.spawn = False

	#renders or draws the cars on screen
	def spawn_cars(self):
		global score
		if self.cars_list:
			for position in self.cars_list:
				pygame.draw.rect(win, position[3], (position[0], position[1], 20, 10))
				pygame.draw.rect(win, position[3], (position[0] + 5, position[1] + 10, 10, 10))
				pygame.draw.rect(win, position[3], (position[0], position[1] + 20, 20, 10))
				pygame.draw.rect(win, position[3], (position[0], position[1], 20, 30), 1)
				position[1] += self.vel
				if position[1] > 550:
					self.cars_list.remove(position)
					score += 1
				if self.cars_list[-1][1] == 70:
					self.spawn = True


class Road:
	def __init__(self):
		# These are the lane partition positions
		self.left_lane = [[110, 555],[110, 515], [110, 475],[110, 435],[110, 395], [110, 355], [110, 315],
						  [110, 275], [110, 235], [110, 195], [110, 155], [110, 110], [110, 75], [110, 35], [110, -5]]
		self.right_lane = [[220, 555], [220, 515], [220, 475], [220, 435], [220, 395], [220, 355], [220, 315], 
						   [220, 275], [220, 235], [220, 195], [220, 155], [220, 110], [220, 75], [220, 35], [220, -5]]
		self.vel = 5

	def draw_lanes(self):
		for pos in self.left_lane:
			pygame.draw.line(win, white, (pos[0], pos[1]), (pos[0], pos[1] + 30), 2) 
		for pos in self.right_lane:
			pygame.draw.line(win, white, (pos[0], pos[1]), (pos[0], pos[1] + 30), 2)

	# This will make it look like the road is moving
	def move_lanes(self):
		for pos in self.left_lane:
			pos[1] += self.vel
			if pos[1] > 550:
				pos[1] = -5
		for pos in self.right_lane:
			pos[1] += self.vel
			if pos[1] > 550:
				pos[1] = -5


player = Player_car()
road = Road()
computer = Cars_To_Be_Dodged()
game_menu = True
game_over = False
text = pygame.font.SysFont("Helvetica", 18)
game_menu_text = pygame.font.SysFont("Helvetica", 22)
header_text = pygame.font.SysFont("Helvetica", 30)
help_txt = pygame.font.SysFont("Helvetica", 15)
nav_x = 15
nav_y = 79

def load_high_score():
	global highscore
	with open("high_score.json") as highscore_file:
		highscore = json.load(highscore_file)

def menu_display():
	win.fill((38, 78, 88))
	win.blit(header_text.render("DODGE THE CARS!!", True, red), (60, 20))
	win.blit(game_menu_text.render("NEW GAME", True, white), (20, 84))
	win.blit(game_menu_text.render("HIGH SCORES", True, white), (20, 128))
	win.blit(help_txt.render("Note: use the up and down arrow keys to navigate the menu", True, white), (5, 200))
	win.blit(help_txt.render("And use the SPACE key to select the option", True, white), (5, 230))
	pygame.draw.rect(win, (0, 0, 255), (nav_x, nav_y, 150, 40), 1)

def everything_stops():
	global game_over
	player.vel = 0
	computer.vel = 0
	road.vel = 0
	game_over = True

def start_game():
	# restores important values back to their initial state
	global score
	score = 0
	road.vel = 5
	player.vel = 11
	player.x = 155
	player.y = 270
	player.move_right = False
	player.move_left = False
	computer.spawn = True
	computer.vel = 10
	computer.cars_list = []

while game_start:
	pygame.time.delay(50)
	if game_menu:
		menu_display()
		load_high_score()
		start_game()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			game_start = False
		if not game_menu:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RIGHT and player.x < 265:
					player.move_right = True
					player.move_left = False
					player.current_pos = player.x
				if event.key == pygame.K_LEFT and player.x > 45:
					player.move_left = True
					player.move_right = False
					player.current_pos = player.x
		# Game menu navigations
		if game_menu:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					if nav_y == 79:
						nav_y = 123
					elif nav_y == 123:
						nav_y = 79
				if event.key == pygame.K_DOWN:
					if nav_y == 79:
						nav_y = 123
					elif nav_y == 123:
						nav_y = 79
				if event.key == pygame.K_SPACE:
					if nav_y == 79:
						game_menu = False
		if game_over:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					if nav_y == 79:
						game_menu = True
						game_over = False

	if not game_menu:
		win.fill((30, 30, 30))
		road.draw_lanes()
		road.move_lanes()
		computer.random_car_pos()
		computer.spawn_cars()
		player.move_car()
		player.draw_car()
		pygame.draw.rect(win, (0, 0, 0), (0, 0, 345, 5))
		win.blit(text.render("SCORE: " + str(score), True, (0, 0, 255)), (250, 5))

		for car in computer.cars_list:
			# If a computer_car has passed the point at which it can crash into a player's car
			if car[1] > 300:
				car[2] = True 

			# If a computer_car has not yet passed the point at which it can crash into a player's car..
			if not car[2]: 
				# ..Python should check for collision
				if player.y in range(car[1], car[1] + 30):
					if player.x in range(car[0], car[0] + 20):
						print(player.x)
						everything_stops()
				elif car[1] in range(player.y, player.y + 30):
					if player.x in range(car[0], car[0] + 20):
						print(player.x)
						everything_stops()
				if player.not_moving:
					if player.x in range(car[0] - 50, car[0] + 65):
						if car[1] + 30 >= player.y:
							everything_stops()

	if game_over:
		# Game over display message
		pygame.draw.rect(win, white, (80, 50, 230, 150))
		pygame.draw.rect(win, blue, (80, 50, 230, 30))
		win.blit(text.render("GAME OVER!", True, green), (130, 55))
		win.blit(text.render("Press SPACE to go to Main Menu", True, green), (90, 85))
		if score > highscore:
			win.blit(text.render("NEW HIGH SCORE: " + str(score), True, red), (110, 95))
			with open("high_score.json", "w") as highscore_file:
				json.dump(score, highscore_file)

	pygame.display.update()
pygame.quit()
