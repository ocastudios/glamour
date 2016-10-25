from settings import *


class GameCamera():
	def __init__(self,universe, goalpos= None):
		self.universe = universe
		self.end_x = float(self.universe.width)
		self.start_x = 0
		self.limit = 0.42
		self.count = 0
		if goalpos:
			self.universe.center_x = goalpos

	def update_all(self):
		princess_pos = self.universe.level.princesses[0].pos[0]
		princess_right = princess_pos+round(100*scale)
		princess_left = princess_pos
		if princess_right > (self.end_x - round(self.end_x*self.limit)):
			self.universe.speed -= round(self.count*scale)
			self.count += round(5*scale)
		elif princess_left < (self.start_x + round(self.end_x*self.limit)):
			self.universe.speed += round(self.count*scale)
			self.count += round(5*scale)
		else:
			self.count = 0
			if self.universe.speed != 0:
				if princess_right > (self.end_x - round(self.end_x*(self.limit+0.1))):
					self.universe.speed += round(1*scale)
				if princess_left < (self.start_x + round(self.end_x*(self.limit +0.1))):
					self.universe.speed -= round(1*scale)
			#Stop the camera
			if princess_left < self.end_x/2 < princess_right:
				self.count *= 0.8
				self.universe.speed *= 0.8 
