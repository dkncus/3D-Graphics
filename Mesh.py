import math
import pygame

vert_width = 4;
edge_width = 1;

class Mesh:
	def __init__(self, primitive_type, name="", pos=[0,0,0], verts=[], edges=[], segments = 4):
		self.name = name;
		if primitive_type == "cube":
			self.verts = [[-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1], [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]]
			for n in self.verts:
				n[0] -= pos[0]
				n[1] -= pos[1]
				n[2] -= pos[2]
			self.edges = [(0,1), (3,2), (4,5), (7,6), (0,3), (4,7), (1,2), (5,6), (0,4), (1,5), (2,6), (3,7)]
		if primitive_type == "point":
			self.verts = [[0, 0, 0]]
			self.verts[0][0] -= pos[0]
			self.verts[0][1] -= pos[1]
			self.verts[0][2] -= pos[2]
			self.edges = []
		if primitive_type == "uvsphere":
			self.verts, self.edges = self.gen_uv_sphere(segments)
			for n in self.verts:
				n[0] -= pos[0]
				n[1] -= pos[1]
				n[2] -= pos[2]
		if primitive_type == "cylinder":
			self.verts, self.edges = self.gen_cylinder(segments)
			for n in self.verts:
				n[0] -= pos[0]
				n[1] -= pos[1]
				n[2] -= pos[2]
	def rotate2d(self, pos, rad): 
		x,y = pos
		s,c = math.sin(rad), math.cos(rad)
		return x*c - y*s, y*c + x*s

	def draw_mesh_ortho(self, cam, screen, cx, cy, draw_edges = True, draw_verts = True):
		if draw_edges:
			for edge in self.edges:
				points = []
				for x, y, z in (self.verts[edge[0]], self.verts[edge[1]]):
					x-=cam.pos[0]
					y-=cam.pos[1]
					z-=cam.pos[2]
					x,z = self.rotate2d((x,z), cam.rot[1])
					y,z = self.rotate2d((y,z), cam.rot[0])

					x = x * cam.dof
					y = y * cam.dof

					points += [(cx + int(x), cy+int(y))]
				
				pygame.draw.line(screen, (255,255,255), points[0], points[1], edge_width)
		if draw_verts:
			for v in self.verts:
				x = v[0] - cam.pos[0]
				y = v[1] - cam.pos[1]
				z = v[2] - cam.pos[2]
				x,z = self.rotate2d((x,z), cam.rot[1])
				y,z = self.rotate2d((y,z), cam.rot[0])

				x = x * cam.dof
				y = y * cam.dof

				pygame.draw.rect(screen, (255, 255, 255), (cx + int(x - vert_width / 2), cy + int(y - vert_width / 2), vert_width, vert_width))

	def draw_mesh_persp(self, cam, screen, cx, cy, draw_edges = True, draw_verts = True):
		if draw_edges:
			for edge in self.edges:
				points = []
				for x, y, z in (self.verts[edge[0]], self.verts[edge[1]]):
					x-=cam.pos[0]
					y-=cam.pos[1]
					z-=cam.pos[2]
					x,z = self.rotate2d((x,z), cam.rot[1])
					y,z = self.rotate2d((y,z), cam.rot[0])

					x = x * (cam.dof/z)
					y = y * (cam.dof/z)

					points += [(cx + int(x), cy+int(y))]
				
				pygame.draw.line(screen, (255,255,255), points[0], points[1], edge_width)
		if draw_verts:
			for v in self.verts:
				x = v[0] - cam.pos[0]
				y = v[1] - cam.pos[1]
				z = v[2] - cam.pos[2]
				x,z = self.rotate2d((x,z), cam.rot[1])
				y,z = self.rotate2d((y,z), cam.rot[0])

				x = x * (cam.dof/z)
				y = y * (cam.dof/z)

				pygame.draw.rect(screen, (255, 255, 255), (cx + int(x - vert_width / 2), cy + int(y - vert_width / 2), vert_width, vert_width))

	def gen_uv_sphere(self, segments):
		verts = []
		edges = []

		verts.append([0,1,0]) #Top Point Vertex

		scale_div = 2 * math.pi / segments
		current_angle = 0
		
		theta_o = 180 /(segments // 2) #theta offset
		theta = 90 - theta_o 

		i = 0
		while theta > -90:
			height = math.sin(math.radians(theta))
			radius = math.cos(math.radians(theta))
			for j in range(segments):
				verts.append([math.sin(current_angle)*radius, height, math.cos(current_angle)*radius])
				current_angle += scale_div
				if j != 0:
					edges.append(((i * segments) + j, (i * segments) + j + 1))
				if j == segments - 1:
					edges.append(((i * segments) + 1, (i * segments) + j + 1))
			theta -= theta_o

			if i == 0:
				for j in range(segments):
					edges.append((0,j + 1))
			elif i != (segments // 2 - 1):
				for j in range(segments):
					edges.append((i*segments + j + 1, i*segments + j - segments + 1))
			i+=1

		verts.append([0,-1,0]) 
		for j in range(segments):
			edges.append((len(verts) - 2 - j, len(verts) - 1));
		return verts, edges

	def gen_cylinder(self, segments):
		verts = []
		edges = []

		scale_div = 2 * math.pi / segments
		current_angle = 0

		for i in range(segments):
			verts.append([math.sin(current_angle), 1, math.cos(current_angle)])
			current_angle += scale_div
			for j in range(segments):
				if j > 0:
					edges.append((j,j-1))
				if j == segments - 1:
					edges.append((0, j))

		current_angle = 0
		for i in range(segments):
			verts.append([math.sin(current_angle), -1, math.cos(current_angle)])
			current_angle += scale_div
			for j in range(segments):
				if j > 0:
					edges.append((segments + j, segments + j-1))
				if j == segments - 1:
					edges.append((segments, segments + j))

		for i in range(segments):
			edges.append((i, i + segments))
		return verts, edges