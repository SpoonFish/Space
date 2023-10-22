import pygame as pg
import Entities.projectiles
import Entities.enemies
import random as rnd
import Entities.player
import Data.monster_data

class EntityManager:
    def __init__(self) -> None:
        self.player_projectiles = []
        self.enemy_projectiles = []
        self.enemies = []
        self.asteroid_time = 0
        self.current_wave = 0
        self.wave_timer = 2
        self.player = Entities.player.Player()

    def CreateAsteroid(self, pos, size, vel=None):
        hp = max(1,size//30)
        if size <= 37:
            return
        vela = None
        if vel != None:
            vela = pg.Vector2(vel.x/rnd.uniform(0.7,1.7)+rnd.uniform(-1,1),vel.y/rnd.uniform(0.7,1.7)+rnd.uniform(-1,1))
        self.enemies.append(Entities.enemies.AsteroidEnemy(pos, hp, size+rnd.randint(-10,10), size+rnd.randint(-25,5), vela))


    def CreatePlayerBullet(self, pos, vel):
        self.player_projectiles.append(Entities.projectiles.PlayerBullet(pos, vel))

    def SummonWave(self, wave_num, gui_manager):
        self.current_wave = wave_num
        gui_manager.SetFallingText(f"WAVE {wave_num}")
        wave = Data.monster_data.WAVES[wave_num]
        for i in range(len(wave.enemies)):
            pos = pg.Vector2(wave.enemies[i][0][0],wave.enemies[i][0][1]+0.15) * (1920/12)
            enemy = wave.enemies[i][1]
            match enemy.type:
                case "dasher":
                    self.enemies.append(Entities.enemies.DasherEnemy(pos, enemy.hp))
                case "shooter":
                    self.enemies.append(Entities.enemies.ShooterEnemy(pos, enemy.hp))
                case "burster":
                    self.enemies.append(Entities.enemies.BursterEnemy(pos, enemy.hp))
                case "bola":
                    self.enemies.append(Entities.enemies.BolaEnemy(pos, enemy.hp))
                case "star":
                    self.enemies.append(Entities.enemies.StarEnemy(pos, enemy.hp))
                case "launcher":
                    self.enemies.append(Entities.enemies.LauncherEnemy(pos, enemy.hp))
                case "asteroid":
                    self.enemies.append(Entities.enemies.AsteroidEnemy(pos, enemy.hp))


    def CreateEnemyBullet(self, pos, vel, type = "normal"):
        match type:
            case "normal":
                self.enemy_projectiles.append(Entities.projectiles.EnemyBullet(pos, vel))
            case "burst":
                self.enemy_projectiles.append(Entities.projectiles.EnemyBurstBullet(pos, vel))
            case "bola":
                self.enemy_projectiles.append(Entities.projectiles.EnemyBolaBullet(pos, vel))
            case "star":
                self.enemy_projectiles.append(Entities.projectiles.EnemyStarBullet(pos, vel))

    def Update(self, dt, particle_manager, gui_manager):
        if Data.monster_data.WAVES[self.current_wave].asteroid_rate > 0:
            self.asteroid_time -= dt
            if self.asteroid_time < 0:
                self.asteroid_time = rnd.uniform(1,2) / Data.monster_data.WAVES[self.current_wave].asteroid_rate
                self.CreateAsteroid(rnd.choice([pg.Vector2(rnd.randint(-100,1700),-60),pg.Vector2(-100,rnd.randint(-60,800))]), rnd.randint(40,120), )
        for projectile in self.player_projectiles:
            projectile.Update(dt, particle_manager)
            if projectile.remove:
                self.player_projectiles.remove(projectile)
        for projectile in self.enemy_projectiles:
            projectile.Update(dt, particle_manager, self)
            if projectile.remove:
                self.enemy_projectiles.remove(projectile)

        for enemy in self.enemies:
            enemy.Update(dt, self, particle_manager)
            if enemy.remove:
                self.enemies.remove(enemy)

        if self.IsWaveOver() and self.current_wave > 0:
            self.wave_timer -= dt
            if self.wave_timer < 0:
                self.wave_timer = 5
                self.SummonWave(self.current_wave + 1, gui_manager)
    def IsWaveOver(self) -> bool:
        if Data.monster_data.WAVES[self.current_wave].asteroid_rate > 0:
            for enemy in self.enemies:
                if not isinstance(enemy, Entities.enemies.AsteroidEnemy):
                    return False
            return True
        else:
            return len(self.enemies) == 0
    def Draw(self, screen):
        for projectile in self.player_projectiles:
            projectile.Draw(screen)
        for projectile in self.enemy_projectiles:
            projectile.Draw(screen)


        for enemy in self.enemies:
            enemy.Draw(screen)

        self.player.Draw(screen)