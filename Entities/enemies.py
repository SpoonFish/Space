import pygame as pg
import random as rnd
import math
import Graphics.particle

RANDOM_NUMS = [5.5,5.9,6.7,8.7,6.5,9.4,14.3,12.5,11.1,10,13.3,13.4,15.1]

class Enemy:
    def __init__(self, pos, hp, width,height) -> None:
        self.end_of_init_pos = pg.Vector2(pos.x-width/2,pos.y)
        self.pos = pg.Vector2(pos.x-width/2,-100)
        self.width = width
        self.height = height
        self.initialise_time = 0
        self.vel = pg.Vector2(0,3)
        self.hp = hp
        self.max_hp = hp
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
        
        rnd1 = RANDOM_NUMS[round(x*y+x+y/0.7)%13]
        add_x = 1.5*math.cos(self.rnd_timer*rnd1)
        add_y = 1.5*math.sin(self.rnd_timer*rnd1)
        return (pg.Vector2(x+add_x*strength,y+add_y*strength) - pg.Vector2(self.width/2,self.height/2)).rotate(self.direction) + pg.Vector2(self.width/2+self.width*0.25,self.height/2+self.width*0.25)
    
    def P(self, k):
        if round(self.hit_time*20)%4>1:
            return 0
        return min(1,((math.sin(self.rnd_timer+k)+1)/2+2)/3)
    
    def DrawHp(self,screen):
        if self.max_hp < 20:
            for i in range(self.max_hp):
                if i < self.hp:
                    colour = (205,205,255)
                else:
                    colour = (60,60,105)

                pg.draw.rect(screen,colour,pg.Rect(i/self.max_hp*(self.width+20)-10+self.pos.x+2, self.pos.y-14, 1/self.max_hp*(self.width+20)-4,3))
        else:
            
            pg.draw.rect(screen,(60,60,105),pg.Rect(-10+self.pos.x, self.pos.y-15, (self.width+20),5))
            pg.draw.rect(screen,(205,205,255),pg.Rect(-10+self.pos.x, self.pos.y-15, self.hp/self.max_hp*(self.width+20),5))

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
        self.DrawHp(screen)


        self.surf.set_alpha(255)
        screen.blit(self.surf, self.pos-pg.Vector2(self.width*0.25,self.width*0.25))

class DasherEnemy(Enemy):
    def __init__(self, pos, hp, width=50,height=50) -> None:
        super().__init__(pos, hp, width,height)
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
                self.target_pos = pg.Vector2(rnd.randint(0,1920),rnd.randint(0,1080))
                self.target_direction = self.AngleToPoint(self.target_pos)
            self.vel /= 1+.01*(dt*60)**2
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
        self.DrawHp(screen)


        self.surf.set_alpha(255)
        screen.blit(self.surf, self.pos-pg.Vector2(self.width*0.25,self.width*0.25))


class ShooterEnemy(Enemy):
    def __init__(self, pos, hp, width=60,height=60) -> None:
        super().__init__(pos, hp, width,height)
        self.range = 300
        self.direction = 0
        self.accel = pg.Vector2(0,0)
        self.stage = 1
        self.shoot_time = 2
        self.vel = pg.Vector2(0,2)

    def UniqueUpdate(self, dt, entity_manager, particle_manager):
        self.shoot_time -= dt
        if self.stage == 1:
            self.vel /= 1+.01*(dt*60)**2
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
            self.shoot_time = rnd.uniform(1,2)
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
        self.DrawHp(screen)


        self.surf.set_alpha(255)
        screen.blit(self.surf, self.pos-pg.Vector2(self.width*0.25,self.width*0.25))

class BursterEnemy(Enemy):
    def __init__(self, pos, hp, width=70,height=70) -> None:
        super().__init__(pos, hp, width,height)
        self.range = 300
        self.burst_cooldown = 0
        self.burst_time = 0
        self.shoot_time = 2
        self.vel = pg.Vector2(rnd.uniform(2,3), 0)

    def UniqueUpdate(self, dt, entity_manager, particle_manager):
        self.shoot_time -= dt
        self.burst_time -= dt
        self.burst_cooldown -= dt
        self.vel.y = math.sin(self.rnd_timer*8)

        if self.pos.x < 30:
            self.vel.x = 3
        elif self.pos.x > 1920-90:
            self.vel.x = -3

        if abs(self.pos.x-entity_manager.player.pos.x) < 250 and self.burst_cooldown < 0:
            self.burst_time = 0.6
            self.burst_cooldown = 2.7

        limited_vel = pg.Vector2(self.vel.x,self.vel.y)
        if self.shoot_time < 0 and self.burst_time > 0:
            self.shoot_time = 0.078
            entity_manager.CreateEnemyBullet(self.pos+ pg.Vector2(self.width/2,self.height/2), pg.Vector2(rnd.uniform(-16,16),rnd.uniform(-4,4)), "burst")
        if self.burst_time > 0:
            limited_vel.x *= 4

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
        self.DrawHp(screen)


        self.surf.set_alpha(255)
        screen.blit(self.surf, self.pos-pg.Vector2(self.width*0.25,self.width*0.25))

        
