import pygame as pg
import Entities.projectiles
import Entities.player

class EntityManager:
    def __init__(self) -> None:
        self.player_projectiles = []
        self.enemy_projectiles = []
        self.enemies = []
        self.player = Entities.player.Player()

    def CreatePlayerBullet(self, pos, vel):
        self.player_projectiles.append(Entities.projectiles.PlayerBullet(pos, vel))

    def CreateEnemyBullet(self, pos, vel):
        self.enemy_projectiles.append(Entities.projectiles.EnemyBullet(pos, vel))

    def Update(self, dt, particle_manager):
        for projectile in self.player_projectiles:
            projectile.Update(dt, particle_manager)
            if projectile.remove:
                self.player_projectiles.remove(projectile)
        for projectile in self.enemy_projectiles:
            projectile.Update(dt, particle_manager)
            if projectile.remove:
                self.enemy_projectiles.remove(projectile)

        for enemy in self.enemies:
            enemy.Update(dt, self, particle_manager)
            if enemy.remove:
                self.enemies.remove(enemy)

    def Draw(self, screen):
        for projectile in self.player_projectiles:
            projectile.Draw(screen)
        for projectile in self.enemy_projectiles:
            projectile.Draw(screen)


        for enemy in self.enemies:
            enemy.Draw(screen)

        self.player.Draw(screen)