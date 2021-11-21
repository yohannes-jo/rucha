import sys
from random import randint
import time

import pygame

from background import Background
from hurdle import Hurdle
from runner import Runner
from scoreboard import ScoreBoard
from settings import Settings

class Rucha:

    def __init__(self):

        pygame.init()
        self.settings = Settings()

        pygame.display.set_caption('Ayzosh Gelete!')
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        self.screen_rect = self.screen.get_rect()
        self.bg_color = self.settings.bg_color

        self.runner = Runner(self)
        self.scoreboard = ScoreBoard(self)
        self.backgrounds = pygame.sprite.Group()
        self.hurdles = pygame.sprite.Group()


        # Add a single background sprite as initializer
        self.backgrounds.add(Background(self, 0))

        # Background music and sound effects.
        self.ag = pygame.mixer.Sound('sounds/ayzosh_gelete.mp3')
        self.bgm = pygame.mixer.Sound('sounds/background_1.mp3')

        # Create a variable to store a highscore
        try:
            with open('stats/highscore.txt', 'r') as highscore:
                try:
                    self.scoreboard.high_score = int(highscore.read())
                    self.scoreboard.prep_highscore()
                except ValueError:
                    print('hello')
                    pass
        except FileNotFoundError:
                pass

    def run(self):

        # Start background music.
        self.bgm.play()

        while True:
            self._check_events()
            self._update_entities()
            self._update_score()
            self._update_screen()
    
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.bgm.stop()
                # Record current high score
                with open('stats/highscore.txt', 'w') as hs:
                    hs.write(str(self.scoreboard.high_score))
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
    
    def _check_keydown_events(self, event):
        if event.key == pygame.K_a:
            self.runner.moving_left = True
        elif event.key == pygame.K_d:
            self.runner.moving_right = True
        elif event.key == pygame.K_w:
            self.runner.moving_up = True
        elif event.key == pygame.K_s:
            self.runner.moving_down = True

    def _check_keyup_events(self, event):
        if event.key == pygame.K_a:
            self.runner.moving_left = False
        elif event.key == pygame.K_d:
            self.runner.moving_right = False
        elif event.key == pygame.K_w:
            self.runner.moving_up = False
        elif event.key == pygame.K_s:
            self.runner.moving_down = False
    
    def _check_hurdle_collisions(self):
        collided_hurdles = pygame.sprite.spritecollide(self.runner, self.hurdles, True)

        # Deduct a heart if the runner has collided with a hurdle
        if collided_hurdles:
            rand_scream = randint(1, 3)
            self.sc = pygame.mixer.Sound(f'sounds/scream_{rand_scream}.mp3')
            self.sc.play()
            
            self.scoreboard.hearts_left -= 1
            self.scoreboard.prep_hearts()

            if self.scoreboard.hearts_left == 0:
                self.game_over()

    def _update_entities(self):
        """Update entity information for the next screen update."""
        self.runner.update()
        self._update_background()
        self._update_hurdles()

    def _update_background(self):
        """Update background position(s) and add/remove as needed."""
        # Add a new background or remove one when the current sprite starts disappearing.
        for background in self.backgrounds.sprites():
            if background.rect.left <= self.screen_rect.left and len(self.backgrounds) <= 2:
                self.backgrounds.add(Background(self))
                break

            if background.rect.right <= self.screen_rect.left:
                self.backgrounds.remove(background)
        
        self.backgrounds.update()
    
    def _update_hurdles(self):
        """Update hurdles' positions and add/remove as needed."""
        self._check_hurdle_collisions()

        # Remove a hurdle when it leaves the screen
        for hurdle in self.hurdles.sprites():
            if hurdle.rect.right <= self.screen_rect.left:
                self.hurdles.remove(hurdle)
        
        # Add a hurdle if there are less than 2 at any given moment.
        if len(self.hurdles) < 2:
            # Give it one of three random positions
            y = randint(0, 2) * 90 + 415

            hurdle = Hurdle(self, self.screen_rect.right, y)
            self.hurdles.add(hurdle)
        
        self.hurdles.update()
    
    def _update_score(self):
        self.scoreboard.score += 1
        self.scoreboard.prep_score()

        # Change the highscore when necessary
        if self.scoreboard.score > self.scoreboard.high_score:
            self.scoreboard.high_score = self.scoreboard.score
            self.scoreboard.prep_highscore()

    def _update_screen(self):
        """Render the current frame based on updated information."""
        self.screen.fill(self.bg_color)
        self.backgrounds.draw(self.screen)
        self.hurdles.draw(self.screen)
        self.runner.draw()

        # Draw the score information.
        self.scoreboard.show_score()
        
        pygame.display.flip()

    def game_over(self):
        """Configuration of what happens when the game is over."""
        # Record current high score
        with open('stats/highscore.txt', 'w') as hs:
            hs.write(str(self.scoreboard.high_score))

        self.bgm.stop()
        self.ag.play()
        self.bgm.play()

        time.sleep(0.5)

        # Reset physical counters
        self.scoreboard.score = 0
        self.scoreboard.hearts_left = self.settings.heart_limit
        
        # Reset the GUI counters
        self.scoreboard.prep_hearts()
        self.scoreboard.prep_score()

        # Reset the runner's position
        self.runner.reset_runner()
        
if __name__ == '__main__':
    game = Rucha()
    game.run()