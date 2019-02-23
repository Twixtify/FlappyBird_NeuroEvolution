from FlappyBird_NeuroEvolution.config import *
from FlappyBird_NeuroEvolution.GeneticAlgorithm.tools.selection import *
from FlappyBird_NeuroEvolution.GeneticAlgorithm.tools.mutation import *
from FlappyBird_NeuroEvolution.GeneticAlgorithm.tools.breed import *


def evolve_best(individuals, fitness, n_parents):
    """
    Breed only the best individuals
    :param individuals: List of floats
    :param fitness: List of floats
    :param n_parents: Integer
    :return: List
    """
    # -- Select parents --
    parents = sel_best(fitness, n_parents)  # Indexes of best individuals in descending order

    # -- Produce children --
    children = breed_uniform(individuals, parents, n_children=POPULATION, co_prob=CO_PROB)

    # -- Mutate children --
    for child in children:
        mut_gauss(child, MUT_PROB)

    new_individuals = list(children)

    # -- Elitism --
    if N_SURVIVE > 0:
        best_id = sel_best(fitness, N_SURVIVE)
        for i, best in enumerate(best_id):
            new_individuals[i] = list(individuals[best])

    return new_individuals


def evolve_tournament(individuals, fitness, tournaments, tour_size):
    """
    Perform tournament selection and mutate children.
    :param individuals: List of floats
    :param fitness: List of floats
    :param tournaments: Integer
    :param tour_size: Integer
    :return: List
    """
    # ------- Tournament selection --------
    parents = sel_tournament(fitness, tournaments, tour_size, replace=False)

    # -- Perform Crossover --
    children = breed_uniform(individuals, parents, n_children=POPULATION, co_prob=CO_PROB)

    # ------- Mutate children -------
    for child in children:
        mut_gauss(child, MUT_PROB)

    new_individuals = list(children)

    # -- Elitism --
    if N_SURVIVE > 0:
        best_id = sel_best(fitness, N_SURVIVE)
        for i, best in enumerate(best_id):
            new_individuals[i] = list(individuals[best])

    return new_individuals


def evolve_roulette(individuals, fitness, tournaments):
    """
    Breed a new population using roulette selection.
    :param individuals: List of floats
    :param fitness: List of floats
    :param tournaments: Integer
    :return: List
    """
    # -- Select parents --
    parents = sel_roulette(fitness, tournaments)

    # -- Perform Crossover --
    children = breed_uniform(individuals, parents, n_children=POPULATION, co_prob=CO_PROB)

    # ------- Mutate children -------
    for child in children:
        mut_gauss(child, MUT_PROB)

    new_individuals = list(children)

    # -- Elitism --
    if N_SURVIVE > 0:
        best_id = sel_best(fitness, N_SURVIVE)
        for i, best in enumerate(best_id):
            new_individuals[i] = list(individuals[best])

    return new_individuals


def evolve_breed_roulette(individuals, fitness, tournaments):
    """
    Breed a new population using breed_roulette.

    **
    This method does - NOT - use roulette selection to pick parents from the population.
    It uses roulette selection when picking which parents should breed.
    See 'evolve_roulette' for using roulette selection.
    **

    :param individuals: List of floats
    :param fitness: List of floats
    :param tournaments: Integer
    :return: List
    """
    # -- Select parents --
    parents = sel_random(list(range(len(fitness))), tournaments)
    parents_fitness = [fitness[val] for val in parents]

    # -- Perform Crossover --
    children = breed_roulette(individuals, parents, parents_fitness, n_children=POPULATION, co_prob=CO_PROB)

    # ------- Mutate children -------
    for child in children:
        mut_gauss(child, MUT_PROB)

    new_individuals = list(children)

    # -- Elitism --
    if N_SURVIVE > 0:
        best_id = sel_best(fitness, N_SURVIVE)
        for i, best in enumerate(best_id):
            new_individuals[i] = list(individuals[best])

    return new_individuals


def evolve_sus(individuals, fitness, n_parents):
    """
    Breed a new population using Stochastic Universal Sampling
    :param individuals: List of floats
    :param fitness: List of floats
    :param n_parents: Integer
    :return: List
    """
    # -- Select parents --
    parents = sel_sus(fitness, n_parents)

    # -- Perform crossover --
    children = breed_uniform(individuals, parents, n_children=POPULATION, co_prob=CO_PROB)

    # ------- Mutate children -------
    for child in children:
        mut_gauss(child, MUT_PROB)

    new_individuals = list(children)

    # -- Elitism --
    if N_SURVIVE > 0:
        best_id = sel_best(fitness, N_SURVIVE)
        for i, best in enumerate(best_id):
            new_individuals[i] = list(individuals[best])

    return new_individuals
