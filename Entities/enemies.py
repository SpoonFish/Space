import pygame as pg
import random
import math

class Enemy:
    def __init__(self, pos, type, hp, width,height) -> None:
        self.end_of_init_pos = pg.Vector2(pos.x-width/2,pos.y)
        self.pos = pg.Vector2(pos.x-width/2,-100)
        self.width = width
        self.height = height
        self.initialise_time = 0
        self.vel = pg.Vector2(0,3)
        self.type = type
        self.hp = hp
        self.direction = 0
        self.hit_time = 0
        self.rnd_timer = 0
        self.reload = 0.3
        self.remove = False
        self.surf = pg.surface.Surface((width*1.5,width*1.5)).convert_alpha()

    def UniqueUpdate(self, dt, entity_manager, particle_manager):
        pass

    def Update(self, dt, entity_manager, particle_manager):
        if self.initialise_time < 1:
            self.initialise_time += dt
            self.pos.y = -100+self.end_of_init_pos.y*self.initialise_time+100*self.initialise_time
            return

        self.UniqueUpdate(dt, entity_manager, particle_manager)
        self.hit_time = max(self.hit_time-dt, 0)
        self.rnd_timer += dt

        for projectile in entity_manager.player_projectiles:
            if self.hit_time == 0 and pg.Rect(self.pos.x, self.pos.y, self.width, self.height).collidepoint(projectile.pos):
                projectile.remove = True
                self.hit_time = 0.3
                particle_manager.CreateHitSparks(projectile.pos)
                self.hp -= 1

        if self.hp <= 0 and self.hit_time < 0.1:
            particle_manager.CreateDeathSparks(self.pos +pg.Vector2(self.width/2,self.height/2))
            self.remove = True


    def AngleToPoint(self, point):
        hypo = self.pos.distance_to(point)
        opp = self.pos.y-point.y
        angle = math.degrees(math.asin(opp/hypo))+90
        if point.x > self.pos.x:
            angle = -angle
        return angle

    def R(self, x,y, strength=1):
        oldstate = random.getstate()
        random.seed(x*y+x+y)
        rnd = random.uniform(5.5,15.5)
        random.setstate(oldstate)
        add_x = 1.5*math.cos(self.rnd_timer*rnd)
        add_y = 1.5*math.sin(self.rnd_timer*rnd)
        return (pg.Vector2(x+add_x*strength,y+add_y*strength) - pg.Vector2(self.width/2,self.height/2)).rotate(self.direction) + pg.Vector2(self.width/2+self.width*0.25,self.height/2+self.width*0.25)
    
    def P(self, k):
        if round(self.hit_time*20)%4>1:
            return 0
        return min(1,((math.sin(self.rnd_timer+k)+1)/2+2)/3)

    def Draw(self,screen):
        self.surf.fill((0,0,0,0))
        #pg.draw.rect(self.surf, (255,245,245), pg.Rect(0,0, 75,75), 2, 0,35,35,0)
        pg.draw.circle(self.surf, (240,240,255,60), self.R(self.width/2,self.height/2,0.5), 20.1*self.P(self.rnd_timer*6)**0.5)
        pg.draw.circle(self.surf, (240,240,255,128), self.R(self.width/2,self.height/2,0.5), 14.1*self.P(self.rnd_timer*5)**0.5)
        
        pg.draw.line(self.surf, (255*self.P(1),255*self.P(1),255), self.R(0,0),self.R(0,self.height), 2)
        pg.draw.line(self.surf, (255*self.P(2),255*self.P(2),255), self.R(0,self.height),self.R(self.width,self.height), 2)
        pg.draw.line(self.surf, (255*self.P(3),255*self.P(3),255), self.R(self.width,self.height),self.R(self.width,0), 2)
        pg.draw.line(self.surf, (255*self.P(4),255*self.P(4),255), self.R(self.width,0),self.R(0,0), 2)

        pg.draw.circle(self.surf, (205,205,255), self.R(self.width/2,self.height/2,0.5), 11.1*math.sqrt(self.P(self.rnd_timer*4)))
        pg.draw.circle(self.surf, (255,255,255), self.R(self.width/2,self.height/2,0.5), 6.1*math.sqrt(self.P(self.rnd_timer*3)))


        self.surf.set_alpha(255)
        screen.blit(self.surf, self.pos-pg.Vector2(self.width*0.25,self.width*0.25))

