import pygame
from hurdle import Hurdle

class ScoreBoard:
    def __init__(self, game):

        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings

        # Current score, High score, Number of Hearts left
        self.score = 0
        self.high_score = 0

        self.hearts_left = game.settings.heart_limit

        self.font = pygame.font.SysFont(None, 48)
        self.text_color = (0, 0, 0)


        self.prep_score()
        self.prep_highscore()
        self.prep_hearts()
    
    def prep_score(self):
        """Turn the score into a rendered image."""
        rounded_score = round(self.score, -1)
        score_str = '{:,}'.format(rounded_score)

        self.score_image = self.font.render(score_str, True,
            self.text_color, self.settings.bg_color)
        
        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
    
    def prep_highscore(self):
        """Turn the highscore into a rendered image."""
        rounded_score = round(self.high_score, -1)
        score_str = '{:,}'.format(rounded_score)

        self.high_score_image = self.font.render(score_str, True,
            self.text_color, self.settings.bg_color)
        
        # Display the score at the top right of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.midtop = self.screen_rect.midtop
        self.high_score_rect.top = 20
    
    def prep_hearts(self):
        self.hurdles = pygame.sprite.Group()
        for hurdle in range(self.hearts_left):
            new_hurdle = Hurdle(self.game)
            new_hurdle_width = new_hurdle.rect.width
            new_hurdle.rect.left = 10 + hurdle * (new_hurdle_width // 2)
            new_hurdle.rect.top = 10
            self.hurdles.add(new_hurdle)

    def show_score(self):
        """Draw score to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.hurdles.draw(self.screen)