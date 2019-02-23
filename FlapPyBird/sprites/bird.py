import pygame
import numpy as np

from FlappyBird_NeuroEvolution.FlapPyBird.resources.config import *


class Bird(pygame.sprite.Sprite):
    # Variable for loading player picture. Require module that import player.py to initialize this variable
    image = []
    # Dictionary
    birds = {}
    # tag
    total_number = 0
    # Layer for LayeredUpdates()
    _layer = 3

    def __init__(self, initial_info, game_display=pygame.Surface):
        pygame.sprite.Sprite.__init__(self, self.groups)
        # Save game display as a rectangular area object
        self.area = game_display.get_rect()  # where the sprite is allowed to move
        # Score variable for each player
        self.score = 0
        # ---- Create variables for keeping track of sprite position ----
        self.x_pos = initial_info['player_pos_x']
        self.y_pos = initial_info['player_pos_y']
        self.index = initial_info['player_index']
        self.index_generator = initial_info['player_index_generator']
        self.loop_iter = 0
        self._layer = Bird._layer

        # ----------------- Player parameters -------------------
        # player velocity, max velocity, downward acceleration, acceleration on flap
        self.y_vel = 0  # player's velocity along Y
        self.max_y_vel = 10  # max vel along Y, max descend speed
        self.gravity = 1  # players downward acceleration
        self.rotate = 45  # player's rotation
        self.rotate_speed = 3  # angular speed
        self.rotate_threshold = 20  # rotation threshold
        self.flap_acc = -9
        self.flapped = False  # True when player flaps
        # -------------------------------------------------------

        # Load normal image
        self.image = IMAGES['player'][self.index]  # Bird image
        self.mask = HITMASKS['player'][self.index]  # Birds hitbox
        # ---- Create hitbox the size of the player image at it's starting location
        self.rect = self.image.get_rect(topleft=(round(self.x_pos), round(self.y_pos)))
        # ---- Flag for Game Over
        self.remove = False
        # ---- Update static variables -----
        self.number = Bird.total_number
        Bird.total_number += 1
        Bird.birds[self.number] = self

    def next_index(self):
        self.index = next(self.index_generator)

    def kill(self):
        # Remove player from dictionary
        Bird.birds[self.number] = None  # kill Player in sprite dictionary
        # Reduce total number of players by 1
        Bird.total_number -= 1
        # Call super method to remove player
        pygame.sprite.Sprite.kill(self)

    def connect_ai(self, ai_mind):
        """
        Create a reference to a neural network object
        :param ai_mind: Neural network object
        :return: None
        """
        # Feed forward neural network
        self.ai_mind = ai_mind
        self.ai_input_size = ai_mind.input_layer.shape[1]

    def ai_decision(self, inputs):
        """
        Make a prediction for the next action to take
        :param inputs: Numpy array
        :return: Output of neural network
        """
        return self.ai_mind.get_predict(input_sample=inputs, classify=False)

    def move(self, base, pipes):
        """
        Collection of sprite movements:
        AI flap decision
        Gravity
        Angular rotation
        Rotation due to flapping
        Image rotation
        Bird position update
        Hitbox positional update
        :param base: Sprite for base (or ground) object
        :param pipes: Dictionary of sprites
        :return: None
        """
        """AI decision to move"""
        ai_decision = self.ai_decision(self.get_ai_input(pipes))
        # If 1 output node
        if ai_decision.size == 1:
            if ai_decision[0] >= 0.5:
                self.y_vel = self.flap_acc  # move down
                self.flapped = True
        # If 2 output nodes
        else:
            if ai_decision[0][0] > ai_decision[0][1]:
                self.y_vel = self.flap_acc  # move down
                self.flapped = True

        # Gravity accelerate downward if bird does not flap
        if self.y_vel < self.max_y_vel and not self.flapped:
            self.y_vel += self.gravity

        # Angular speed downward due to gravity
        if self.rotate > -90:  # Maximum downward rotation
            self.rotate -= self.rotate_speed

        # Flag when bird flaps
        if self.flapped:
            self.flapped = False
            # more rotation to cover the threshold (calculated in visible rotation)
            self.rotate = 45

        # Player rotation has a threshold
        visible_rotation = self.rotate_threshold
        if self.rotate <= self.rotate_threshold:
            visible_rotation = self.rotate
        self.image = pygame.transform.rotate(IMAGES['player'][self.index], visible_rotation)  # Rotate player image

        # Update position
        self.y_pos += min([self.y_vel, (base.y_pos + 1) - (self.y_pos + self.rect.height)])

        # ---- Updated position for bird hitbox
        self.rect.topleft = (round(self.x_pos), round(self.y_pos))

    def get_ai_input(self, pipes):
        """
        Get the distance to the closest pipe edge
        :param pipes: Dictionary of pipe sprites
        :return: Numpy array of floats
        """
        closest_pipe = pipes.get_sprite(0)
        closest_distance = np.infty
        for i, pipe in enumerate(pipes):
            d = (pipe.x_pos + pipe.rect.width) - self.x_pos
            if 0 < d < closest_distance:
                closest_pipe = pipes.get_sprite(i)
                closest_distance = d

        ai_input = np.ones(self.ai_input_size)
        index = iter(range(len(ai_input)))  # Iterator of the list [0, 1, 2, ... , len(ai_input) - 1]
        # Height to ground
        ai_input[next(index)] = (self.y_pos + self.rect.height / 2) / self.area.height
        # Pipe x position
        ai_input[next(index)] = (closest_pipe.x_pos + closest_pipe.rect.width) / self.area.width
        # Distance to lower pipe height
        ai_input[next(index)] = closest_pipe.y_pos / self.area.height
        # Distance to upper pipe height
        ai_input[next(index)] = (closest_pipe.y_pos - PIPEGAPSIZE) / self.area.height
        # ------------------------------------------------

        ai_input.shape = (1, -1)
        return ai_input

    def out_of_bound(self, dangerous):
        """
        Out of bound condition
        :param dangerous: Boolean
        :return: None
        """
        if dangerous:
            if not self.area.contains(self.rect):
                if self.y_pos < self.area.top:
                    self.remove = True
        else:
            if not self.area.contains(self.rect):
                if self.y_pos < self.area.top:
                    self.y_pos = self.area.top

    def update(self, base, pipes, *args):
        """
        All pygame.sprite.Sprite objects in a group receive the arguments of the update function.
        :param base: Ground object
        :param pipes: Tuple of object and integer (ai_input, ai_input_size)
        :param args: If arguments are added to other sprite groups
        :return: None
        """
        # -- Check if Game Over --
        if self.remove:
            self.kill()  # Game over
        self.loop_iter = (self.loop_iter + 1) % FPS  # Return 1, 2, ..., FPS - 1
        # Update index, bird image and hitbox
        if (self.loop_iter + 1) % 3 == 0:
            self.next_index()
            self.image = IMAGES['player'][self.index]
            self.mask = HITMASKS['player'][self.index]
        # -- Move player --
        self.move(base, pipes)
        # Edge cases
        self.out_of_bound(dangerous=True)
        # -- Update score (i.e time alive) --
        self.score += 1
