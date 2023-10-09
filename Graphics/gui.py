import pygame as pg
import math

pg.font.init()

font = pg.font.SysFont("arial", 60)
class GuiManager:
    def __init__(self):
        self.active = True
        self.fade_timer = 0
        self.fade_max = 1
        self.fade_type = "none"
        self.opacity = 0
        self.buttons = []

    def Fade(self, time: float, fade_type: str):
        self.fade_type = fade_type
        self.fade_max = time
        self.fade_timer = time
        if fade_type == "out":
            self.opacity = 0
        else:
            self.opacity = 1

    def Update(self, dt):
        if self.fade_timer > 0:
            self.fade_timer = min(self.fade_timer-dt,self.fade_max)

            if self.fade_type == "out":
                self.opacity = 1-(self.fade_timer/self.fade_max)
                print(self.opacity)
            else:
                self.opacity = (self.fade_timer/self.fade_max)

    def Draw(self, screen):
        for button in self.buttons:
            button.Draw(screen, self.opacity)


class Button:
    def __init__(self, rect, text, colour, hov_colour, key):
        self.rect = pg.Rect(rect)
        self.pos = pg.Vector2(rect.x, rect.y)
        self.width, self.height = rect.width, rect.height
        self.text = text
        self.key = key
        self.colour = colour
        self.line_surf = pg.surface.Surface((self.width+32, self.height+32)).convert_alpha()
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
                return self.key
            else: 
                self.clicked = False
        else:
            self.hovered = False
            self.clicked = False

        if self.hovered:
            self.hover_time = min(0.2, self.hover_time +dt)
        else:
            
            self.hover_time = max(0, self.hover_time -dt)

    def Draw(self, screen, opacity):
        if self.hovered:
            colour = self.hov_colour
        else:
            colour = self.colour

        spread = pg.Vector2(15*math.pow(self.hover_time*5, 0.7))
        
        self.line_surf.fill((0,0,0,0))
        if self.hover_time >0:
            pg.draw.line(self.line_surf, colour, (15+40,15 - spread.y), (15+self.width,15- spread.y), 2)
            pg.draw.line(self.line_surf, colour, (15,15+self.height + spread.y), (15+self.width-40,15+self.height+ spread.y), 2)
            pg.draw.line(self.line_surf, colour, (15- spread.x,15+40), (15-spread.x,15+self.height), 2)
            pg.draw.line(self.line_surf, colour, (15+self.width+spread.x,15), (15+self.width+spread.x,15+self.height-40), 2)
            
            pg.draw.line(self.line_surf, colour, (15+40-spread.x*0.7,15-spread.y*0.7), (15-spread.x*0.7,15-spread.y*0.7+40), 2)
            pg.draw.line(self.line_surf, colour, (15+self.width+spread.x*0.7,15+self.height+spread.x*0.7-40), (15+self.width-40+spread.x*0.7,15+self.height+spread.x*0.7), 2)

            dcolour = (50,50,50)
            pg.draw.line(self.line_surf, dcolour, (15+40,15), (15+self.width,15), 2)
            pg.draw.line(self.line_surf, dcolour, (15,15+self.height ), (15+self.width-40,15+self.height), 2)
            pg.draw.line(self.line_surf, dcolour, (15,15+40), (15,15+self.height), 2)
            pg.draw.line(self.line_surf, dcolour, (15+self.width,15), (15+self.width,15+self.height-40), 2)
            
            pg.draw.line(self.line_surf, dcolour, (15+40,15), (15,15+40), 2)
            pg.draw.line(self.line_surf, dcolour, (15+self.width,15+self.height-40), (15+self.width-40,15+self.height), 2)
        else:
            pg.draw.line(self.line_surf, colour, (15+40,15), (15+self.width,15), 2)
            pg.draw.line(self.line_surf, colour, (15,15+self.height ), (15+self.width-40,15+self.height), 2)
            pg.draw.line(self.line_surf, colour, (15,15+40), (15,15+self.height), 2)
            pg.draw.line(self.line_surf, colour, (15+self.width,15), (15+self.width,15+self.height-40), 2)
            
            pg.draw.line(self.line_surf, colour, (15+40,15), (15,15+40), 2)
            pg.draw.line(self.line_surf, colour, (15+self.width,15+self.height-40), (15+self.width-40,15+self.height), 2)

        self.rendered_text.set_alpha(255 * (1-opacity))
        self.line_surf.set_alpha(255 * (1-opacity))
        screen.blit(self.rendered_text, self.text_pos+pg.Vector2(15,15))
        screen.blit(self.line_surf, self.pos)
