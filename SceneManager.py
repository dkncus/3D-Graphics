from Viewport import Viewport
from Mesh import Mesh
v = Viewport(disable_mouse=True, w=1280, h=720)

v.add_object(Mesh(name="Sphere4", primitive_type="uvsphere", pos=[3, 0, 0], segments=4))
v.add_object(Mesh(name="Sphere8", primitive_type="uvsphere", pos=[0, 0, 0], segments=8))
v.add_object(Mesh(name="Sphere12", primitive_type="uvsphere", pos=[-3, 0, 0], segments=12))
v.add_object(Mesh(name="Sphere16", primitive_type="uvsphere", pos=[-6, 0, 0], segments=16))
v.add_object(Mesh(name="Sphere32", primitive_type="uvsphere", pos=[-9, 0, 0], segments=32))

while True:
	v.update()