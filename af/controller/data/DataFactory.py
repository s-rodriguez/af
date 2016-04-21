import importlib
import os
import pkgutil

from af.controller.data.DataController import DataController


class DataFactory:
    """Factory class for all DB controllers created in the module directory

    """
    @staticmethod
    def load_modules():
        """Loads all modules contained on the data module directory

        """
        pkg_dir = os.path.dirname(__file__)
        for (module_loader, name, ispkg) in pkgutil.iter_modules([pkg_dir]):
            importlib.import_module('.' + name, __package__)

    @staticmethod
    def create_controller(data_location, controller_type):
        """Given a controller type, it creates a new controller instance based on the existent one on the data module directory.

        :param string data_location: Location of the database to use
        :param string controller_type: Type of controller we want to create the instance
        :rtype: class:`af.controller.anonymization.data.DataController` instance

        """
        DataFactory.load_modules()
        for cls in DataController.__subclasses__():
            if cls.CONTROLLER_TYPE == controller_type:
                return cls(data_location)
        raise ValueError()

    @staticmethod
    def get_available_controllers():
        """Returns all the available controllers tyoes contained on the data module directory.

        :rtype: list of available controller types

        """
        DataFactory.load_modules()
        available_controllers = []
        for cls in DataController.__subclasses__():
            available_controllers.append(cls.CONTROLLER_TYPE)
        return available_controllers

    @staticmethod
    def get_controller_file_extension(controller_type):
        """Given a controller type, it looks for its extension and returns it

        :param string controller_type: Type of DataController
        :rtype: DataController extension

        """
        DataFactory.load_modules()
        for cls in DataController.__subclasses__():
            if cls.CONTROLLER_TYPE == controller_type:
                return cls.CONTROLLER_EXTENSION
        raise ValueError()

    @staticmethod
    def get_controller_from_extension(controller_extension):
        """Given a controller extension, it retrieves the class to which it belongs.

        :param string controller_extension: Extension of the DataController intended to be looked for
        :rtype: class:`af.controller.anonymization.data.DataController` class

        """
        DataFactory.load_modules()
        for cls in DataController.__subclasses__():
            if controller_extension in cls.CONTROLLER_EXTENSION:
                return cls
        raise ValueError()
