import pygame
from sys import exit as closeApplication
pygame.init()

class rocketClass:
	def __init__(self, size: tuple, dest: tuple, color: tuple | str):
		self.image = pygame.Surface(size); self.image.fill(color)
		self.rect = self.image.get_rect(midbottom = dest)
		self.vector = pygame.math.Vector2()
		self.DISPLAY = pg.display.get_surface()

	def gravity(self):
		self.vector.y += constant_g
		if self.rect.bottom > 664:
			self.rect.bottom = 664
			self.vector.y = 0

		self.rect.y += self.vector.y

	def input(self):
		mouse = pygame.mouse.get_pressed()
		if mouse[0]: self.vector.y -= 0.6

	def render(self):
		self.DISPLAY.blit(self.image, self.rect)

	def update(self):
		self.render()
		self.input()
		self.gravity()

class mainClass:
	def __init__(self):
		self.clock = pygame.time.Clock()
		self.DISPLAY = pygame.display.set_mode((832, 664))
		self.rocket = rocketClass((15, 100), (416, 664), "white")
		self.font = pygame.font.SysFont(None, 25)

	def display_info(self):
		info1 = self.font.render(f"net force: {int(-self.rocket.vector.y)}", True, "white")
		self.DISPLAY.blit(info1, (0, 0))

	def execute(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit(); closeApplication()

			self.DISPLAY.fill((50, 50, 50)); self.rocket.update(); self.display_info()
			pygame.display.update(); self.clock.tick(60)

# use left mouse button to make rocket rise
constant_g = 0.5
main_object = mainClass()
main_object.execute()
