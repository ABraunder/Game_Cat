import pgzrun
import random
import time
from pgzero.builtins import *
import requests
import threading
import re

# Размеры игрового окна
WIDTH = 320
HEIGHT = 411
TITLE = "Игровой котик"
FPS = 60

# Класс для игры
class Game:
    def __init__(self):
        # URL для отправки запросов
        self.url = 'http://localhost:5000/api'
        self.ui = Actor("ui", center=(WIDTH / 2 + 20, HEIGHT /2 - 158))
        self.bg = Actor("background", center=(WIDTH / 2, HEIGHT / 2 + 48))
        self.cat = Cat(None)
        self.coin = Coin("coin")
        self.cells = [Cell(i * 32, j * 32 + 93) for i in range(10) for j in range(10)]
        self.players = []
        music.play("music")
        music.set_volume(0.1) 
        self.load_players()
        
    def load_players(self):
        new_api_data = {'player': None, 'command': 'load_players'}
        response = requests.post(self.url, json=new_api_data)

    # Метод для отрисовки игры
    def draw(self):
        screen.draw.filled_rect(Rect(0, 0, 320, 92), (255, 255, 255))
        self.ui.draw()
        self.bg.draw()
        for cell in self.cells:
            cell.draw()
        self.update()
        self.coin.draw()
        for player in self.players:
            player.draw()
            screen.draw.text(player.name, center=(player.actor.x, player.actor.y - 15), color=(255, 0, 0))
        screen.draw.text("Игровой котик", center=(self.ui.x, self.ui.y), color=(0,0,0), fontname=("font"))

    # Метод для добавления игрока
    def add_player(self, name, x=None, y=None):
        # Проверка, существует ли игрок с таким именем
        for player in self.players:
            if player.name == name:
                # Если игрок существует, то обновляем его координаты
                if x is not None and y is not None:
                    player.actor.x = x
                    player.actor.y = y
                return player

        # Если игрок не существует, то создаем нового игрока
        if x is None or y is None:
            # Установка координат игрока
            x = random.randint(0, 9) * 32 + 16
            y = random.randint(0, 9) * 32 + 106

        # Создание нового игрока
        new_player = Cat(name)
        new_player.actor.x = x
        new_player.actor.y = y
        # Добавление игрока в список
        self.players.append(new_player)
        command = f'{new_player.actor.x}, {new_player.actor.y}'
        print(f'Создан кот с именем {name} на координатах {command}')
        # Отправка запроса на создание игрока
        new_api_data = {'player': name, 'command': command}
        response = requests.post(self.url, json=new_api_data)
        # Обновление игры
        new_api_data = {'player': None, 'command': None}
        response = requests.post(self.url, json=new_api_data)
        # Запланирование обновления игры
        clock.schedule_unique(game.draw, 0.1)
    
    # Метод для обработки запросов от API
    def handle_api_request(self):
        while True:
            # Отправка запроса на получение данных от API
            response = requests.get(self.url)
            if response.status_code == 200:
                # Получение данных от API
                data = response.json()
                # Команда от API
                command = data.get('command')
                player_name = data.get('player')
                print("Функция: ", data)
                if command is not None:
                    if command == 'load_players':
                        # Получение словаря игроков и их координат
                        players = data.get('players')
                        if players is not None:
                            for name, coors in players.items():
                                # Обработка строки с координатами
                                if coors is not None:
                                    coors_parts = coors.split(',')
                                    if len(coors_parts) == 2:
                                        x_str, y_str = coors_parts
                                        x = None if x_str.lower() == 'none' else float(x_str)
                                        y = None if y_str.lower() == 'none' else float(y_str)
                                        self.add_player(name, x, y)
                                        new_api_data = {'player': None, 'command': None}
                                        response = requests.post(self.url, json=new_api_data)
                                    else:
                                        print(f"Неправильный формат строки с координатами: {coors}")
                                else:
                                    # Создание нового игрока, если координат нет
                                    self.add_player(name, 80.0, 170.0)
                                    new_api_data = {'player': None, 'command': None}
                                    response = requests.post(self.url, json=new_api_data)
                        else:
                            print("Нет данных о игроках")
                    # Обработка команды от API
                    elif command in ['move_right','move_left','move_up','move_down']:
                        # Обработка перемещения игрока
                        for player in self.players:
                            if player.name == player_name:
                                player.on_key_down(command)
                                # Отправка запроса на обновление игрока
                                new_api_data = {'player': None, 'command': None}
                                response = requests.post(self.url, json=new_api_data)
                    elif command == 'create_player':
                        # Обработка создания игрока
                        print(data)
                        self.add_player(player_name)
                    else:
                        # Затычка
                        pass
                else:
                    # Обработка ошибки получения данных от API
                    print('Failed to retrieve API data')
            # Пауза между запросами
            time.sleep(1)
            
            """"Да, я согласен, это треш, но вы видели ТЗ?!
            Каким ещё образом я должен управлять игрой через Flask с помощью кнопок в Discord"""
        
    # Метод для обновления игры
    def update(self):
        self.cat.update()

