import pgzrun
import random
import time
from pgzero.builtins import *

WIDTH = 320
HEIGHT = 411
TITLE = "Игровой котик"
FPS = 30

class Game:
    def __init__(self):
        self.ui = Actor("ui", center=(WIDTH / 2 + 20, HEIGHT /2 - 158))
        self.bg = Actor("background", center=(WIDTH / 2, HEIGHT / 2 + 48))
        self.coin_score = Actor("coin", center=(WIDTH / 2 - 132 , HEIGHT /2 - 182))
        self.cat = Cat()
        self.coin = Coin()
        self.cells = [Cell(i * 32, j * 32 + 93) for i in range(10) for j in range(10)]
        self.player_name = "None"
        music.play("music")
        music.set_volume(0.1) 
        self.coin_collect = 0

    def draw(self):
        screen.draw.filled_rect(Rect(0, 0, 320, 92), (255, 255, 255))
        self.ui.draw()
        self.bg.draw()
        for cell in self.cells:
            cell.draw()
        self.update()
        self.coin.draw()
        self.cat.draw()
        self.coin_score.draw()
        screen.draw.text(self.player_name, center=(self.cat.actor.x, self.cat.actor.y - 15), color=(255, 0, 0)) 
        screen.draw.text("Игровой котик", center=(self.ui.x, self.ui.y), color=(0,0,0), fontname=("font"))
        screen.draw.text(str(self.coin_collect), center=(self.coin_score.x, self.coin_score.y + 20), color=(0,0,0), fontname=("font"))
        

    def update(self):
        self.cat.update()
        
class Cat:
    def __init__(self):
        self.actor = Actor("cat_sit_down", center=(random.randint(0, 9) * 32 + 16, random.randint(0, 9) * 32 + 106))
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
        self.animation_playing = False
        self.animation_frame = 0

    def draw(self):
        self.actor.draw()

    def on_key_down(self):
        if self.animation_playing:
            return
        if keyboard.left and self.actor.x > 16:
            self.animation_playing = True
            self.animation_frame = 0
            self.direction = "left"
            animate(self.actor, tween='linear', duration=2, x=self.actor.x - 32, on_finished=self.on_animation_finished)
        elif keyboard.right and self.actor.x < 304:
            self.animation_playing = True
            self.animation_frame = 0
            self.direction = "right"
            animate(self.actor, tween='linear', duration=2, x=self.actor.x + 32, on_finished=self.on_animation_finished)
        elif keyboard.up and self.actor.y > 112:
            self.animation_playing = True
            self.animation_frame = 0
            self.direction = "up"
            animate(self.actor, tween='linear', duration=2, y=self.actor.y - 32, on_finished=self.on_animation_finished)
        elif keyboard.down and self.actor.y < 400:
            self.animation_playing = True
            self.animation_frame = 0
            self.direction = "down"
            animate(self.actor, tween='linear', duration=2, y=self.actor.y + 32, on_finished=self.on_animation_finished)

    def on_animation_finished(self):
        collision_check_result = self.actor.colliderect(game.coin.actor)
        if collision_check_result:
            sounds.coin_collect.play()
            game.coin.update()
        self.animation_playing = False
        if self.direction == "left":
            self.actor.image = "cat_sit_left"
        elif self.direction == "right":
            self.actor.image = "cat_sit_right"
        elif self.direction == "up":
            self.actor.image = "cat_sit_up"
        elif self.direction == "down":
            self.actor.image = "cat_sit_down"

    def update(self):
        if self.animation_playing:
            self.animation_frame = (self.animation_frame + 1) % 3
            time.sleep(0.1)
            if self.direction == "left":
                self.actor.image = self.images_left[self.animation_frame]
            elif self.direction == "right":
                self.actor.image = self.images_right[self.animation_frame]
            elif self.direction == "up":
                self.actor.image = self.images_up[self.animation_frame]
            elif self.direction == "down":
                self.actor.image = self.images_down[self.animation_frame]


class Coin:
    def __init__(self):
        self.actor = Actor("coin", center=(random.randint(0, 9) * 32 + 16, random.randint(0, 9) * 32 + 112))

    def draw(self):
        self.actor.draw()
        
    def update(self):
        self.actor.x = random.randint(0, 9) * 32 + 16
        self.actor.y = random.randint(0, 9) * 32 + 112
        game.coin_collect += 1

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
    game.cat.on_key_down()

def start():
    pgzrun.go()
    
start()