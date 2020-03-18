from Viewport import Viewport
from Mesh import Mesh
import pickle
import pygame
motion = pickle.load(open("tensor.pickle", "rb"))

v = Viewport(disable_mouse=True, w=700, h=600)

v.add_object(Mesh(name="Skeleton", primitive_type="skeleton", pos=[0,0,0]))
#v.add_object(Mesh(name="Sphere4", primitive_type="uvsphere", pos=[3, 0, 0], segments=10))
#v.add_object(Mesh(namew="Sphere8", primitive_type="uvsphere", pos=[0, 0, 0], segments=8))
#v.add_object(Mesh(name="Sphere12", primitive_type="uvsphere", pos=[-3, 0, 0], segments=12))
#v.add_object(Mesh(name="Sphere16", primitive_type="uvsphere", pos=[-6, 0, 0], segments=16))
#v.add_object(Mesh(name="Sphere32", primitive_type="uvsphere", pos=[-9, 0, 0], segments=32))

frame = 0
frames = 0
v.objects[0].set_skeleton_state(motion[0], 0, 0, 0)
x_off = v.objects[0].verts[11][0]
y_off = v.objects[0].verts[11][1]
z_off = v.objects[0].verts[11][2]

while True:
	v.update()
	v.objects[0].set_skeleton_state(motion[frame%len(motion)], x_off, y_off, z_off)
	frames += 1;
	if frames % 10 == 0:
		frame += 1;