class BolaEnemy(Enemy):
    def __init__(self, pos, hp, width=100,height=50) -> None:
        super().__init__(pos, hp, width,height)
        self.shoot_time = 2
        self.vel = pg.Vector2(rnd.uniform(2,3), 0)

    def UniqueUpdate(self, dt, entity_manager, particle_manager):
        self.shoot_time -= dt

        if self.pos.x < 30:
            self.vel.x = 3
        elif self.pos.x > 1920-90:
            self.vel.x = -3


        limited_vel = pg.Vector2(self.vel.x,self.vel.y)
        if self.shoot_time < 0:
            self.shoot_time = rnd.uniform(1,2)
            entity_manager.CreateEnemyBullet(self.pos+ pg.Vector2(self.width/2,self.height/2), pg.Vector2(self.vel.x,0), "bola")
       

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
        self.DrawHp(screen)


        self.surf.set_alpha(255)
        screen.blit(self.surf, self.pos-pg.Vector2(self.width*0.25,self.width*0.25))

        
class StarEnemy(Enemy):
    def __init__(self, pos, hp, width=80,height=80) -> None:
        super().__init__(pos, hp, width,height)
        self.direction = 0
        self.vel = pg.Vector2(0,0)
        self.shoot_time = rnd.uniform(1,3)
        self.accel = pg.Vector2(0,0)

    def UniqueUpdate(self, dt, entity_manager, particle_manager):
        self.shoot_time-=dt

        if self.pos.y < 1080/2-30:
            self.accel.y = 0.05
        else:
            self.accel.y = -0.05

        self.direction -= 2*60*dt
                

        self.vel += self.accel*60*dt
        self.vel.x = math.sin(self.rnd_timer/2)*2
        self.pos += self.vel *60*dt

        
        if self.shoot_time < 0:
            self.shoot_time = 1.3
            bullet_vel = pg.Vector2(math.cos(self.direction%90)*3,math.sin(self.direction%90)*3)
            for i in range(5):
                entity_manager.CreateEnemyBullet(self.pos+ pg.Vector2(self.width/2,self.height/2), bullet_vel.rotate(72*i), "star")

    def Draw(self,screen):
        self.surf.fill((0,0,0,0))
        #pg.draw.rect(self.surf, (255,245,245), pg.Rect(0,0, 75,75), 2, 0,35,35,0)
        pg.draw.circle(self.surf, (240,240,255,60), self.R(self.width/2,self.height/2+2,0.5), 20.1*self.P(self.rnd_timer*6)**0.5)
        pg.draw.circle(self.surf, (240,240,255,128), self.R(self.width/2,self.height/2+2,0.5), 14.1*self.P(self.rnd_timer*5)**0.5)
        
        pg.draw.line(self.surf, (255*self.P(1),255*self.P(1),255), self.R(self.width*0.5,0),self.R(self.width*0.2,self.height), 2)
        pg.draw.line(self.surf, (255*self.P(2),255*self.P(2),255), self.R(self.width*0.5,0),self.R(self.width*0.8,self.height), 2)
        pg.draw.line(self.surf, (255*self.P(3),255*self.P(3),255), self.R(0,self.height*0.38),self.R(self.width*0.8,self.height), 2)
        pg.draw.line(self.surf, (255*self.P(4),255*self.P(4),255), self.R(self.width,self.height*0.38),self.R(self.width*0.2,self.height), 2)
        pg.draw.line(self.surf, (255*self.P(5),255*self.P(5),255), self.R(0,self.height*0.38),self.R(self.width,self.height*0.38), 2)

        pg.draw.circle(self.surf, (205,205,255), self.R(self.width/2,self.height/2+2,0.5), 11.1*math.sqrt(self.P(self.rnd_timer*4)))
        pg.draw.circle(self.surf, (255,255,255), self.R(self.width/2,self.height/2+2,0.5), 6.1*math.sqrt(self.P(self.rnd_timer*3)))
        self.DrawHp(screen)

        self.surf.set_alpha(255)
        screen.blit(self.surf, self.pos-pg.Vector2(self.width*0.25,self.width*0.25))


