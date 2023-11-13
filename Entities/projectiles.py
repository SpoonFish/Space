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

    def Collide(self, rect):
        return rect.collidepoint(self.pos)
    def Update(self, dt, particle_manager, entity_manager):
        self.timer += dt
        self.particle_reload -= dt
        self.vel.x /= 1+.01*(dt*60)
        while self.particle_reload < 0:
            self.particle_reload += 0.015
            particle_manager.particles.append(Graphics.particle.Particle(self.pos,
                                                                         pg.Vector2(rnd.uniform(-1,1),rnd.uniform(1,4)),
                                                                         "big_spark",
                                                                         2,
                                                                         (255,100,100,255),
                                                                         rnd.uniform(0.2,0.25),
                                                                         (255,0,0,255)))
            
        if self.timer > self.lifetime:
            self.remove = True
        self.pos += self.vel*dt*60

    def Draw(self, screen):
        pg.draw.rect(screen, (225,100,100, 100), pg.Rect(self.pos.x-4,self.pos.y-7,8,28), 0, 5)
        pg.draw.rect(screen, (255,255,255), pg.Rect(self.pos.x-2,self.pos.y-5,4,16), 0, 5)

class PlayerBolaBullet:
    def __init__(self, pos, influencing_vel) -> None:
        self.pos = pg.Vector2(pos.x,pos.y)
        self.pos2 = pg.Vector2(pos.x,pos.y)
        self.timer = 0
        self.lifetime = 5.5
        self.breaks_on_hit = False
        self.particle_reload = 0.1
        self.remove = False
        self.joint_vel = pg.Vector2(rnd.uniform(-1,1)+influencing_vel.x/4,-6+influencing_vel.y/4)
        self.vel = pg.Vector2(rnd.uniform(-2,3),rnd.uniform(-0.2,0.2))
        self.vel2 = pg.Vector2(rnd.uniform(-3,2),rnd.uniform(-0.2,0.2))

    def Collide(self, rect):
        for i in range(17):
            if rect.collidepoint(self.pos + (self.pos2-self.pos)/16*i):
                return True
        return False

    def Update(self, dt, particle_manager, entity_manager):
        
        for projectile in entity_manager.enemy_projectiles:
            if self.Collide(pg.Rect(projectile.pos.x-10,projectile.pos.y-8,20,30*60*dt)):
                projectile.remove = True
                particle_manager.CreateHitSparks(projectile.pos)
        self.timer += dt
        self.particle_reload -= dt
            
        if self.timer > self.lifetime:
            self.remove = True
        else:
            self.remove = False
        self.pos += (self.vel+self.joint_vel)*dt*60
        self.pos2 += (self.vel2+self.joint_vel)*dt*60
        self.vel /= 1+.01*(dt*60)
        self.joint_vel.x /= 1+.02*(dt*60)
        self.vel2 /= 1+.01*(dt*60)

    def Draw(self, screen):
        pg.draw.circle(screen, (120,70,70), self.pos, 8)
        pg.draw.circle(screen, (120,70,70), self.pos2, 8)
        pg.draw.line(screen, (120,80,80), self.pos, self.pos2, 4)
        brightness = (math.sin(self.timer*10)+1)/2
        pg.draw.line(screen, (220*brightness,190*brightness,190*brightness), self.pos, self.pos2, 2)
        pg.draw.circle(screen, (250,200,200), self.pos, 4)
        pg.draw.circle(screen, (250,200,200), self.pos2, 4)

class EnemyBullet:
    def __init__(self, pos, influencing_vel) -> None:
        self.pos = pg.Vector2(pos.x,pos.y)
        self.timer = 0
        self.lifetime = 3.5
        self.breaks_on_hit = True
        self.particle_reload = 0.015
        self.remove = False
        self.vel = pg.Vector2(0+influencing_vel.x/8,10+influencing_vel.y/2)

    def Collide(self, rect):
        return rect.collidepoint(self.pos)

    def Update(self, dt, particle_manager, entity_manager):
        self.timer += dt
        self.particle_reload -= dt
        while self.particle_reload < 0:
            self.particle_reload += 0.015
            particle_manager.particles.append(Graphics.particle.Particle(self.pos,
                                                                         pg.Vector2(rnd.uniform(-1,1),rnd.uniform(-2,-5)),
                                                                         "big_spark",
                                                                         2,
                                                                         (185,185,255,255),
                                                                         rnd.uniform(0.1,0.25),
                                                                         (100,100,255,0))

        )
            
        if self.timer > self.lifetime:
            self.remove = True
        self.pos += self.vel*dt*60

    def Draw(self, screen):
        pg.draw.rect(screen, (100,100,255,100), pg.Rect(self.pos.x-4,self.pos.y-13,8,26), 0, 5)
        pg.draw.rect(screen, (225,225,255), pg.Rect(self.pos.x-2,self.pos.y-5,4,16), 0, 5)


