import math
import pygame
import random
import sys
import time

import behavior
import settings
import weapons

window_w_h = (settings.map_width, settings.map_height)
pygame.init()
screen = pygame.display.set_mode(window_w_h)
pygame.display.set_caption("WDWPG")
pygame.display.init()
#pygame.display.set_icon(pygame.image.load("pic/corpse.png")) #Later, I don't want to do it now...
bg_color=(0,0,0)
pygame.mouse.set_cursor(*pygame.cursors.diamond)
clock = pygame.time.Clock()

r = pygame.Rect(5, 5, 4, 3)

class Entity():
	def __init__(self, img):
		self.img = pygame.image.load("pics/{}.png".format(img)).convert_alpha()
		self.rect = self.img.get_rect()
		self.screen = screen
	def draw(self, offset):
		self.screen.blit(self.img, (self.pos[0] + offset[0], self.pos[1] + offset[1]))
	def get_rect(self):
		self.rect.topleft = self.pos
	def get_hit(self, bullet):
		if self.alive:
			self.HP -= bullet.damage
			if self.HP <= 0:
				self.die()
			return True
		else:
			return False
	def die(self):
		self.speed = 0
		self.alive = False
		self.last_animation = tick
		#animate death
	def attack(self, player):
		if self.alive and self.last_attacked + self.attack_cooldown < tick:
			player.HP -= self.damage
			self.last_attacked = tick
	def distance_from(self, entity):
		return math.sqrt(
			+ (entity.pos[0] - self.pos[0])**2
			+ (entity.pos[1] - self.pos[1])**2
			)
	def walk(self): #TODO
		"Resolves repositioning given speed, angle of movement and surface(eg. dead bodies)."
		pass

class Player(Entity): #regenerate after beeing idle for a while
	window_w_h = window_w_h
	draw_holded_weapon_bar_size = (272, 84)
	weapon = weapons.pistol
	current_weapon = "pistol"
	weapon_img = pygame.image.load("pics/pistol.png").convert_alpha()
	weapon_rect = weapon_img.get_rect()
	weapon_rect.center = (window_w_h[0]-draw_holded_weapon_bar_size[0]/2, window_w_h[1]-draw_holded_weapon_bar_size[1]/2)
	owned_weapons = []
	for w in dir(weapons):
		if not w.startswith("__"):
			owned_weapons.append(w)
	direction = (0, 0)
	pos = (600, 360)
	health_bar = (
		window_w_h[0]/4,
		window_w_h[1] * 7/8,
		window_w_h[0]/2,
		20,
		)
	def __init__(self):
		super().__init__("player")
		self.HP = 100
	def change_weapon(self):
		current = self.owned_weapons.index(self.current_weapon)
		if current + 1 < len(self.owned_weapons):
			self.current_weapon = self.owned_weapons[current + 1]
		else:
			self.current_weapon = self.owned_weapons[0]
		self.weapon = getattr(weapons, self.current_weapon)
		self.weapon_img = pygame.image.load("pics/{}.png".format(self.weapon["img"])).convert_alpha()
		self.weapon_rect = self.weapon_img.get_rect()
		self.weapon_rect.center = (window_w_h[0]-self.draw_holded_weapon_bar_size[0]/2, window_w_h[1]-self.draw_holded_weapon_bar_size[1]/2)
	def draw(self, offset):
		#pygame.draw.rect(screen, color, (x,y,width,height), thickness)
		self.screen.blit(self.img, (self.window_w_h[0]/2 + offset[0], self.window_w_h[1]/2 + offset[1]))
	def draw_health_bar(self):
		if self.HP < 100:
			#red
			self.screen.fill((255, 0, 0), self.health_bar)
			#green
			self.screen.fill((0, 255, 0), (self.health_bar[0], self.health_bar[1], self.health_bar[2]*self.HP/100, self.health_bar[3]))
	def draw_holded_weapon(self):
		#272, 184 - size
		self.screen.fill((169, 169, 169), (self.window_w_h[0]-self.draw_holded_weapon_bar_size[0], self.window_w_h[1]-self.draw_holded_weapon_bar_size[1], self.draw_holded_weapon_bar_size[0], self.draw_holded_weapon_bar_size[1]))
		self.screen.blit(self.weapon_img, self.weapon_rect)