class DasherEnemy(Enemy):
    def __init__(self, pos, type, hp, width,height) -> None:
        super().__init__(pos, type, hp, width,height)
        self.range = 300
        self.direction = 0
        self.charge_time = 2
        self.target_pos = pg.Vector2(0,0)
        self.target_direction = 0
        self.charging = False
        self.vel = pg.Vector2(0,3)

    def UniqueUpdate(self, dt, entity_manager, particle_manager):
        
        if self.target_direction != self.direction:
            change_angle = ""
            if self.target_direction < self.direction:
                change_angle = "backwards"
            else:
                change_angle = "forwards"

            if self.target_direction > 90 and self.direction < -90:
                change_angle = "backwards"
            if self.target_direction < -90 and self.direction > 90:
                change_angle = "forwards"

            if change_angle == "forwards":
                self.direction += 2*60*dt
            else:
                self.direction -= 2*60*dt
                

            if self.direction < -180:
                self.direction = 180
            if self.direction > 180:
                self.direction = -180

            if abs(self.direction - self.target_direction) < 2.5:
                self.direction = self.target_direction
                self.charging = True
                self.rotating = False
                self.vel = (self.target_pos-self.pos).normalize()*8

        if self.charging:
            self.charge_time -= dt
            if self.charge_time < 0:
                self.charge_time = 3
                self.charging = False
                self.vel = pg.Vector2(0,0)
                self.target_pos = pg.Vector2(random.randint(0,1920),random.randint(0,1080))
                self.target_direction = self.AngleToPoint(self.target_pos)
            self.vel /= 1.01
        self.pos += self.vel *60*dt


        if not self.charging and (self.pos.distance_to(entity_manager.player.pos) < self.range or self.pos.y > 600):
            self.target_direction = self.AngleToPoint(entity_manager.player.pos)#self.rnd_timer*6
            self.target_pos = pg.Vector2(entity_manager.player.pos.x, entity_manager.player.pos.y)
            self.rotating = True
            self.vel = pg.Vector2(0,0)
            pass

    def Draw(self,screen):
        self.surf.fill((0,0,0,0))
        #pg.draw.rect(self.surf, (255,245,245), pg.Rect(0,0, 75,75), 2, 0,35,35,0)
        pg.draw.circle(self.surf, (240,240,255,60), self.R(self.width/2,self.height/2,0.5), 20.1*self.P(self.rnd_timer*6)**0.5)
        pg.draw.circle(self.surf, (240,240,255,128), self.R(self.width/2,self.height/2,0.5), 14.1*self.P(self.rnd_timer*5)**0.5)
        
        pg.draw.line(self.surf, (255*self.P(1),255*self.P(1),255), self.R(0,0),self.R(self.width/2,self.height), 2)
        pg.draw.line(self.surf, (255*self.P(2),255*self.P(2),255), self.R(self.width/2,self.height),self.R(self.width,0), 2)
        pg.draw.line(self.surf, (255*self.P(3),255*self.P(3),255), self.R(0,0),self.R(self.width/2,self.height/2), 2)
        pg.draw.line(self.surf, (255*self.P(4),255*self.P(4),255), self.R(self.width/2,self.height/2),self.R(self.width,0), 2)

        pg.draw.circle(self.surf, (205,205,255), self.R(self.width/2,self.height/2,0.5), 11.1*math.sqrt(self.P(self.rnd_timer*4)))
        pg.draw.circle(self.surf, (255,255,255), self.R(self.width/2,self.height/2,0.5), 6.1*math.sqrt(self.P(self.rnd_timer*3)))


        self.surf.set_alpha(255)
        screen.blit(self.surf, self.pos-pg.Vector2(self.width*0.25,self.width*0.25))


class ShooterEnemy(Enemy):
    def __init__(self, pos, type, hp, width,height) -> None:
        super().__init__(pos, type, hp, width,height)
        self.range = 300
        self.direction = 0
        self.accel = pg.Vector2(0,0)
        self.stage = 1
        self.shoot_time = 2
        self.vel = pg.Vector2(0,2)

    def UniqueUpdate(self, dt, entity_manager, particle_manager):
        self.shoot_time -= dt
        if self.stage == 1:
            self.vel /= 1.01
            if self.vel.y < 0.1:
                self.stage = 2
        elif self.stage == 2:
            self.vel.y = math.sin(self.rnd_timer)/2+math.sin(self.rnd_timer/2)/6
            if self.pos.x < 1920/2-30:
                self.accel.x = 0.05
            else:
                self.accel.x = -0.05

        self.vel += self.accel *60*dt
        self.pos += self.vel *60*dt

        if self.shoot_time < 0:
            self.shoot_time = random.uniform(1,2)
            entity_manager.CreateEnemyBullet(self.pos+ pg.Vector2(self.width/2,self.height/2), self.vel)


    def Draw(self,screen):
        self.surf.fill((0,0,0,0))
        #pg.draw.rect(self.surf, (255,245,245), pg.Rect(0,0, 75,75), 2, 0,35,35,0)
        pg.draw.circle(self.surf, (240,240,255,60), self.R(self.width/2,self.height/2,0.5), 20.1*self.P(self.rnd_timer*6)**0.5)
        pg.draw.circle(self.surf, (240,240,255,128), self.R(self.width/2,self.height/2,0.5), 14.1*self.P(self.rnd_timer*5)**0.5)
        
        pg.draw.line(self.surf, (255*self.P(1),255*self.P(1),255), self.R(0,0),self.R(self.width*0.35,self.height), 2)
        pg.draw.line(self.surf, (255*self.P(1),255*self.P(1),255), self.R(self.width*0.5,self.height*0.8),self.R(self.width*0.35,self.height), 2)
        pg.draw.line(self.surf, (255*self.P(2),255*self.P(2),255), self.R(self.width*0.65,self.height),self.R(self.width*0.5,self.height*0.8), 2)
        pg.draw.line(self.surf, (255*self.P(2),255*self.P(2),255), self.R(self.width*0.65,self.height),self.R(self.width,0), 2)
        pg.draw.line(self.surf, (255*self.P(3),255*self.P(3),255), self.R(0,0),self.R(self.width/2,self.height*0.25), 2)
        pg.draw.line(self.surf, (255*self.P(4),255*self.P(4),255), self.R(self.width/2,self.height*0.25),self.R(self.width,0), 2)

        pg.draw.circle(self.surf, (205,205,255), self.R(self.width/2,self.height/2,0.5), 11.1*math.sqrt(self.P(self.rnd_timer*4)))
        pg.draw.circle(self.surf, (255,255,255), self.R(self.width/2,self.height/2,0.5), 6.1*math.sqrt(self.P(self.rnd_timer*3)))


        self.surf.set_alpha(255)
        screen.blit(self.surf, self.pos-pg.Vector2(self.width*0.25,self.width*0.25))

