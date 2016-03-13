from af.model.algorithms.BaseAlgorithm import BaseAlgorithm
class BaseKAlgorithm(BaseAlgorithm):

    def __init__(self, data_config, k):
        BaseAlgorithm.__init__(self, data_config)
        if k < 1:
            raise Exception("Invalid k param")
        self.k = k