class Bulp(Entity):
	"""A smurph(?) enemy that ignores obstacles and slowly moves towards the player. Their dead bodies slowes anyone passing them."""
	#TODO:  Terrain(dead bodies slowing down)
	speed = 0.75
	damage = 5
	attack_cooldown = 60
	def __init__(self, pos):
		super().__init__("bulp")
		self.pos = pos
		self.HP = 10
		self.stages = ["bulp", "bulp_animation_1", "bulp_animation_2", "bulp_dead"]
		self.stage = 0
		self.last_animation = -31
		self.alive = True
		self.last_attacked = 0
	def move(self):
		if self.alive:
			angle = fake_angle((
				player.pos[0] - self.pos[0],
				player.pos[1] - self.pos[1],
				))
			speed = (
				angle[0]*speed_konstant*self.speed,
				angle[1]*speed_konstant*self.speed,
				)
			self.pos = (self.pos[0] + speed[0], self.pos[1] + speed[1])
		else:
			if self.last_animation + 20 == tick and self.stage < 3: # len(self.stages) - 1
				self.last_animation = tick
				self.stage += 1
				self.img = pygame.image.load("pics/{}.png".format(self.stages[self.stage])).convert_alpha()

class Smurph(Entity):
	"""A galagal(?) enemy that ignores obstacles and charge at player."""
	speed_walking = 0.6
	damage = 15
	attack_cooldown = 60
	def __init__(self, pos):
		super().__init__("Smurph")
		self.pos = pos
		self.speed = self.speed_walking
		
		self.HP = 75
		self.alive = True
		self.last_attacked = -31

		self.AI = behavior.Smurph_AI
		self.AI_stage = None
		self.AI_recharged_at = 0
	def move(self):
		if self.alive:
			#start special move
			if self.AI_stage == None and self.distance_from(player) <= self.AI["distance"] and self.AI_recharged_at <= tick:
				print("ROAR!")
				self.AI_stage = 0
				self.AI_final_stage = len(self.AI["behavior"]) - 1
				self.AI_until = tick + self.AI["behavior"][0]["ticks"]
				self.speed = self.AI["behavior"][0]["speed"]
				if not self.AI["behavior"][0]["locked_direction"]:
					self.angle = fake_angle((
						player.pos[0] - self.pos[0],
						player.pos[1] - self.pos[1],
						))
			#special move proceed
			if self.AI_stage != None:
				if self.AI_until == tick:
					self.AI_stage += 1
					if self.AI_stage <= self.AI_final_stage:
						self.AI_until = tick + self.AI["behavior"][self.AI_stage]["ticks"] + 1
						self.speed = self.AI["behavior"][self.AI_stage]["speed"]
					else:
						self.AI_recharged_at = tick + self.AI["recharge"]
						self.speed = self.speed_walking
						self.AI_stage = None
				else:
					if not self.AI["behavior"][self.AI_stage]["locked_direction"]:
						self.angle = fake_angle((
							player.pos[0] - self.pos[0],
							player.pos[1] - self.pos[1],
							))
			#normal movement
			else:
				self.angle = fake_angle((
					player.pos[0] - self.pos[0],
					player.pos[1] - self.pos[1],
					))
			speed = (
				self.angle[0]*speed_konstant*self.speed,
				self.angle[1]*speed_konstant*self.speed,
				)
			self.pos = (self.pos[0] + speed[0], self.pos[1] + speed[1])

class Pillar(Entity):
	def __init__(self, pos):
		super().__init__("pillar")
		self.pos = pos


class Bullet(Entity):
	def __init__(self, pos):
		super().__init__("bullet")
		self.pos = pos
		self.lifespawn_in_ticks = player.weapon["bullet_lifespawn"]

def fake_angle(num):
	#TODO: radnomize a bit
	a = num[0]
	b = num[1]
	size = (math.sqrt(a**2 + b**2))
	if size == 0:
		return(0, 0)
	a_ = a/size
	b_ = b/size
	return (a_, b_)

player = Player()
speed_konstant = 2

#enemies
bulps = []
smurphs = []

bullets = []
to_shoot = False
next_shoot_avaible_at = 0

pillars = []
for x in range(5):
	for y in range(5):
		p = Pillar((x*100, y*100))
		pillars.append(p)

smurphs.append(Smurph((
	random.randint(int(player.pos[0] - window_w_h[0]/2), int(player.pos[0] + window_w_h[0]/2)),
	random.randint(int(player.pos[1] - window_w_h[1]/2), int(player.pos[1] + window_w_h[1]/2)),
	)))

tick = 0

