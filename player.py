import math

import settings


class Ship:

    def __init__(self, root):

        self.position_x = settings.pos_x
        self.position_y = settings.pos_y
        self.phi = 270             # угол в градусах для поворота корабля
        self.DELTA_PHI = 5
        self.SIZE_CONST = 20         # размер корабля
        self.alpha = 270             # угол для расчета вектора скорости
        self.DELTA_ALPHA = 5
        self.movement_speed = 0      # текущее значение скорости
        self.DELTA_MOVEMENT_SPEED = 1
        self.MOVEMENT_SPEED_MAX = 5  # максимальное значение скорости
        self.MOVEMENT_SPEED_MIN = -3  # минимальное значение скорости

        self.outline = '#201571'
        self.fill = '#5610ff'

        root.bind('<Up>', self.move_forward)
        root.bind('<Down>', self.move_backward)
        root.bind('<Left>', self.rotate_left)
        root.bind('<Right>', self.rotate_right)

    def shape(self):
        shape = [
            self.position_x + self.SIZE_CONST * math.cos(math.radians(self.phi)),
            self.position_y + self.SIZE_CONST * math.sin(math.radians(self.phi)),
            self.position_x + self.SIZE_CONST * math.cos(math.radians(self.phi)-40),
            self.position_y + self.SIZE_CONST * math.sin(math.radians(self.phi)-40),
            self.position_x + self.SIZE_CONST * math.cos(math.radians(self.phi)+40),
            self.position_y + self.SIZE_CONST * math.sin(math.radians(self.phi)+40),
                ]
        return shape

    def move_forward(self, event):
        if self.movement_speed < self.MOVEMENT_SPEED_MAX:
            self.movement_speed += self.DELTA_MOVEMENT_SPEED

    def move_backward(self, event):
        if self.movement_speed > self.MOVEMENT_SPEED_MIN:
            self.movement_speed -= self.DELTA_MOVEMENT_SPEED

    def rotate_left(self, event):
        if self.movement_speed >= 0:
            self.phi -= self.DELTA_PHI
        else:
            self.phi += self.DELTA_PHI
        if self.phi < 0:
            self.phi = 360
        if self.phi > 360:
            self.phi = 0

    def rotate_right(self, event):
        if self.movement_speed >= 0:
            self.phi += self.DELTA_PHI
        else:
            self.phi -= self.DELTA_PHI
        if self.phi > 360:
            self.phi = 0
        if self.phi < 0:
            self.phi = 360

    def borders(self):
        if self.position_x >= settings.width:
            self.position_x = 0
        elif self.position_x <= 0:
            self.position_x = settings.width
        if self.position_y >= settings.height:
            self.position_y = 0
        elif self.position_y <= 0:
            self.position_y = settings.height

    def direction(self):
        if math.fabs(self.phi - self.alpha) < 180:
            if self.phi > self.alpha:
                self.alpha += self.DELTA_ALPHA
            elif self.phi < self.alpha:
                self.alpha -= self.DELTA_ALPHA
            else:
                pass
        elif math.fabs(self.phi - self.alpha) > 180:
            if (360 - self.phi) < self.phi:
                if self.alpha >= 0:
                    self.alpha -= self.DELTA_ALPHA
                else:
                    self.alpha = 360
            else:
                if self.alpha <= 360:
                    self.alpha += self.DELTA_ALPHA
                else:
                    self.alpha = 0
        elif ((math.fabs(self.phi - self.alpha) == 0)
              or (math.fabs(self.phi - self.alpha) == 360)):
            pass

        self.position_x = self.movement_speed * math.cos(math.radians(self.alpha)) + self.position_x
        self.position_y = self.movement_speed * math.sin(math.radians(self.alpha)) + self.position_y
        self.borders()
