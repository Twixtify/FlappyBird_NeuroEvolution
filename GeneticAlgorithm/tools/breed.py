import random

import numpy as np

from FlappyBird_NeuroEvolution.GeneticAlgorithm.tools.crossover import co_uniform
from FlappyBird_NeuroEvolution.GeneticAlgorithm.tools.crossover import co_one_point
from FlappyBird_NeuroEvolution.GeneticAlgorithm.tools.selection import sel_roulette


def breed_uniform(individuals, parents, n_children, co_prob):
    """
    Parents are chosen in an uniform matter to produce children for the next generation.
    Note a pair of parents produce only one child (child1).
    :param individuals: List of floats
    :param parents: List of integers (index of individuals to mate)
    :param n_children: Integer
    :param co_prob: Float
    :return: Tuple of lists
    """
    children = ()
    sample_size = 2
    for i in range(n_children):
        parent1, parent2 = random.sample(parents, sample_size)
        child1, child2 = co_uniform(individuals[parent1], individuals[parent2], co_prob)
        children += (child1,)
    return children


def breed_roulette(individuals, parents, parents_fitness, n_children, co_prob):
    """
    Parents are chosen in a roulette fashion to produce children for the next generation.
    Note a pair of parents produce only one child (child1).
    :param individuals: List of floats
    :param parents: List of integers (index of individuals to mate)
    :param parents_fitness: List of floats
    :param n_children: Integer
    :param co_prob: Float
    :return: Tuple of lists
    """
    children = ()
    sample_size = 2
    for i in range(n_children):
        index = sel_roulette(parents_fitness, sample_size)  # Select parent index through roulette selection
        parent1, parent2 = parents[index[0]], parents[index[1]]
        child1, child2 = co_uniform(individuals[parent1], individuals[parent2], co_prob)
        children += (child1,)
    return children


def breed_uniform_one_point(individuals, parents, n_children):
    """
    Parents selected uniformly and uses one point crossover to produce children for the next generation.
    :param individuals: List of floats
    :param parents: List of integers (index of individuals to mate)
    :param n_children: Integer
    :return: Tuple of lists
    """
    children = ()
    sample_size = 2
    for i in range(n_children):
        parent1, parent2 = random.sample(parents, sample_size)
        child1, child2 = co_one_point(individuals[parent1], individuals[parent2])
        children += (child1,)
    return children


def breed_unique(individuals, parents):
    """
    Breed all parents once.
    :param individuals:
    :param parents:
    :return:
    """
    if len(parents) % 2 != 0:
        print("The number of parents are not even")
    children = ()
    for i, parent in enumerate(parents):
        if i < np.floor(len(parents) / 2):
            child1, child2 = co_uniform(individuals[parents[i]], individuals[parents[-i-1]], co_prob=0.5)
            children += (child1,)

    return children


def breed_copy(individuals, parents):
    """
    Copy the parents
    :param individuals: List
    :param parents: List of integers (indexes)
    :return: List
    """
    children = ()
    for parent in parents:
        children += (list(individuals[parent]),)
    return children
