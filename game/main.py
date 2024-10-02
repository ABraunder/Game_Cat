import pgzrun
import random
import time
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
        self.cat_animation_playing = False
        self.cat_animation_frame = 0

    def draw(self):
        self.ui.draw()
        self.bg.draw()
        self.coin.draw()
        self.cat.draw()
        screen.draw.text("Игровой котик", bottomright=(WIDTH / 2 + 96, HEIGHT /2 - 145), color=(0,0,0), fontname=("font"))
        for cell in self.cells:
            cell.draw()
        self.update()

    def on_key_down(self):
        if self.cat_animation_playing == True:
            return
        if keyboard.left and self.cat.actor.x > 16:
            self.cat_animation_playing = True
            self.cat_animation_frame = 0
            self.cat.direction = "left"
            animate(self.cat.actor, tween='linear', duration=2, x=self.cat.actor.x - 32, on_finished=self.on_animation_finished)
        elif keyboard.right and self.cat.actor.x < 304:
            self.cat_animation_playing = True
            self.cat_animation_frame = 0
            self.cat.direction = "right"
            animate(self.cat.actor, tween='linear', duration=2, x=self.cat.actor.x + 32, on_finished=self.on_animation_finished)
        elif keyboard.up and self.cat.actor.y > 112:
            self.cat_animation_playing = True
            self.cat_animation_frame = 0
            self.cat.direction = "up"
            animate(self.cat.actor, tween='linear', duration=2, y=self.cat.actor.y - 32, on_finished=self.on_animation_finished)
        elif keyboard.down and self.cat.actor.y < 400:
            self.cat_animation_playing = True
            self.cat_animation_frame = 0
            self.cat.direction = "down"
            animate(self.cat.actor, tween='linear', duration=2, y=self.cat.actor.y + 32, on_finished=self.on_animation_finished)

    def on_animation_finished(self):
        self.cat_animation_playing = False
        collision_check_result =  self.cat.actor.colliderect(self.coin.actor)
        if collision_check_result:
            self.coin.update()
        if self.cat.direction == "left":
            self.cat.actor.image = "cat_sit_left"
        elif self.cat.direction == "right":
            self.cat.actor.image = "cat_sit_right"
        elif self.cat.direction == "up":
            self.cat.actor.image = "cat_sit_up"
        elif self.cat.direction == "down":
            self.cat.actor.image = "cat_sit_down"

    def update(self):
        if self.cat_animation_playing:
            self.cat_animation_frame = (self.cat_animation_frame + 1) % 3
            time.sleep(0.1)
            if self.cat.direction == "left":
                self.cat.actor.image = self.cat.images_left[self.cat_animation_frame]
            elif self.cat.direction == "right":
                self.cat.actor.image = self.cat.images_right[self.cat_animation_frame]
            elif self.cat.direction == "up":
                self.cat.actor.image = self.cat.images_up[self.cat_animation_frame]
            elif self.cat.direction == "down":
                self.cat.actor.image = self.cat.images_down[self.cat_animation_frame]

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


class Coin:
    def __init__(self):
        self.actor = Actor("coin", center=(random.randint(0, 9) * 32 + 16, random.randint(0, 9) * 32 + 112))
        self.coin_collect = 0

    def draw(self):
        self.actor.draw()
        
    def update(self):
        self.actor.x = random.randint(0, 9) * 32 + 16
        self.actor.y = random.randint(0, 9) * 32 + 112
        self.coin_collect += 1

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