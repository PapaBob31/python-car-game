
import random
import pygame
import json
pygame.init()

win = pygame.display.set_mode((330, 550))
pygame.display.set_caption("Dodge the Cars!!")
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
purple = (255, 0, 180)
yellow = (255, 255, 0)
white = (255, 255, 255)
text = pygame.font.SysFont("Helvetica", 18)
game_menu_text = pygame.font.SysFont("Helvetica", 22)
header_text = pygame.font.SysFont("Helvetica", 30)
help_txt = pygame.font.SysFont("Helvetica", 15)


class Player_car:
	def __init__(self):
		self.vel = 10
		self.x = 155
		self.y = 270
		self.width = 20
		self.move_right = False
		self.move_left = False
		self.current_pos = ""
		self.jump_pos = ""
		self.moving = False
		self.jumping =  False
		# counter for how long the player will jump
		self.jump_count = 0
		self.margin = 5

	def draw_car(self):
		pygame.draw.rect(win, blue, (self.x, self.y, self.width, 10))
		pygame.draw.rect(win, blue, (self.x + self.margin, self.y + 10, self.width/2, 10))
		pygame.draw.rect(win, blue, (self.x, self.y + 20, self.width, 10))
		pygame.draw.rect(win, blue, (self.x, self.y, self.width, 30), 1)

	def set_car_direction(self, event):
		if not self.jumping:
			if event.key == pygame.K_RIGHT and self.x < 265:
				self.move_right = True
				self.move_left = False
				# the variable below stores the position at which a movement key is pressed
				self.current_pos = self.x
			if event.key == pygame.K_LEFT and self.x > 45:
				self.move_left = True
				self.move_right = False
				self.current_pos = self.x
		if not self.moving:
			if event.key == pygame.K_UP:
				self.jump_pos = self.x
				self.jumping = True

	def move_car(self):
		if self.x in range(45, 266, 110):
			self.moving = False
		else:
			self.moving = True
		
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

	def jump_over(self):
		if self.jumping:
			self.x = self.jump_pos - 10
			self.margin = 10
			self.width = 40
			self.jump_count += 10
			if self.jump_count == 100:
				self.width = 20
				self.margin = 5
				self.x = self.jump_pos
				self.jump_count = 0
				self.jump_pos = ""
				self.jumping = False


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

	# Creates a random position and colour for a car
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

	# Renders or draws the cars on screen
	def spawn_cars(self):
		global score
		if self.cars_list:
			for position in self.cars_list:
				pygame.draw.rect(win, position[3], (position[0], position[1], 20, 10))
				pygame.draw.rect(win, position[3], (position[0] + 5, position[1] + 10, 10, 10))
				pygame.draw.rect(win, position[3], (position[0], position[1] + 20, 20, 10))
				pygame.draw.rect(win, position[3], (position[0], position[1], 20, 30), 1)
				position[1] += self.vel
				if position[1] > 600:
					self.cars_list.remove(position)
					manager.score += 1
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


