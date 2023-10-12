import pygame as pg
import math
import Graphics.particle
import random as rnd

class PlayerBullet:
    def __init__(self, pos, influencing_vel) -> None:
        self.pos = pg.Vector2(pos.x,pos.y)
        self.timer = 0
        self.lifetime = 3.5
        self.particle_reload = 0.03
        self.remove = False
        self.vel = pg.Vector2(0+influencing_vel.x/8,-8+influencing_vel.y/2)

    def Update(self, dt, particle_manager):
        self.timer += dt
        self.particle_reload -= dt
        while self.particle_reload < 0:
            self.particle_reload += 0.03
            particle_manager.particles.append(Graphics.particle.Particle(self.pos,
                                                                         pg.Vector2(rnd.uniform(-1,1),rnd.uniform(0,4)),
                                                                         "spark",
                                                                         2,
                                                                         (255,255,255,255),
                                                                         rnd.uniform(0.2,0.5),
                                                                         (255,100,100,0))

        )
            
        if self.timer > self.lifetime:
            self.remove = True
        self.pos += self.vel*dt*60
        self.vel.x = math.sin(self.timer*10)

    def Draw(self, screen):
        pg.draw.rect(screen, (255,255,255), pg.Rect(self.pos.x-2,self.pos.y-5,4,10), 0, 5)
