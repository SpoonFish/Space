import pygame as pg
import random as rnd
import math
import Graphics.particle
import Entities.player
import Entities.entity_manager
import Graphics.gui


#boiler plate usual stuff yk
pg.init()

clock = pg.time.Clock()
width, height = 1920, 1080
screen = pg.display.set_mode((width, height), pg.FULLSCREEN)
running = True
font = pg.font.SysFont("sys", 80)

gui_manager = Graphics.gui.GuiManager()
particle_manager = Graphics.particle.ParticleManager()
player = Entities.player.Player()
entity_manager = Entities.entity_manager.EntityManager()
gui_manager.buttons.append(Graphics.gui.Button(pg.Rect(width/2-150,height/2-40, 300, 80), "PLAY", (255,255,255), (255,255,255), "play"))

timer = 0
for i in range(60):
    bright = rnd.uniform(0,1)
    particle_manager.particles.append(Graphics.particle.Particle(
        pg.Vector2(rnd.randint(0, width), rnd.randint(0, height)),
        pg.Vector2(0,rnd.uniform(8,16)*(0.5+bright/2)),
        "star",
        2+1,
        (255*bright,205*bright,205*bright,255)

    ))

while running:
    dt = clock.tick(120)/1000
    timer += dt
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False


    keys = pg.key.get_pressed()
   # if keys[pg.K_w]:
    #    particle_manager.star_speed += dt
   # if keys[pg.K_s]:
   #     particle_manager.star_speed = max(0.00000001, particle_manager.star_speed-dt)

    if timer > 0.06/particle_manager.star_speed:
        bright = rnd.uniform(0,1)
        timer -=0.06/particle_manager.star_speed
        particle_manager.particles.append(Graphics.particle.Particle(
            pg.Vector2(rnd.randint(0, width), 0),
            pg.Vector2(0,rnd.uniform(8,16)*(0.5+bright/2)),
            "star",
            2+1,
            (255*bright,205*bright,205*bright,255)

        ))

    screen.fill("black")

    particle_manager.Update(dt)
    player.Update(dt, keys, entity_manager)
    entity_manager.Update(dt, particle_manager)
    gui_manager.Update(dt)
    for button in gui_manager.buttons:
        event = button.Update(pg.mouse.get_pos(), pg.mouse.get_pressed()[0], dt)

        if event != None:
            match event:
                case "play":
                    gui_manager.Fade(0.5, "out")
                    particle_manager.ChangeStarSpeed(3, 2)
                    player.SpawnIn()

    particle_manager.Draw(screen)
    player.Draw(screen)
    entity_manager.Draw(screen)
    gui_manager.Draw(screen)




    #pg.draw.circle(screen, "white", pg.mouse.get_pos(), 100, 1)

    pg.display.flip()