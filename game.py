import pygame
from pygame.locals import*
from time import sleep

class Sprite():
	def __init__(self, x1, y1, w1, h1, image_url):
		self.x = x1
		self.y = y1
		self.w = w1
		self.h = h1
		self.image = pygame.image.load(image_url)

	def isMario():
		return False

	def isPipe():
		return False
	
	def isGoomba():
		return False

	def isFireball():
		return False

class Mario():
	def __init__(self, x, y, w, h, image_url):
		Sprite.__init__(self, x, y, w, h, image_url)
		self.currentImage = 0
		self.vertVelocity = 1.2
		self.prevX = 0
		self.prevY = 0
		self.numFramesInAir = 0
		self.rightFacing = True
		
		self.images = []
		self.images.append(pygame.image.load("mario1.png"))
		self.images.append(pygame.image.load("mario2.png"))
		self.images.append(pygame.image.load("mario3.png"))
		self.images.append(pygame.image.load("mario4.png"))
		self.images.append(pygame.image.load("mario5.png"))

	def update(self):
		self.vertVelocity += 1.2
		self.y += self.vertVelocity
		self.numFramesInAir += 1

		if(self.y > 400 - self.h):
			self.vertVelocity = 0
			self.y = 400 - self.h
			self.numFramesInAir = 0

	def getOutOfPipe(self, pipe):
		marioLeft   = self.x
		marioRight 	= self.x + self.w
		marioHead 	= self.y
		marioFeet 	= self.y + self.h

		spriteLeft 	= pipe.x
		spriteRight = pipe.x  + pipe.w
		spriteTop 	= pipe.y
		spriteBot 	= pipe.y  + pipe.h


		if marioRight >= spriteLeft and self.prevX + self.w <= spriteLeft:
			self.x = spriteLeft - self.w
			
		if(marioLeft <= spriteRight and self.prevX >= spriteRight):
			self.x = spriteRight
		
		if(marioFeet >= spriteTop and marioFeet <= spriteBot and self.prevY + self.h <= spriteTop):
			self.y = spriteTop - self.h
			self.numFramesInAir = 0
			self.vertVelocity = 0
		
		if(marioHead <= spriteBot and self.prevY >= spriteBot):
			self.y = spriteBot
			self.vertVelocity = 0
		
	def setPreviousPosition(self):
		self.prevX = self.x
		self.prevY = self.y
	
	def changeImageState(self):
		self.currentImage += 1
		if(self.currentImage > 4):
			self.currentImage = 0
		self.image = self.images[self.currentImage]

	def isMario(self):
		return True
	
	def isGoomba(self):
		return False
	
	def isFireball(self):
		return False
	
	def isPipe(self): 
		return False
	


class Pipe():
	def __init__(self, x, y, w, h, image_url):
		Sprite.__init__(self, x, y, w, h, image_url)
		self.rightFacing = None
	
	def update(self):
		return

	def isPipe(self):
		return True
	
	def isGoomba(self):
		return False
	
	def isFireball(self):
		return False
	
	def isMario(self):
		return False
	


