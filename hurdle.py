import pygame
from pygame.sprite import Sprite


class Hurdle(Sprite):

    def __init__(self, game, x=0, y=0):

        super().__init__()

        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings

        self.image = pygame.image.load('images/hurdle.bmp')
        im_width, im_height = self.image.get_size()

        self.rect = pygame.Rect(x, y, im_width, im_height)
        self.x = float(self.rect.x)
    
    def update(self):
        self.x -= self.settings.background_speed
        self.rect.x = self.x