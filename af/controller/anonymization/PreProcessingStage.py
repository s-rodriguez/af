import os

from af.controller.data.DataFactory import DataFactory
from af.model.hierarchies.BaseHierarchy import BaseHierarchy
from af.utils import ANONYMIZATION_DIRECTORY, COPY_OF_ORIGINAL_DB


class PreProcessingStage(object):

    def __init__(self, initial_db_location):
        self.initial_db_location = initial_db_location
        self.db_location = os.path.join(ANONYMIZATION_DIRECTORY, COPY_OF_ORIGINAL_DB)

    def clean_previous_work(self):
        if os.path.isfile(self.db_location):
            os.remove(self.db_location)

    def create_db_copy(self):
        extension = os.path.basename(self.initial_db_location).split('.')[1]
        controller = DataFactory.get_controller_from_extension(extension)
        controller.create_db_copy(self.initial_db_location, self.db_location)

    def remove_identifiable_attributes(self, identifiable_list):
        #supression_value = BaseHierarchy.supression_node()
        #query = update set **** on attributes: asdasd
        #sql_controller.execute_query(query)
        pass

    def set_indexes_over_qi(self, qi_list):
        # qi_list_str = ",".join(qi_list)
        # query = create index qi_index over (qi_list_str)
        # sql_controller.execute(query)
        pass
