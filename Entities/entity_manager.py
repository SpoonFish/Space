import pygame as pg
import Entities.projectiles

class EntityManager:
    def __init__(self) -> None:
        self.player_projectiles = []

    def CreatePlayerBullet(self, pos, vel):
        self.player_projectiles.append(Entities.projectiles.PlayerBullet(pos, vel))

    def Update(self, dt, particle_manager):
        for projectile in self.player_projectiles:
            projectile.Update(dt, particle_manager)
            if projectile.remove:
                self.player_projectiles.remove(projectile)

    def Draw(self, screen):
        for projectile in self.player_projectiles:
            projectile.Draw(screen)