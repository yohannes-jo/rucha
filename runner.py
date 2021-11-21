import pygame
from pygame.sprite import Sprite

class Runner(Sprite):

    def __init__(self, game):

        super().__init__()

        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings

        self.image = pygame.image.load('images/runner.bmp')
        self.rect = self.image.get_rect()

        # Set the avatar on the midleft part of the screen.
        self.rect.y, self.rect.x = 430, 10

        # Movement configuration flags
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
    
    def update(self):
        if self.moving_left and self.rect.left >= 0:
            self.rect.x -= self.settings.runner_speed
        elif self.moving_right and self.rect.right <= self.screen_rect.right:
            self.rect.x += self.settings.runner_speed
        
        if self.moving_up and self.rect.bottom >= 425:
            self.rect.y -= self.settings.runner_speed
        elif self.moving_down and self.rect.bottom <= self.screen_rect.bottom:
            self.rect.y += self.settings.runner_speed

    def draw(self):

        self.screen.blit(self.image, self.rect)

    def reset_runner(self):
        # Set the avatar on the midleft part of the screen.
        self.rect.y, self.rect.x = 430, 10
