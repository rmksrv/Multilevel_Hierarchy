from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wlexpr


class ArborescenceWorker:
    """
    Class, calling all features from ArborescenceKernel.wl
    """
    def get_connection_probability(self, x):
        """
        :param x: distance of two separate nodes
        :return: connection probability of two nodes [0; 1]
        """
        return self.__session__.evaluate(
            wlexpr("GetProb[{}]".format(x)))

    def make_static_hierarchy(self, connection_prob):
        """
        Creates maximum tree of spanning arborescence
        :param connection_prob:
        :return: Weighted adjacency matrix of tree
        """
        return self.__session__.evaluate(
            wlexpr("StaticHierarchy[{}]".format(connection_prob)))

    def __init__(self):
        self.__session__ = WolframLanguageSession()
        print("WolframSession started")
        self.__session__.evaluate(
            wlexpr("Get[\"ArborescenceKernel.wl\"]"))
        print("Imported ArborescenceKernel.wl")

    def __del__(self):
        self.__session__.terminate()
        print("WolframSession terminated")


if __name__ == "__main__":
    a = ArborescenceWorker()
    test_mx = """{
        {0.1, 0.5, 0.6},
        {0.4, 0.4, 0.3},
        {0.1, 0.4, 0.8}
    }"""
    print(test_mx, test_mx.__class__)
    res = a.make_static_hierarchy(wlexpr("ToExpression[{}]".format(test_mx)))
    print(res, res.__class__)
    del a
