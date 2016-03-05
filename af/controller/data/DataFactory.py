from af.controller.data.SqliteController import SqliteController
from af.controller.data.CSVController import CSVController


class DataFactory:

    @staticmethod
    def create_controller(data_location, controller_type):
        #TODO reimplement using subclasses correctly
        #for cls in DataController.__subclasses__():
        #    if cls.CONTROLLER_TYPE == controller_type:
        #        return cls(data_location)
        for cls in (SqliteController, CSVController):
            if cls.CONTROLLER_TYPE == controller_type:
                return cls(data_location)
        raise ValueError()

    @staticmethod
    def get_available_controllers():
        available_controllers = []
        #TODO reimplement using subclasses correctly
        for cls in (SqliteController, CSVController):
            available_controllers.append(cls.CONTROLLER_TYPE)
        return available_controllers

    @staticmethod
    def get_controller_file_extension(controller_type):
        #TODO reimplement using subclasses correctly
        for cls in (SqliteController, CSVController):
            if cls.CONTROLLER_TYPE == controller_type:
                return cls.CONTROLLER_EXTENSION
        raise ValueError()
