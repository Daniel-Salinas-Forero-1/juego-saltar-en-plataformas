
import pygame, sys
from settings import * 
from level import Level
from pygame import mixer
# Pygame setup
pygame.mixer.init()
pygame.init()
background=pygame.image.load( "/Users/kiler/OneDrive/Escritorio/universidah/compugrafica/proyecto final/skul the samurai/graphics/fondo/space.jpg" )	
#pygame.mixer.music.load("/Users/kiler/OneDrive/Escritorio/universidah/compugrafica/1 - logic/1 - Basic platformer/music/background music/Hollow Knight OST - Greenpath.mp3")
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
level = Level(level_map,screen)#a partir de la clase level con su método, definimos el nivel basados en level_map y superficie

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		
		#pygame.mixer.music.play(-1)
	screen.blit(background,(0,0))
	level.run()
	pygame.display.update()
	
	clock.tick(60)