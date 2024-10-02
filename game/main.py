import pgzrun
import random
from pgzero.builtins import *

WIDTH = 320
HEIGHT = 416
TITLE = "Игровой котик"
FPS = 30

class Game:
    def __init__(self):
        self.ui = Actor("ui", topup=(160, 48))
        self.bg = Actor("background", center=(WIDTH / 2, HEIGHT / 2 + 48))
        self.cat = Cat()
        self.coin = Coin()
        self.cells = [Cell(i * 32, j * 32 + 96) for i in range(10) for j in range(10)]
        self.cat_target_x = self.cat.actor.x
        self.cat_target_y = self.cat.actor.y
    
    def draw(self):
        self.ui.draw()
        self.bg.draw()
        self.cat.draw()
        self.coin.draw()
        screen.draw.text("Игровой котик", bottomright=(WIDTH / 2 + 96, HEIGHT /2 - 145), color=(0,0,0), fontname=("font"))
        for cell in self.cells:
            cell.draw()
            
    def on_key_down(self):
        if keyboard.left and self.cat.actor.x > 16:
            self.cat.update(-32, 0)
        elif keyboard.right and self.cat.actor.x < 304:
            self.cat.update(32, 0)
        elif keyboard.up and self.cat.actor.y > 112:
            self.cat.update(0, -32)
        elif keyboard.down and self.cat.actor.y < 400:
            self.cat.update(0, 32)
        

class Cat:
    def __init__(self):
        self.actor = Actor("cat_sit_down", center=(random.randint(0, 9) * 32 + 16, random.randint(0, 9) * 32 + 112))
        self.images_left = [
            "cat_walk_left_1",
            "cat_walk_left_2",
            "cat_walk_left_3",
            "cat_sit_left"
            ]
        self.images_right = [
            "cat_walk_right_1",
            "cat_walk_right_2",
            "cat_walk_right_3",
            "cat_sit_right"
            ]
        self.images_up = [
            "cat_walk_up_1",
            "cat_walk_up_2",
            "cat_walk_up_3",
            "cat_sit_up"
            ]
        self.images_down = [
            "cat_walk_down_1",
            "cat_walk_down_2",
            "cat_walk_down_3",
            "cat_sit_down"
            ]
        self.frame = 0
        self.direction = None

    def draw(self):
        self.actor.draw()
        
    def update(self, dx, dy):
        self.actor.x += dx
        self.actor.y += dy
        if dx < 0:
            self.actor.image = self.images_left[self.frame]
            self.direction = "left"
        elif dx > 0:
            self.actor.image = self.images_right[self.frame]
            self.direction = "right"
        elif dy < 0:
            self.actor.image = self.images_up[self.frame]
            self.direction = "up"
        elif dy > 0:
            self.actor.image = self.images_down[self.frame]
            self.direction = "down"
        self.frame = (self.frame + 1) % 3
        if self.frame == 0:
            if self.direction == "left":
                self.actor.image = self.images_left[3]
            elif self.direction == "right":
                self.actor.image = self.images_right[3]
            elif self.direction == "up":
                self.actor.image = self.images_up[3]
            elif self.direction == "down":
                self.actor.image = self.images_down[3]

class Coin:
    def __init__(self):
        self.actor = Actor("coin", center=(random.randint(0, 9) * 32 + 16, random.randint(0, 9) * 32 + 112))

    def draw(self):
        self.actor.draw()

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        screen.draw.line((self.x, self.y), (self.x + 32, self.y), (0, 0, 0))
        screen.draw.line((self.x + 32, self.y), (self.x + 32, self.y + 32), (0, 0, 0))
        screen.draw.line((self.x + 32, self.y + 32), (self.x, self.y + 32), (0, 0, 0))
        screen.draw.line((self.x, self.y + 32), (self.x, self.y), (0, 0, 0))

game = Game()

def draw():
    game.draw()

def on_key_down():
    game.on_key_down()

pgzrun.go()