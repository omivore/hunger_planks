# brain.py

import numpy as np

def nonlin(x, derivative=False):
    if derivative:
        return x * (1 - x) 
    return 1 / (1 + np.exp(-x))

x = np.array([[0, 0, 1],
              [0, 1, 1],
              [1, 0, 1],
              [1, 1, 1]])
y = np.array([[0],
              [0],
              [1],
              [1]])
np.random.seed(1)
synapse0 = 2 * np.random.random((3, 1)) - 1

for _ in range(10000):
    # Forward propagation
    layer0 = x
    layer1 = nonlin(np.dot(layer0, synapse0))

    # Calculate error
    layer1_error = y - layer1

    layer1_delta = layer1_error * nonlin(layer1, True)

    # Update the weights
    synapse0 += np.dot(layer0.T, layer1_delta)

print(layer1)