class Goomba():
	def __init__(self, x, y, w, h, image_url):
		Sprite.__init__(self, x, y, w, h, image_url)
		self.onFire = False
		self.goombaDied = False
		self.rightFacing = False
		self.offScreen = False
		self.xVelocity = 3
		self.vertVelocity = 1.2
		self.fireCount = 0
	

	def update(self):
		self.setPreviousPosition()
		self.x += self.xVelocity 

		self.vertVelocity += 1.2
		self.y += self.vertVelocity

		if(self.y > 400 - self.h):
			self.vertVelocity = 0
			self.y = 400 - self.h
		
		if(self.onFire):
			self.xVelocity = 0
			self.image = pygame.image.load("goomba_fire.png")
		
		while(self.onFire):
			self.fireCount += 1
			if(self.fireCount < 50):
				break
			if(self.fireCount > 50):
				self.goombaDied = True
				break
			

	def reverseDirection(self, pipe):
		if(self.x + self.w >= pipe.x and self.prevX + self.w <= pipe.x):
			self.xVelocity = -self.xVelocity
			self.rightFacing = not self.rightFacing
		
		if(self.x <= pipe.x  + pipe.w and self.prevX >= pipe.x  + pipe.w):
			self.xVelocity = -self.xVelocity
			self.rightFacing = not self.rightFacing
		
		if(pipe.y <= self.y + self.h and self.y + self.h <= pipe.y  + pipe.h and self.prevY + self.h <= pipe.y):
			self.y = pipe.y - self.h
			self.vertVelocity = 0
		
		if(self.y >= pipe.y + pipe.h and self.prevY >= pipe.y + pipe.h):
			self.y = pipe.y + pipe.h
			self.vertVelocity = 0
		
	
	def setPreviousPosition(self):
		self.prevX = self.x
		self.prevY = self.y

	def isGoomba(self):
		return True

	def isFireball(self):
		return False

	def isMario(self):
		return False

	def isPipe(self):
		return False




class Fireball():
	def __init__(self, x, y, w, h, image_url, goingRight):
		Sprite.__init__(self, x, y, w, h, image_url)
		self.xVelocity = 3
		self.goingRight = goingRight
		self.rightFacing = None
		self.vertVelocity = 1.2

	def update(self):
		self.vertVelocity += 1.2
		if(self.goingRight == True):
			self.x += self.xVelocity
		elif(self.goingRight == False):
			self.x -= self.xVelocity
		
		self.y += self.vertVelocity

		if(self.y > 400 - self.h):		
			self.y = 400 - self.h
			self.vertVelocity = -15

	def isGoomba(self):
		return False
	
	def isFireball(self):
		return True
	
	def isMario(self):
		return False
	
	def isPipe(self):
		return False
	

class View():
	def __init__(self, model):
		screen_size = (950,500)
		self.screen = pygame.display.set_mode(screen_size, 32)
		self.ground = pygame.image.load("ground.png")
		self.model = model
		self.model.rect = self.ground.get_rect()
		
	def update(self):
		scrollpos = self.model.mario.x - 100
		self.screen.fill([123, 145, 215])
		resizedGround = pygame.transform.scale(self.ground, (500, 100))

		#Draw Sprites
		for i in range(len(self.model.sprites)):
			sprite = self.model.sprites[i]
			resize = pygame.transform.scale(sprite.image, (sprite.w, sprite.h))

			if(sprite.rightFacing == None):
				self.screen.blit(resize, (sprite.x - scrollpos, sprite.y))
			elif(sprite.rightFacing == True):
				self.screen.blit(resize, (sprite.x - scrollpos, sprite.y))
			elif(sprite.rightFacing == False):
				flip = pygame.transform.flip(resize, True, False)
				self.screen.blit(flip, (sprite.x - scrollpos, sprite.y))


		#Draw Ground
		self.screen.blit(resizedGround, (0 - scrollpos, 400))
		self.screen.blit(resizedGround, (500 - scrollpos, 400))
		self.screen.blit(resizedGround, (-500 - scrollpos, 400))		
		self.screen.blit(resizedGround, (1000 - scrollpos, 400))
		self.screen.blit(resizedGround, (-1000 - scrollpos, 400))
		pygame.display.flip()


class Controller():
	def __init__(self, model):
		self.model = model
		self.keyRight = False
		self.keyLeft = False
		self.keep_going = True

	def update(self):
		self.model.mario.setPreviousPosition()
		for event in pygame.event.get():
			if event.type == QUIT:
				self.keep_going = False
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					self.keep_going = False
				if event.key == K_LCTRL and K_RCTRL:
					self.model.sprites.append(Fireball(self.model.mario.x, self.model.mario.y, 47, 47, "fireball.png", self.model.mario.rightFacing))

		keys = pygame.key.get_pressed()
		if keys[K_LEFT]:
			self.model.mario.rightFacing = False
			self.model.mario.x-=4
			self.model.mario.changeImageState()

		if keys[K_RIGHT]:
			self.model.mario.rightFacing = True
			self.model.mario.x+=4
			self.model.mario.changeImageState()

		if keys[K_SPACE]:	
			if(self.model.mario.numFramesInAir < 5):
				self.model.mario.vertVelocity = -20

