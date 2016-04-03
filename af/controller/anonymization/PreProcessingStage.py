import os

from af.controller.data.DataFactory import DataFactory
from af.controller.data.SqliteController import SqliteController
from af.model.hierarchies.BaseHierarchy import BaseHierarchy
from af.utils import (
    ANONYMIZATION_DIRECTORY,
    ANONYMIZATION_DB_NAME,
    PRIVACY_TYPE_IDENTIFIER,
)


class PreProcessingStage(object):

    def __init__(self, data_config):
        self.data_config = data_config
        self.initial_db_location = self.data_config.location
        self.db_location = os.path.join(ANONYMIZATION_DIRECTORY, ANONYMIZATION_DB_NAME)
        self.table = self.data_config.table
        self.db_controller = None

    def preprocess(self):
        self.clean_previous_work()
        self.create_db_copy()
        self.db_controller = SqliteController(self.db_location)
        self.remove_identifiable_attributes()
        self.set_indexes_over_qi()

    def clean_previous_work(self):
        if os.path.isfile(self.db_location):
            os.remove(self.db_location)

    def create_db_copy(self):
        extension = os.path.basename(self.initial_db_location).split('.')[1]
        controller = DataFactory.get_controller_from_extension(extension)
        controller.create_db_copy(self.initial_db_location, self.db_location)

    def remove_identifiable_attributes(self):
        identifiable_list = [att.name for att in self.data_config.get_privacy_type_attributes_list(PRIVACY_TYPE_IDENTIFIER)]
        supression_value = BaseHierarchy.supression_node()
        update_ident_list = ["{0}='{1}'".format(att, supression_value) for att in identifiable_list]
        query = "UPDATE {0} SET {1};".format(self.table, ', '.join(update_ident_list))
        list(self.db_controller.execute_query(query))

    def set_indexes_over_qi(self):
        qi_list = []

        # Individual indexes
        for att in self.data_config.get_privacy_type_attributes_list():
            query = "CREATE INDEX {0}_index ON {1} ({2});".format(att.name,
                                                                  self.table,
                                                                  att.name)
            list(self.db_controller.execute_query(query))
            qi_list.append(att.name)

        # Composite index
        query = "CREATE INDEX qi_index ON {0} ({1});".format(self.table, ', '.join(qi_list))
        list(self.db_controller.execute_query(query))
