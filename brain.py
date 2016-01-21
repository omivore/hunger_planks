# brain.py

import numpy as np

class Brain():

    def __init__(self):
        self.past_values = np.zeroes(10)
        self.input_synapses = 2 * np.random.random((18, 10)) - 1
        self.hidden_synapses = 2 * np.random.random((10, 10)) - 1

    @staticmethod
    def nonlin(x, derivative=False):
        if derivative:
            return x * (1 - x)
        return 1 / (1 + np.exp(-x))

    def think(self, inputs: [float for _ in range(8)]):
        # Here's the inputs...
        inputs = np.array(inputs)
        # Use that to generate the outputs (input combined with the previous hidden layer)
        ouputs = nonlin(np.dot(inputs, self.input_synapses) + np.dot(self.pas_values[-1], self.hidden_synapses))
        self.past_values = outputs

        print(outputs)
        return (outputs[0], outputs[1]) # Return two of the neurons' outputs. Doesn't really matter which.