class EnemyStarBullet:
    def __init__(self, pos, influencing_vel) -> None:
        self.pos = pg.Vector2(pos.x,pos.y)
        self.timer = 0
        self.lifetime = 6.5
        self.breaks_on_hit = True
        self.particle_reload = 0.015
        self.remove = False
        self.vel = influencing_vel

    def Collide(self, rect):
        return rect.collidepoint(self.pos)

    def Update(self, dt, particle_manager, entity_manager):
        self.timer += dt
        self.particle_reload -= dt
        while self.particle_reload < 0:
            self.particle_reload += 0.05
            particle_manager.particles.append(Graphics.particle.Particle(self.pos,
                                                                         pg.Vector2(0,0),
                                                                         "burst_ball",
                                                                         2,
                                                                         (145,145,145,255),
                                                                         rnd.uniform(0.08,0.1),
                                                                         (100,100,185,0))

        )
         
            
        if self.timer > self.lifetime:
            self.remove = True
        self.pos += self.vel*(dt*60)

    def Draw(self, screen):
        pg.draw.circle(screen, (70,70,170), self.pos, 8)
        pg.draw.circle(screen, (225,225,225), self.pos, 6)

class EnemyBurstBullet(EnemyBullet):
    def __init__(self, pos, influencing_vel) -> None:
        self.pos = pg.Vector2(pos.x,pos.y)
        self.timer = 0
        self.breaks_on_hit = True
        self.lifetime = 5.5
        self.particle_reload = 0.1
        self.remove = False
        self.vel = pg.Vector2(0+influencing_vel.x/8,10+influencing_vel.y/2)

    def Update(self, dt, particle_manager, entity_manager):
        self.timer += dt
        self.particle_reload -= dt
        while self.particle_reload < 0:
            self.particle_reload += 0.05
            particle_manager.particles.append(Graphics.particle.Particle(self.pos,
                                                                         pg.Vector2(0,0),
                                                                         "burst_ball",
                                                                         2,
                                                                         (145,145,145,255),
                                                                         rnd.uniform(0.08,0.1),
                                                                         (100,100,185,0))

        )
            
        if self.timer > self.lifetime:
            self.remove = True
        self.pos += self.vel*dt*60
        self.vel /= 1+.005*(dt*60)

    def Draw(self, screen):
        pg.draw.circle(screen, (100,100,150), self.pos, 8)
        pg.draw.rect(screen, (190,190,255,100), pg.Rect(self.pos.x-6,self.pos.y-7,12,12), 0, 5)
        pg.draw.rect(screen, (225,225,255), pg.Rect(self.pos.x-4,self.pos.y-5,8,8), 0, 5)

class EnemyBolaBullet:
    def __init__(self, pos, influencing_vel) -> None:
        self.pos = pg.Vector2(pos.x,pos.y)
        self.pos2 = pg.Vector2(pos.x,pos.y)
        self.timer = 0
        self.lifetime = 5.5
        self.breaks_on_hit = False
        self.particle_reload = 0.1
        self.remove = False
        self.joint_vel = pg.Vector2(rnd.uniform(-1,1)+influencing_vel.x,4+influencing_vel.y/2)
        self.vel = pg.Vector2(rnd.uniform(-3,3),rnd.uniform(-1,1))
        self.vel2 = pg.Vector2(rnd.uniform(-3,3),rnd.uniform(-1,1))

    def Collide(self, rect):
        for i in range(17):
            if rect.collidepoint(self.pos + (self.pos2-self.pos)/16*i):
                return True
        return False

    def Update(self, dt, particle_manager, entity_manager):
        
        for projectile in entity_manager.player_projectiles:
            if self.Collide(pg.Rect(projectile.pos.x-10,projectile.pos.y-8,20,30*60*dt)):
                projectile.remove = True
                particle_manager.CreateHitSparks(projectile.pos)
        self.timer += dt
        self.particle_reload -= dt
            
        if self.timer > self.lifetime:
            self.remove = True
        self.pos += (self.vel+self.joint_vel)*dt*60
        self.pos2 += (self.vel2+self.joint_vel)*dt*60
        self.vel /= 1+.01*(dt*60)
        self.joint_vel.x /= 1+.02*(dt*60)
        self.vel2 /= 1+.01*(dt*60)

    def Draw(self, screen):
        pg.draw.circle(screen, (70,70,150), self.pos, 8)
        pg.draw.circle(screen, (70,70,150), self.pos2, 8)
        pg.draw.line(screen, (80,80,120), self.pos, self.pos2, 4)
        brightness = (math.sin(self.timer*10)+1)/2
        pg.draw.line(screen, (190*brightness,190*brightness,220*brightness), self.pos, self.pos2, 2)
        pg.draw.circle(screen, (200,200,250), self.pos, 4)
        pg.draw.circle(screen, (200,200,250), self.pos2, 4)
