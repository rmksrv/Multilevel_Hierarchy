import sys
import math
import numpy as np
import networkx as nx

class StructureBuilder:
    def connection_probability(self, coords):
        '''
        Calculate `connection probability` mx from `coords` mx
        Coords example:
            (
            (1.0, 3.0),
            (8.0, 5.0),
              .  .  .
            (x_n, y_n),
            )
        '''
        msize = len(coords)
        cprob = np.empty((msize, msize))
        for i in range(msize):  # Row bypass
            for j in range(msize):  # Column bypass
                # No one can connect to root node or to itself
                if j == 0 or i == j:
                    cprob[i][j] = 0.0
                else:
                    cprob[i][j] = Utils.get_prob(Utils.dist2(coords[i], coords[j]))
        return cprob

    def connection_power(self, cprob: np.ndarray):
        '''
        Calculate `connection power` mx from `connection probability` mx
        '''
        msize = len(cprob[0])
        cpower = cprob * np.transpose(cprob)
        # After multiplication of cprobs we get ruined cpower of `root`` -> `other node`
        # It caused by zeroes in row 0 (nobody can connect to root as master).
        # As fix: sqr of current cprob
        for i in range(msize):
            cpower[0][i] = cprob[0][i]**2
        return cpower

    def build_tree(self, cprob: np.ndarray, mode='connection_probability', as_matrix=False, recalculate_probs=False, max_slaves=0, max_depth=0):
        '''
        Get structure from conention probability mx
            `mode`:
                'connection_probability' -- method takes `connection_probability` on input and calculate connection_power itself
                'connection_power'       -- method takes `connection_power`on input; it suppose to correctness of cpower
                                            (actually it is needed to implement some features - you really should not use it)
            `as_matrix`:
                True                     -- returns adjacency matrix instead of networkx.DiGraph
                False                    -- returns networkx.DiGraph object
            `recalculate_probs`:         -- recalculate cpowers feature
            `max_slaves`                 -- max slaves feature. If it > 0 => for each node number of connections will be limited
            `max_depth`                  -- max depth feature. If it > 0 => tree_depth will be limited
        '''
        
        msize = len(cprob[0])
        # Mode checking
        if mode == 'connection_probability':
            cpower = self.connection_power(cprob)
        elif mode == 'connection_power':
            cpower = cprob
        
        # recalculating_probs feature (look on `DynamicHierarhy` function in Wolfram Notebook)
        if recalculate_probs:
            # Build base tree
            base_tree = self.build_tree(cprob, mode=mode, as_matrix=True, max_slaves=max_slaves, max_depth=max_depth)
            # Searching nodes to reweight
            nodes_to_reweight = []
            for i in range(msize):  # Row bypass
                connection_counter = 0  # counter of i node 
                for j in range(msize):  # Column bypass
                    if base_tree[i][j] > 0:
                        connection_counter += 1
                if connection_counter > 1:  # add node to reweight list if more than 1 connection
                    nodes_to_reweight.append(i)
            # Reweighting nodes
            for i in nodes_to_reweight:
                div = 1  # divider of conn power
                for j in range(msize):
                    if base_tree[i][j] > 0:
                        cpower[i][j] = cpower[i][j] / div
                        div *= 2
        
        # max_slaves feature
        if max_slaves > 0:
            cpower_changed = True
            while cpower_changed:
                # Build base tree from existing cpower mx
                base_tree = self.build_tree(cpower, mode='connection_power', as_matrix=True, recalculate_probs=recalculate_probs, max_depth=max_depth)
                # Searching first meeting of node with more than `max_slaves` connection
                cpower_changed = False
                for i in range(msize):
                    current_connections_index = []
                    current_connections_power = []
                    for j in range(msize):
                        # all exist connections are adding to list to get one with min cpower to drop it
                        if base_tree[i][j] > 0:
                            current_connections_index.append((i, j))  # need to write index of node and its power
                            current_connections_power.append(base_tree[i][j])
                    # If node with too many slaves is found, then we fix cpower -> cprob
                    # and rebuild tree (kind of recursive way)
                    if len(current_connections_power) > max_slaves:
                        # Setting flag
                        cpower_changed = True
                        # Search min connection
                        min_listindex = current_connections_power.index(min(current_connections_power))
                        min_i = current_connections_index[min_listindex][0]
                        min_j = current_connections_index[min_listindex][1]
                        # and drop it
                        cpower[min_i][min_j] = 0
        
        # max_depth feature
        if max_depth > 0:
            cpower_changed = True
            while cpower_changed:
                # Build base tree from existing cpower mx
                #base_tree_matrix = self.build_tree(cpower, mode='connection_power', as_matrix=True, recalculate_probs=recalculate_probs, max_slaves=max_slaves)
                base_tree = self.build_tree(cpower, mode='connection_power', as_matrix=False, recalculate_probs=recalculate_probs, max_slaves=max_slaves)
                cpower_changed = False
                # If we have too far node, then we fix cpower -> cprob (cpower [-2][-1] := 0)
                # and rebuild tree (kind of recursive way)
                if Utils.tree_depth(base_tree) > max_depth:
                    # Setting flag
                    cpower_changed = True
                    longest_path = nx.dag_longest_path(base_tree)
                    # Farest node
                    far_i = longest_path[-2]
                    far_j = longest_path[-1]
                    # Drop it
                    cpower[far_i][far_j] = 0
        
        # Make structure
        G = nx.from_numpy_array(cpower, create_using=nx.DiGraph)
        try:
            res = nx.maximum_spanning_arborescence(G, default=0)
            if as_matrix:
                res = nx.to_numpy_array(res)
        except nx.exception.NetworkXException:  # if no tree found
            raise  # handle this in interface part
        return res


