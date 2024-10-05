# Импортируем необходимые библиотеки
import discord
from discord.ext import commands
from discord.ui import View, Button
import requests

#  Токен бота Discord
TOKEN = 'TOKEN'

# Настройки интентов бота
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)
client = discord.Client(intents=intents)

# Класс для отображения кнопок управления котом
class ButtonView(View):
    def __init__(self):
        super().__init__()

    # Обработчик нажатия кнопки "вправо"
    @discord.ui.button(label='→', style=discord.ButtonStyle.blurple)
    async def button_right_callback(self, interaction, button):
        await interaction.response.defer()
        await interaction.followup.send("Обработка...", ephemeral=True)
        await self.send_button_press('move_right', interaction)

    # Обработчик нажатия кнопки "влево"
    @discord.ui.button(label='←', style=discord.ButtonStyle.blurple)
    async def button_left_callback(self, interaction, button):
        await interaction.response.defer()
        await interaction.followup.send("Обработка...", ephemeral=True)
        await self.send_button_press('move_left', interaction)

    # Обработчик нажатия кнопки "вверх"
    @discord.ui.button(label='↑', style=discord.ButtonStyle.blurple)
    async def button_up_callback(self, interaction, button):
        await interaction.response.defer()
        await interaction.followup.send("Обработка...", ephemeral=True)
        await self.send_button_press('move_up', interaction)

    # Обработчик нажатия кнопки "вниз"
    @discord.ui.button(label='↓', style=discord.ButtonStyle.blurple)
    async def button_down_callback(self, interaction, button):
        await interaction.response.defer()
        await interaction.followup.send("Обработка...", ephemeral=True)
        await self.send_button_press('move_down', interaction)

    # Метод для отправки запроса на перемещение кота
    async def send_button_press(self, button_label, interaction):
        url = 'http://localhost:5000/api'
        try:
            # Отправляем GET-запрос на сервер API
            response = requests.get(url) 
            data = {'command': button_label, 'player': interaction.user.name}
            headers = {'Content-Type': 'application/json'}
            # Отправляем POST-запрос на сервер API
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                # Отправляем сообщение об успешном перемещении кота
                await interaction.followup.send("Кот передвинулся", ephemeral=True)
            else:
                await interaction.followup.send("Ошибка", ephemeral=True)
        except requests.exceptions.RequestException as e:
            await interaction.followup.send("Ошибка соединения", ephemeral=True)
            print(f"Ошибка соединения: {e}")

# Команда для присоединения к игре
@bot.command(name='join')
async def join(ctx):
    # Получаем имя пользователя
    discord_name = ctx.author.name
    url = 'http://localhost:5000/api'
    data = {' command': 'create_player', 'player': discord_name}
    headers = {'Content-Type': 'application/json'}
    # Отправляем POST-запрос на сервер API
    response = requests.post(url, headers=headers, json=data)
    # Создаем экземпляр класса ButtonView
    view = ButtonView()
    await ctx.send('Управление котами:', view=view)

# Запускаем бота
bot.run(TOKEN)