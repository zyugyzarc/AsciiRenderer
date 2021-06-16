from render import Display, Object3dPersp, np
from random import randint as random

d = Display()


o = Object3dPersp('untitled.obj')
d.scene.append(o)

while True:
    d.clear()    
    d.render()
    d.show()
