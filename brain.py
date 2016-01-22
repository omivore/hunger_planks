# brain.py

import numpy as np

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
