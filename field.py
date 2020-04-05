# coding: utf-8
import os
import sys
from time import sleep
from typing import Tuple, List

from pygame.rect import Rect
from pygame.draw import line, rect

import settings
from snake import GameObject, SnakeBlock, Snake


class Field(Rect):

    def __init__(self,
                 surface,
                 position=(0, 0),
                 dimensions=settings.DEFAULT_FIELD_DIMENSIONS,
                 grid_size=settings.DEFAULT_SIZE,
                 *args, **kwargs):
        self.position = position
        self.dimensions = dimensions
        super().__init__(self.position, self.dimensions, *args, **kwargs)
        self.grid_size = grid_size
        self.surface = surface

    def set_center(self, window):
        if isinstance(window, Rect):
            self.left = window.centerx - self.width / 2
            self.top = window.centery - self.height / 2

    def draw(self):
        rect(self.surface, settings.WHITE, self, 2)
        for x in range(self.left, self.right, self.grid_size):
            line(self.surface, settings.WHITE, (x, self.top), (x, self.bottom))
        for y in range(self.top, self.bottom, self.grid_size):
            line(self.surface, settings.WHITE, (self.left, y), (self.right, y))