# Класс для кота
class Cat:
    def __init__(self, name):
        self.name = name
        self.actor = Actor("cat_sit_down", center=(random.randint(0, 9) * 32 + 16, random.randint(0, 9) * 32 + 106))
        # Изображения для анимации кота
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

    # Метод для отрисовки кота
    def draw(self):
        self.actor.draw()
        
    # Метод для обработки нажатия клавиши
    def on_key_down(self, button_label):
        # Проверка анимации
        if self.animation_playing:
            return
        # Обработка перемещения кота
        if button_label == "move_left" and self.actor.x > 16:
            self.animation_playing = True
            self.animation_frame = 0
            self.direction = "left"
            animate(self.actor, tween='linear', duration=2, x=self.actor.x - 32, on_finished=self.on_animation_finished)
            self.animate_move()
        elif button_label == "move_right" and self.actor.x < 304:
            self.animation_playing = True
            self.animation_frame = 0
            self.direction = "right"
            animate(self.actor, tween='linear', duration=2, x=self.actor.x + 32, on_finished=self.on_animation_finished)
            self.animate_move()
        elif button_label == "move_up" and self.actor.y > 112:
            self.animation_playing = True
            self.animation_frame = 0
            self.direction = "up"
            animate(self.actor, tween='linear', duration=2, y=self.actor.y - 32 , on_finished=self.on_animation_finished)
            self.animate_move()
        elif button_label == "move_down" and self.actor.y < 400:
            self.animation_playing = True
            self.animation_frame = 0
            self.direction = "down"
            animate(self.actor, tween='linear', duration=2, y=self.actor.y + 32, on_finished=self.on_animation_finished)
            self.animate_move()

    # Метод для анимации перемещения кота
    def animate_move(self):
        # Запланирование обновления анимации
        clock.schedule_interval(self.update, 0.1)

    # Метод для обработки окончания анимации
    def on_animation_finished(self):
        # Проверка столкновения с монетой
        collision_check_result = self.actor.colliderect(game.coin.actor)
        if collision_check_result:
            # Воспроизведение звука сбора монеты
            sounds.coin_collect.play()
            # Отправка запроса на сбор монеты
            new_api_data = {'command': 'coin_collect', 'player': self.name}
            response = requests.post(game.url, json=new_api_data)
            # Обновление монеты
            game.coin.update()
        # Сброс флага анимации
        self.animation_playing = False
        # Установка изображения кота в зависимости от направления движения
        if self.direction == "left":
            self.actor.image = "cat_sit_left"
        elif self.direction == "right":
            self.actor.image = "cat_sit_right"
        elif self.direction == "up":
            self.actor.image = "cat_sit_up"
        elif self.direction == "down":
            self.actor.image = "cat_sit_down"
        # Отправка запроса на обновление координат кота
        self.send_coors()
            
    # Метод для отправки координат кота
    def send_coors(self):
        # Команда для отправки координат
        command = f"{self.actor.x}, {self.actor.y}"
        print(command)
        # Отправка запроса на обновление координат
        new_api_data = {'player': self.name, 'command': command}
        response = requests.post(game.url, json=new_api_data)

    # Метод для обновления кота
    def update(self):
        # Проверка анимации
        if self.animation_playing:
            # Обновление текущего кадра анимации
            self.animation_frame = (self.animation_frame + 1) % 3
            # Пауза между кадрами анимации
            time.sleep(0.1)
            # Установка изображения кота в зависимости от направления движения
            if self.direction == "left":
                self.actor.image = self.images_left[self.animation_frame]
            elif self.direction == "right":
                self.actor.image = self.images_right[self.animation_frame]
            elif self.direction == "up":
                self.actor.image = self.images_up[self.animation_frame]
            elif self.direction == "down":
                self.actor.image = self.images_down[self.animation_frame]
            

# Класс для монеты
class Coin:
    def __init__(self, name):
        self.name = None
        self.actor = Actor("coin", center=(random.randint(0, 9) * 32 + 16, random.randint(0, 9) * 32 + 112))

    # Метод для отрисовки монеты
    def draw(self):
        self.actor.draw()
        
    # Метод для обновления монеты
    def update(self):
        # Установка случайных координат монеты
        self.actor.x = random.randint(0, 9) * 32 + 16
        self.actor.y = random.randint(0, 9) * 32 + 112
        # Отправка запроса на сбор монеты
        new_api_data = {'command': 'coin_collect', 'player': self.name}
        response = requests.post(game.url, json=new_api_data)


# Класс для ячеек
class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Метод для отрисовки ячейки
    def draw(self):
        screen.draw.line((self.x, self.y), (self.x + 32, self.y), (0, 0, 0))
        screen.draw.line((self.x + 32, self.y), (self.x + 32, self.y + 32), (0, 0, 0))
        screen.draw.line((self.x + 32, self.y + 32), (self.x, self.y + 32), (0, 0, 0))
        screen.draw.line((self.x, self.y + 32), (self.x, self.y), (0, 0, 0))


# Создание игры
game = Game()

# Функция для отрисовки игры
def draw():
    game.draw()

# Функция для обработки нажатия клавиши
def on_key_down():
    game.cat.on_key_down()
    
# Функция для отправки запроса на сбор монеты
def get_api_data(button_label):
    game.cat.on_key_down(button_label)

# Функция для запуска игры
def start():
    # Запуск обработки запросов от API
    threading.Thread(target=game.handle_api_request).start()
    # Запуск игры
    pgzrun.go()
    
# Запуск игры
start()