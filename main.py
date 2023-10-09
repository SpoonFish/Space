import pygame as pg
import random as rnd
import math
import Graphics.particle
import Graphics.gui


#boiler plate usual stuff yk
pg.init()

clock = pg.time.Clock()
width, height = 1920, 880
screen = pg.display.set_mode((width, height), pg.FULLSCREEN)
running = True
font = pg.font.SysFont("sys", 80)

particles = []
gui_manager = Graphics.gui.GuiManager()

gui_manager.buttons.append(Graphics.gui.Button(pg.Rect(width/2-150,height/2-40, 300, 80), "PLAY", (255,255,255), (255,255,255), "play"))

timer = 0
timer2 = 0.5
for i in range(60):
    bright = rnd.uniform(0,1)
    particles.append(Graphics.particle.Particle(
        pg.Vector2(rnd.randint(0, width), rnd.randint(0, height)),
        pg.Vector2(0,rnd.uniform(8,16)*(0.5+bright/2)),
        "star",
        2+1,
        (255*bright,205*bright,205*bright)

    ))

while running:
    dt = clock.tick(60)/1000
    timer += dt
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False


    keys = pg.key.get_pressed()
    if keys[pg.K_w]:
        timer2 += dt
    if keys[pg.K_s]:
        timer2 = max(0.00000001, timer2-dt)

    if timer > 0.06/timer2:
        bright = rnd.uniform(0,1)
        timer -=0.06/timer2
        particles.append(Graphics.particle.Particle(
            pg.Vector2(rnd.randint(0, width), 0),
            pg.Vector2(0,rnd.uniform(8,16)*(0.5+bright/2)),
            "star",
            2+1,
            (255*bright,205*bright,205*bright)

        ))

    screen.fill("black")

    for particle in particles:
        particle.Update(dt, timer2, height)
        if particle.remove:
            particles.remove(particle)
        particle.Draw(screen, timer2)

    gui_manager.Update(dt)
    for button in gui_manager.buttons:
        event = button.Update(pg.mouse.get_pos(), pg.mouse.get_pressed()[0], dt)

        if event != None:
            match event:
                case "play":
                    gui_manager.Fade(0.5, "out")

    gui_manager.Draw(screen)



    print(len(particles))

    #pg.draw.circle(screen, "white", pg.mouse.get_pos(), 100, 1)

    pg.display.flip()