class BursterEnemy(Enemy):
    def __init__(self, pos, type, hp, width,height) -> None:
        super().__init__(pos, type, hp, width,height)
        self.range = 300
        self.direction = 0
        self.accel = pg.Vector2(0,0)
        self.stage = 1
        self.shoot_time = 2
        self.vel = pg.Vector2(0,2)

    def UniqueUpdate(self, dt, entity_manager, particle_manager):
        self.shoot_time -= dt
        if self.stage == 1:
            self.vel /= 1.01
            if self.vel.y < 0.1:
                self.stage = 2
        elif self.stage == 2:
            self.vel.y = math.sin(self.rnd_timer*8)
            if self.pos.x < 1920/2-30:
                self.accel.x = 0.05
            else:
                self.accel.x = -0.05

        self.vel += self.accel *60*dt
        limited_vel = pg.Vector2(max(-3,min(3,self.vel.x)), self.vel.y)

        if self.shoot_time < 0 and abs(self.pos.x-entity_manager.player.pos.x) < 200:
            self.shoot_time = 0.1
            entity_manager.CreateEnemyBullet(self.pos+ pg.Vector2(self.width/2,self.height/2), self.vel)
            limited_vel.x*=2

        self.pos += limited_vel *60*dt



    def Draw(self,screen):
        self.surf.fill((0,0,0,0))
        #pg.draw.rect(self.surf, (255,245,245), pg.Rect(0,0, 75,75), 2, 0,35,35,0)
        pg.draw.circle(self.surf, (240,240,255,60), self.R(self.width/2,self.height/2,0.5), 20.1*self.P(self.rnd_timer*6)**0.5)
        pg.draw.circle(self.surf, (240,240,255,128), self.R(self.width/2,self.height/2,0.5), 14.1*self.P(self.rnd_timer*5)**0.5)
        
        pg.draw.line(self.surf, (255*self.P(1),255*self.P(1),255), self.R(0,0),self.R(self.width*0.35,self.height), 2)
        pg.draw.line(self.surf, (255*self.P(1),255*self.P(1),255), self.R(self.width*0.5,self.height*0.8),self.R(self.width*0.35,self.height), 2)
        pg.draw.line(self.surf, (255*self.P(2),255*self.P(2),255), self.R(self.width*0.65,self.height),self.R(self.width*0.5,self.height*0.8), 2)
        pg.draw.line(self.surf, (255*self.P(2),255*self.P(2),255), self.R(self.width*0.65,self.height),self.R(self.width,0), 2)
        pg.draw.line(self.surf, (255*self.P(3),255*self.P(3),255), self.R(0,0),self.R(self.width/2,self.height*0.25), 2)
        pg.draw.line(self.surf, (255*self.P(4),255*self.P(4),255), self.R(self.width/2,self.height*0.25),self.R(self.width,0), 2)

        pg.draw.circle(self.surf, (205,205,255), self.R(self.width/2,self.height/2,0.5), 11.1*math.sqrt(self.P(self.rnd_timer*4)))
        pg.draw.circle(self.surf, (255,255,255), self.R(self.width/2,self.height/2,0.5), 6.1*math.sqrt(self.P(self.rnd_timer*3)))


        self.surf.set_alpha(255)
        screen.blit(self.surf, self.pos-pg.Vector2(self.width*0.25,self.width*0.25))