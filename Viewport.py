import pygame
import sys
from Camera import Camera
from Mesh import Mesh
import math

vert_width = 4
edge_width = 1

class Viewport:
	objects = []

	def __init__(self, w=1280, h=720, c=Camera(pos=(0, 0, -5),rot=(0,0,0),cam_type="persp"), obj=[], disable_mouse = False):
		pygame.init()
		#Screen setup/View Settings
		self.width = w
		self.height = h
		self.cx = w//2
		self.cy = h//2;
		self.screen = pygame.display.set_mode((w,h))
		#Game Clock
		self.clock = pygame.time.Clock()
		self.cam = c
		objects = obj
		#Pygame Settings
		pygame.event.get()
		pygame.mouse.get_rel()
		if disable_mouse == True:
			pygame.mouse.set_visible(0)
			pygame.event.set_grab(1)

	def add_object(self, mesh):
		m = mesh
		self.objects.append(m)

	def update(self):
		dt = self.clock.tick()/1000
		#get the current event type
		for event in pygame.event.get():
			if event.type == pygame.QUIT: pygame.quit(); sys.exit();
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: pygame.quit(); sys.exit();
			self.cam.events(event)

		self.screen.fill((64, 64, 64))
		for mesh in self.objects:
			self.draw_mesh(mesh)
		#Update screen
		pygame.display.flip()
		key = pygame.key.get_pressed()
		self.cam.update(dt,key)

	def draw_mesh(self, mesh, draw_edges = True, draw_verts = False, draw_faces = True):
		if draw_edges:
			for edge in mesh.edges:
				points = []
				for x, y, z in (mesh.verts[edge[0]], mesh.verts[edge[1]]):
					if self.cam.projection == "ortho":
						x = x - self.cam.pos[0]
						y = y - self.cam.pos[1]
						z = z - self.cam.pos[2]
						x,z = self.rotate((x,z), self.cam.rot[1])
						y,z = self.rotate((y,z), self.cam.rot[0])
						x = x * self.cam.e_z + self.cx
						y = y * self.cam.e_z + self.cy
					if self.cam.projection == "persp":
						x,z = self.rotate((x,z), self.cam.rot[1])
						y,z = self.rotate((y,z), self.cam.rot[0])
						x, y = self.get_persp_coords(x=x , y=y, z=z)
					points.append([int(x), int(y)])
				pygame.draw.line(self.screen, (255,255,255), points[0], points[1], edge_width)
		if draw_verts:
			for v in mesh.verts:
				if self.cam.projection == "ortho":
					x = v[0] - self.cam.pos[0]
					y = v[1] - self.cam.pos[1]
					z = v[2] - self.cam.pos[2]
					x,z = self.rotate((x,z), self.cam.rot[1])
					y,z = self.rotate((y,z), self.cam.rot[0])
					x = x * self.cam.e_z + self.cx
					y = y * self.cam.e_z + self.cy
				if self.cam.projection == "persp":
					x = v[0]
					y = v[1]
					z = v[2]
					x,z = self.rotate((x,z), self.cam.rot[1])
					y,z = self.rotate((y,z), self.cam.rot[0])
					x, y = self.get_persp_coords(x=x , y=y, z=z)
				
				#only draw vertex if the object is on the screen
				if int(x) > 0 and int(y) > 0 and int(x) < self.width and int(y) < self.height:
					pygame.draw.rect(self.screen, (255, 255, 255), (int(x - vert_width // 2), int(y - vert_width // 2), vert_width, vert_width))
	
	def rotate(self, pos, rad): 
		x,y = pos
		s,c = math.sin(rad), math.cos(rad)
		return x*c - y*s, y*c + x*s

	def get_persp_coords(self,x,y,z):
		x = x - self.cam.pos[0]
		y = y - self.cam.pos[1]
		z = z - self.cam.pos[2]
		Cx = math.cos(self.cam.rot[0])
		Cy = math.cos(self.cam.rot[1])
		Cz = math.cos(self.cam.rot[2])
		Sx = math.sin(self.cam.rot[0])
		Sy = math.sin(self.cam.rot[1])
		Sz = math.sin(self.cam.rot[2])
		e_z = self.cam.e_z

		dx = Cy * (Sz*y + Cz*x) - Sy*z
		dy = Sx * (Cy*z + Sy*(Sz*y + Cz * x)) + Cx * (Cz * y - Sz * x)
		dz = Cz * (Cy*z + Sy*(Sz*y + Cz * x)) - Sx * (Cz * y - Sz * x)

		Bx = 0
		By = 0

		if dz != 0:
			Bx = (e_z / dz) * dx + self.cx
			By = (e_z / dz) * dy + self.cy
		else:
			Bx = self.cx
			By = self.cy

		return Bx, By