class Model():
	def __init__(self):
		self.sprites = []
		self.mario = Mario(50, 50, 60, 95, "mario1.png")
		self.sprites.append(self.mario)

		self.sprites.append(Pipe(150, 300, 55, 400, "pipe.png"))
		self.sprites.append(Pipe(0, 150, 55, 100, "pipe.png"))
		self.sprites.append(Goomba(200, 200, 37, 45, "goomba.png"))
		self.sprites.append(Pipe(300, 300, 55, 400, "pipe.png"))
		self.sprites.append(Goomba(500, 200, 37, 45, "goomba.png"))

		self.sprites.append(Pipe(500, 150, 55, 400, "pipe.png"))
		self.sprites.append(Goomba(0, 200, 37, 45, "goomba.png"))
		self.sprites.append(Pipe(650, 300, 55, 400, "pipe.png"))
	

	def update(self):
		for i in range(len(self.sprites)):
			self.sprites[i].update()

			if(self.sprites[i].isMario()):
			
				for j in range(len(self.sprites)):
					check = self.isThereACollision(self.sprites[i], self.sprites[j])

					#Case 1, Mario collides with pipe
					if(check == True and self.sprites[j].isPipe()):
						self.mario.getOutOfPipe(self.sprites[j])
					
					#Case 2, Mario hits a goomba
					if(check == True and self.sprites[i].isGoomba()):
						self.sprites[i].goombaGameOver()
					
			#GOOMBA COLLISION
			#Cases 3 and 4
			if(self.sprites[i].isGoomba()):
			
				#If there are any invisible sprites, delete them
				#Is goomba onfire for too long?
				#Is goomba offscreen?
				if((self.sprites[i]).goombaDied == True):
					self.sprites.pop(i)
					return
			
				for j in range(len(self.sprites)):
				
					check = self.isThereACollision(self.sprites[i], self.sprites[j])
					#Case 3, Goomba hits a pipe
					if(check and self.sprites[j].isPipe()):
					
						#Switch Direction
						(self.sprites[i]).reverseDirection(self.sprites[j])
					
					#Case 4, Goomba hits a fireball
					if(check and self.sprites[j].isFireball()):
					
						#Set to onfire
						if(self.sprites[j].isFireball()):
							self.sprites.pop(j)
							self.sprites[i].onFire = True
							return
						
			#FIREBALL COLLISION
			#Case 5
			if(self.sprites[i].isFireball()):
			
				for j in range(len(self.sprites)):
				
					check = self.isThereACollision(self.sprites[i], self.sprites[j])

					check2 = self.isOffscreen(self.sprites[i], self.mario.x - 100)
					
					if(check2 == True):
						self.sprites.pop(i)
						return

	def isOffscreen(self, a, scrollpos):
		
		if(a.x - scrollpos > 950):
			return True
		if(a.x - scrollpos < -50):
			return True
		else:
			return False
		
	#Collision check sprites a and b. Sprites: Mario, Goomba, Pipe, Fireball
	def isThereACollision(self, a, b):
	
		aLeft 	= a.x
		aRight 	= a.x + a.w
		aTop 	= a.y
		aBot 	= a.y + a.h

		bLeft 	= b.x
		bRight 	= b.x  + b.w
		bTop 	= b.y
		bBot 	= b.y  + b.h
		
		#if there is collision
		if (aRight < bLeft):
			return False
		if (aLeft > bRight):
			return False
		if (aBot < bTop):
			return False
		if (aTop > bBot):
			return False

		#if he fails any check, he is colliding
		else:		
			return True
		
	

print("Use the arrow keys to move. Press Esc to quit.")
pygame.init()
m = Model()
v = View(m)
c = Controller(m)
while c.keep_going:
	c.update()
	m.update()
	v.update()
	sleep(0.025)
print("Goodbye")

