import os

from af.controller.data.DataFactory import DataFactory
from af.controller.data.SqliteController import SqliteController
from af.model.hierarchies.BaseHierarchy import BaseHierarchy
from af.utils import (
    ANONYMIZATION_DIRECTORY,
    ANONYMIZATION_DB_NAME,
    ADDITIONAL_INFO_TABLE,
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
        """Method that calls all the necessary steps before a data transformation

        """
        self.clean_previous_work()
        self.create_db_copy()
        self.db_controller = SqliteController(self.db_location)
        self.remove_identifiable_attributes()
        self.set_indexes_over_qi()
        self.create_additional_information_table()

    def clean_previous_work(self):
        """If an anonymized db from a previous session exists, then delete it.
        db_location contains the path where the new db will be created

        """
        if os.path.isfile(self.db_location):
            os.remove(self.db_location)

    def create_db_copy(self):
        """Takes the original DB and creates a new copy ready to be manipulated and modified.
        It preserves the state of the db with the raw data.

        initial_db_location: contains the original path to the raw db.
        controller: given the original db extension, it creates an instance of a db controller capable of querying the db.

        """
        extension = os.path.basename(self.initial_db_location).split('.')[1]
        controller = DataFactory.get_controller_from_extension(extension)
        controller.create_db_copy(self.initial_db_location, self.db_location)

    def remove_identifiable_attributes(self):
        """Given a list of identifiable attributes, it suppreses them, as they are forbidden to appear in any form once the data is anonymized.

        identifiable_list: contains all those attributes from the data config that were selected as Identifiable.
        supression_value: default string based on the supression node ('**********')
        query: simple update query, to set values to supression_value for all identifiable attributes.

        """
        identifiable_list = [att.name for att in self.data_config.get_privacy_type_attributes_list(PRIVACY_TYPE_IDENTIFIER)]
        supression_value = BaseHierarchy.supression_node()
        update_ident_list = ["{0}='{1}'".format(att, supression_value) for att in identifiable_list]
        query = "UPDATE {0} SET {1};".format(self.table, ', '.join(update_ident_list))
        list(self.db_controller.execute_query(query))

    def set_indexes_over_qi(self):
        """In order to make queries more efficients, we set indexes over each attribute selected as Quasi-identifable,
        and a composite index over all of them.

        """
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

    def create_additional_information_table(self):
        """Each algorithm that transforms the data, can leave related information about the process. This information is to be saved on a new table on the same db file.

        """
        create_table_query = "CREATE TABLE {0} (id INTEGER PRIMARY KEY, key TEXT, value TEXT);".format(ADDITIONAL_INFO_TABLE)
        list(self.db_controller.execute_query(create_table_query))