class Utils:
    @staticmethod
    def get_prob(r):
        '''
        Get connection_probability by distance r of two nodes
        '''
        return math.exp(-r**2 / 500)

    @staticmethod
    def dist2(p1, p2):
        '''
        Distance between two points
        '''
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

    @staticmethod
    def tree_depth(T):
        '''
        return longest path of T (amount of edges of longest path)
        '''
        return len(nx.dag_longest_path(T))-1


if __name__ == '__main__':
    np.set_printoptions(suppress=True, linewidth=np.inf)  # disable mantissa view for numbers
    sb = StructureBuilder()
    #test_coords = (
    #    (0.0, 0.0),
    #    (5.0, 0.0),
    #    (10.0, 0.0),
    #    (15.0, 0.0),
    #    (20.0, 0.0),
    #    (0.0, 5.0),
    #    (0.0, 10.0),
    #    (0.0, -5.0),
    #    (-5.0, 0.0),
    #)
    test_coords = (
        (0.0, 0.0),
        (4.0, 0.0),
        (10.0, 0.0),
        (13.0, 0.0),
        (20.0, 0.0),
        (0.0, 3.0),
        (0.0, 6.0),
        (0.0, -3.0),
        (-5.0, 0.0),
    )

    
    print('\ntest_coords:')
    for i in test_coords:
        print('({}, {})'.format(i[0], i[1]))
    
    print('\nconnection_probability:')
    test_cprob = sb.connection_probability(test_coords)
    print(test_cprob)
    
    print('\nconnection_power:')
    test_cpower = sb.connection_power(test_cprob)
    print(test_cpower)
     
    print('\nstructure matrix data:')
    test_adjmx = sb.build_tree(test_cprob)
    print('  __class__: {}'.format(test_adjmx.__class__))
    print('  is_tree: {}'.format(nx.is_tree(test_adjmx)))
    print('  is_arborescence: {}'.format(nx.is_arborescence(test_adjmx)))
    print('  longest_path: {}'.format(nx.dag_longest_path(test_adjmx)))
    print('  longest_path_length: {}'.format(Utils.tree_depth(test_adjmx)))
    
    print('\nstructure matrix:')
    test_adjmx = sb.build_tree(test_cprob, as_matrix=True)
    print(test_adjmx)
    
    print('\nstructure matrix (recalculate_probs=True):')
    test_adjmx = sb.build_tree(test_cprob, as_matrix=True, recalculate_probs=True)
    print(test_adjmx)
    
    print('\nstructure matrix (max_slaves=2):')
    test_adjmx = sb.build_tree(test_cprob, as_matrix=True, max_slaves=2)
    print(test_adjmx)
    
    print('\nstructure matrix (max_depth=3):')
    test_adjmx = sb.build_tree(test_cprob, as_matrix=True, max_depth=3)
    print(test_adjmx)
    
    print('\nstructure matrix (max_slaves=2, max_depth=3):')
    test_adjmx = sb.build_tree(test_cprob, as_matrix=True, max_slaves=2, max_depth=3)
    print(test_adjmx)


