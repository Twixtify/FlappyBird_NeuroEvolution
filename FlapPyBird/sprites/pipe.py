import pygame

from FlappyBird_NeuroEvolution.FlapPyBird.resources.config import *


class Pipe(pygame.sprite.Sprite):
    # Variable for loading player picture. Require module that import player.py to initialize this variable
    image = []
    # Dictionary
    pipes = {}
    # tag
    total_number = 0
    # Layer for LayeredUpdates()
    _layer = 1

    def __init__(self, initial_info, game_display=pygame.Surface):
        # Add pipe to group
        pygame.sprite.Sprite.__init__(self, self.groups)
        # Rect object of game display
        self.area = game_display.get_rect()
        # Return (x,y) position of an upper and lower pipe
        self.movement_speed = -4
        # Position and index
        self.x_pos = initial_info['x']
        self.y_pos = initial_info['y']
        self.index = initial_info['index']  # Either 0 (upper pipe) or 1 (lower pipe)
        self._layer = Pipe._layer
        # Image and mask
        self.image = IMAGES['pipe'][self.index]
        self.mask = HITMASKS['pipe'][self.index]
        # Rect object
        self.rect = self.image.get_rect(topleft=(round(self.x_pos), round(self.y_pos)))
        # ---- Flag for Game Over
        self.remove = False
        # ---- Update static variables -----
        self.number = Pipe.total_number
        Pipe.total_number += 1
        Pipe.pipes[self.number] = self

    def kill(self):
        # Remove player from dictionary
        Pipe.pipes[self.number] = None  # kill Player in sprite dictionary
        # Reduce total number of players by 1
        Pipe.total_number -= 1
        # Call super method to remove player
        pygame.sprite.Sprite.kill(self)

    def move(self):
        self.x_pos += self.movement_speed
        self.rect.topleft = (round(self.x_pos), round(self.y_pos))

    def update(self, *args):
        # Flag pipe to be removed if it's outside of the screen
        if self.x_pos < -IMAGES['pipe'][self.index].get_width():
            self.remove = True
        # Remove pipe
        if self.remove:
            self.kill()
        # Move pipe
        self.move()
