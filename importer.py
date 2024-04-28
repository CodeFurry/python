import pygame
pygame.init()

# please consider giving feedback

class imageCutter:
	def __init__(self, base_path: str, sheet: str | pygame.surface.Surface):
		''' defines a sheet or image as the spritesheet used in the whole program '''
    if isinstance(sheet, str):
			self.sheet = pygame.image.load(f"{base_path}/{sheet}")
		else: self.sheet = sheet

	def cutImages(self, width: int, height: int, frame: int):
    ''' cut images from a sprite sheet horizontally in squares '''
		surface = pygame.Surface((width, height), pygame.SRCALPHA)
		surface.blit(self.sheet, (0, 0), (width * frame, 0, width, height))
		return surface

	def cutTilesUndefined(self, width: int, height: int, start_hor: int, start_ver: int):
    ''' cut image from a spritesheet from any part of the sheet '''
		surface = pygame.Surface((width, height), pygame.SRCALPHA)
		surface.blit(self.sheet, (0, 0), (start_hor, start_ver, width, height))
		return surface

	def cutRandomTiles(self, width: int, height: int, start_hor: int, start_ver: int, scale: tuple = None):
    ''' works exactly like cutTilesUndefined function but with resizing, not useful at all '''
		surface = pygame.Surface((width, height), pygame.SRCALPHA)
		surface.blit(self.sheet, (0, 0), (start_hor, start_ver, width, height))
		surface = pygame.transform.scale(surface, scale) if scale != None else surface
		return surface
