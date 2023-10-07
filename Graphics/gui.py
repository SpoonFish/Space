import pygame as pg
import math

pg.font.init()

font = pg.font.SysFont("arial", 60)

class Button:
    def __init__(self, rect, text, colour, hov_colour):
        self.rect = pg.Rect(rect)
        self.pos = pg.Vector2(rect.x, rect.y)
        self.width, self.height = rect.width, rect.height
        self.text = text
        self.colour = colour
        self.hover_time = 0
        self.hov_colour = hov_colour
        self.clicked = False
        self.hovered = False
        self.rendered_text = font.render(text, True, colour)
        self.text_pos = self.pos + pg.Vector2((self.width-self.rendered_text.get_width())/2,(self.height-self.rendered_text.get_height())/2)

    def Update(self, mouse_pos, pressed, dt):
        if self.rect.collidepoint(mouse_pos):
            self.hovered = True
            if pressed:
                self.clicked = True
            else: 
                self.clicked = False
        else:
            self.hovered = False
            self.clicked = False

        if self.hovered:
            self.hover_time = min(0.2, self.hover_time +dt)
        else:
            
            self.hover_time = max(0, self.hover_time -dt)

    def Draw(self, screen):
        if self.hovered:
            colour = self.hov_colour
        else:
            colour = self.colour

        spread = pg.Vector2(25*math.sqrt(self.hover_time*5))
        
        if self.hover_time >0:
            pg.draw.line(screen, colour, (self.pos.x+40,self.pos.y - spread.y), (self.pos.x+self.width,self.pos.y- spread.y), 2)
            pg.draw.line(screen, colour, (self.pos.x,self.pos.y+self.height + spread.y), (self.pos.x+self.width-40,self.pos.y+self.height+ spread.y), 2)
            pg.draw.line(screen, colour, (self.pos.x- spread.x,self.pos.y+40), (self.pos.x-spread.x,self.pos.y+self.height), 2)
            pg.draw.line(screen, colour, (self.pos.x+self.width+spread.x,self.pos.y), (self.pos.x+self.width+spread.x,self.pos.y+self.height-40), 2)
            
            pg.draw.line(screen, colour, (self.pos.x+40-spread.x*0.7,self.pos.y-spread.y*0.7), (self.pos.x-spread.x*0.7,self.pos.y-spread.y*0.7+40), 2)
            pg.draw.line(screen, colour, (self.pos.x+self.width+spread.x*0.7,self.pos.y+self.height+spread.x*0.7-40), (self.pos.x+self.width-40+spread.x*0.7,self.pos.y+self.height+spread.x*0.7), 2)

            dcolour = (50,50,50)
            pg.draw.line(screen, dcolour, (self.pos.x+40,self.pos.y), (self.pos.x+self.width,self.pos.y), 2)
            pg.draw.line(screen, dcolour, (self.pos.x,self.pos.y+self.height ), (self.pos.x+self.width-40,self.pos.y+self.height), 2)
            pg.draw.line(screen, dcolour, (self.pos.x,self.pos.y+40), (self.pos.x,self.pos.y+self.height), 2)
            pg.draw.line(screen, dcolour, (self.pos.x+self.width,self.pos.y), (self.pos.x+self.width,self.pos.y+self.height-40), 2)
            
            pg.draw.line(screen, dcolour, (self.pos.x+40,self.pos.y), (self.pos.x,self.pos.y+40), 2)
            pg.draw.line(screen, dcolour, (self.pos.x+self.width,self.pos.y+self.height-40), (self.pos.x+self.width-40,self.pos.y+self.height), 2)
        else:
            pg.draw.line(screen, colour, (self.pos.x+40,self.pos.y), (self.pos.x+self.width,self.pos.y), 2)
            pg.draw.line(screen, colour, (self.pos.x,self.pos.y+self.height ), (self.pos.x+self.width-40,self.pos.y+self.height), 2)
            pg.draw.line(screen, colour, (self.pos.x,self.pos.y+40), (self.pos.x,self.pos.y+self.height), 2)
            pg.draw.line(screen, colour, (self.pos.x+self.width,self.pos.y), (self.pos.x+self.width,self.pos.y+self.height-40), 2)
            
            pg.draw.line(screen, colour, (self.pos.x+40,self.pos.y), (self.pos.x,self.pos.y+40), 2)
            pg.draw.line(screen, colour, (self.pos.x+self.width,self.pos.y+self.height-40), (self.pos.x+self.width-40,self.pos.y+self.height), 2)


        screen.blit(self.rendered_text, self.text_pos)
