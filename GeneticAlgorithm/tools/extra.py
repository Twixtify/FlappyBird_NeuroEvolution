import numpy as np


def is_numpy(ind):
    """
    Check if ind is a numpy array
    :param ind: Array representing the individual
    :return: Boolean
    """
    if type(ind) is np.ndarray:
        return True
    else:
        return False


def sort_lists(list1, list2, descending=True):
    """
    If descending = True:
        Sort list1 in descending order (largest-to-smallest value)
        and each element of list2 is mapped to list1 elements
    If descending = False:
        Same as above but instead sort in ascending order (smallest-to-largest sorting)
    :param list1: List
    :param list2: List
    :param descending: Boolean
    :return: Sorted lists
    """
    sorted_list1, sorted_list2 = (list(t) for t in zip(*sorted(zip(list1, list2), reverse=descending)))
    return sorted_list1, sorted_list2


def unique_list(list1, list2):
    """
    Return unique elements of list1, i.e return elements of list1 that is not in  list2.
    :param list1: List
    :param list2: List
    :return: List
    """
    unique_list1 = list(set(list1).difference(list2))
    return unique_list1


def map_to_interval(t, old_range, new_range):
    """
    Map a number 't' in a range 'old_range' to a new interval 'new_range'
    1) First, apply the map t ↦ t−a so the left endpoint shifts to the origin. The image interval is [0,b−a].
    2) Next scale the interval to unit length by dividing by its length
    (this is the only place the requirement a≠b is needed).
    The map that does this is t↦1/(b−a)*t. The image interval is [0,1].
    3) Scale up by the desired length d−c using the map t↦(d−c)⋅t, and the image is [0,d−c].
    4) Finally shift the left endpoint to c by the map. t↦c+t. The image is [c,d].
    :param t: Float
    :param old_range: List
    :param new_range: List
    :return: Float
    """
    return new_range[0] + (new_range[1] - new_range[0]) / (old_range[1] - old_range[0]) * (t - old_range[0])
