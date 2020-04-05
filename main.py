import os

import pygame, sys
from pygame.draw import rect
from pygame.locals import *
from pygame import time

from field import Field
from snake import SnakeBlock, Snake

import settings


class Game:
    field = None

    def __init__(self, name=settings.GAME_NAME, resolution=settings.DEFAULT_RESOLUTION, window_mode=False):
        os.environ['SDL_VIDEO_CENTERED'] = "1"
        pygame.init()
        self.display_surface = pygame.display.set_mode(resolution)
        pygame.display.set_caption(name)
        self.window = Rect((0, 0), resolution)
        self.field = Field(self.display_surface)
        self.field.set_center(self.window)

    def loop(self):
        snake = Snake(self.display_surface)

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        snake.set_dir_to_up()
                    if event.key == K_DOWN:
                        snake.set_dir_to_down()
                    if event.key == K_LEFT:
                        snake.set_dir_to_left()
                    if event.key == K_RIGHT:
                        snake.set_dir_to_right()
            if snake.head.left < self.field.left:
                snake.head.left = self.field.left
                snake.dead()
            elif snake.head.top < self.field.top:
                snake.head.top = self.field.top
                snake.dead()
            elif snake.head.right > self.field.right:
                snake.head.right = self.field.right
                snake.dead()
            elif snake.head.bottom > self.field.bottom:
                snake.head.bottom = self.field.bottom
                snake.dead()
            snake.move()
            objects = [snake]
            self.draw(objects)

    def draw(self, objects=None):
        rect(self.display_surface, settings.BLACK, self.window)
        self.field.draw()
        for game_object in objects:
            game_object.draw()
        pygame.display.update()
        time.wait(int(1 / 60 * 1000))


if __name__ == '__main__':
    game = Game()
    game.loop()
