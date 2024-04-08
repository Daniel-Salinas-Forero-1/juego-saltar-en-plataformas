import pygame 
from support import import_folder

class Player(pygame.sprite.Sprite):
	def __init__(self,pos,surface):
		super().__init__()
		self.import_character_assets()
		self.frame_index = 0#un numero el cual podemos elegir cuál de las animaciones se pueden ver en el frame 
		self.animation_speed = 0.09#la actualizacion de cada frame
		self.image = self.animations['idle'][self.frame_index]#animacion en la cual se inicializa el jugador
		self.rect = self.image.get_rect(topleft = pos)#get_rect(), crea el objeto del bloque a partir de la superficie y posición dada
		self.attacking=False
		self.attack_cooldown=1000#declaramos el cooldown del ataque para que luego en una función, le demos un tiempo de espera para cada ataque
		self.attack_time=0#tiempo en el que atacó lo inicializamos
	
		# player movement
		self.direction = pygame.math.Vector2(0,0)#dirección del jugador
		self.speed = 5#velocidad del jugador
		self.gravity = 0.8#gravedad de caida
		self.jump_speed = -16#distancia de salto

		# player status. Dependiendo del estado del jugador, se haría alguna cosa u otra 
		self.status = 'idle'
		self.facing_right = True
		self.on_ground = False
		self.on_ceiling = False
		self.on_left = False
		self.on_right = False

	def import_character_assets(self):
		character_path = '/Users/kiler/OneDrive/Escritorio/universidah/compugrafica/proyecto final/skul the samurai/graphics/character/'
		self.animations = {'idle':[],'run':[],'jump':[],'fall':[],'attack':[]}

		for animation in self.animations.keys():#importamos todas las animaciones dependiendo  de lo que se esté haciendo
			full_path = character_path + animation
			self.animations[animation] = import_folder(full_path)

	

	def animate(self):
		animation = self.animations[self.status]#la variable animacion obtiene el estado del jugador

		# loop over frame index 
		self.frame_index += self.animation_speed#como no hay un número ilimitado de frames en cada animacion, lo que se hace es que si, el frame index es mayor al tamaño de la animación escogida, este se vuelve en 0
		if self.frame_index >= len(animation):
			self.frame_index = 0

		image = animation[int(self.frame_index)]#todo esto que queda de la función, sirve para poder voltear la imagen, eso si el jugador está mirando la derecha o no
		if self.facing_right:
			self.image = image
		else:
			flipped_image = pygame.transform.flip(image,True,False)
			self.image = flipped_image

	

	def get_input(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_RIGHT]:
			self.direction.x = 1
			self.facing_right = True
		elif keys[pygame.K_LEFT]:
			self.direction.x = -1
			self.facing_right = False
		else:
			self.direction.x = 0

		if keys[pygame.K_z] and self.on_ground:#salta si y sólo si el jugador presiona la tecla y está en el piso
			self.jump()
			
		
		#ataques
		elif keys[pygame.K_x]and not self.attacking and self.on_ground:
			self.attacking=True
			self.attack_time= pygame.time.get_ticks()#obtiene el momento en el que se atacó
			print("attack")

	def get_status(self):#los "estados", en esta función, es  lo que nos permite averiguar qué está haciendo el jugador en este moemnto, para luego "animarlo" con sus respectivos sprites.
		if self.direction.y < 0:
			self.status = 'jump'
		elif self.direction.y > 1:
			self.status = 'fall'
		else:
			if self.direction.x != 0:
				self.status = 'run'
			else:
				self.status = 'idle'
		if self.attacking:
			self.direction.x=0
			self.direction.y=0
			if not 'attack' in self.status:
					self.status= self.status.replace('idle','attack')
			else:
					self.status=self.status+'attack'

			
			
		

	def gravedad(self):#función para la gravedad del muñeco
		self.direction.y += self.gravity
		self.rect.y += self.direction.y

	def jump(self):#función para el salto
		self.direction.y = self.jump_speed
	
	def cooldowns(self):
		current_time=pygame.time.get_ticks()
		if self.attacking:
			if current_time - self.attack_time >= self.attack_cooldown:#si es menor el tiempo actual menos el ataque que se hizo, comparado con el cooldown de ataque, se hará el efecto de esperar 500ms para el próximo ataque
				self.attacking=False



	def update(self):#básicamente este método a través de los get y demás, va obteniendo los inputs y va dibujándolos
		self.get_input()
		self.get_status()
		self.animate()
		self.cooldowns()
		