import random

import numpy as np

from FlappyBird_NeuroEvolution.GeneticAlgorithm.tools.extra import sort_lists, is_numpy


def sel_best(fitness, size):
    """
    Return list of indexes with length 'size' in descending order [from best to worst]
    :param fitness: List
    :param size: Integer
    :return: List with indexes of 'fitness'
    """
    fitness_index = []
    for i, _ in enumerate(fitness):
        fitness_index.append(i)
    sorted_fitness, sorted_index = sort_lists(fitness, fitness_index, descending=True)
    return [sorted_index[k] for k in range(size)]


def sel_worst(fitness, size):
    """
    Return list of indexes with length 'size' in ascending order [from worst to best]
    :param fitness: List
    :param size: Integer
    :return: List with indexes of 'fitness'
    """
    fitness_index = []
    for i, _ in enumerate(fitness):
        fitness_index.append(i)
    sorted_fitness, sorted_index = sort_lists(fitness, fitness_index, descending=False)
    return [sorted_index[k] for k in range(size)]


def sel_random(individuals, size, replacement=False):
    """
    Return list of size 'size' with randomly selected individuals
    :param individuals: List of objects
    :param size: Integer, returned list length
    :param replacement: Boolean
    :return: List with elements of 'individuals'
    """
    if is_numpy(individuals):
        return [np.random.choice(individuals, replace=replacement) for _ in range(size)]
    else:
        if replacement:
            return random.choices(individuals, k=size)
        else:
            return random.sample(individuals, k=size)


def sel_roulette(fitness, tournaments=2, replace=False):
    """
    Fitness proportionate selection or roulette wheel selection.
    Note that all fitness values should be positive
    :param fitness: List of fitness values
    :param tournaments: Integer, number of tournaments to hold
    :param replace: Boolean, select individuals with replacement (True) or unique (False)
    :return: List with indexes of 'fitness'
    """
    # Create list of indexes
    tmp_index, tmp_fitness = [], []
    for i, val in enumerate(fitness):
        tmp_index.append(i)
        tmp_fitness.append(val)
    # Normalize with regard to total fitness
    total_fitness = sum(tmp_fitness)
    # Draw individuals
    sel_individuals = []
    for tournament in range(tournaments):
        # Get random value between [0, total_fitness)
        i, value = 0, random.random() * total_fitness
        while True:
            value -= tmp_fitness[i]
            # Check if 'tmp_index[i]' is the winner
            if value < 0:
                sel_individuals.append(tmp_index[i])
                break
            i += 1
        if replace is False:
            del tmp_fitness[i]
            del tmp_index[i]
            # Adjust interval for random number
            total_fitness = sum(tmp_fitness)
    return sel_individuals


def sel_sus(fitness, size):
    """
    Perform Stochastic Universal Sampling (SUS), this method has no bias and minimal spread.
    The idea is to map evenly spaced points to fitness values which have been sorted in descending order.
    The number of points is equal to the number of individuals to be selected.
    The larger fitness values will have more pointers inside them. As a consequence, individuals with higher fitness
    will be selected more frequently.

    "https://en.wikipedia.org/wiki/Stochastic_universal_sampling"

    :param fitness: List of fitness values for the population
    :param size: Integer
    :return: List of indexes of 'fitness'
    """
    # Sort fitness in descending order
    sorted_fitness, sorted_index = sort_lists(fitness, list(range(len(fitness))), descending=True)
    # Total fitness
    total_fitness = sum(sorted_fitness)
    # Normalize fitness (i.e map fitness values to the interval [0, 1])
    sorted_fitness[:] /= total_fitness
    # Distance between the pointers to create
    distance = 1 / size
    # Initial pointer start
    start = random.uniform(0, distance)
    # Pointers
    pointers = [start + i * distance for i in range(size)]

    # Perform selection
    sel_individuals = []
    for pointer in pointers:
        i = 0
        tmp_sum = sorted_fitness[i]
        while tmp_sum < pointer:
            i += 1
            tmp_sum += sorted_fitness[i]
        sel_individuals.append(sorted_index[i])

    return sel_individuals


def sel_tournament(fitness, tournaments=1, tour_size=2, replace=False):
    """
    Tournament selection.
    :param fitness: List of fitness
    :param tour_size: Number of individuals participating in each tournament
    :param tournaments: Integer, number of tournaments held (if replace=True, then tournaments <= len(fitness) - 1
    :param replace: Boolean, select individuals with replacement (True) or unique (False)
    :return: List with indexes of 'fitness'
    """
    # List of indexes
    tmp_index, tmp_fitness = [], []
    for i, val in enumerate(fitness):
        tmp_index.append(i)
        tmp_fitness.append(val)
    # Perform tournament
    sel_individuals = []
    for tournament in range(tournaments):
        # Draw a set of individuals from current tmp_fitness population
        # It's OK to draw with replacement because the individual is removed if 'replace=False'
        tour_individuals = sel_random(tmp_fitness, tour_size, replacement=True)
        # Select best individual from tournament individuals
        best_ind = max(tour_individuals)
        # Append corresponding index of best performing individual to selected individuals
        for i, val in enumerate(tmp_fitness):
            if val == best_ind:
                sel_individuals.append(tmp_index[i])
                break
        # Using replacement
        if replace is False:
            del tmp_index[tmp_fitness.index(best_ind)]
            del tmp_fitness[tmp_fitness.index(best_ind)]
    return sel_individuals
