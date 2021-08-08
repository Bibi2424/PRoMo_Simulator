import pygame
from pygame.locals import *



BLACK = (0, 0, 0)
BACKGROUND_COLOR = (32, 32, 32)
RESOLUTION = (1200, 720)



class Terrain(pygame.Surface):
	LINE_COLOR = (64, 64, 64)
	LINE_SPACE = 50
	# LINE_COLOR = 'test'

	def __init__(self, size):
		super().__init__(size)
		width, height = size
		
		self.font = pygame.font.SysFont('arial', 12, True)
		self.fill(BACKGROUND_COLOR)

		# Grid
		color_horizontal = self.LINE_COLOR if self.LINE_COLOR != 'test' else (0, 128, 0)
		for i in range(0, height, self.LINE_SPACE):
			pygame.draw.line(self, color_horizontal, (0, i), (width, i), 1)
		pygame.draw.line(self, color_horizontal, (0, height - 1), (width, height - 1), 1)

		color_vertical = self.LINE_COLOR if self.LINE_COLOR != 'test' else (0, 0, 128)
		for i in range(0, width, self.LINE_SPACE):
			pygame.draw.line(self, color_vertical, (i, 0), (i, height), 1)
		pygame.draw.line(self, color_vertical, (width - 1, 0), (width - 1, height), 1)

		# coord
		for i in range(0, height, self.LINE_SPACE):
			for j in range(0, width, self.LINE_SPACE):
				surface = self.font.render(f'{i // self.LINE_SPACE}.{j // self.LINE_SPACE}', True, self.LINE_COLOR)
				self.blit(surface, surface.get_rect(center=(i + self.LINE_SPACE // 2, j + self.LINE_SPACE // 2)))



class Camera:
	def __init__(self, screen, background, sprite_group, target = None):
		self.screen = screen
		self.target = target
		self.background = background
		self.sprites = sprite_group

		self.camera_offset = (0, 0)
		self.scale = 1
		# self.scale = self.screen.get_size()[1] / self.background.get_size()[1]	# For auto scaling at init
		self.pan_speed = 5


	def add_sprite(self, sprite):
		self.sprites.add(sprite)


	def process_event(self, event):
		if event.type == KEYDOWN:
			if event.key == K_m:
				self.scale += 0.1
			elif event.key == K_n:
				self.scale -= 0.1 if self.scale >= 0.2 else 0


	def update(self):
		# TODO: pan speed could be made independant of zoom

		keys = pygame.key.get_pressed()

		if keys[K_LEFT] == True:
			x, y = self.camera_offset
			self.camera_offset = (x - self.pan_speed, y)

		elif keys[K_RIGHT] == True:
			x, y = self.camera_offset
			self.camera_offset = (x + self.pan_speed, y)

		if keys[K_UP] == True:
			x, y = self.camera_offset
			self.camera_offset = (x, y - self.pan_speed)

		elif keys[K_DOWN] == True:
			x, y = self.camera_offset
			self.camera_offset = (x, y + self.pan_speed)


	def draw(self):
		self.screen.fill(BLACK)

		# Make temp surface and add background
		temp_surface = pygame.Surface(self.background.get_size())
		temp_surface.blit(self.background, (0, 0))

		# Add sprites
		self.sprites.draw(temp_surface)

		# Zoom
		new_size = tuple(int(i*self.scale) for i in temp_surface.get_size())
		scaled_surface = pygame.transform.scale(temp_surface, new_size)

		# Draw on screen with offset
		if not self.target:
			center = tuple(i - j for i, j in zip(self.screen.get_rect().center, self.camera_offset))
			self.screen.blit(scaled_surface, scaled_surface.get_rect(center = center))
		# Draw on screen centered on target
		else:
			target_center = tuple( j - int((i) * self.scale) for i, j in zip(self.target.rect.center, self.screen.get_rect().center))
			print(self.scale)
			print(target_center)
			self.screen.blit(scaled_surface, target_center)

		# To Mark the center for debug
		# screen_size = self.screen.get_rect().size
		# pygame.draw.line(self.screen, (128, 128, 128), (screen_size[0] // 2, 0), (screen_size[0] // 2, screen_size[1]))
		# pygame.draw.line(self.screen, (128, 128, 128), (0, screen_size[1] // 2), (screen_size[0], screen_size[1] // 2))



class Obstacle(pygame.sprite.Sprite):
	def __init__(self, pos, size, color = (128, 0, 0)):
		super().__init__()

		self.image = pygame.Surface(size)
		self.rect = self.image.get_rect(center = pos)

		self.image.fill(color)



class Character(pygame.sprite.Sprite):
	def __init__(self, pos, size, color = (0, 128, 0)):
		super().__init__()

		self.image = pygame.Surface(size)
		self.rect = self.image.get_rect(center = pos)
		self.image.fill(color)

		self.speed = 5


	def update(self):
		keys = pygame.key.get_pressed()

		if keys[K_w] == True:
			self.rect.center = (self.rect.center[0], self.rect.center[1] - self.speed)
		elif keys[K_s] == True:
			self.rect.center = (self.rect.center[0], self.rect.center[1] + self.speed)
		if keys[K_a] == True:
			self.rect.center = (self.rect.center[0] - self.speed, self.rect.center[1])
		elif keys[K_d] == True:
			self.rect.center = (self.rect.center[0] + self.speed, self.rect.center[1])




def main():

	# Pygame stuff init
	pygame.init()
	pygame.display.set_caption('Camera test')
	screen = pygame.display.set_mode(RESOLUTION)
	screen.fill(BLACK)

	clock = pygame.time.Clock()

	# Environment init
	terrain = Terrain((2000, 2000))

	sprites = pygame.sprite.Group()
	sprites.add(Obstacle((100, 200), (50, 50)))
	sprites.add(Obstacle((400, 400), (50, 50)))

	player = Character((500, 500), (100, 100))
	sprites.add(player)

	# Camera is init last since it needs reference to the rest
	# camera = Camera(screen, terrain, sprites)		# Handle Camera with arrows
	camera = Camera(screen, terrain, sprites, target = player)	# Camera will follow players

	running = True
	while running:

		# Event
		for event in pygame.event.get():

			if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
				running = False

			camera.process_event(event)

		# Update
		player.update()
		camera.update()

		# Draw
		camera.draw()

		# Update the screen
		pygame.display.update()

	pygame.quit()



if __name__ == "__main__":
	main()
