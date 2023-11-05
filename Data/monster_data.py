import pygame as pg

class MonsterData:
    def __init__(self, type, hp) -> None:
        self.type = type
        self.hp = hp

class WaveData:
    def __init__(self, enemies: list[list[(int, int), MonsterData]], asteroids = 0) -> None:
        self.enemies = enemies
        self.asteroid_rate = asteroids

WAVES = {
    0: WaveData([],False),
    1: WaveData([
        [(3,0), MonsterData("shooter",2)],
        [(6,0), MonsterData("dasher",2)],
        [(9,0), MonsterData("dasher",2)],
    ]
    ),
    2: WaveData([
        [(3,0), MonsterData("shooter",3)],
        [(4,0), MonsterData("dasher",3)],
        [(9,0), MonsterData("dasher",3)],
        [(8,0), MonsterData("shooter",3)],
    ]),
    3: WaveData([
        [(4,0), MonsterData("burster",3)],
        [(7,0), MonsterData("star",3)],
        [(8,0), MonsterData("bola",3)],
    ]),
    4: WaveData([
        [(3,0), MonsterData("star",2)],
        [(4,0), MonsterData("launcher",2)],
        [(8,0), MonsterData("shooter",2)],
        [(9,0), MonsterData("star",2)],
    ]),
    5: WaveData([
        [(3,0), MonsterData("shooter",20)],
        [(4,0), MonsterData("dasher",2)],
        [(8,0), MonsterData("dasher",2)],
        [(9,0), MonsterData("dasher",2)],
    ])
}