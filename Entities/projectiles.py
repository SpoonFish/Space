import pygame as pg
import math
import Graphics.particle
import random as rnd

class PlayerBullet:
    def __init__(self, pos, influencing_vel) -> None:
        self.pos = pg.Vector2(pos.x,pos.y)
        self.timer = 0
        self.lifetime = 3.5
        self.particle_reload = 0.015
        self.remove = False
        self.vel = pg.Vector2(0+influencing_vel.x/8,-14+influencing_vel.y/2)

    def Update(self, dt, particle_manager):
        self.timer += dt
        self.particle_reload -= dt
        while self.particle_reload < 0:
            self.particle_reload += 0.015
            particle_manager.particles.append(Graphics.particle.Particle(self.pos,
                                                                         pg.Vector2(rnd.uniform(-1,1),rnd.uniform(2,5)),
                                                                         "spark",
                                                                         2,
                                                                         (185,185,185,255),
                                                                         rnd.uniform(0.1,0.25),
                                                                         (185,100,100,0))

        )
            
        if self.timer > self.lifetime:
            self.remove = True
        self.pos += self.vel*dt*60

    def Draw(self, screen):
        pg.draw.rect(screen, (225,100,100, 100), pg.Rect(self.pos.x-4,self.pos.y-7,8,20), 0, 5)
        pg.draw.rect(screen, (255,255,255), pg.Rect(self.pos.x-2,self.pos.y-5,4,16), 0, 5)

class EnemyBullet:
    def __init__(self, pos, influencing_vel) -> None:
        self.pos = pg.Vector2(pos.x,pos.y)
        self.timer = 0
        self.lifetime = 3.5
        self.particle_reload = 0.015
        self.remove = False
        self.vel = pg.Vector2(0+influencing_vel.x/8,10+influencing_vel.y/2)

    def Update(self, dt, particle_manager):
        self.timer += dt
        self.particle_reload -= dt
        while self.particle_reload < 0:
            self.particle_reload += 0.015
            particle_manager.particles.append(Graphics.particle.Particle(self.pos,
                                                                         pg.Vector2(rnd.uniform(-1,1),rnd.uniform(-2,-5)),
                                                                         "spark",
                                                                         2,
                                                                         (185,185,185,255),
                                                                         rnd.uniform(0.1,0.25),
                                                                         (100,100,185,0))

        )
            
        if self.timer > self.lifetime:
            self.remove = True
        self.pos += self.vel*dt*60

    def Draw(self, screen):
        pg.draw.rect(screen, (100,100,255,100), pg.Rect(self.pos.x-6,self.pos.y-7,12,20), 0, 5)
        pg.draw.rect(screen, (225,225,255), pg.Rect(self.pos.x-4,self.pos.y-5,8,16), 0, 5)

class EnemyBurstBullet:
    def __init__(self, pos, influencing_vel) -> None:
        self.pos = pg.Vector2(pos.x,pos.y)
        self.timer = 0
        self.lifetime = 3.5
        self.particle_reload = 0.1
        self.remove = False
        self.vel = pg.Vector2(0+influencing_vel.x/8,10+influencing_vel.y/2)

    def Update(self, dt, particle_manager):
        self.timer += dt
        self.particle_reload -= dt
        while self.particle_reload < 0:
            self.particle_reload += 0.1
            particle_manager.particles.append(Graphics.particle.Particle(self.pos,
                                                                         pg.Vector2(rnd.uniform(-0.5,0.5),rnd.uniform(-0,-1)),
                                                                         "spark",
                                                                         2,
                                                                         (185,185,185,255),
                                                                         rnd.uniform(0.1,0.25),
                                                                         (100,100,185,0))

        )
            
        if self.timer > self.lifetime:
            self.remove = True
        self.pos += self.vel*dt*60

    def Draw(self, screen):
        pg.draw.circle(screen, (100,100,150), self.pos, 8)
        pg.draw.rect(screen, (100,100,255,100), pg.Rect(self.pos.x-6,self.pos.y-7,12,12), 0, 5)
        pg.draw.rect(screen, (225,225,255), pg.Rect(self.pos.x-4,self.pos.y-5,8,8), 0, 5)
