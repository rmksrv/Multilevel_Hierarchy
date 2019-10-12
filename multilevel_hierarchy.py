import networkx as nx
import numpy as np


class MultilevelHierarchy:
    def __init__(self, connprob: np.array):
        """
        :param connprob: matrix(NxN) of connection probability with each node
        self.connpwr: connection power matrix (0 on diag and 1-st row)
        """
        self.connprob = connprob
        self.connpwr = connprob * connprob.transpose()
        self.connpwr[0] = pow(self.connprob[0], 2)

    def debug_print(self):
        print('connprob =\n', h.connprob)
        print('connpwr =\n', h.connpwr)


m = np.array([
    [0, 0.5, 0.7],
    [0, 0, 0.5],
    [0, 0.4, 0]
])
h = MultilevelHierarchy(m)
h.debug_print()
