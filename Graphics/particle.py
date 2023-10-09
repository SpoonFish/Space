import pygame as pg
import random as rnd
import math


class Particle:
    def __init__(self, pos, vel, shape, size, colour, rotation_vel=0, rotation=0) -> None:
        self.pos = pos
        self.vel = vel
        self.ovel = vel
        self.shape = shape
        self.size = size
        self.age = 0
        self.colour = colour
        self.rotation_vel = rotation_vel
        self.rotation = rotation
        self.remove = False

    def Update(self, dt, star_speed=0, height=0):
        self.age += dt
        self.pos += self.vel*(60*dt)
        self.vel = self.ovel*(star_speed/2)
        if (self.shape == "star") and self.pos.y > height+self.vel.y*5*star_speed*2:
            self.remove = True
        

    def Draw(self, screen, star_speed=0):
        if (self.shape == "circle"):
            pg.draw.circle(screen, self.colour, self.pos - pg.Vector2(self.size/2,self.size/2), self.size/2)
        
        elif (self.shape == "square"):
            pg.draw.rect(screen, self.colour, pg.Rect(self.pos.x-self.size/2,self.pos.y-self.size/2, self.size, self.size))

        elif (self.shape == "drop"):
            pg.draw.line(screen, self.colour, self.pos, self.pos-self.vel*2.5, self.size)
        elif (self.shape == "star"):
            pg.draw.line(screen, self.colour, self.pos, self.pos-self.vel, 2)
            pg.draw.line(screen, (self.colour[0]/2,self.colour[1]/2,self.colour[2]/2), self.pos-self.vel, self.pos-self.vel*2*star_speed, 2)
            pg.draw.line(screen, (self.colour[0]/6,self.colour[1]/6,self.colour[2]/6), self.pos-self.vel*2* star_speed, self.pos-self.vel*5*(star_speed*2), 2)
            pg.draw.line(screen, (self.colour[0]/15,self.colour[1]/15,self.colour[2]/15), self.pos-self.vel*5*(star_speed*2), self.pos-self.vel*7*(star_speed*2), 2)