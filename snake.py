# coding: utf8
from typing import List
from pygame.sprite import Sprite, Group
from pygame import Rect
from pygame.draw import rect, circle

import settings
from settings import DEFAULT_BLOCK_SIZE, STARTUP_X, STARTUP_Y


class GameObject:
    __slots__ = ['pos_x', 'pos_y', 'symbol']


class SnakeGroup(Group):
    pass


class SnakeBlock(Rect):
    group = SnakeGroup
    color = settings.WHITE

    def __init__(self, surface, size=DEFAULT_BLOCK_SIZE, position=(STARTUP_X, STARTUP_Y), *args, **kwargs):
        super().__init__(position, (size, size))
        self.surface = surface

    def set_position(self, pos_x, pos_y):
        self.centerx = pos_x
        self.centery = pos_y

    def draw(self):
        rect(self.surface, self.color, self)


class SnakeEye:
    color = None

    def __init__(self, head, color=settings.RED, state=1, side=None):
        self.head = head
        self.color = color
        self.state = state
        self.size = int(self.head.width / 6)
        self.side = side

    @property
    def is_left(self):
        if self.side == 'left':
            return True
        else:
            return False

    @property
    def is_right(self):
        if self.side == 'right':
            return True
        else:
            return False

    def close(self):
        self.state = 2

    def draw(self):
        head = self.head
        eye_position = None
        if head.direction == head.TO_LEFT:
            if self.is_left:
                eye_position = (int(head.centerx - head.width / 4), int(head.centery - head.height / 4))
            elif self.is_right:
                eye_position = (int(head.centerx - head.width / 4), int(head.centery + head.height / 4))

        elif head.direction == head.TO_RIGHT:
            if self.is_left:
                eye_position = (int(head.centerx + head.width / 4), int(head.centery - head.height / 4))
            elif self.is_right:
                eye_position = (int(head.centerx + head.width / 4), int(head.centery + head.height / 4))

        elif head.direction == head.TO_UP:
            if self.is_left:
                eye_position = (int(head.centerx - head.width / 4), int(head.centery - head.height / 4))
            elif self.is_right:
                eye_position = (int(head.centerx + head.width / 4), int(head.centery - head.height / 4))

        elif head.direction == head.TO_DOWN:
            if self.is_left:
                eye_position = (int(head.centerx - head.width / 4), int(head.centery + head.height / 4))
            elif self.is_right:
                eye_position = (int(head.centerx + head.width / 4), int(head.centery + head.height / 4))

        if self.state == 1:  # Open
            circle(self.head.surface, self.color, eye_position, self.size)
        elif self.state == 2: # Close
            circle(self.head.surface, self.color, eye_position, self.size, 1)

class SnakeHead(SnakeBlock):
    TO_LEFT = 1
    TO_RIGHT = 2
    TO_UP = 3
    TO_DOWN = 4
    direction = None
    eye_color = settings.RED

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.direction = self.TO_LEFT
        self.left_eye = SnakeEye(self, self.eye_color, 1, 'left')
        self.right_eye = SnakeEye(self, self.eye_color, 1, 'right')

    def draw(self):
        super().draw()
        self.left_eye.draw()
        self.right_eye.draw()

    def set_direction(self, direction):
        self.direction = direction


class Snake:
    speed = None
    TO_LEFT = 1
    TO_RIGHT = 2
    TO_UP = 3
    TO_DOWN = 4
    is_live = True

    def __init__(self, surface, start_position=(STARTUP_X, STARTUP_Y), blocks: List['SnakeBlock'] = None):
        self.surface = surface
        self.head = SnakeHead(self.surface)
        if blocks:
            self.body = blocks
        else:
            self.body = [self.head]

        self.speed_x = 0
        self.speed_y = 0

        self.birth()

    def __repr__(self):
        return self.body

    def __iter__(self):
        for block in self.body:
            yield block

    def get_blocks(self):
        return self.body

    def set_dir_to_left(self):
        if self.is_live:
            if self.direction != self.TO_RIGHT:
                self.direction = self.TO_LEFT

    def set_dir_to_right(self):
        if self.is_live:
            if self.direction != self.TO_LEFT:
                self.direction = self.TO_RIGHT

    def set_dir_to_up(self):
        if self.is_live:
            if self.direction != self.TO_DOWN:
                self.direction = self.TO_UP

    def set_dir_to_down(self):
        if self.is_live:
            if self.direction != self.TO_UP:
                self.direction = self.TO_DOWN

    def birth(self):
        self.speed = DEFAULT_BLOCK_SIZE / 10
        self.direction = self.TO_LEFT
        self.is_live = 1

    def dead(self):
        self.is_live = 0
        self.speed = 0
        self.head.left_eye.close()
        self.head.right_eye.close()
    def move(self):
        if self.head.top % settings.DEFAULT_CELL_SIZE == 0:
            if self.direction == self.TO_LEFT:
                self.speed_x = -self.speed
                self.speed_y = 0
                self.head.direction = self.direction
            elif self.direction == self.TO_RIGHT:
                self.speed_x = self.speed
                self.speed_y = 0
                self.head.direction = self.direction
        if self.head.left % settings.DEFAULT_CELL_SIZE == 0:
            if self.direction == self.TO_UP:
                self.speed_y = -self.speed
                self.speed_x = 0
                self.head.direction = self.direction
            elif self.direction == self.TO_DOWN:
                self.speed_y = self.speed
                self.speed_x = 0
                self.head.direction = self.direction
        self.head.centerx += self.speed_x
        self.head.centery += self.speed_y

    def add_block(self, block):
        if isinstance(block, SnakeBlock):
            self.body.append(block)

    def draw(self):
        for block in self.body:
            block.draw()
