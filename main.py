import pygame as pg
import random as rnd
import math
import Graphics.particle
import Entities.player
import Entities.entity_manager
import Entities.enemies
import Graphics.gui
import copy


#boiler plate usual stuff yk
pg.init()


clock = pg.time.Clock()
width, height = 1920, 1080
screen = pg.display.set_mode((width, height), pg.FULLSCREEN)
running = True
font = pg.font.SysFont("sys", 80)

gui_manager = Graphics.gui.GuiManager()
particle_manager = Graphics.particle.ParticleManager()
entity_manager = Entities.entity_manager.EntityManager()
gui_manager.buttons.append(Graphics.gui.Button(pg.Rect(width/2-210,height/2-40, 380, 80), "PLAY", (255,255,255), (255,255,255), "play"))
game_speed = 1
timer = 0
for i in range(60):
    bright = rnd.uniform(0,1)
    particle_manager.particles.append(Graphics.particle.Particle(
        pg.Vector2(rnd.randint(0, width), rnd.randint(0, height)),
        pg.Vector2(0,rnd.uniform(8,16)*(0.5+bright/2)),
        "star",
        2+1,
        (205*bright,175*bright,175*bright,255)

    ))
while running:
    dt = clock.tick(1000)/1000
    real_dt = dt
    dt*=game_speed
    timer += dt

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    keys = pg.key.get_pressed()

    if timer > 0.06/particle_manager.star_speed:
        bright = rnd.uniform(0,0.7)
        timer -=0.06/particle_manager.star_speed
        particle_manager.particles.append(Graphics.particle.Particle(
            pg.Vector2(rnd.randint(0, width), 0),
            pg.Vector2(0,rnd.uniform(8,16)*(0.5+bright/2)),
            "star",
            2+1,
            (205*bright,175*bright,175*bright,255)

        ))

    screen.fill("black")

    if entity_manager.player.dead:
        game_speed = max(0,game_speed-dt/3)
        if game_speed < 0.01:
            game_speed = 0

    if entity_manager.player.cant_get_hit == True and not entity_manager.game_over:
        entity_manager.game_over = True
        gui_manager.SetFallingText("GAME OVER")
    if entity_manager.player.time_since_death > 2:
        entity_manager.player.time_since_death = -10
        gui_manager.LoadMenu("game_over")
        gui_manager.Fade(1.5, "in")

    particle_manager.Update(dt)
    entity_manager.player.Update(dt, keys, entity_manager, particle_manager)
    entity_manager.Update(dt, particle_manager, gui_manager)
    gui_manager.Update(dt)
    for button in gui_manager.buttons:
        event = button.Update(pg.mouse.get_pos(), pg.mouse.get_pressed()[0], real_dt, gui_manager.buttons_active)

        if event != None:
            match event:
                case "play":
                    entity_manager.game_over = False
                    game_speed = 1
                    gui_manager.Fade(0.5, "out")
                    particle_manager.ChangeStarSpeed(3, 2)
                    entity_manager.player.Spawn()
                    entity_manager.SummonWave(1, gui_manager)

    particle_manager.Draw(screen)
    gui_manager.DrawBackground(screen, entity_manager.player.hp)
    entity_manager.Draw(screen)
    gui_manager.Draw(screen)




    #pg.draw.circle(screen, "white", pg.mouse.get_pos(), 100, 1)

    pg.display.flip()