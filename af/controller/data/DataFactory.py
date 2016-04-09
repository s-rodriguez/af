import importlib
import os
import pkgutil

from af.controller.data.DataController import DataController


class DataFactory:
    @staticmethod
    def load_modules():
        pkg_dir = os.path.dirname(__file__)
        for (module_loader, name, ispkg) in pkgutil.iter_modules([pkg_dir]):
            importlib.import_module('.' + name, __package__)

    @staticmethod
    def create_controller(data_location, controller_type):
        DataFactory.load_modules()
        for cls in DataController.__subclasses__():
            if cls.CONTROLLER_TYPE == controller_type:
                return cls(data_location)
        raise ValueError()

    @staticmethod
    def get_available_controllers():
        DataFactory.load_modules()
        available_controllers = []
        for cls in DataController.__subclasses__():
            available_controllers.append(cls.CONTROLLER_TYPE)
        return available_controllers

    @staticmethod
    def get_controller_file_extension(controller_type):
        DataFactory.load_modules()
        for cls in DataController.__subclasses__():
            if cls.CONTROLLER_TYPE == controller_type:
                return cls.CONTROLLER_EXTENSION
        raise ValueError()

    @staticmethod
    def get_controller_from_extension(controller_extension):
        DataFactory.load_modules()
        for cls in DataController.__subclasses__():
            if controller_extension in cls.CONTROLLER_EXTENSION:
                return cls
        raise ValueError()
