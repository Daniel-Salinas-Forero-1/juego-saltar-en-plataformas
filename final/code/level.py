import pygame 
from bloque import bloque 
from settings import tamaño_bloque, screen_width
from player import Player


class Level:
	def __init__(self,level_data,surface):#creamos el constructor de la clase con el level_data(para poder pasarle distintos diseños de nivel) y la superficice
		
		# variables
		self.display_surface = surface 
		self.setup_level(level_data)#enviamos a la función de crear nivel la varaible level_data
		self.world_shift = 0#esta variable servirá cuando se haga el movimiento de cámara
		self.current_x = 0

		

	def get_player_on_ground(self):
		if self.player.sprite.on_ground:
			self.player_on_ground = True
		else:
			self.player_on_ground = False


	def setup_level(self,layout):#función que para cada 'X', dibujará un bloque
		self.bloque = pygame.sprite.Group()#usamos el método Group de sprite, para poder manejar varios objetos de tipo sprite, lo cual servirá para crear los bloques
		self.player = pygame.sprite.GroupSingle()#en caso contrario de group, single group lo hace para un sólo objeto, en este caso el jugador

		for row_index,row in enumerate(layout):#como desconoceremos la posición de las X para los bloques, primero usamos el método enumerate el cual nos dirá el índice en dónde está parado el for en la lista
			for col_index,cell in enumerate(row):#Itero entre cada fila de la matriz
				x = col_index * tamaño_bloque
				y = row_index * tamaño_bloque
				
				if cell == 'X':#si hay una X en esa posición, llamamos a la clase bloque y le mandamos los parámetros pertinentes, su posición y el tamaño
					rectangulo = bloque((x,y),tamaño_bloque)
					self.bloque.add(rectangulo)
				if cell == 'P':#si ha una P en esa posición, dibujo al jugadorf con las descripciones dadas en la siguiente línea
					player_sprite = Player((x,y),self.display_surface)
					self.player.add(player_sprite)

	def scroll_x(self):#función para la "camara" del juego
		player = self.player.sprite#instancio el jugador
		player_x = player.rect.centerx#instancio la coordenada del jugador en x
		direction_x = player.direction.x#instancio la direccion

		if player_x < screen_width / 4 and direction_x < 0:#calculamos el límite de la pantalla
			self.world_shift = 8#velocidad de movimiento de cámara en derecha
			player.speed = 0#como haremos el efecto de cámara, necesitamos que la velocidad del jugador sea 0 en ese momento de la pantalla
		elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
			self.world_shift = -8#velocidad de movimiento de cámara en izquierda
			player.speed = 0
		else:
			self.world_shift = 0#sino se cumple alguna de las 2 condiciones, no hay movimiento de cámara
			player.speed = 8

	def horizontal_movement_collision(self):
		player = self.player.sprite
		player.rect.x += player.direction.x * player.speed#como es movimiento horizontal, necesito los valores de la direccion y la velocidad del jugador

		for sprite in self.bloque.sprites():#recorro en todos los bloques posibles
			if sprite.rect.colliderect(player.rect):#usamos colliderect para las colisiones con los bloques. mandándole a este jugador.rect
				if player.direction.x < 0: #si la direccion del jugador es menor que 0, se está moviendo a la izquierda
					player.rect.left = sprite.rect.right#la colision seria del jugador que está a la izquierda, con el bloque a la derecha
					player.on_left = True
					self.current_x = player.rect.left#momento en el que jugador está en la izquierda
				elif player.direction.x > 0:#si la direccion del jugador es menor que 0, se está moviendo a la derecha
					player.rect.right = sprite.rect.left#la colision seria del jugador que está a la derecha, con el bloque a la izquierda
					player.on_right = True
					self.current_x = player.rect.right#momento en el que jugador está en la derecha
	

	def vertical_movement_collision(self):
		player = self.player.sprite
		player.gravedad()#aplicamos gravedad para la colision

		for sprite in self.bloque.sprites():#nuevamente recorremos  los bloques los cuáles ocurra la colision
			if sprite.rect.colliderect(player.rect):
				if player.direction.y > 0: #si la direccion del jugador es mayor a 0, el jugador está "cayendo", colisionando hacia el bloque
					player.rect.bottom = sprite.rect.top#la colision seria del jugador que está a la abajo, con el bloque a la arriba
					player.direction.y = 0
					player.on_ground = True#el jugador está  en el piso, esto servirá para evitar que el jugador salte de forma infinita más abajo
				elif player.direction.y < 0:#si la direccion del jugador es mayor a 0, el jugador está "subiendo", colisionando hacia el bloque

					player.rect.top = sprite.rect.bottom#la colision seria del jugador que está a la arriba, con el bloque a la abajo
					player.direction.y = 0
					player.on_ceiling = True#el jugador está  en el techo, esto servirá para evitar que el jugador salte de forma infinita más abajo

		if player.on_ground and player.direction.y < 0 or player.direction.y > 1:#esto evaluá si eljugador está en el suelo y si está saltado o cayendo (de ahí si es menor a 0 o mayor 1), el jugador no puede estar en el suelo 
			player.on_ground = False
		if player.on_ceiling and player.direction.y > 0.1:#esto hace que si el jugador está en un techo, pueda seguir saltando, por eso la comparación es que si es menor a 0.1, porque no está totalmente en el suelo
			player.on_ceiling = False

	def run(self):
	
		# dibujar los bloques en el nivel
		self.bloque.update(self.world_shift)
		self.bloque.draw(self.display_surface)
		self.scroll_x()


		# el jugador con sus animaciones y colisiones 
		self.player.update()
		self.horizontal_movement_collision()
		self.get_player_on_ground()
		self.vertical_movement_collision()
		self.player.draw(self.display_surface)
