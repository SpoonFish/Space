import pygame as pg

class MonsterData:
    def __init__(self, type, hp) -> None:
        self.type = type
        self.hp = hp

class WaveData:
    def __init__(self, enemies: list[list[(int, int), MonsterData]]) -> None:
        self.enemies = enemies

WAVES = {
    1: WaveData([
        [(3,0), MonsterData("burster",2)],
        [(4,0), MonsterData("burster",2)],
        [(8,0), MonsterData("burster",2)],
        [(9,0), MonsterData("burster",2)],
    ]),
    2: WaveData([
        [(3,0), MonsterData("shooter",2)],
        [(4,0), MonsterData("dasher",2)],
        [(10,0), MonsterData("burster",5)],
        [(8,0), MonsterData("dasher",2)],
        [(9,0), MonsterData("shooter",2)],
    ]),
    3: WaveData([
        [(1,0), MonsterData("shooter",3)],
        [(4,0), MonsterData("shooter",3)],
        [(8,0), MonsterData("shooter",3)],
        [(11,0), MonsterData("shooter",3)],
    ]),
    4: WaveData([
        [(1,0), MonsterData("dasher",2)],
        [(2,0), MonsterData("dasher",2)],
        [(3,0), MonsterData("dasher",2)],
        [(4,0), MonsterData("dasher",2)],
        [(8,0), MonsterData("dasher",2)],
        [(9,0), MonsterData("dasher",2)],
        [(10,0), MonsterData("dasher",2)],
        [(11,0), MonsterData("dasher",2)],
    ]),
    5: WaveData([
        [(3,0), MonsterData("shooter",20)],
        [(4,0), MonsterData("dasher",2)],
        [(8,0), MonsterData("dasher",2)],
        [(9,0), MonsterData("dasher",2)],
    ])
}