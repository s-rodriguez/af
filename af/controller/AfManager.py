from af.utils import (
    PRIVACY_TYPE_IDENTIFIER,
    PRIVACY_TYPE_QI,
    PRIVACY_TYPE_NON_SENSITIVE,
    PRIVACY_TYPE_SENSITIVE,
    K_PRIVACY_MODEL,
    L_PRIVACY_MODEL,
    BASIC_TYPE_STRING,
    BASIC_TYPE_DATE,
    BASIC_TYPE_INT
)

from af.model.algorithms.BaseAlgorithm import BaseAlgorithm


class AfController:

    def __init__(self):
        self.privacy_types = {PRIVACY_TYPE_IDENTIFIER, PRIVACY_TYPE_QI, PRIVACY_TYPE_SENSITIVE, PRIVACY_TYPE_NON_SENSITIVE}
        self.privacy_models = {K_PRIVACY_MODEL, L_PRIVACY_MODEL}
        self.data_types = {BASIC_TYPE_STRING, BASIC_TYPE_INT, BASIC_TYPE_DATE}

    @staticmethod
    def get_algorithms(privacy_model):
        algorithms = []
        for algorithm in BaseAlgorithm.__subclasses__():
            if algorithm.PRIVACY_MODEL is privacy_model:
                algorithms.append(algorithm.ALGORITHM_NAME)
        return algorithms
