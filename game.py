import math
import random
from tkinter import PhotoImage, NW, Canvas, StringVar, Label, ALL

from settings import asteroids_count, lives


class Game:

    def __init__(self, root):
        #  корды всех вершин треугольника
        self.all_player_coords = [0, 0, 0, 0, 0, 0]
        self.fires_IDs = []
        self.vx_fires = []
        self.vy_fires = []
        self.created_ball = None

        self.player = []
        self.ship_ID = []

        # полотно для рисования
        self.c = Canvas(root, width=1000, height=600, bg='white')

        #  лэйбл со счетом, временем, жизнями
        self.game_time = 0
        self.score = 0
        self.lives = lives
        self.state_label = StringVar()
        Label(root, textvariable=self.state_label).pack()

        self.x_speeds = []
        self.y_speeds = []

        # список с фигурами
        self.asteroids = []

        # координаты первой вершины треугольника
        self.x_player = 0
        self.y_player = 0

        #  картинки
        self.asteroid_image = PhotoImage(file='asteroid.gif')
        self.bullet = PhotoImage(file='bullet.gif')
        self.sky_image = PhotoImage(file='sky.gif')
        self.game_over = PhotoImage(file='game_over.gif')
        #  небо
        self.c.create_image(0, 0, image=self.sky_image, anchor=NW)

    def create_asteroids(self):
        for i in range(asteroids_count):
            # координаты астероида
            x = random.randint(50, 950)
            y = random.randint(50, 550)

            # создаем астероид
            asteroid = self.c.create_image(x, y, image=self.asteroid_image, anchor=NW)

            # придумываем скорость
            vx = random.randint(-12, 12)
            vy = random.randint(-12, 12)

            # добавляем астероид в список
            self.asteroids.append(asteroid)

            # добавляем скорости в списки
            self.x_speeds.append(vx)
            self.y_speeds.append(vy)

    def move_asteroids(self):

        self.game_time += 0.05  # увеличиваем время
        self.state_label.set(f"Score: {str(self.score)}\n"
                             f"Lives: {str(self.lives)}\n"
                             f"Game time: {str(round(self.game_time))}")

        # для каждого астероида из N
        for i in range(asteroids_count):
            # берем номер астероида c номером i из списка
            asteroid = self.asteroids[i]
            # и его скорости
            vx = self.x_speeds[i]
            vy = self.y_speeds[i]

            # получаем текущие координаты астероида (левый верхний)
            x1, y1 = self.c.coords(asteroid)
            x2 = x1 + 20
            y2 = y1 + 20  # координаты правой нижней

            # если астероид на границе по x - развернуть скорость по x
            if x1 <= 5 or x2 >= 980:
                vx *= -1
            # аналогично по y
            if y1 <= 5 or y2 >= 580:
                vy *= -1

            # если астероид пересекается с вершинами игрока - уменьшить жизнь
            v1 = self.all_player_coords[:2]
            v2 = self.all_player_coords[2:4]
            v3 = self.all_player_coords[4:]
            if (x1 <= v1[0] <= x2 and y1 <= v1[1] <= y2) \
                    or (x1 <= v2[0] <= x2 and y1 <= v2[1] <= y2) \
                    or (x1 <= v3[0] <= x2 and y1 <= v3[1] <= y2):
                self.lives -= 1

            # если жизнь на нуле - закончить игру
            if self.lives == 0:
                self.state_label.set("Oops! You were killed!")
                self.c.delete(ALL)
                self.c.create_image(0, 0, image=self.game_over, anchor=NW)

            # сохраняем скорости обратно в список
            self.x_speeds[i] = vx
            self.y_speeds[i] = vy

            # передвигаем астероид
            self.c.move(asteroid, vx, vy)

        # повторяем через полсекунды
        self.c.after(50, self.move_asteroids)

    def create_player(self, player):
        shape = player.shape()  # координаты треугольника
        player_ship = self.c.create_polygon(shape, outline=player.outline, fill=player.fill)
        self.ship_ID.append(player_ship)
        self.player.append(player)
        self.c.pack()

    def update_player(self):
        new_player_coords = []  # список со СПИСКАМИ координат игрока
        for i in self.player:
            new_player_coords.append(i.shape())
            i.direction()

        i = 0
        while i < len(new_player_coords):
            self.c.coords(self.ship_ID[i], new_player_coords[i])
            i += 1
        self.all_player_coords = new_player_coords[-1]
        self.x_player = self.all_player_coords[0]
        self.y_player = self.all_player_coords[1]
        self.c.after(40, self.update_player)

    def create_fire(self, phi):
        x, y = self.x_player, self.y_player
        self.created_ball = self.c.create_image(x-10, y-10, image=self.bullet,  anchor=NW)  # создаем гор.шар
        self.fires_IDs\
            .append(self.created_ball)  # добавляю шар в список
        self.vx_fires.append(math.cos(math.radians(phi)) * 10)  # добавляю x для перемещения шара
        self.vy_fires.append(math.sin(math.radians(phi)) * 10)  # добавляю y для перемещения шара

    def move_fire(self):
        # каждый шар в списке, двигаю с собственным перемещением
        for i in range(len(self.fires_IDs)):
            x = self.vx_fires[i]
            y = self.vy_fires[i]
            self.c.move(
                self.fires_IDs[i],
                x, y)

        if len(self.fires_IDs) > 7:  # удаляю все горящие шары, если их вдруг стало больше 7
            for i in self.fires_IDs:
                self.c.delete(i)
            self.fires_IDs.clear()
            self.vy_fires.clear()
            self.vx_fires.clear()

        self.c.after(200, self.move_fire)
