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
synapse0 = 2 * np.random.random((3, 4)) - 1
synapse1 = 2 * np.random.random((4, 1)) - 1

for _ in range(60000):
    # Forward propagation
    layer0 = x
    layer1 = nonlin(np.dot(layer0, synapse0))
    layer2 = nonlin(np.dot(layer1, synapse1))

    # Calculate error
    layer2_error = y - layer2
    layer2_delta = layer2_error * nonlin(layer2, True)

    layer1_error = layer2_delta.dot(synapse1.T)
    layer1_delta = layer1_error * nonlin(layer1, True)

    # Update the weights
    synapse1 += np.dot(layer1.T, layer2_delta)
    synapse0 += np.dot(layer0.T, layer1_delta)

print(layer2)
