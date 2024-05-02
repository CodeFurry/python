#!/bin/python3

import pygame # main module
from sys import exit as closeApplication # for safe exit
from random import randrange # for random numbers shuffling

class subjectClass(pygame.sprite.Sprite):
	def __init__(self, display: pygame.surface.Surface, rect: tuple, dest: tuple, color: str | tuple):

		'''
		class that will store all the spawned balls and their logic
		'''

		super().__init__()
		self.DISPLAY: pygame.surface.Surface = display
		self.image: pygame.surface.Surface = pygame.Surface(rect)
		self.rect: pygame.rect.Rect = self.image.get_rect(center = dest)
		self.vector: pygame.math.Vector2 = pygame.math.Vector2()
		self._jump_vel: int = 15
		self.update_subject: bool = True
		self.color: str | tuple = color

	@property
	def jump_vel(self):
		print(f"{self._jump_vel} is current velocity")
		return self._jump_vel

	@jump_vel.setter
	def jump_vel(self, value):
		print(f"{self.vector.y} is current vector")
		self._jump_vel = value

	@jump_vel.deleter
	def jump_vel(self):
		print("deleted subject's jump velocity")
		self.update_subject = False
		del self._jump_vel

	def jump(self):
		self.vector.y -= self._jump_vel

	def update(self, gravity):
		if self.update_subject:
			pygame.draw.ellipse(self.DISPLAY, self.color, self.rect)
			self.vector.y += gravity
			self.rect.y += self.vector.y

		if self._jump_vel < 0:
			print("removing a subject from class")
			self.kill()

class mainClass:
	def __init__(self):

		'''
		base game class that will operete everything
		'''

		self.clock: pygame.time.Clock = pygame.time.Clock()
		self.DISPLAY: pygame.surface.Surface = pygame.display.set_mode((800, 600))
		self.gravity: float = 0.5
		self.load_vars()

	def load_vars(self):
		self.subject: pygame.sprite.Group = pygame.sprite.Group()

	def update(self):
		for subject in self.subject.sprites():
			subject.update(self.gravity)

			if subject.rect.bottom > 600:
				subject.rect.bottom = 600
				subject.jump_vel -= self.gravity * 4
				subject.vector.y = 0
				subject.jump()

	def execute(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit(); closeApplication()
				if event.type == pygame.MOUSEBUTTONDOWN:
					color = (randrange(0, 255), randrange(0, 255), randrange(0, 255))
					size = randrange(15, 30)
					subject: __main__.subjectClass = subjectClass(self.DISPLAY, (size, size), event.pos, color)
					self.subject.add(subject)

			self.DISPLAY.fill((50, 50, 50)); self.update()
			pygame.display.update(); self.clock.tick(60)

main_object = mainClass()
main_object.execute()
