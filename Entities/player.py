import pygame as pg
import random
import math
import Entities.enemies

class Player:
    def __init__(self) -> None:
        self.pos = pg.Vector2(1920/2-20, 900)
        self.opacity = 0
        self.fade_timer = 0
        self.speed = 5
        self.hp = 5
        self.hit_time = 0
        self.vel = pg.Vector2(0,0)
        self.accel = pg.Vector2(0,0)
        self.rnd_timer = 0
        self.reload = 0.3
        self.surf = pg.surface.Surface((85,85)).convert_alpha()
        self.surf.set_alpha(255 * (1-self.opacity))

    def SpawnIn(self):
        self.fade_timer = 1 

    def Update(self, dt, keys, entity_manager, particle_manager):
        self.rnd_timer+=dt
        self.reload -= dt
        self.hit_time = max(self.hit_time-dt, 0)
        if self.fade_timer > 0:
            self.fade_timer = max(self.fade_timer-dt, 0)
            self.opacity = 1-self.fade_timer
            self.pos = pg.Vector2(1920/2-37, 900)
            
        for projectile in entity_manager.enemy_projectiles:
            if self.hit_time == 0 and projectile.Collide(pg.Rect(self.pos.x, self.pos.y, 75,75)):
                self.hit_time = 0.5
                if projectile.breaks_on_hit:
                    projectile.remove = True
                particle_manager.CreateHitSparks(projectile.pos)
                self.hp -= 1
            
        for enemy in entity_manager.enemies:
            if self.hit_time == 0 and pg.Rect(self.pos.x, self.pos.y, 75,75).colliderect(pg.Rect(enemy.pos.x,enemy.pos.y,enemy.width,enemy.height)):
                self.hit_time = 0.8
                particle_manager.CreateHitSparks(self.pos+pg.Vector2(38,38))
                self.hp -= 1
                enemy.hit_time = 0.8
                enemy.hp -= 1
                if isinstance(enemy, Entities.enemies.AsteroidEnemy):
                    enemy.hp = 0
                    enemy.hit_time = 0.3

        self.accel = pg.Vector2(0,0)
        if keys[pg.K_a]:
            self.accel.x = -1
        if keys[pg.K_d]:
            self.accel.x = 1
        if keys[pg.K_w]:
            self.accel.y = -1
        if keys[pg.K_s]:
            self.accel.y = 1
        if self.accel.x*self.accel.y != 0:
            self.accel /= 1+0.3*(dt*60)**2

        self.vel += self.accel*60*dt
        if self.vel.x > 8:
            self.vel.x = 8
        elif self.vel.x < -8:
            self.vel.x = -8
        if self.vel.y > 8:
            self.vel.y = 8
        elif self.vel.y < -8:
            self.vel.y = -8
        
        if self.accel.x == 0:
            self.vel.x /= 1+.1*(dt*60)**2
        if self.accel.y == 0:
            self.vel.y /= 1+.1*(dt*60)**2

        if keys[pg.K_SPACE]:
            if self.reload < 0:
                self.reload = 0.4
                entity_manager.CreatePlayerBullet(self.pos + pg.Vector2(37,37), self.vel)

        
        self.pos.x = min(1900-75,max(20, self.pos.x+self.vel.x*dt*60))
        self.pos.y = min(1060-75,max(150, self.pos.y+self.vel.y*dt*60))

    def R(self, x,y, strength=1):
        oldstate = random.getstate()
        random.seed(x*y+x+y)
        rnd = random.uniform(5.5,15.5)
        random.setstate(oldstate)
        add_x = 1.5*math.cos(self.rnd_timer*rnd)
        add_y = 1.5*math.sin(self.rnd_timer*rnd)
        return (x+add_x*strength+5,y+add_y*strength+5)
    
    def P(self, k):
        if round(self.hit_time*20)%4>1:
            return 0
        return min(1,((math.sin(self.rnd_timer+k)+1)/2+2)/3)

    def Draw(self,screen):
        if self.opacity > 0:
            self.surf.fill((0,0,0,0))
            #pg.draw.rect(self.surf, (255,245,245), pg.Rect(0,0, 75,75), 2, 0,35,35,0)
            pg.draw.circle(self.surf, (255,240,240,60), self.R(37,37,0.5), 20.1*self.P(self.rnd_timer*6)**0.5)
            pg.draw.circle(self.surf, (255,240,240,128), self.R(37,37,0.5), 14.1*self.P(self.rnd_timer*5)**0.5)
            pg.draw.line(self.surf, (255,255*self.P(1),255*self.P(1)), self.R(5,75),self.R(20,45), 2)
            pg.draw.line(self.surf, (255,255*self.P(2),255*self.P(2)), self.R(5,75),self.R(0,40), 2)
            pg.draw.line(self.surf, (255,255*self.P(3),255*self.P(3)), self.R(0,40),self.R(15,20), 2)
            pg.draw.line(self.surf, (255,255*self.P(4),255*self.P(4)), self.R(75,40),self.R(60,20), 2)
            pg.draw.line(self.surf, (255,255*self.P(5),255*self.P(5)), self.R(55,0),self.R(60,20), 2)
            pg.draw.line(self.surf, (255,255*self.P(6),255*self.P(6)), self.R(20,0),self.R(15,20), 2)
            pg.draw.line(self.surf, (255,255*self.P(7),255*self.P(7)), self.R(20,0),self.R(37,20), 2)
            pg.draw.line(self.surf, (255,255*self.P(8),255*self.P(8)), self.R(55,0),self.R(37,20), 2)
            pg.draw.line(self.surf, (255,255*self.P(9),255*self.P(9)), self.R(70,75),self.R(75,40), 2)
            pg.draw.line(self.surf, (255,255*self.P(10),255*self.P(10)), self.R(70,75),self.R(55,45), 2)
            pg.draw.line(self.surf, (255,255*self.P(11),255*self.P(11)), self.R(20,45),self.R(37,40), 2)
            pg.draw.line(self.surf, (255,255*self.P(12),255*self.P(12)), self.R(37,40),self.R(55,45), 2)
            pg.draw.circle(self.surf, (255,205,205), self.R(37,37,0.5), 11.1*math.sqrt(self.P(self.rnd_timer*4)))
            pg.draw.circle(self.surf, (255,255,255), self.R(37,37,0.5), 6.1*math.sqrt(self.P(self.rnd_timer*3)))


            self.surf.set_alpha(255 * (self.opacity))
            screen.blit(self.surf, self.pos-pg.Vector2(5,5))

            
