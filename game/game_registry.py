from game.Apple_game.game.oop_classes import Game as AppleGame
from game.zombie_shooter.zombie_shooter import ZombieShooter
from game.flappy_bird.flappy_bird import FlappyBirdGame
from game.battle_ship.battleship import BattleshipGame

games = [
    {
        "id": "flappy_bird",
        "name": "FLAPPY BIRD",
        "class": FlappyBirdGame
    },
    {
        "id": "apple_game",
        "name": "Apple Game",
        "class": AppleGame
    },
    {
        "id": "zombie_shooter",
        "name": "Zombie Shooter",
        "class": ZombieShooter
    },
    {
        "id": "battleship",
        "name": "Battle Ship",
        "class": BattleshipGame
    }
]
