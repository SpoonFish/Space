import math
import pygame as pg

class PowerUp():
    def __init__(self, type: str, pos: pg.Vector2):
        self.pos = pos-pg.Vector2(35,32)
        self.type = type
        self.timer = 0
        self.vel = pg.Vector2(0,-1)
        self.remove = False

    def Collide(self, hitbox):
        if pg.Rect(self.pos.x, self.pos.y, 70, 64).colliderect(hitbox):
            self.remove = True
            return True
        return False

    def Update(self, dt, particle_manager):
        self.timer += dt

        if self.vel.y < 3:
            self.vel.y+= 0.03 *60*dt

        if self.remove:
            particle_manager.CreateHitSparks(self.pos+pg.Vector2(35,32))

        self.pos.y += self.vel.y*60*dt

    def SquashCoords(self, coords1, coords2=None):
        if coords2 == None:
            coords = coords1
        else:
            coords = pg.Vector2(coords1,coords2)
        squash_factor = (math.sin(self.timer*3))
        x = coords.x*squash_factor
        x += 35 * (1-squash_factor)
        return pg.Vector2(x, coords.y) + self.pos

    def UniqueDraw(self, screen): 

        colour = (255,255,127*(math.sin(self.timer*12)+1))

        offset = pg.Vector2(10,6)
        if self.type == "life":
            pg.draw.line(screen,colour, self.SquashCoords((8,50)+offset),self.SquashCoords((14,30)+offset), 2)
            pg.draw.line(screen,colour, self.SquashCoords((8,50)+offset),self.SquashCoords((0,26)+offset), 2)
            pg.draw.line(screen,colour, self.SquashCoords((0,26)+offset),self.SquashCoords((10,14)+offset),2)
            pg.draw.line(screen,colour, self.SquashCoords((50,26)+offset),self.SquashCoords((40,14)+offset),2)
            pg.draw.line(screen,colour, self.SquashCoords((36,0)+offset),self.SquashCoords((40,14)+offset),2)
            pg.draw.line(screen,colour, self.SquashCoords((14,0)+offset),self.SquashCoords((10,14)+offset),2)
            pg.draw.line(screen,colour, self.SquashCoords((14,0)+offset),self.SquashCoords((24,14)+offset),2)
            pg.draw.line(screen,colour, self.SquashCoords((36,0)+offset),self.SquashCoords((24,14)+offset),2)
            pg.draw.line(screen,colour, self.SquashCoords((42,50)+offset),self.SquashCoords((50,26)+offset),2)
            pg.draw.line(screen,colour, self.SquashCoords((42,50)+offset),self.SquashCoords((36,30)+offset),2)
            pg.draw.line(screen,colour, self.SquashCoords((14,30)+offset),self.SquashCoords((24,26)+offset),2)
            pg.draw.line(screen,colour, self.SquashCoords((24,26)+offset),self.SquashCoords((36,30)+offset),2)
        elif self.type == "triple":
            pg.draw.line(screen,colour, self.SquashCoords((20,00)+offset),self.SquashCoords((30,00)+offset), 2)
            pg.draw.line(screen,colour, self.SquashCoords((20,0)+offset),self.SquashCoords((20,30)+offset), 2)
            pg.draw.line(screen,colour, self.SquashCoords((20,30)+offset),self.SquashCoords((30,30)+offset),2)
            pg.draw.line(screen,colour, self.SquashCoords((30,30)+offset),self.SquashCoords((30,00)+offset),2)

            pg.draw.line(screen,colour, self.SquashCoords((5,20)+offset),self.SquashCoords((15,20)+offset), 2)
            pg.draw.line(screen,colour, self.SquashCoords((5,20)+offset),self.SquashCoords((5,50)+offset), 2)
            pg.draw.line(screen,colour, self.SquashCoords((15,20)+offset),self.SquashCoords((15,50)+offset),2)
            pg.draw.line(screen,colour, self.SquashCoords((15,50)+offset),self.SquashCoords((5,50)+offset),2)

            pg.draw.line(screen,colour, self.SquashCoords((35,20)+offset),self.SquashCoords((45,20)+offset), 2)
            pg.draw.line(screen,colour, self.SquashCoords((35,20)+offset),self.SquashCoords((35,50)+offset), 2)
            pg.draw.line(screen,colour, self.SquashCoords((35,50)+offset),self.SquashCoords((45,50)+offset),2)
            pg.draw.line(screen,colour, self.SquashCoords((45,50)+offset),self.SquashCoords((45,20)+offset),2)
        elif self.type == "rapid":
            pg.draw.line(screen,colour, self.SquashCoords((20,00)+offset),self.SquashCoords((30,00)+offset), 2)
            pg.draw.line(screen,colour, self.SquashCoords((20,0)+offset),self.SquashCoords((20,30)+offset), 2)
            pg.draw.line(screen,colour, self.SquashCoords((20,30)+offset),self.SquashCoords((30,30)+offset),2)
            pg.draw.line(screen,colour, self.SquashCoords((30,30)+offset),self.SquashCoords((30,00)+offset),2)

            pg.draw.line(screen,colour, self.SquashCoords((10,50)+offset),self.SquashCoords((25,35)+offset),2)
            pg.draw.line(screen,colour, self.SquashCoords((40,50)+offset),self.SquashCoords((25,35)+offset),2)
            pg.draw.line(screen,colour, self.SquashCoords((10,30)+offset),self.SquashCoords((20,20)+offset),2)
            pg.draw.line(screen,colour, self.SquashCoords((40,30)+offset),self.SquashCoords((30,20)+offset),2)
            pg.draw.line(screen,colour, self.SquashCoords((10,40)+offset),self.SquashCoords((20,30)+offset),2)
            pg.draw.line(screen,colour, self.SquashCoords((40,40)+offset),self.SquashCoords((30,30)+offset),2)
        elif self.type == "bola":
            pg.draw.line(screen,colour, self.SquashCoords((5,5)+offset),self.SquashCoords((15,5)+offset), 2)
            pg.draw.line(screen,colour, self.SquashCoords((15,5)+offset),self.SquashCoords((15,15)+offset), 2)
            pg.draw.line(screen,colour, self.SquashCoords((5,15)+offset),self.SquashCoords((15,15)+offset), 2)
            pg.draw.line(screen,colour, self.SquashCoords((5,15)+offset),self.SquashCoords((5,5)+offset), 2)
            pg.draw.line(screen,colour, self.SquashCoords((45,45)+offset),self.SquashCoords((35,45)+offset), 2)
            pg.draw.line(screen,colour, self.SquashCoords((35,45)+offset),self.SquashCoords((35,35)+offset), 2)
            pg.draw.line(screen,colour, self.SquashCoords((45,35)+offset),self.SquashCoords((35,35)+offset), 2)
            pg.draw.line(screen,colour, self.SquashCoords((45,35)+offset),self.SquashCoords((45,45)+offset), 2)
            pg.draw.line(screen,colour, self.SquashCoords((15,15)+offset),self.SquashCoords((35,35)+offset), 2)

    def Draw(self, screen):

        colour = (155,155,75*(math.sin(self.timer*6)+1))

        pg.draw.line(screen, colour, self.SquashCoords(15,0),self.SquashCoords(55,0), 2)
        pg.draw.line(screen, colour, self.SquashCoords(0,32),self.SquashCoords(15,0), 2)
        pg.draw.line(screen, colour, self.SquashCoords(0,32),self.SquashCoords(15,64), 2)
        pg.draw.line(screen, colour, self.SquashCoords(70,32),self.SquashCoords(55,0), 2)
        pg.draw.line(screen, colour, self.SquashCoords(70,32),self.SquashCoords(55,64), 2)
        pg.draw.line(screen, colour, self.SquashCoords(15,64),self.SquashCoords(55,64), 2)
        self.UniqueDraw(screen)