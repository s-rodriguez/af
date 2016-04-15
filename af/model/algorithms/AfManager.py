import importlib
import inspect
import os
import pkgutil

from af.model.algorithms.BaseAlgorithm import BaseAlgorithm
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


class AfManager:

    def __init__(self):
        self.privacy_types = {PRIVACY_TYPE_IDENTIFIER, PRIVACY_TYPE_QI, PRIVACY_TYPE_SENSITIVE, PRIVACY_TYPE_NON_SENSITIVE}
        self.privacy_models = {K_PRIVACY_MODEL, L_PRIVACY_MODEL}
        self.data_types = {BASIC_TYPE_STRING, BASIC_TYPE_INT, BASIC_TYPE_DATE}
        self.load_modules()

    @staticmethod
    def load_modules():
        pkg_dir = os.path.dirname(__file__)
        for (module_loader, name, ispkg) in pkgutil.iter_modules([pkg_dir]):
            importlib.import_module('.' + name, __package__)

    def get_algorithms(self, privacy_model):
        algorithms = []
        for algorithm in self.get_all_algorithms():
            if algorithm.PRIVACY_MODEL == privacy_model:
                algorithms.append(algorithm.ALGORITHM_NAME)
        return algorithms

    def get_all_algorithms(self):
        a = []
        for algorithm in BaseAlgorithm.__subclasses__():
            a += (self.get_all_subclasses(algorithm))
        return a

    def get_all_subclasses(self, cls):
        all_subclasses = []

        for subclass in cls.__subclasses__():
            all_subclasses.append(subclass)
            all_subclasses.extend(self.get_all_subclasses(subclass))

        return all_subclasses

    def get_algoritm_parameters(self, algorithm_selected):
        for algorithm in self.get_all_algorithms():
            if algorithm.ALGORITHM_NAME == algorithm_selected:
                common_args = ('self', 'data_config', 'optimized_processing')
                particular_arguments = [i for i in inspect.getargspec(algorithm.__init__).args if i not in common_args]
                return particular_arguments
        return None

    def get_algorithm_instance(self, data_config, algorithm_name, algorithm_arguments, optimized_processing):
        for algorithm in self.get_all_algorithms():
            if algorithm.ALGORITHM_NAME == algorithm_name:
                algorithm_instance = algorithm(data_config=data_config, optimized_processing=optimized_processing, **algorithm_arguments)
                return algorithm_instance
        return None
