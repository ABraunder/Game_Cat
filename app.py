from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Соединение с базой данных
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

# Функция для получения списка лидеров по количеству монет
def get_leaders():
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
    return leaders

# Функция для добавления монет игроку
def add_coins(player):
    # Проверяем, существует ли игрок в базе данных
    cursor.execute('SELECT * FROM players WHERE name = ?', (player,))
    if cursor.fetchone() is None:
        print('Игрок с таким именем не существует')
        return
    # Добавляем монеты игроку
    cursor.execute('UPDATE players SET coins = coins + 1 WHERE name = ?', (player,))
    conn.commit()
    print('Монеты добавлены')

# Функция для добавления координат игроку
def add_coordinates(player, command):
    # Проверяем, существует ли игрок в базе данных
    cursor.execute('SELECT * FROM players WHERE name = ?', (player,))
    if cursor.fetchone() is None:
        print('Игрок с таким именем не существует')
        return
    # Добавляем координаты игроку
    cursor.execute('UPDATE players SET cat_coors = ? WHERE name = ?', (command, player))
    conn.commit()
    print('Координаты добавлены')

# Функция для создания нового игрока
def add_player(player):
    # Проверяем, существует ли игрок в базе данных
    cursor.execute('SELECT * FROM players WHERE name = ?', (player,))
    if cursor.fetchone() is not None:
        print('Игрок с таким именем уже существует')
        return
    # Создаем нового игрока
    join_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('INSERT INTO players (name, cat_coors, date, coins) VALUES (?, ?, ?, ?)', (player, None, join_date, 0))
    conn.commit()
    print('Учетка создана')

# Функция для обработки POST-запросов
@app.route('/api', methods=['GET', 'POST'])
def handle_button_press():
    if request.method == 'POST':
        # Получаем данные из POST-запроса
        data = request.get_json()
        command = data.get('command')
        player = data.get('player')
        # Обрабатываем команды
        if command == 'create_player':
            add_player(player)
        elif command == 'coin_collect':
            add_coins(player)
        elif command in ['move_right','move_left','move_up','move_down']:
            pass
        else:
            add_coordinates(player, command)
        return jsonify({'message': 'OK'})
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