from math import sin, cos
import numpy as np
from time import time

class Object3dPersp:
    def __init__(self, file=None):#color=(0,255,0),shape = None):
        #self.r = 
        if not file:
            self.verts = np.array([[[-1], [-1], [-1]],[[-1], [1], [-1]],[[-1], [-1], [1]], [[-1], [1], [1]], [[1], [-1], [-1]], [[1], [-1], [1]], [[1], [1], [-1]], [[1], [1], [1]]])
            self.edges = np.array([[0,1],[0,2],[0,4],[1,3],[1,6],[2,3],[2,5],[3,7],[4,5],[4,6],[5,7],[6,7]])
            #self.faces = np.array([[0,1,3,2],[0,2,5,4],[0,1,6,4],[1,3,7,6],[2,3,7,5],[4,5,7,6]])
        else:
            d = parse_obj(file)
            self.verts = d["verts"]
            self.edges = d["edges"]
            self.faces = d["faces"]
            self.normals = d["facenormals"]
        #self.pos = np.array([0,0,0])
        self.pos = np.array([50,50,0])
        self.scale = 120

        self.zbuf = np.zeros((len(self.faces)))
        #pyramid
        #self.verts = [[[-1],[-1],[-0.5]],[[1],[1],[-0.5]],[[1],[-1],[-0.5]],[[-1],[1],[-0.5]],[[0],[0],[1]]]
        #self.edges = [[0,2],[1,3],[2,1],[3,0],[0,4],[1,4],[2,4],[3,4]]

    def render(self,anglex=45, angley=45,anglez=0):


        points = self.verts
        scale = self.scale
        pos = self.pos
 
        anglex /= -100; angley /= 100; anglez = 0

        projected_points = np.zeros((len(points), 3))

        rotation_x = np.array([[1, 0, 0],
                      [0, cos(anglex), -sin(anglex)],
                      [0, sin(anglex), cos(anglex)]])

        rotation_y = np.array([[cos(angley), 0, -sin(angley)],
                      [0, 1, 0],
                      [sin(angley), 0, cos(angley)]])

        rotation_z = np.array([[cos(anglez), -sin(anglez), 0],
                      [sin(anglez), cos(anglez), 0],
                      [0, 0 ,1]])

        index = 0
        for point in points:
            rotated_2d = rotation_x @ point
            rotated_2d = rotation_y @ rotated_2d
            rotated_2d = rotation_z @ rotated_2d
            distance = 5
            z = 1/(distance - rotated_2d[2][0])
            projection_matrix = np.array([[z, 0, 0],
                                [0, z, 0]])
            projected_2d = projection_matrix @ rotated_2d

            x = projected_2d[0,0]
            y = projected_2d[1,0]
            projected_points[index] = np.array([x, y, z])
            index += 1

        projected_points = projected_points * scale + pos
        
        self.zbuf = []
        for i in self.faces:
            t = [  projected_points[j-1][2] for j in i]
            t = sum(t)/len(t)
            self.zbuf.append(t)
        return projected_points

def parse_obj(path, mode=None):
    src = ''
    if mode:
        src = path
    else:
        src = open(path,'r').read()
    
    data = {
        "verts": [],
        "edges": [],
        "faces": [],
        "vertexnormals": [],
        "facenormals": []
    }

    for line in src.split('\n'):
        if line.startswith('v '):
            t = line.strip('v ').split(' ')
            t = np.array([[float(i)] for i in t])
            data["verts"].append(t)
        
        if line.startswith('vn '):
            t = line.strip('vn ').split(' ')
            t = np.array([float(i) for i in t])
            data["vertexnormals"].append(t)
            #print(len(data["vertexnormals"]))
        
        if line.startswith('f '):
            n = line.strip('f ').split(' ')
            t = np.array([ int(i.split('//')[0]) for i in n])
            data["faces"].append(t)

            n = [ int(i.split('//')[1]) for i in n]
            #print(n)
            n = [ data["vertexnormals"][i-1] for i in n]
            n = sum(n)/len(n)
            data["facenormals"].append(n)


    
    for i in data['faces']:
        if len(i) == 3:
            t = [[i[0] -1, i[1] -1],
                 [i[1] -1, i[2] -1],
                 [i[2] -1, i[0] -1]]
            data['edges'] += t
        elif len(i) == 4:
            t = [[i[0] -1, i[1] -1], 
                 [i[1] -1, i[2] -1],
                 [i[2] -1, i[3] -1],
                 [i[3] -1, i[0] -1]]
            data['edges'] += t

    return data