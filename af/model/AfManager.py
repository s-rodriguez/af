import importlib
import inspect
import os
import pkgutil

from af.model.algorithms.BaseAlgorithm import BaseAlgorithm
from af.controller.hierarchies.AutomaticDimension import AutomaticDimension

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
    """This class is to be used as a proxy against external applications that want to integrate with the AF

    """
    def __init__(self):
        self.privacy_types = {PRIVACY_TYPE_IDENTIFIER, PRIVACY_TYPE_QI, PRIVACY_TYPE_SENSITIVE, PRIVACY_TYPE_NON_SENSITIVE}
        self.privacy_models = {K_PRIVACY_MODEL, L_PRIVACY_MODEL}
        self.data_types = {BASIC_TYPE_STRING, BASIC_TYPE_INT, BASIC_TYPE_DATE}
        self.load_modules()

    @staticmethod
    def load_modules():
        """Load every module contained inside the algorithms module directory.

        """
        pkg_dir = os.path.join(os.path.dirname(__file__), 'algorithms')
        for (module_loader, name, ispkg) in pkgutil.iter_modules([pkg_dir]):
            importlib.import_module('.' + name, __package__+'.algorithms')

    def get_all_subclasses(self, cls):
        """Given a class, retrieve all the subclasses (From root to leaves)

        :param cls: A class
        :rtype: list of all subclasses of cls

        """
        all_subclasses = []

        for subclass in cls.__subclasses__():
            all_subclasses.append(subclass)
            all_subclasses.extend(self.get_all_subclasses(subclass))

        return all_subclasses

    def get_algorithms(self, privacy_model):
        """Return a list of all the available algoritms.

        :rtype: List of algorithm names

        """
        algorithms = []
        for algorithm in self.get_all_subclasses(BaseAlgorithm):
            if algorithm.PRIVACY_MODEL == privacy_model:
                algorithms.append(algorithm.ALGORITHM_NAME)
        return algorithms

    def get_algoritm_parameters(self, algorithm_selected):
        """Return all the particular parameters an algorithm needs to be used.
        The common arguments are: self, data_config and optimized_processing

        :param string algorithm_selected: Name of the algorithm
        :rtype: List of arguments

        """
        for algorithm in self.get_all_subclasses(BaseAlgorithm):
            if algorithm.ALGORITHM_NAME == algorithm_selected:
                common_args = ('self', 'data_config', 'optimized_processing')
                particular_arguments = [i for i in inspect.getargspec(algorithm.__init__).args if i not in common_args]
                return particular_arguments
        return None

    def get_algorithm_instance(self, data_config, algorithm_name, algorithm_arguments, optimized_processing):
        """Create an instance of a certain algorithm and return it. It receives all the arguments necessary for the instance creation.

        :param data_config: Data configuration object
        :type data_config: class:`af.model.DataConfig` instance
        :param string algorithm_name: Name of the algorithm intended to create the instance
        :param list algorithm_arguments: List of particular arguments the algorithm needs
        :param bool optimized_processing: Indicates if the algorithm should try to optimize the processing while transforming
        :rtype: class:`af.model.algorithms.BaseAlgorithm` instance

        """
        for algorithm in self.get_all_subclasses(BaseAlgorithm):
            if algorithm.ALGORITHM_NAME == algorithm_name:
                algorithm_instance = algorithm(data_config=data_config, optimized_processing=optimized_processing, **algorithm_arguments)
                return algorithm_instance
        return None

    def get_automatic_dimensions_names(self, attribute_type):
        """Return a list of all the available automatic dimensios for a given type.

        :rtype: List of automatic dimensions

        """
        automatic_dimensions = []
        for automatic_dimension in self.get_all_subclasses(AutomaticDimension):
            if attribute_type in automatic_dimension.VALID_FOR_TYPE:
                automatic_dimensions.append(automatic_dimension.AD_NAME)
        return automatic_dimensions

    def get_automatic_dimension_description(self, automatic_dimension_name):
        """Return the description of the automatic dimension

        :rtype: Automatic dimension description

        """

        for automatic_dimension in self.get_all_subclasses(AutomaticDimension):
            if automatic_dimension_name == automatic_dimension.AD_NAME:
                return automatic_dimension.AD_DESCRIPTION
        return None

    def get_automatic_dimension_instance(self, automatic_dimension_name, list_of_values, automatic_dimension_arguments):
        """Create an instance of a certain automatic dimension and return it. It receives all the arguments necessary for the instance creation.

        :param string automatic_dimension_name: Name of the automatic dimension intended to create the instance
        :param list automatic_dimension_arguments: List of particular arguments the automatic dimension needs
        :param bool list_of_values: Values that uses to create the automatic dimension
        :rtype: class:`af.controller.hierarchies.AutomaticDimension` instance

        """
        # TODO: add automatic_dimension_arguments
        for automatic_dimension in self.get_all_subclasses(AutomaticDimension):
            if automatic_dimension_name == automatic_dimension.AD_NAME:
                automatic_dimension_instance = automatic_dimension(list_of_values)
                return automatic_dimension_instance
        return None
