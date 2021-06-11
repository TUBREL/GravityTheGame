#imports
import math
import numpy
import scipy
import random


class gravity() :
    def initial(self,xres,yres,velocity,angle):
        #variables
        self.xposition = []
        self.yposition = []
        #constants
        self.G = 10000 #gravity constant
        self.xres = xres
        self.yres = yres
        #initial position of rocket
        self.x = 50 #might fuck things up
        self.y = yres/2
        self.density = 0.01
        v_0 = velocity*2
        theta0 = math.radians(angle)

        self.v_x = v_0 * math.cos(theta0)
        self.v_y = -v_0 * math.sin(theta0)
        print(theta0)
        print(velocity)
        print(self.v_x,self.v_y)


    #functions
    def gravity_acc (self,xplanet, yplanet,radius):
        deltay = int(yplanet) - self.y
        deltax = int(xplanet) - self.x
        self.M = (4/3)*math.pi*radius**2*self.density

        r = math.sqrt(deltay ** 2 + deltax ** 2)

        a = self.G * self.M / r ** 2 #total acceleration

        a_y = deltay/r * a
        a_x = deltax/r * a

        return a_y, a_x

    def position(self,planets,) :
        self.a_y = 0
        self.a_x = 0
        a_y0, a_x0 = gravity.gravity_acc(self.yres/2,self.xres,200)
        self.f = 0
        for self.i in planets :
            a_yt, a_xt = gravity.gravity_acc(int(planets[self.f][0]), int(planets[self.f][1]),int(planets[self.f][2]))
            self.a_y += a_yt
            self.a_x += a_xt
            self.f += 1
            
        a_ytotal = a_y0 + self.a_y
        a_xtotal = a_x0 + self.a_x

    #velocity
        dt = 1/60
        self.v_x += a_xtotal * dt #constant x velocity - gravity does not affect it
        self.v_y += a_ytotal * dt

    #position
    
        self.x += self.v_x * dt + 0.5 * a_xtotal * dt ** 2
        self.y += self.v_y * dt + 0.5 * a_ytotal * dt ** 2

    #history of information (to check program)
        self.xposition.append (self.x)
        self.yposition.append (self.y)
        #print(self.x,self.y)
        return self.x,self.y,self.v_x,self.v_y
gravity = gravity()

