from sys import stdout
from time import time, sleep
from math import sqrt, floor, atan
import numpy as np
import os
from obj import Object3dPersp
from random import randint as random

ASCIIGRADIENT = ' .:`\'-,;~_!"?c\\^<>|=sr1Jo*(C)utia3zLvey75jST{lx}IfY]qp9n0G62Vk8UXhZ4bgdPEKA$wQm&#HDR@WNBM'
GRADLEN = len(ASCIIGRADIENT)

class COLOR:
    r = "\u001b[31m"
    g = "\u001b[32m"
    b = "\u001b[34m"
    y = "\u001b[33m"
    c = "\u001b[36m"
    m = "\u001b[35m"
    _ = "\u001b[37m"


class Display:
    
    def __init__(self, res=[156, 52]):
        self.res = res
        self.buf = np.array([ [COLOR._+' ']*self.res[0] ] * self.res[1])
        self.fps_t = 90
        self.scene = []
        self.lights = [ np.array((5, 5, -6)) ]
        self.t = 1
        self._init_t = time()   
    
    def clear(self):
        self.buf = np.array([ [COLOR._+' ']*self.res[0] ] * self.res[1])
        self._init_t = time()
    
    def point(self, x, y, char='@'):
        if len(char) == 1:
            self.buf[ max(0, int(y/2)), max(0,int(x)) ] = COLOR._+char
        else:
            self.buf[ max(0, int(y/2)), max(0,int(x)) ] = char
    
    def line(self, x1, y1, x2, y2, char='.'):
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

        try:
            m = (y2-y1)/(x2-x1)
            c = y1-m * x1
            for i in range(min(x1,x2),max(x1,x2)):
                self.point(i ,m*i + c , char)
        except ZeroDivisionError:
            pass
        try:
            m= (x2-x1)/(y2-y1)
            c= x1-m * y1
            for i in range(min(y1,y2),max(y1,y2)):
                self.point(m*i + c ,i , char)
        except ZeroDivisionError:
            pass
    
    def flat_top_tri(self, x1, y1, x2, y2, x3, y3, char='.'):

        x1, y1, x2, y2, x3, y3 = int(x1), int(y1/2), int(x2), int(y2/2), int(x3), int(y3/2)
        if y1 != y2: raise RuntimeError( "not flat top triangle" )
        try:
            m1 = (x3 - x1)/(y3 - y1)
            c1 = x1 - m1 * y1
            m2 = (x3 - x2)/(y3 - y2)
            c2 = x2 - m2 * y2
            for y in range( y1, y3+1, -(y1-y3)//abs(y1-y3)):
                x1 = int( m1 * y + c1 )
                x2 = int( m2 * y + c2 )
                if len(char) -1:
                    self.buf[ y, min(x1, x2):max(x1, x2) ] = [char] * abs(x1- x2)
                else:
                    self.buf[ y, min(x1, x2):max(x1, x2) ] = [COLOR._+char] * abs(x1- x2)

        except ZeroDivisionError:
            if len(char) - 1:
                self.buf[ y1, min(x1, x2):max(x1, x2) ] = [char] * abs(x1- x2)
            else:
                self.buf[ y1, min(x1, x2):max(x1, x2) ] = [COLOR._+char] * abs(x1- x2)
    
    def flat_bot_tri(self, x1, y1, x2, y2, x3, y3, char='.'):
        
        x1, y1, x2, y2, x3, y3 = int(x1), int(y1/2), int(x2), int(y2/2), int(x3), int(y3/2)
        if y3 != y2: raise RuntimeError( "not flat bottom triangle" )
        try:
            m1 = (x2 - x1)/(y2 - y1)
            c1 = x1 - m1 * y1
            m2 = (x3 - x1)/(y3 - y1)
            c2 = x1 - m2 * y1
            for y in range( y1, y3+1, -(y1-y3)//abs(y1-y3) ):
                x1 = int( m1 * y + c1 )
                x2 = int( m2 * y + c2 )
                if len(char)-1:
                    self.buf[ y, min(x1, x2)-1:max(x1, x2)+1 ] = [char] * (abs(x1- x2)+2)
                else:
                    self.buf[ y, min(x1, x2)-1:max(x1, x2)+1 ] = [COLOR._+char] * (abs(x1- x2)+2)

        except ZeroDivisionError:
            if len(char)-1:
                self.buf[ y1, min(x1, x2)-1:max(x1, x2)+1 ] = [char] * (abs(x1- x2)+2)
            else:
                self.buf[ y1, min(x1, x2)-1:max(x1, x2)+1 ] = [COLOR._+char] * (abs(x1- x2)+2)
            

    def triangle(self, x1, y1, x2, y2, x3, y3, char='.'):
        

        ps = np.array([(x1, y1), (x2, y2), (x3, y3)])
        ps = ps[ps[:, 1].argsort()]
        x1, y1 = ps[0] ; x2, y2 = ps[1] ; x3, y3 = ps[2]
        
        

        if y1 == y2:
            self.flat_top_tri(x1, y1, x2, y2, x3, y3 , char)
        elif y2 == y3:
            self.flat_bot_tri(x1, y1, x2, y2, x3, y3 , char)

        try: 
            m = (x1- x3)/(y1- y3)
            # x= y*m + c
            c = x1 - m * y1

            y4 = y2
            x4 = y4 * m + c

            try:
                self.flat_bot_tri( x1, y1, x2, y2, x4, y4, char)
                self.flat_top_tri( x2, y2, x4, y4, x3, y3, char)
            except Exception as e:
                print(e)
            

        except ZeroDivisionError:
            pass

    def quad(self, x1, y1, x2, y2, x3, y3, x4, y4, char='.'):
    
        try:
            self.triangle(x1,y1, x2,y2, x3,y3, char)
            self.triangle(x1,y1, x4,y4, x3,y3, char)

        except Exception as e:
            pass

    def gradient_test(self):
        
        for y, i in enumerate(self.buf):
            for x, _ in enumerate(i):
                d = floor( ( (x  -  self.res[0]//2)**2 + (y*2 -  self.res[1])**2)**0.5  + self.t)
                self.buf[y, x] = ASCIIGRADIENT[ d % len(ASCIIGRADIENT) ]

    def show(self):

        stdout.write(
            ''.join(
                self.buf.ravel()
            )
        )
        stdout.flush()
        self.t -= (1/self.fps_t) * 100

        t = time() - self._init_t
        print(t*1000, 'ms', ' ', 1/t,'fps')
        sleep( max(0, 1/self.fps_t - t) )
    
    def render_wireframe(self):

        for o in self.scene:
            
            points = o.render( self.t/2, self.t )
            for i in o.edges:
            
                p1 = i[0] ; p2 = i[1]
                self.line( points[p1][0] , points[p1][1], points[p2][0], points[p2][1], '#')
            
            for i in points:
            
                self.point( *i )
    
    def render(self):
        
        for o in self.scene:

            points = o.render( self.t/2, self.t)
            faces = np.array(list(zip(o.zbuf, o.faces, list(range(len(o.faces))))))
            faces = faces[faces[:, 0].argsort()]

            for s, i in enumerate(faces):
                s = len(faces) -s -1
                x = i[2]
                i = i[1]
                l = np.array([ points[j-1][:2] for j in i ]).ravel()

                lum = 0
                for m in self.lights:
                    lum += max( np.dot(m - o.zbuf[x], o.normals[x]) , 0)

                lum = ASCIIGRADIENT[ int(lum*1.5) + 1 ]

                if s == 2:
                    lum = COLOR.c + "@" + COLOR._

                if len(i) == 3:
                    self.triangle( *l , lum)
                elif len(i) == 4:
                    self.quad( *l , lum)
                else:
                    print("[WARN] Skipping face at {}, cant draw n-gon that is not a tri or quad.".format(i))
