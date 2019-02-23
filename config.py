# -- Neural network configurations --
INPUT_SHAPE = (4,)  # Bird y + Pipe x + Pipes y
NEURONS_LAYER = [10, 2]  # Neurons per hidden layer and output neurons
ACTIVATIONS = ["sigmoid", "softmax"]
POPULATION = 100

# -- Genetic algorithm configurations --
MUT_PROB = 0.05  # Mutation probability
CO_PROB = 0.5  # Crossover probability
N_SURVIVE = 5  # Elitism
