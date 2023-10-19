import pygame as pg
import Entities.projectiles
import Entities.enemies
import Entities.player
import Data.monster_data

class EntityManager:
    def __init__(self) -> None:
        self.player_projectiles = []
        self.enemy_projectiles = []
        self.enemies = []
        self.current_wave = 0
        self.wave_timer = 2
        self.player = Entities.player.Player()

    def CreatePlayerBullet(self, pos, vel):
        self.player_projectiles.append(Entities.projectiles.PlayerBullet(pos, vel))

    def SummonWave(self, wave_num, gui_manager):
        self.current_wave = wave_num
        gui_manager.SetFallingText(f"WAVE {wave_num}")
        wave = Data.monster_data.WAVES[wave_num]
        for i in range(len(wave.enemies)):
            pos = pg.Vector2(wave.enemies[i][0][0],wave.enemies[i][0][1]) * (1920/12)
            enemy = wave.enemies[i][1]
            match enemy.type:
                case "dasher":
                    self.enemies.append(Entities.enemies.DasherEnemy(pos, "dasher", enemy.hp, 60,60))
                case "shooter":
                    self.enemies.append(Entities.enemies.ShooterEnemy(pos, "shooter", enemy.hp, 60,60))
                case "burster":
                    self.enemies.append(Entities.enemies.BursterEnemy(pos, "burster", enemy.hp, 60,60))


    def CreateEnemyBullet(self, pos, vel):
        self.enemy_projectiles.append(Entities.projectiles.EnemyBullet(pos, vel))

    def Update(self, dt, particle_manager, gui_manager):
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

        if len(self.enemies) == 0 and self.current_wave > 0:
            self.wave_timer -= dt
            if self.wave_timer < 0:
                self.wave_timer = 2
                self.SummonWave(self.current_wave + 1, gui_manager)

    def Draw(self, screen):
        for projectile in self.player_projectiles:
            projectile.Draw(screen)
        for projectile in self.enemy_projectiles:
            projectile.Draw(screen)


        for enemy in self.enemies:
            enemy.Draw(screen)

        self.player.Draw(screen)