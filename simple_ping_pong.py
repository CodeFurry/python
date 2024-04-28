import pygame
from sys import exit as closeApplication
from random import randrange, randint
pygame.init()

class playerClass(pygame.sprite.Sprite):
	def __init__(self, size, color, dest, playerIndex):
		super().__init__()
		self.image = pygame.Surface(size); self.image.fill(color)
		self.rect = self.image.get_rect(topleft = dest)
		self.playerID = playerIndex
		self.vector = pygame.math.Vector2()
		self.verticalSpeed = 9
		self.playerScore = 0
		self.allocatedKeys = (pygame.K_w, pygame.K_s) if self.playerID == 0 else (pygame.K_UP, pygame.K_DOWN)

	def update(self):
		key = pygame.key.get_pressed()

		if key[self.allocatedKeys[0]]:
			self.vector.y = -1
		elif key[self.allocatedKeys[1]]:
			self.vector.y = 1
		else: self.vector.y = 0

		if self.rect.top < 0:
			self.verticalSpeed = 0; self.rect.y = 0
		elif self.rect.bottom > 600:
			self.verticalSpeed = 0; self.rect.bottom = 600
		else: self.verticalSpeed = 5

		self.rect.y += self.vector.y * self.verticalSpeed

class ballClass(pygame.sprite.Sprite):
	def __init__(self, size, color, dest, surface):
		super().__init__()
		self.image = pygame.Surface(size); self.color = color
		self.initCords = dest
		self.rect = self.image.get_rect(center = self.initCords)
		self.vector = pygame.math.Vector2()
		self.ballHorizontal, self.ballVertical = randint(-1, 1), randint(-1, 1)
		if self.ballHorizontal == 0: 
			self.ballHorizontal = randint(-1, 1)
		elif self.ballVertical == 0:
			self.ballVertical = randint(-1, 1)
		self.gameSurface = surface
		self.randomVector()

	def drawBall(self): pygame.draw.ellipse(self.gameSurface, self.color, self.rect)

	def randomVector(self, change = (True, True)):
		if change[0] and not change[1]:
			self.vector.x = (abs(randrange(4, 9)) * self.ballHorizontal)
			self.vector.y = (abs(self.vector.y) * self.ballVertical)
		elif change[1] and not change[0]:
			self.vector.x = (abs(self.vector.x) * self.ballHorizontal)
			self.vector.y = (randrange(4, 9) * self.ballVertical)
		elif change[0] and change[1]:
			self.vector.x = (abs(randrange(4, 9)) * self.ballHorizontal)
			self.vector.y = (abs(randrange(4, 9)) * self.ballVertical)
		else:
			self.vector.x = (abs(self.vector.x) * self.ballHorizontal)
			self.vector.y = (abs(self.vector.y) * self.ballVertical)

	def changeVector(self):
		if self.rect.y < 1:
			self.ballVertical = 1
			self.randomVector((False, False))
		elif self.rect.bottom > 600:
			self.ballVertical = -1
			self.randomVector((False, False))

	def moveBall(self):
		self.rect.x += self.vector.x
		self.rect.y += self.vector.y

	def update(self):
		self.changeVector()
		self.moveBall()
		self.drawBall()

class gameClass:
	def __init__(self):
		self.clock = pygame.time.Clock()
		self.DISPLAY = pygame.display.set_mode((800, 600))
		self.playerObject = pygame.sprite.Group()
		self.ballObject = pygame.sprite.GroupSingle()
		self.gameFont = pygame.font.SysFont(None, 50)
		self.gameRunning = False
		self.gameStartTime = 3
		self.playerScores = [0, 0]
		self.timerEvent = pygame.USEREVENT + 1
		self.gameStartTimer = pygame.time.set_timer(self.timerEvent, 1000)

		self.loadEverything()

	def gameStartCount(self):
		blittedCount = self.gameFont.render(f"{self.gameStartTime}", True, "black")
		if self.gameStartTime < 4: self.DISPLAY.blit(blittedCount, self.gameFontRect)

	def blitPlayerScore(self):
		player0 = self.gameFont.render(f"{self.playerScores[0]}", True, "red")
		player1 = self.gameFont.render(f"{self.playerScores[1]}", True, "blue")
		self.DISPLAY.blit(player0, self.playerScoresRects[0]); self.DISPLAY.blit(player1, self.playerScoresRects[1])

	def resetBall(self):
		self.ballObject.empty()
		self.ballObject.add(ballClass((20, 20), "orange", (400, 300), self.DISPLAY))

	def ballCollision(self):
		ballObject = self.ballObject.sprite
		for playerObject in self.playerObject.sprites():
			if playerObject.rect.colliderect(ballObject.rect):
				if playerObject.playerID == 0:
					ballObject.ballHorizontal = 1
				else: ballObject.ballHorizontal = -1
				ballObject.randomVector((True, False))
		if self.gameRunning:
			if ballObject.rect.x < -5:
				self.playerScores[1] += 1
				self.gameRunning = False
			elif ballObject.rect.x > 805:
				self.playerScores[0] += 1
				self.gameRunning = False
		else: pass

	def loadEverything(self):
		self.playerObject.add(playerClass((5, 150), "red", (5, 0), 0))
		self.playerObject.add(playerClass((5, 150), "blue", (790, 0), 1))
		self.ballObject.add(ballClass((20, 20), "white", (400, 300), self.DISPLAY))
		self.gameFontRect = pygame.Rect(50, 50, 0, 0); self.gameFontRect.center = (390, 300)
		playerScoresRects = [pygame.Rect(50, 50, 0, 0), pygame.Rect(50, 50, 0, 0)]
		playerScoresRects[0].center = (200, 300); playerScoresRects[1].center = (600, 300)
		self.playerScoresRects = tuple(playerScoresRects)

	def updateDisplay(self):
		pygame.draw.line(self.DISPLAY, "white", (399, 0), (399, 600), 1)
		self.ballCollision()
		self.playerObject.draw(self.DISPLAY)
		self.playerObject.update()
		self.blitPlayerScore()
		if self.gameRunning:
			self.ballObject.update()
		else: self.gameStartCount()

	def execute(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					closeApplication()
				if not self.gameRunning:
					if event.type == self.timerEvent:
						self.gameStartTime -= 1
						if self.gameStartTime == 0: self.gameRunning = True; self.gameStartTime = 4; self.resetBall()

			self.DISPLAY.fill((50, 155, 50)); self.updateDisplay()
			pygame.display.update(); self.clock.tick(60)

gameObject = gameClass()
gameObject.execute()
