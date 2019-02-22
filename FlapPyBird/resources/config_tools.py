from resources.config import *
from itertools import cycle
import random
import pygame
import sys


def load_images():
    # numbers sprites for score display
    IMAGES['numbers'] = (
        pygame.image.load('assets/sprites/0.png').convert_alpha(),
        pygame.image.load('assets/sprites/1.png').convert_alpha(),
        pygame.image.load('assets/sprites/2.png').convert_alpha(),
        pygame.image.load('assets/sprites/3.png').convert_alpha(),
        pygame.image.load('assets/sprites/4.png').convert_alpha(),
        pygame.image.load('assets/sprites/5.png').convert_alpha(),
        pygame.image.load('assets/sprites/6.png').convert_alpha(),
        pygame.image.load('assets/sprites/7.png').convert_alpha(),
        pygame.image.load('assets/sprites/8.png').convert_alpha(),
        pygame.image.load('assets/sprites/9.png').convert_alpha()
    )

    # game over sprite
    IMAGES['gameover'] = pygame.image.load('assets/sprites/gameover.png').convert_alpha()
    # message sprite for welcome screen
    IMAGES['message'] = pygame.image.load('assets/sprites/message.png').convert_alpha()
    # base (ground) sprite
    IMAGES['base'] = pygame.image.load('assets/sprites/base.png').convert_alpha()


def load_sounds():
    """Load sound"""
    if 'win' in sys.platform:
        soundExt = '.wav'
    else:
        soundExt = '.ogg'

    SOUNDS['die'] = pygame.mixer.Sound('assets/audio/die' + soundExt)
    SOUNDS['hit'] = pygame.mixer.Sound('assets/audio/hit' + soundExt)
    SOUNDS['point'] = pygame.mixer.Sound('assets/audio/point' + soundExt)
    SOUNDS['swoosh'] = pygame.mixer.Sound('assets/audio/swoosh' + soundExt)
    SOUNDS['wing'] = pygame.mixer.Sound('assets/audio/wing' + soundExt)


def initialize_random_sprites():
    """Initialize random background, player and pipe images"""
    # select random background sprites
    random_background_image = random.randint(0, len(BACKGROUNDS_LIST) - 1)
    IMAGES['background'] = pygame.image.load(BACKGROUNDS_LIST[random_background_image]).convert()

    # select random player sprites
    random_player_image = random.randint(0, len(PLAYERS_LIST) - 1)
    IMAGES['player'] = (
        pygame.image.load(PLAYERS_LIST[random_player_image][0]).convert_alpha(),
        pygame.image.load(PLAYERS_LIST[random_player_image][1]).convert_alpha(),
        pygame.image.load(PLAYERS_LIST[random_player_image][2]).convert_alpha(),
    )

    # select random pipe sprites
    pipeindex = random.randint(0, len(PIPES_LIST) - 1)
    IMAGES['pipe'] = (pygame.transform.rotate(pygame.image.load(PIPES_LIST[pipeindex]).convert_alpha(), 180),
                      pygame.image.load(PIPES_LIST[pipeindex]).convert_alpha(),)


def initialize_movement_info():
    """Shows welcome screen animation of flappy bird"""

    # index of player to blit on screen
    player_index = 0
    player_index_generator = cycle([0, 1, 2, 1])  # Infinite iterable
    # iterator used to change playerIndex after every 5th iteration
    loop_iter = 0

    player_pos_x = int(SCREENWIDTH * 0.2)
    player_pos_y = int((SCREENHEIGHT - IMAGES['player'][0].get_height()) / 2)

    message_pos_x = int((SCREENWIDTH - IMAGES['message'].get_width()) / 2)
    message_pos_y = int(SCREENHEIGHT * 0.12)

    base_x = 0
    base_y = SCREENHEIGHT * 0.79
    # amount by which base can maximum shift to left
    base_shift = IMAGES['base'].get_width() - IMAGES['background'].get_width()

    # player oscillate for up-down motion on welcome screen
    player_oscillate = {'val': 0, 'dir': 1}

    return {'player_index': player_index,
            'player_index_generator': player_index_generator,
            'loop_iter': loop_iter,
            'player_pos_x': player_pos_x,
            'player_pos_y': player_pos_y + player_oscillate['val'],
            'message_pos_x': message_pos_x,
            'message_pos_y': message_pos_y,
            'base_x': base_x,
            'base_y': base_y,
            'base_shift': base_shift,
            'player_oscillate': player_oscillate}


def initialize_hitmask():
    """
    Useful for fast pixel perfect collision detection.
    A mask uses 1 bit per-pixel to store which parts collide.
    """
    # hismask for pipes
    HITMASKS['pipe'] = (
        getHitmask(IMAGES['pipe'][0]),
        getHitmask(IMAGES['pipe'][1]),
    )

    # hitmask for player
    HITMASKS['player'] = (
        getHitmask(IMAGES['player'][0]),
        getHitmask(IMAGES['player'][1]),
        getHitmask(IMAGES['player'][2]),
    )

    HITMASKS['base'] = (
        getHitmask(IMAGES['base'])
    )


def getHitmask(image):
    """returns a hitmask using an image's alpha."""
    #mask = []
    #for x in range(image.get_width()):
    #    mask.append([])
    #    for y in range(image.get_height()):
    #        mask[x].append(bool(image.get_at((x, y))[3]))
    mask = pygame.mask.from_surface(image)
    return mask


def load_and_initialize():
    """Load necessary images/sounds/hitboxes"""
    load_images()
    load_sounds()
    initialize_random_sprites()
    initialize_hitmask()

    return initialize_movement_info()
