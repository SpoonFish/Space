import pygame as pg
import random as rnd
import math

class ParticleManager:
    def __init__(self):
        self.particles = []
        self.star_speed = 0.3
        self.max_time = 0
        self.speed_change_timer = 0
        self.old_speed = 0
        self.new_speed = 0

    def Update(self, dt):
        for particle in self.particles:
            particle.Update(dt, self.star_speed, 1080)
            if particle.remove:
                self.particles.remove(particle)

        
        if self.speed_change_timer > 0:
            self.speed_change_timer = min(self.speed_change_timer-dt,self.max_time)

            self.star_speed = (self.new_speed-self.old_speed)*math.pow(1-self.speed_change_timer/self.max_time, 1.3)+self.old_speed

    def CreateDeathSparks(self, pos, influence_vel, player = False):
        if not player:
            for _ in range(rnd.randint(20,25)):
                self.particles.append(Particle(pos,
                                                pg.Vector2(rnd.uniform(-2,2),rnd.uniform(-1,1))+influence_vel/2,
                                                "spark",
                                                2,
                                                (255,255,255,255),
                                                rnd.uniform(0.5,0.7),
                                                (55,55,255,0)))
        else:
            for _ in range(rnd.randint(30,35)):
                vel = pg.Vector2(rnd.uniform(-3,3),rnd.uniform(-3,3))
                vel = vel/vel.magnitude()*rnd.uniform(0.5,3)
                self.particles.append(Particle(pos,
                                                vel+influence_vel/2,
                                                "big_spark",
                                                2,
                                                (255,55,55,255),
                                                rnd.uniform(0.3,0.7),
                                                (255,0,0,0)))
            for _ in range(rnd.randint(30,35)):
                vel = pg.Vector2(rnd.uniform(-6,6),rnd.uniform(-6,6))
                vel = vel/vel.magnitude()*rnd.uniform(0.5,3)
                self.particles.append(Particle(pos,
                                                vel+influence_vel/2,
                                                "big_spark",
                                                2,
                                                (255,155,155,255),
                                                rnd.uniform(0.5,1.7),
                                                (255,50,50,0)))

    def CreateHitSparks(self, pos):
        for _ in range(rnd.randint(10,15)):
            self.particles.append(Particle(pos,
                                            pg.Vector2(rnd.uniform(-1,1),rnd.uniform(-1,1)),
                                            "spark",
                                            2,
                                            (185,185,185,255),
                                            rnd.uniform(0.25,0.5),
                                            (255,255,255,0)))

    def Draw(self, screen):
        for particle in self.particles:
            particle.Draw(screen, self.star_speed)

    def ChangeStarSpeed(self, new_speed, time):
        self.max_time = time
        self.speed_change_timer = time
        self.old_speed = self.star_speed
        self.new_speed = new_speed


class Particle:
    def __init__(self, pos, vel, shape, size, colour, lifetime= 100, colour_fade = (0,0,0,0)) -> None:
        self.pos = pg.Vector2(pos.x,pos.y)
        self.vel = vel
        self.ovel = vel
        self.shape = shape
        self.size = size
        self.age = 0
        self.colour = colour
        self.orig_colour = colour
        self.lifetime = lifetime
        self.colour_fade = colour_fade
        self.life_progress = 0
        self.remove = False

    def Update(self, dt, star_speed=0, height=0):
        self.age += dt
        self.life_progress = min(self.age/self.lifetime,1)
        self.pos += self.vel*(60*dt)
        self.vel = self.ovel*(star_speed/2)

        if (self.lifetime != 100):
            self.colour = (self.orig_colour[0]*(1-self.life_progress)+self.colour_fade[0]*self.life_progress,self.orig_colour[1]*(1-self.life_progress)+self.colour_fade[1]*self.life_progress,self.orig_colour[2]*(1-self.life_progress)+self.colour_fade[2]*self.life_progress,self.orig_colour[3]*(1-self.life_progress)+self.colour_fade[3]*self.life_progress)
            self.colour = (self.colour[0]*(1-self.life_progress),self.colour[1]*(1-self.life_progress),self.colour[2]*(1-self.life_progress))
        if (self.shape == "star" and self.pos.y > height+self.vel.y*5*star_speed*2) or self.life_progress == 1:
            self.remove = True
        

    def Draw(self, screen, star_speed=0):
        if (self.shape == "circle"):
            pg.draw.circle(screen, self.colour, self.pos - pg.Vector2(self.size/2,self.size/2), self.size/2)
        
        elif (self.shape == "square"):
            pg.draw.rect(screen, self.colour, pg.Rect(self.pos.x-self.size/2,self.pos.y-self.size/2, self.size, self.size))

        elif (self.shape == "drop"):
            pg.draw.line(screen, self.colour, self.pos, self.pos-self.vel*2.5, self.size)
        elif (self.shape == "spark"):
            pg.draw.line(screen, self.colour, self.pos, self.pos-self.vel, self.size)
        elif (self.shape == "big_spark"):
            pg.draw.line(screen, self.colour, self.pos, self.pos-self.vel*2, self.size)
        elif (self.shape == "star"):
            pg.draw.line(screen, self.colour, self.pos, self.pos-self.vel, 2)
            pg.draw.line(screen, (self.colour[0]/2,self.colour[1]/2,self.colour[2]/2), self.pos-self.vel, self.pos-self.vel*2*star_speed, 2)
            pg.draw.line(screen, (self.colour[0]/6,self.colour[1]/6,self.colour[2]/6), self.pos-self.vel*2* star_speed, self.pos-self.vel*5*(star_speed*2), 2)
            pg.draw.line(screen, (self.colour[0]/15,self.colour[1]/15,self.colour[2]/15), self.pos-self.vel*5*(star_speed*2), self.pos-self.vel*7*(star_speed*2), 2)
        elif (self.shape == "burst_ball"):
            pg.draw.circle(screen, self.colour, self.pos, 8)