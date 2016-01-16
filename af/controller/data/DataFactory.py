from af.controller.data.DataController import DataController
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


if __name__ == '__main__':
    location = '/home/srodriguez/repos/edat/edat/utils/test.db'
    dbtype = 'sqlite'
    controller = DataFactory.create_controller(location, dbtype)
    print controller
