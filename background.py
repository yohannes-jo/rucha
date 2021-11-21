import pygame

from pygame.sprite import Sprite

class Background(Sprite):
    
    def __init__(self, game, x=640, y=0):

        super().__init__()
        
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings

        self.image = pygame.image.load('images/background.bmp')
        self.rect = pygame.Rect(x, y, game.settings.screen_width,
                game.settings.screen_height)
        
        self.x = float(self.rect.x)
    
    def update(self):
        """Update background position."""
        self.x -= self.settings.background_speed
        self.rect.x = self.x
