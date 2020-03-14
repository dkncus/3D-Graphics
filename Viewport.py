import pygame
import sys
from Camera import Camera
from Mesh import Mesh

pygame.init()

#Screen setup/View Settings
w, h = 720, 550;
cx, cy = w//2, h//2;
screen = pygame.display.set_mode((w,h))

#Game Clock
clock = pygame.time.Clock()
frame = 0

#Camera Settings
cam = Camera((0,0,0),(-0.1,0))

#Pygame Settings
pygame.event.get()
pygame.mouse.get_rel()
#pygame.mouse.set_visible(0)
#pygame.event.set_grab(1)

objects = []
m = Mesh(name="cylinder001", primitive_type = "cylinder", segments = 12, pos=[3,0,0])
objects.append(m)
m = Mesh(name="cube001", primitive_type="cube")
objects.append(m)
m = Mesh(name="sphere001", primitive_type="uvsphere", pos=[-3, 0, 0], segments=12)
objects.append(m)

while True:
	dt = clock.tick()/1000
	#get the current event type
	for event in pygame.event.get():
		if event.type == pygame.QUIT: pygame.quit(); sys.exit();
		if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: pygame.quit(); sys.exit();
		#cam.events(event)

	#Background Color
	screen.fill((64, 64, 64))
	#draw each object
	for mesh in objects:
		mesh.draw_mesh_ortho(cam, screen, cx, cy, draw_verts = True)
	#Update screen
	pygame.display.flip()
	if frame % 10 == 0:
		cam.rot[1] += .001
	key = pygame.key.get_pressed()
	cam.update(dt,key)