class LauncherEnemy(Enemy):
    def __init__(self, pos, hp, width=70,height=70) -> None:
        super().__init__(pos, hp, width,height)
        self.range = 700
        self.direction = 0
        self.particle_reload = 0
        self.charge_time = 0
        self.target_pos = pg.Vector2(0,0)
        self.target_direction = 0
        self.charging = False
        self.vel = pg.Vector2(0,5)

    def UniqueUpdate(self, dt, entity_manager, particle_manager):
        
        change_angle = ""
        if self.target_direction != self.direction and not self.charging:
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

            if abs(self.direction - self.target_direction) < 5:
                self.direction = self.target_direction
                self.charging = True
                self.rotating = False
                self.vel = (self.target_pos-self.pos).normalize()*14

        if self.charging:
            self.charge_time -= dt

            self.particle_reload -= dt
            while self.particle_reload < 0:
                self.particle_reload += 0.005
                particle_manager.particles.append(Graphics.particle.Particle(self.pos+pg.Vector2(rnd.randint(-10,10)+30,rnd.randint(-10,10)+30),
                                                                            -self.vel/2 + pg.Vector2(rnd.uniform(-2,2),rnd.uniform(-2,2)),
                                                                            "spark",
                                                                            2,
                                                                            (185,185,185,255),
                                                                            rnd.uniform(0.25,0.35),
                                                                            (100,100,185,0))

            )
                
            if self.charge_time > 0.7 and self.pos.distance_to(entity_manager.player.pos) > 100:
                self.vel = (self.target_pos-self.pos).normalize()*14
                self.direction = self.AngleToPoint(self.target_pos)
                self.target_pos = pg.Vector2(entity_manager.player.pos.x, entity_manager.player.pos.y)
            if self.charge_time < 0:
                self.charge_time = 1
                self.charging = False
                self.vel = pg.Vector2(0,0)
                self.target_pos = pg.Vector2(rnd.randint(0,1920),rnd.randint(0,1080))
                self.target_direction = self.AngleToPoint(self.target_pos)
            self.vel /= 1+.012*(dt*60)**2
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
        self.DrawHp(screen)


        self.surf.set_alpha(255)
        screen.blit(self.surf, self.pos-pg.Vector2(self.width*0.25,self.width*0.25))

        
class AsteroidEnemy(Enemy):
    def __init__(self, pos, hp, width=80,height=80, vel=None) -> None:
        super().__init__(pos, hp, width,height)
        self.direction = 0
        self.pos = pg.Vector2(pos.x,pos.y)
        self.particle_time = 0.1
        self.size = (width+height)//2
        if vel == None:
            self.vel = pg.Vector2(rnd.uniform(.5,5.5),rnd.uniform(-1,3))*(80/(self.size/4+60))*2
        else:
            self.vel = pg.Vector2(vel.x,vel.y)
            
        self.points = [
            pg.Vector2(rnd.uniform(0,width*0.33),rnd.uniform(0,width*0.33)),
            pg.Vector2(rnd.uniform(width*0.33,width*0.66),rnd.uniform(0,width*0.1)),
            pg.Vector2(rnd.uniform(width*0.66,width),rnd.uniform(0,width*0.33)),
            pg.Vector2(rnd.uniform(width*0.9,width),rnd.uniform(width*0.33,width*0.66)),
            pg.Vector2(rnd.uniform(width*0.66,width),rnd.uniform(width*0.66,width)),
            pg.Vector2(rnd.uniform(width*0.33,width*0.66),rnd.uniform(width*0.9,width)),
            pg.Vector2(rnd.uniform(0,width*0.33),rnd.uniform(width*0.66,width)),
            pg.Vector2(rnd.uniform(0,width*0.1),rnd.uniform(width*0.33,width*0.66)),
        ]
        self.accel = pg.Vector2(0,0)

    def Update(self, dt, entity_manager, particle_manager):
        
        self.UniqueUpdate(dt, entity_manager, particle_manager)
        self.particle_time -= dt

        self.hit_time = max(self.hit_time-dt, 0)
        self.rnd_timer += dt

        for projectile in entity_manager.player_projectiles:
            if self.hit_time == 0 and pg.Rect(self.pos.x, self.pos.y, self.width, self.height).collidepoint(projectile.pos):
                projectile.remove = True
                self.hit_time = 0.3
                particle_manager.CreateHitSparks(projectile.pos)
                self.hp -= 1
        if self.pos.x > 1990 or self.pos.x < -200:
            self.remove = True

        if self.hp <= 0 and self.hit_time < 0.1:
            particle_manager.CreateDeathSparks(self.pos +pg.Vector2(self.width/2,self.height/2))
            self.remove = True
            entity_manager.CreateAsteroid(self.pos,self.size//1.3,self.vel)
            entity_manager.CreateAsteroid(self.pos,self.size//1.3,self.vel)
    def UniqueUpdate(self, dt, entity_manager, particle_manager):


        self.direction -= 1.3*60*dt
                

        self.pos += self.vel *60*dt

        
    def Draw(self,screen):
        self.surf.fill((0,0,0,0))
        #pg.draw.rect(self.surf, (255,245,245), pg.Rect(0,0, 75,75), 2, 0,35,35,0)
        
        for i in range(-1,7):
            pg.draw.line(self.surf, (255*self.P(i+2),255*self.P(i+2),255), self.R(self.points[i].x,self.points[i].y),self.R(self.points[i+1].x,self.points[i+1].y), 2)


        self.surf.set_alpha(255)
        screen.blit(self.surf, self.pos-pg.Vector2(self.width*0.25,self.width*0.25))