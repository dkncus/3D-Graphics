from Viewport import Viewport
from Mesh import Mesh
v = Viewport(disable_mouse=True, w=1280, h=720)

v.add_object(Mesh(name="Ball 1", primitive_type="uvsphere", pos=[0, 0, 0], segments=12))
#dick
#v.add_object(Mesh(name="Ball 1", primitive_type="uvsphere", pos=[-.85, 0, 0], segments=12))
#v.add_object(Mesh(name="Ball 2", primitive_type="uvsphere", pos=[.85, 0, 0], segments=12))
#v.add_object(Mesh(name="Shaft Base", primitive_type="cylinder", pos=[0,.5,0],segments=12))
#v.add_object(Mesh(name="Shaft Mid", primitive_type="cylinder", pos=[0,1.5,0],segments=12))
#v.add_object(Mesh(name="Shaft Top", primitive_type="cylinder", pos=[0,2.5,0],segments=12))
#v.add_object(Mesh(name="Head", primitive_type="uvsphere", pos=[0,3.5,0],segments=12))

while True:
	v.update()