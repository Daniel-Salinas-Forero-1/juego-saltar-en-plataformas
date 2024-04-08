import pygame 

class bloque(pygame.sprite.Sprite):#lo que me permite acá es inicializar la clase la cual podré crear el bloque
	def __init__(self,pos,size):#definimos los parámetros del bloque, con posición y tamaño
		super().__init__()
		self.image = pygame.Surface((size,size))#definimos la superficie del bloque
		self.image.fill('grey')
		self.rect = self.image.get_rect(topleft = pos)#get_rect(), crea el objeto del bloque a partir de la superficie y posición dada

	def update(self,x_shift):
		self.rect.x += x_shift