while True:
	clock.tick(settings.FPS)
	tick += 1

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.display.quit()
			sys.exit()

		elif event.type == pygame.KEYDOWN:
			#mooving
			if event.key == pygame.K_w:
				player.direction = (player.direction[0], player.direction[1] - 1)
			elif event.key == pygame.K_s:
				player.direction = (player.direction[0], player.direction[1] + 1)
			elif event.key == pygame.K_a:
				player.direction = (player.direction[0] - 1, player.direction[1])
			elif event.key == pygame.K_d:
				player.direction = (player.direction[0] + 1, player.direction[1])

			#change weapon
			if event.key == pygame.K_v:
				player.change_weapon()

			#escape
			if event.key == pygame.K_ESCAPE:
				pygame.display.quit()
				sys.exit()

		elif event.type == pygame.KEYUP:
			#mooving
			if event.key == pygame.K_w:
				player.direction = (player.direction[0], player.direction[1] + 1)
			elif event.key == pygame.K_s:
				player.direction = (player.direction[0], player.direction[1] - 1)
			elif event.key == pygame.K_a:
				player.direction = (player.direction[0] + 1, player.direction[1])
			elif event.key == pygame.K_d:
				player.direction = (player.direction[0] - 1, player.direction[1])

		#shoting
		to_shoot = False
		if pygame.mouse.get_pressed()[0]:
			to_shoot = True

	#player movement
	angle = fake_angle(player.direction)
	player.pos = (player.pos[0] + angle[0]*speed_konstant, player.pos[1] + angle[1]*speed_konstant)

	mouse_pos = pygame.mouse.get_pos()

	player_relative_pos = (
		window_w_h[0]/2 + (mouse_pos[0] - window_w_h[0]/2)/2,
		window_w_h[1]/2 + (mouse_pos[1] - window_w_h[1]/2)/2,
		)

	#bulp spawning
	if tick % 120 == 0:
		bulps.append(Bulp((
			random.randint(int(player.pos[0] - window_w_h[0]/2), int(player.pos[0] + window_w_h[0]/2)),
			random.randint(int(player.pos[1] - window_w_h[1]/2), int(player.pos[1] + window_w_h[1]/2)),
			)))

	#bullet lifespawn
	#TODO: radnomize a bit
	for b in bullets:
		b.lifespawn_in_ticks -= 1
		if not b.lifespawn_in_ticks:
			del bullets[bullets.index(b)]

	#shoot bullet
	if to_shoot:
		if tick >= next_shoot_avaible_at:
			next_shoot_avaible_at = tick + int(settings.FPS / player.weapon["SPS"])

			bullet = Bullet(player.pos)

			#TODO: make it shoot not from center of player but at small distance from him (make it travel few pixels in angle direction before at spawning)
			angle = fake_angle((
				mouse_pos[0] - player_relative_pos[0],
				mouse_pos[1] - player_relative_pos[1],
				))
			bullet.speed = (
				angle[0]*player.weapon["speed"]*speed_konstant,
				angle[1]*player.weapon["speed"]*speed_konstant,
				)
			bullet.damage = player.weapon["damage"]
			bullets.append(bullet)

	#bullet movement
	for b in bullets:
		b.pos = (b.pos[0] + b.speed[0], b.pos[1] + b.speed[1])

	#enemy movement
	for enemy in bulps + smurphs:
		enemy.move()

	#collisions bullets with (pilliars, bulps, smurphs)
	for b in bullets:
		b.get_rect()
		for p in pillars:
			p.get_rect()
			collision_boolean = pygame.sprite.collide_rect(b, p)
			if collision_boolean:
				del bullets[bullets.index(b)]
		for bulp in bulps:
			bulp.get_rect()
			collision_boolean = pygame.sprite.collide_rect(b, bulp)
			if collision_boolean and b in bullets: 
				if bulp.get_hit(bullet):
					del bullets[bullets.index(b)]
		for smurph in smurphs:
			smurph.get_rect()
			collision_boolean = pygame.sprite.collide_rect(b, smurph)
			if collision_boolean and b in bullets: 
				if smurph.get_hit(bullet):
					del bullets[bullets.index(b)]

	#collisions (bulps, smurphs) with player
	player_pos = player.get_rect()
	for entity in bulps + smurphs:
		entity.get_rect()
		collision_boolean = pygame.sprite.collide_rect(player, entity)
		if collision_boolean:
			entity.attack(player)

	#drawing
	screen.fill(bg_color)
	r.center = mouse_pos
	pygame.draw.rect(screen, (255, 14, 78), (window_w_h[0]/2, window_w_h[1]/2, r[2], r[3]), 1)
	player_offset = (
		(mouse_pos[0] - window_w_h[0]/2)/player.weapon["zoom"],
		(mouse_pos[1] - window_w_h[1]/2)/player.weapon["zoom"],
		) #constant with meele/no weapon
	offset = (
		-player.pos[0] -player_offset[0] + window_w_h[0]/2,
		-player.pos[1] -player_offset[1] + window_w_h[1]/2,
		)
	for b in bulps:
		b.draw(offset)
	for s in smurphs:
		s.draw(offset)
	for b in bullets:
		b.draw(offset)
	for p in pillars:
		p.draw(offset)
	player.draw_health_bar()
	player.draw_holded_weapon()
	player.draw((-player_offset[0], -player_offset[1]))
	pygame.display.update()
