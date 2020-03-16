import pygame
import sys
from Camera import Camera
from Mesh import Mesh
import math
import random

vert_width = 4
edge_width = 2

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

	def update(self, draw_f=True, draw_v=True, draw_e=True):
		dt = self.clock.tick()/1000
		#get the current event type
		for event in pygame.event.get():
			if event.type == pygame.QUIT: pygame.quit(); sys.exit();
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: pygame.quit(); sys.exit();
			self.cam.events(event)

		self.screen.fill((64, 64, 64))
		for mesh in self.objects:
			self.draw_mesh(mesh, draw_verts=draw_v, draw_edges=draw_e, draw_faces=draw_f)
		#Update screen
		pygame.display.flip()
		key = pygame.key.get_pressed()
		self.cam.update(dt,key)

	def draw_mesh(self, mesh, draw_verts = True, draw_edges = True, draw_faces = True):
		render_queue = []
		if draw_verts:
			for v in mesh.verts:
				x, y = self.get_screen_loc(x=v[0], y=v[1], z=v[2])
				#only draw vertex if the object is on the screen
				if int(x) > 0 and int(y) > 0 and int(x) < self.width and int(y) < self.height:
					dist = self.get_dist_to_cam(v[0], v[1], v[2])
					render_queue.append([0, dist, [int(x), int(y)]])
		if draw_edges:
			for edge in mesh.edges:
				points = []
				points3d = [mesh.verts[edge[0]], mesh.verts[edge[1]]]
				for x, y, z in (mesh.verts[edge[0]], mesh.verts[edge[1]]):
					x, y = self.get_screen_loc(x=x, y=y, z=z)
					points.append([int(x), int(y)])
				center = [((points3d[1][0]+points3d[0][0])/2), ((points3d[1][1]+points3d[0][1])/2), ((points3d[1][2]+points3d[0][2])/2)]
				dist = self.get_dist_to_cam(center[0], center[1], center[2])
				render_queue.append([1, dist, points])

		#If drawing faces is enabled
		if draw_faces:
			for f in mesh.faces:
				p1 = f[0]
				p2 = f[1]
				p3 = f[2]
				points = []
				points3d = [mesh.verts[f[0]], mesh.verts[f[1]], mesh.verts[f[2]]]
				for x,y,z in mesh.verts[f[0]], mesh.verts[f[1]], mesh.verts[f[2]]:
					x, y = self.get_screen_loc(x=x, y=y, z=z)
					points.append([int(x), int(y)])
				center = [((points3d[2][0]+points3d[1][0]+points3d[0][0])/3), ((points3d[2][1]+points3d[1][1]+points3d[0][1])/3), ((points3d[2][2]+points3d[1][2]+points3d[0][2])/3)]
				dist = self.get_dist_to_cam(center[0], center[1], center[2])
				render_queue.append([2, dist, points])
		
		#Sort the render queue by decending order of distance
		render_queue.sort(key=self.get_dist, reverse=True)

		#Render each item in the queue
		for item in render_queue:
			if item[0] == 0 and draw_verts:
				coord = item[2]
				pygame.draw.rect(self.screen, (255, 255, 255), (coord[0] - vert_width // 2, coord[1] - vert_width // 2, vert_width, vert_width))
			if item[0] == 1 and draw_edges:
				points = item[2]
				pygame.draw.aaline(self.screen, (255,255,255), points[0], points[1], edge_width)
			if item[0] == 2 and draw_faces:
				points = item[2]
				r = 140
				pygame.draw.polygon(self.screen, (r,r,r), points)
		#Verts
		#pygame.draw.rect(self.screen, (255, 255, 255), (int(x - vert_width // 2), int(y - vert_width // 2), vert_width, vert_width))
		#Edges
		#pygame.draw.aaline(self.screen, (255,255,255), points[0], points[1], edge_width)
		#Polys
		#pygame.draw.polygon(self.screen,(140,140,140),points)
		
	def get_dist(self,elem):
		return elem[1]

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

	def get_dist_to_cam(self,x,y,z):
		x2, y2, z2 = x, y, z
		x1, y1, z1 = self.cam.pos[0], self.cam.pos[1], self.cam.pos[2]
		x_dist = (x2 - x1) * (x2 - x1)
		y_dist = (y2 - y1) * (y2 - y1)
		z_dist = (z2 - z1) * (z2 - z1)
		dist = math.sqrt(x_dist + y_dist + z_dist)
		return dist

	def get_screen_loc(self,x,y,z):
		#if the projection is orthographic
		if self.cam.projection == "ortho":
			x = x - self.cam.pos[0]
			y = y - self.cam.pos[1]
			z = z - self.cam.pos[2]
			x = x * self.cam.e_z + self.cx
			y = y * self.cam.e_z + self.cy
		#if the projection is perspective
		if self.cam.projection == "persp":
			x, y = self.get_persp_coords(x=x , y=y, z=z)
		return x,y