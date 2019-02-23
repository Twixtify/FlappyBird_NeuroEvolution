import random


def mut_uniform(ind, mut_prob, range_max, range_min):
    """
    Mutate an individual
    :param ind: List of values
    :param mut_prob: Double, Mutation rate
    :param range_max: Float, maximum constraint
    :param range_min: Float, minimum constraint
    :return: List
    """
    for i, val in enumerate(ind):
        if random.random() <= mut_prob:
            ind[i] = range_min + (range_max - range_min) * random.random()
    return ind


def mut_gauss(ind, mut_prob, perturb_size=1.):
    """
    Mutate an individual using a Gaussian distribution
    :param ind: List of values
    :param mut_prob: Float, probability for mutation
    :param perturb_size: Float, size of perturbation
    :return: List
    """
    for i, val in enumerate(ind):
        if random.random() <= mut_prob:
            ind[i] = val + perturb_size * random.gauss(0, 0.1)
    return ind
