import pygame as pg
import math
import Graphics

pg.font.init()

font = pg.font.Font("Assets/font3.ttf",64)
class GuiManager:
    def __init__(self):
        self.timer = 0
        self.active = True
        self.buttons_active = True
        self.life_counter = LifeCounter()
        self.falling_text = FallingText("WAVE 1")
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
            self.buttons_active = False
        else:
            self.opacity = 1
            self.buttons_active = True

    def LoadMenu(self, menu):
        self.buttons.clear()
        self.buttons_active = True
        match menu:
            case "game_over":
                self.buttons.append(Graphics.gui.Button(pg.Rect(1920/2-210,1080/2+20, 380, 80), "PLAY AGAIN", (255,255,255), (255,255,255), "play"))

    def SetFallingText(self, text):
        self.falling_text.text = font.render(text, True, (60,50,50))
        self.falling_text.y = -50
    def Update(self, dt):
        self.timer += dt
        self.falling_text.y += 3*60*dt

        if self.fade_timer > 0:
            self.fade_timer = min(self.fade_timer-dt,self.fade_max)

            if self.fade_type == "out":
                self.opacity = 1-(self.fade_timer/self.fade_max)
            else:
                self.opacity = (self.fade_timer/self.fade_max)

    def DrawBackground(self, screen, player_hp):
        self.life_counter.Draw(screen, player_hp, self.timer)
        self.falling_text.Draw(screen)

    def Draw(self, screen):
        for button in self.buttons:
            button.Draw(screen, self.opacity)

'''
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
            pg.draw.circle(self.surf, (255,205,205), self.R(37,37,0.5), 11.1*math.sqrt(self.P(self.rnd_timer*'''

class LifeCounter:
    def __init__(self) -> None:
        self.text = font.render("LIVES:", True, (60,50,50))
        self.pos = pg.Vector2(12,1080-self.text.get_height())

    def Draw(self, screen, lives, timer):
        for i in range(5):
            offset = pg.Vector2(self.text.get_width()+15+60*i,self.pos.y+2)
            if i+1 < lives:
                colour = (60,50,50)
            elif i+1 == lives:
                colour = (60+(70*(math.sin(timer*(5-i))+1)),50+(70*(math.sin(timer*(5-i))+1)*i/5),50+(70*(math.sin(timer*(5-i))+1)*i/5))

            else:
                colour = (20,15,15)

            pg.draw.line(screen,colour, (3,50)+offset,(14,30)+offset, 2)
            pg.draw.line(screen,colour, (3,50)+offset,(0,26)+offset, 2)
            pg.draw.line(screen,colour, (0,26)+offset,(10,14)+offset,2)
            pg.draw.line(screen,colour, (50,26)+offset,(40,14)+offset,2)
            pg.draw.line(screen,colour, (36,0)+offset,(40,14)+offset,2)
            pg.draw.line(screen,colour, (14,0)+offset,(10,14)+offset,2)
            pg.draw.line(screen,colour, (14,0)+offset,(24,14)+offset,2)
            pg.draw.line(screen,colour, (36,0)+offset,(24,14)+offset,2)
            pg.draw.line(screen,colour, (47,50)+offset,(50,26)+offset,2)
            pg.draw.line(screen,colour, (47,50)+offset,(36,30)+offset,2)
            pg.draw.line(screen,colour, (14,30)+offset,(24,26)+offset,2)
            pg.draw.line(screen,colour, (24,26)+offset,(36,30)+offset,2)
        screen.blit(self.text, self.pos)


class FallingText:
    def __init__(self, text) -> None:
        self.text = font.render(text, True, (60,50,50))
        self.y = 1081

    def Draw(self, screen):
        if self.y < 1080:
            screen.blit(self.text, (1920/2-self.text.get_width()/2, self.y))
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

    def Update(self, mouse_pos, pressed, dt, active):
        if self.rect.collidepoint(mouse_pos):
            self.hovered = True
            if pressed:
                if active:
                    self.clicked = True
                    return self.key
                else:
                    self.clicked = False
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
        screen.blit(self.rendered_text, self.text_pos+pg.Vector2(25,22))
        screen.blit(self.line_surf, self.pos)
