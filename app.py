from flask import Flask, render_template, request, jsonify
import requests
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Глобальные переменные для хранения игрока и команды
player = None
command = None

# Функция для получения списка лидеров по количеству монет
def get_leaders():
    # Подключаемся к базе данных SQLite
    conn = sqlite3.connect('players.db')
    cursor = conn.cursor()
    # Выполняем запрос для получения списка лидеров
    cursor.execute('''
        SELECT 
            ROW_NUMBER() OVER (ORDER BY coins DESC) AS place,
            name,
            date,
            coins
        FROM players
        ORDER BY coins DESC
    ''')
    # Получаем результаты запроса
    leaders = cursor.fetchall()
    # Закрываем соединение с базой данных
    conn.close()
    return leaders

# Функция для добавления монет игроку
def add_coins(player):
    conn = sqlite3.connect('players.db')
    cursor = conn.cursor()
    # Проверяем, существует ли игрок в базе данных
    cursor.execute('SELECT * FROM players WHERE name = ?', (player,))
    if cursor.fetchone() is None:
        print('Игрок с таким именем не существует')
        conn.close()
        return
    # Добавляем монеты игроку
    cursor.execute('UPDATE players SET coins = coins + 1 WHERE name = ?', (player,))
    conn.commit()
    print('Монеты добавлены')
    conn.close()

# Функция для добавления координат игроку
def add_coordinates(player, command):
    conn = sqlite3.connect('players.db')
    cursor = conn.cursor()
    # Проверяем, существует ли игрок в базе данных
    cursor.execute('SELECT * FROM players WHERE name = ?', (player,))
    if cursor.fetchone() is None:
        print('Игрок с таким именем не существует')
        conn.close()
        return
    # Добавляем координаты игроку
    cursor.execute('UPDATE players SET cat_coors = ? WHERE name = ?', (command, player))
    conn.commit()
    print('Координаты добавлены')
    conn.close()
    
# Функция для получения списка игроков и их координат
def get_players():
    # Подключаемся к базе данных SQLite
    conn = sqlite3.connect('players.db')
    cursor = conn.cursor()
    # Выполняем запрос для получения списка игроков и их координат
    cursor.execute('SELECT name, cat_coors FROM players')
    # Получаем результаты запроса
    players = cursor.fetchall()
    # Закрываем соединение с базой данных
    conn.close()
    # Формируем словарь игроков и их координат
    players_dict = {player[0]: player[1] for player in players}
    print(players_dict)
    return players_dict

# Функция для создания нового игрока
def add_player(player):
    # Создаем новые значения для игрока
    cat_coors = None
    coins = 0
    command = 'create_player'
    # Подключаемся к базе данных SQLite
    conn = sqlite3.connect('players.db')
    cursor = conn.cursor()
    # Создаем таблицу players, если она не существует
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY,
            name TEXT,
            cat_coors TEXT,
            date TEXT,
            coins INTEGER
        )
    ''')
    # Проверяем, существует ли игрок в базе данных
    cursor.execute('SELECT * FROM players WHERE name = ?', (player,))
    if cursor.fetchone() is not None:
        print('Игрок с таким именем уже существует')
        conn.close()
        return
    # Создаем нового игрока
    join_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('INSERT INTO players (name, cat_coors, date, coins) VALUES (?, ?, ?, ?)', (player, cat_coors, join_date, coins))
    conn.commit()
    # Отправляем POST-запрос для создания игрока
    url = 'http://localhost:5000/api'
    headers = {'Content-Type': 'application/json'}
    new_data = {'command': command, 'player': player}
    response = requests.post(url, headers=headers, json=new_data)
    print('Учетка создана', new_data)
    conn.close()

# Функция для обработки POST-запросов
@app.route('/api', methods=['GET', 'POST'])
def handle_button_press():
    global player
    global command
    if request.method == 'POST':
        # Получаем данные из POST-запроса
        data = request.get_json()
        command = data.get('command')
        player = data.get('player')
        # Обрабатываем команды
        if command == 'create_player':
            return add_player(player)
        elif command == 'coin_collect':
            add_coins(player)
        elif command in ['move_right','move_left','move_up','move_down']:
            add_coordinates(player, command)
        elif command == 'load_players':
            players = get_players()
            players_dict = {}
            for player_name, coors in players.items():
                players_dict[player_name] = coors
            return jsonify({'command': 'load_players', 'players': players_dict})
        else:
            add_coordinates(player, command)
        return jsonify({'message': ' OK'})
    elif request.method == 'GET':
        if command == 'create_player':
            return jsonify({'player': player, 'command': command})
        elif command in ['move_right','move_left','move_up','move_down']:
            return jsonify({'player': player, 'command': command})
        elif command == 'load_players':
            players = get_players()
            players_dict = {}
            for player_name, coors in players.items():
                players_dict[player_name] = coors
            return jsonify({'command': 'load_players', 'players': players_dict})
        else:
            return jsonify({'message': 'Invalid request'})

# Функция для отображения лидеров по количеству монет
@app.route('/leaders', methods=['GET'])
def show_leaders():
    leaders = get_leaders()
    return render_template('leaders.html', leaders=leaders)

# Просто портфолио с честно спиз...взятого с интернета оформлением
@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)