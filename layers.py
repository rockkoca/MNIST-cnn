import abc

import numpy as np

import functions


class Layer(metaclass=abc.ABCMeta):
    def __init__(self, n_in, n_out):
        self.n_in = n_in
        self.n_out = n_out

    @abc.abstractmethod
    def feedforward(self):
        raise NotImplementedError

    @abc.abstractmethod
    def backpropagate(self):
        raise NotImplementedError


###############################################################################

class InputLayer(Layer):
    def __init__(self, n_in, n_out):
        super().__init__(n_in, n_out)

    def feedforward(self):
        raise NotImplementedError

    def backpropagate(self):
        raise NotImplementedError


###############################################################################

class FullyConnectedLayer(Layer):
    def __init__(self, n_in, n_out, act_func):
        super().__init__(n_in, n_out)
        self.act_func = act_func
        self.der_act_func = functions.get_derivative(act_func)

    def feedforward(self, a, w, b):
        """
        Feedforward the observation through the layer.

        :param a: the activations of the previous layer (shape: (n, 1))
        :param w: the weights connecting this layer with the previous one (shape: (m, n))
        :param b: the bias associated to this layer (shape: (m, 1))
        :returns: zetas and activations of this layer (shape: (m, 1))
        """
        z = np.dot(w, a) + b
        return z, self.act_func(z)

    def backpropagate(self, z, a, w, delta_zlp):
        """
        Backpropagate the error through the layer.

        :param z: the zetas of this layer (computed during feedforward)
        :param a: the activations of this layer (computed during feedforward)
        :param w: the weights associated to this layer and the previous one
        :param delta_zlp: the error propagated by the previous layer
        :returns: the amount of change of the weights under consideration, the amount of change of the biases under
            consideration and the error propagated by this layer
        """
        # compute the derivatives of the weights and biases
        d_der_w = np.dot(delta_zlp, a.T)
        # propagate the error for the next layer
        delta_zl = np.dot(w.T, delta_zlp) * self.der_act_func(z)
        return d_der_w, delta_zlp, delta_zl
