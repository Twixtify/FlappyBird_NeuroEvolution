import sys

import pygame
from pygame.locals import *

# Game configurations
from FlappyBird_NeuroEvolution.FlapPyBird.resources.config import *
from FlappyBird_NeuroEvolution.FlapPyBird.resources import config_tools as tools
# Sprites
from FlappyBird_NeuroEvolution.FlapPyBird.sprites.bird import Bird
from FlappyBird_NeuroEvolution.FlapPyBird.sprites.base import Base
from FlappyBird_NeuroEvolution.FlapPyBird.sprites.pipe import Pipe
# Neuroevolution methods
from FlappyBird_NeuroEvolution.neuralnetwork.ai_population import AIPopulation
from FlappyBird_NeuroEvolution.GeneticAlgorithm.tools.evolve import *


class FlappyBirds:
    # Center window on screen
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    # Initialize pygame
    pygame.init()
    # Set caption on game display
    pygame.display.set_caption('Flappy Bird')

    def __init__(self):
        self.clock = pygame.time.Clock()
        # Game display size
        size = self.W_WIDTH, self.W_HEIGHT = (SCREENWIDTH, SCREENHEIGHT)
        # Screen object
        self.screen = pygame.display.set_mode(size)  # Create window which graphics are rendered on
        # Load images + sounds and create hitmask on player and pipe images
        self.initial_info = tools.load_and_initialize()

        # --------- Initialize AIs ----------
        # Initialize AI options
        self.ai_population = AIPopulation(INPUT_SHAPE, NEURONS_LAYER, ACTIVATIONS)
        # Create population of Neural Networks
        self.ai_population.init_pop(POPULATION)
        # -----------------------------------

        # ---- Welcome animation ----
        self.show_welcome_animation()
        # Evolution
        self.start_evolution()

    def start_evolution(self):
        fitness = np.zeros(POPULATION)
        generation = 0
        self.best_bird = []
        while True:
            # Start a game
            score, best_bird, best_score = self.start_game()

            # Save the best bird if it has beaten the previous best birds
            if generation == 0:
                self.best_bird.append((best_score, best_bird))
            elif max(self.best_bird, key=lambda t: t[0])[0] < best_score:
                self.best_bird.append((best_score, best_bird))

            # Save fitness values and normalize them
            total_score = 0
            for i, val in score:
                total_score += val
                fitness[i] = val

            # -- Get current individuals --
            individuals = [self.ai_population.get_ind(i, use_bias=True) for i in range(POPULATION)]
            # -- Evolve through genetic algorithm --
            # new_individuals = evolve_best(individuals, fitness, n_parents=10)
            # new_individuals = evolve_roulette(individuals, fitness, tournaments=10)
            # new_individuals = evolve_tournament(individuals, fitness, tournaments=10, tour_size=6)
            new_individuals = evolve_sus(individuals, fitness, 20)
            # -- Update AI population
            self.ai_population.set_pop(new_individuals)

            # Print stuff for generation
            print("Generation %i Mean fitness %s" % (generation, np.mean(fitness)))
            generation += 1

    def init_sprites(self):
        # Initialize sprite groups
        self.make_sprite_groups()
        # Load background
        self.load_background()
        # Base
        self.base = Base(self.initial_info, self.screen)
        # Pipe
        self.new_pipe()
        # Bird
        self.birds = [Bird(self.initial_info, self.screen) for _ in range(POPULATION)]
        [bird.connect_ai(self.ai_population.get_ai(i)) for i, bird in enumerate(self.birds)]

    def start_game(self):
        self.init_sprites()
        self.pipes_cleared = 0
        cycles = 2
        score = []
        while True:
            # ----------- Perform game logic for #cycles -----------
            for _ in range(cycles):
                self.new_pipe()
                # Handle events
                self.event_handle()
                # Check for game over
                gameover_dict = pygame.sprite.groupcollide(self.bird_group, self.gameover_group, False, False,
                                                           pygame.sprite.collide_mask)
                # Remove birds that have crashed
                for bird in gameover_dict:
                    bird.remove = True
                    score.append((bird.number, bird.score))
                # Update sprites
                self.all_sprites_group.update(self.base, self.pipes_group)

            # ----------- Draw sprites -----------
            # Clear sprites
            self.all_sprites_group.clear(self.screen, self.background)
            # Redraw sprites
            self.all_sprites_group.draw(self.screen)
            # Display score
            self.show_score()
            # Update screen
            pygame.display.update()
            # Captions
            pygame.display.set_caption("Birds: %i" % (len(self.bird_group)))
            self.clock.tick(FPS)
            if not self.bird_group:
                self.clear_sprites()  # Delete sprites
                tmp_best = max(score, default=(0, 1), key=lambda t: t[1])  # Default used if all birds
                # decide to die at the same time
                print("Maximum score (Bird ID, Score): ", tmp_best)
                best_bird = list(self.ai_population.get_ind(tmp_best[0], use_bias=True))
                bird_score = tmp_best[1]
                break

        return score, best_bird, bird_score

    def show_score(self):
        """displays score in center of screen"""
        for bird in self.bird_group:
            pipe = self.pipes_group.get_sprite(0)
            if pipe.x_pos < bird.x_pos < pipe.x_pos + FPS / 2:
                self.pipes_cleared += 1
                break
        score_digits = [int(x) for x in list(str(self.pipes_cleared))]
        total_width = 0  # total width of all numbers to be printed

        for digit in score_digits:
            total_width += IMAGES['numbers'][digit].get_width()

        x_offset = (self.W_WIDTH - total_width) / 2

        for digit in score_digits:
            self.screen.blit(IMAGES['numbers'][digit], (x_offset, self.W_HEIGHT * 0.1))
            x_offset += IMAGES['numbers'][digit].get_width()

    def clear_sprites(self):
        # Clear all sprites
        for sprite in self.all_sprites_group:
            sprite.remove = True
        self.all_sprites_group.update()

    def load_background(self):
        self.background = IMAGES['background']
        self.screen.blit(self.background, (0, 0))

    def get_random_pipe_pair(self):
        """returns a randomly generated pipe"""
        "Note that the pipes spawn 10 pixels off screen and the y gap is random"
        # y of gap between upper and lower pipe
        gap_y = random.randrange(0, int(self.initial_info['base_y'] * 0.6 - PIPEGAPSIZE))
        gap_y += int(self.initial_info['base_y'] * 0.2)
        pipe_height = IMAGES['pipe'][0].get_height()
        pipe_x = self.W_WIDTH + 10

        return [
            {'x': pipe_x, 'y': gap_y + PIPEGAPSIZE, 'index': 1},  # lower pipe
            {'x': pipe_x, 'y': gap_y - pipe_height, 'index': 0},  # upper pipe
        ]

    def get_pipe_pair(self):
        # Create upper and lower pipe
        lower_pipe, upper_pipe = self.get_random_pipe_pair()  # Pipe initial (x,y) position
        Pipe(lower_pipe, self.screen)  # Lower pipe
        Pipe(upper_pipe, self.screen)  # Upper pipe

    def new_pipe(self):
        # New pipe pair if old about to go off screen
        n_pair = 0
        for pipe in self.pipes_group:
            if 0 < pipe.x_pos < 5 and n_pair < 1:
                self.get_pipe_pair()
                n_pair += 1
        # If no pipes exist, create a new pipe pair
        if not self.pipes_group:
            self.get_pipe_pair()

    def make_sprite_groups(self):
        # assign default groups to each sprite class
        self.all_sprites_group = pygame.sprite.LayeredUpdates()  # All sprites in this group
        self.gameover_group = pygame.sprite.LayeredUpdates()
        self.bird_group = pygame.sprite.LayeredUpdates()
        self.base_group = pygame.sprite.LayeredUpdates()
        self.pipes_group = pygame.sprite.LayeredUpdates()
        # ---- Enemy group
        Pipe.groups = self.pipes_group, self.gameover_group, self.all_sprites_group
        Base.groups = self.base_group, self.gameover_group, self.all_sprites_group
        # ---- Player group
        Bird.groups = self.bird_group, self.all_sprites_group

    def intro_player_oscillate(self):
        """oscillates the value of player_oscillate['val'] between 4 and -4"""
        if abs(self.initial_info['player_oscillate']['val']) == 4:
            self.initial_info['player_oscillate']['dir'] *= -1

        if self.initial_info['player_oscillate']['dir'] == 1:
            self.initial_info['player_oscillate']['val'] += 1
        else:
            self.initial_info['player_oscillate']['val'] -= 1
        return self.initial_info['player_oscillate']['val']

    def event_handle(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_q:
                    pygame.quit()
                    sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                # make first flap sound and return values for mainGame
                self.intro = False

    def show_welcome_animation(self):
        base_x = self.initial_info['base_x']
        self.intro = True
        while self.intro:
            self.event_handle()

            # adjust player_pos_y, player_index, base_x
            if (self.initial_info['loop_iter'] + 1) % 5 == 0:
                self.initial_info['player_index'] = next(self.initial_info['player_index_generator'])
            self.initial_info['loop_iter'] = (self.initial_info['loop_iter'] + 1) % 30
            base_x = -((-base_x + 4) % self.initial_info['base_shift'])
            self.initial_info['player_pos_y'] += self.intro_player_oscillate()

            # draw sprites
            self.screen.blit(IMAGES['background'], (0, 0))
            self.screen.blit(IMAGES['player'][self.initial_info['player_index']],
                             (self.initial_info['player_pos_x'], self.initial_info['player_pos_y']))
            self.screen.blit(IMAGES['message'],
                             (self.initial_info['message_pos_x'], self.initial_info['message_pos_x']))
            self.screen.blit(IMAGES['base'], (base_x, self.initial_info['base_y']))

            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    FlappyBirds()
#    cProfile.run('FlappyBirds()')
