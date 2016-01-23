# brain.py

import numpy as np
import random

class Brain():

    def __init__(self, input_synapses, hidden_synapses):
        self.past_values = np.zeros(10)
        self.input_synapses = input_synapses
        self.hidden_synapses = hidden_synapses

    @classmethod
    def from_random(cls):
        input_synapses = 2 * np.random.random((8, 10)) - 1
        hidden_synapses = 2 * np.random.random((10, 10)) - 1
        return cls(input_synapses, hidden_synapses)

    @classmethod
    def cross_mutate(cls, brains):
        # First build input_synapses.
        input_synapses = np.empty([8, 10])
        for i in range(8):
            for j in range(10):
                input_synapses[i][j] = random.choice(brains).input_synapses[i][j]
        # Then do the same with hidden_synapses.
        hidden_synapses = np.empty([10, 10])
        for i in range(10):
            for j in range(10):
                hidden_synapses[i][j] = random.choice(brains).hidden_synapses[i][j]

        # Mutate random weights in the synapses randomly.
        for _ in range(random.randrange(10)):      # Mutate up to ten times.
            if random.choice([-1, 1]):      # Flip a coin to determine if we're going to mutate.
                continue                    # If heads, don't mutate this time.
            synapse_set = random.choice([input_synapses, hidden_synapses])
            i = random.randrange(synapse_set.shape[0])
            j = random.randrange(synapse_set.shape[1])
            synapse_set[i][j] *= random.random()

        return cls(input_synapses, hidden_synapses)

    @staticmethod
    def nonlin(x, derivative=False):
        if derivative:
            return np.divide(1, np.power(np.cosh(x), 2))
        return np.tanh(x)

    def think(self, inputs: [float for _ in range(8)]) -> (float, float):
        inputs = np.array([inputs])
        # Use that to generate the outputs (input combined with the previous hidden layer)
        outputs = Brain.nonlin(np.dot(inputs, self.input_synapses) + np.dot(self.past_values, self.hidden_synapses))
        self.past_values = outputs

        return (outputs[0][0], outputs[0][1]) # Return two of the neurons' outputs. Doesn't really matter which.
