import pygame
import sys
import math

def rotate2d(pos, rad): 
	x,y = pos
	s,c = math.sin(rad), math.cos(rad)
	return x*c - y*s, y*c + x*s

class Camera:
	def __init__(self, pos=(0,0,0), rot =(0,0)):
		self.pos = list(pos)
		self.rot = list(rot)

	def events(self, event):
		if event.type == pygame.MOUSEMOTION:
			x, y = event.rel
			x /= 1/mouse_sensitivity
			y /= 1/mouse_sensitivity
			self.rot[0] += y
			self.rot[1] += x

	def update(self, dt, key):
		s = dt * 10
		if key[pygame.K_w]: self.pos[2] += s
		if key[pygame.K_s]: self.pos[2] -= s
		if key[pygame.K_a]: self.pos[0] -= s
		if key[pygame.K_d]: self.pos[0] += s
		if key[pygame.K_q]: self.pos[1] += s
		if key[pygame.K_e]: self.pos[1] -= s

pygame.init()

#Screen setup/View Settings
w, h = 1280, 720;
cx, cy = w//2, h//2;
screen = pygame.display.set_mode((w,h))
dof = 1000
offset = 1

#Game Clock
clock = pygame.time.Clock()

#Cube coordinates and Settings
verts = (-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)
edges = (0,1), (3,2), (4,5), (7,6), (0,3), (4,7), (1,2), (5,6), (0,4), (1,5), (2,6), (3,7)
vert_width = 7;
edge_width = 3;

#Camera Settings
cam = Camera((0,0,-5))
mouse_sensitivity = 0.001

#Pygame Settings
pygame.event.get()
pygame.mouse.get_rel()
pygame.mouse.set_visible(0)
pygame.event.set_grab(1)
while True:
	dt = clock.tick()/1000

	#get the current event type
	for event in pygame.event.get():
		if event.type == pygame.QUIT: 
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit()
		cam.events(event)

	#Background Color
	screen.fill((0, 0, 0))

	for edge in edges:
		points = []
		for x, y, z in (verts[edge[0]],verts[edge[1]]):
			x-=cam.pos[0]
			y-=cam.pos[1]
			z-=cam.pos[2]
			x,z = rotate2d((x,z), cam.rot[1])
			y,z = rotate2d((y,z), cam.rot[0])

			x *= dof / z
			y *= dof / z
			points += [(cx + int(x + vert_width // 2), cy+int(y + vert_width // 2))]

		pygame.draw.line(screen, (255,255,255), points[0], points[1], edge_width)
	#Update screen?
	pygame.display.flip()

	key = pygame.key.get_pressed()
	cam.update(dt,key)