class Manager:
	"""Class that manages the data the game data"""
	def __init__(self):
		self.menu_nav_x = 15
		self.menu_nav_y = 79
		self.menu_select_width = 140 # Width of the box used for selecting options in menu
		self.menu_select_height = 40 # height of the box used for selecting options in menu
		self.score = 0
		self.highscore = 0
		self.game_menu = True
		self.game_over = False
		self.game_start = True
		self.display_high_score = False

	def display_menu(self):
		win.fill((38, 78, 88))
		win.blit(header_text.render("DODGE THE CARS!!", True, red), (60, 20))
		win.blit(game_menu_text.render("NEW GAME", True, white), (20, 84))
		win.blit(game_menu_text.render("RESET HIGHSCORE", True, white), (20, 128))
		win.blit(game_menu_text.render("HIGH SCORE: " + str(self.highscore), True, white), (20, 176))
		win.blit(help_txt.render("Note: use the up and down arrow keys to navigate the menu", True, white), (5, 220))
		win.blit(help_txt.render("And use the SPACE key to select the option", True, white), (5, 240))
		pygame.draw.rect(win, (0, 0, 255), (self.menu_nav_x, self.menu_nav_y, self.menu_select_width, self.menu_select_height), 1)

	def reset_highscore(self):
		with open("high_score.json", "w") as file:
			json.dump(0, file)
		self.highscore = 0

	def load_high_score(self):
		try:
			with open("high_score.json") as highscore_file:
				self.highscore = json.load(highscore_file)
		except (FileNotFoundError, json.decoder.JSONDecodeError):
			self.reset_highscore()

	def stop_everything(self):
		player.vel = 0
		player.jumping = False
		computer.vel = 0
		road.vel = 0
		self.game_over = True

	def reset_game(self):
		"""Sets important game data to their default values"""
		player.__init__()
		computer.__init__()
		road.__init__()
		self.score = 0
		self.game_menu = False
		self.game_over = False
		self.display_high_score = False

	def navigate_thru_menu(self, event):
		if event.key == pygame.K_UP:
			if self.menu_nav_y == 79:
				self.menu_nav_y = 123
			elif self.menu_nav_y == 123:
				self.menu_nav_y = 79
		if event.key == pygame.K_DOWN:
			if self. menu_nav_y == 79:
				self.menu_nav_y = 123
			elif self.menu_nav_y == 123:
				self.menu_nav_y = 79
		if event.key == pygame.K_SPACE:
			if self.menu_nav_y == 79:
				self.reset_game()
			if self.menu_nav_y == 123:
				self.reset_highscore()

manager = Manager()
manager.load_high_score()

def check_for_collisions():
	for car in computer.cars_list:
		# If a computer_car has passed the point at which it can crash into a player's car
		if car[1] > 300:
			car[2] = True 

		# If a computer_car has not yet passed the point at which it can crash into a player's car..
		if not car[2]: 
			# ..Python should check for collision
			if player.y in range(car[1], car[1] + 31):
				if player.x in range(car[0], car[0] + 21):
					manager.stop_everything()
				if player.x + player.width in range(car[0], car[0] + 21):
					manager.stop_everything()
			elif car[1] in range(player.y, player.y + 31):
				if player.x in range(car[0], car[0] + 21):
					manager.stop_everything()
				if player.x + player.width in range(car[0], car[0] + 21):
					manager.stop_everything()

def update_display_and_data():
	pygame.draw.rect(win, white, (50, 50, 230, 150))
	pygame.draw.rect(win, blue, (50, 50, 230, 30))
	win.blit(text.render("GAME OVER!", True, red), (100, 55))
	win.blit(text.render("Press SPACE to go to Main Menu,", True, green), (55, 100))
	win.blit(text.render("DOWN ARROW key to play again", True, green), (55, 130))
	if manager.score > manager.highscore:
		manager.display_high_score = True
		manager.highscore = manager.score
		with open("high_score.json", "w") as highscore_file:
			json.dump(manager.score, highscore_file)
		manager.highscore = manager.score
	if manager.display_high_score:
		win.blit(text.render("NEW HIGH SCORE: " + str(manager.score), True, red), (80, 155))

while manager.game_start:
	pygame.time.delay(50)
	if manager.game_menu:
		if manager.menu_nav_y == 123:
			manager.menu_select_width = 200
		else:
			manager.menu_select_width = 140
		manager.display_menu()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			manager.game_start = False
		if not manager.game_menu and not manager.game_over:
			if event.type == pygame.KEYDOWN:
				player.set_car_direction(event)
		if manager.game_menu:
			if event.type == pygame.KEYDOWN:
				manager.navigate_thru_menu(event)	
		if manager.game_over:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					manager.game_menu = True
					manager.game_over = False
				if event.key == pygame.K_DOWN:
					manager.reset_game()

	if not manager.game_menu:
		win.fill((30, 30, 30))
		road.draw_lanes()
		road.move_lanes()
		computer.random_car_pos()
		computer.spawn_cars()
		player.draw_car()
		player.move_car()
		player.jump_over()
		pygame.draw.rect(win, (0, 0, 0), (0, 0, 345, 5))
		win.blit(text.render("SCORE: " + str(manager.score), True, (0, 0, 255)), (250, 5))
		check_for_collisions()	

	if manager.game_over:
		update_display_and_data()	

	pygame.display.update()
pygame.quit()
