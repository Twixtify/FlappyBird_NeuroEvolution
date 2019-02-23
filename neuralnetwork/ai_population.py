from FlappyBird_NeuroEvolution.neuralnetwork.feedforward_nn import FeedForwardNN


class AIPopulation:
    """This class is for holding individuals created"""
    def __init__(self, input_shape, neurons_layer, activations):
        self.pop = []
        self.ai_options = {}
        self.set_options(input_shape, neurons_layer, activations)

    def get_pop(self):
        """
        Return population
        :return: None
        """
        return self.pop

    def get_ind(self, i, use_bias=False):
        """Return 1D list of the neural network weights"""
        return self.pop[i].get_flatten_weights(use_bias=use_bias)

    def get_ai(self, i):
        """Return an ai object from population"""
        return self.pop[i]

    def set_pop(self, individuals):
        """
        Update weights for the whole population
        Length of individuals must equal length of population
        Note that each individual should be a 1D list
        """
        for i, ind in enumerate(self.pop):
            ind.update_weights(individuals[i], is_flat=True)

    def set_ind(self, i, ind, is_flat):
        """Update weights of neural network"""
        self.pop[i].update_weights(ind, is_flat)

    def ai_input_size(self):
        """Get neural network options"""
        return self.ai_options['input_shape'][0]

    def init_pop(self, size):
        """
        Initialize the whole population
        :param size: Integer
        :return: None
        """
        for ind in range(size):
            self.pop.append(FeedForwardNN(self.ai_options['input_shape'], self.ai_options['neurons_layer'],
                                          self.ai_options['activations']))

    def append_pop(self, ind):
        """
        Append to population
        :param ind: Object
        :return: None
        """
        self.pop.append(ind)

    def set_options(self, input_shape, neurons_layer, activations):
        """
        Set AI options of population
        :param input_shape: Tuple (Integer,)
        :param neurons_layer: List of integers [hidden_neurons_layer_1, ... , hidden_neurons_layer_k]
        :param activations: List of strings ["relu", "softmax"]
        :return: None
        """
        self.ai_options['input_shape'] = input_shape
        self.ai_options['neurons_layer'] = neurons_layer
        self.ai_options['activations'] = activations

    def clear_pop(self):
        """
        Clear population. Set population to an empty list.
        After call: 'self.pop = []'
        :return: None
        """
        self.pop.clear()

if __name__ == '__main__':
    import random
    ai_pop = AIPopulation(input_shape=(1,), neurons_layer=[2, 1], activations=["relu", "softmax"])
    ai_pop.init_pop(2)

    for i, ind in enumerate(ai_pop.get_pop()):
        print(ai_pop.get_ind(i, use_bias=True))
    print("\n", "-----------------------------------", "\n")

    rand_weights = []
    for _ in range(len(ai_pop.get_ind(0, use_bias=True))):
        rand_weights.append(random.randint(10, 20))
    print(rand_weights)
    print("\n", "-----------------------------------", "\n")

    ai_pop.set_pop([rand_weights, rand_weights])
    for i, ind in enumerate(ai_pop.get_pop()):
        print(ai_pop.get_ind(i, use_bias=True))
    print("\n", "-----------------------------------", "\n")
