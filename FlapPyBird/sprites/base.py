import pygame

from FlappyBird_NeuroEvolution.FlapPyBird.resources.config import *


class Base(pygame.sprite.Sprite):
    # Layer for LayeredUpdates()
    _layer = 2

    def __init__(self, initial_info, game_display=pygame.Surface):
        pygame.sprite.Sprite.__init__(self, self.groups)
        # Game area
        self.area = game_display.get_rect()
        # Position
        self.x_pos = initial_info['base_x']
        self.y_pos = initial_info['base_y']
        self._layer = Base._layer
        # Updating tools
        self.loop_iter = 0  # initial_info['loop_iter']
        self.base_shift = initial_info['base_shift']
        # Image and hitbox
        self.image = IMAGES['base']
        self.mask = HITMASKS['base']
        self.rect = self.image.get_rect(topleft=(self.x_pos, self.y_pos))

    def update(self, *args):
        # Update x position
        self.x_pos = -((-self.x_pos + 100) % self.base_shift)
        # Update image and hitbox
        self.rect.topleft = (self.x_pos, self.y_pos)
